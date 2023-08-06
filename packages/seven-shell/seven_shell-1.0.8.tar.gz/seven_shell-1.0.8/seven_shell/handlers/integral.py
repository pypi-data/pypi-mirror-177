# -*- coding: utf-8 -*-
"""
:Author: ChenXiaolei
:Date: 2022-06-01 17:41:10
:LastEditTime: 2022-11-18 16:33:07
:LastEditors: Kangwenbin
:Description: 
"""
from seven_framework.web_tornado.base_handler.base_api_handler import *
from .seven_base import SevenBaseHandler
from seven_shell.models.db_models.goods.goods_model import *
from seven_shell.models.db_models.exchange.exchange_model import *
from seven_shell.models.db_models.inventory.inventory_record_model import *
import math


class GoodsDetailHandle(SevenBaseHandler):
    @filter_check_params(["goods_id"])
    @filter_check_sign(config.get_value("sign_key"))
    def get_async(self, *args, **kwargs):
        """
        :description: 商品详情
        :last_editors: rigger
        """
        # 商品id
        goods_id = int(self.request_params["goods_id"])

        # TODO 执行业务
        goods_model = GoodsModel().get_dict_by_id(goods_id,"goods_icon,goods_name,goods_integral,goods_detail,goods_inventory,goods_code")
        if goods_model:
            goods_model["goods_detail"] = json.loads(goods_model["goods_detail"]) if goods_model["goods_detail"] else []
            
            is_inventory = config.get_value("is_inventory",0)
            if is_inventory:
                goods_model["goods_inventory"] = self.get_goods_inventory(goods_model["goods_code"])
        else:
            return self.reponse_json_error("无法获取商品信息")

        # 输出模型
        self.reponse_json_success(goods_model)
    
    def get_goods_inventory(self,goods_code):
        """
        :description: 获取商品库存(如果使用自己库存，必须重写此方法)
        :param goods_code 商品编码
        :last_editors: Kangwenbin
        """
        raise NotImplemented


class GoodsListHandle(SevenBaseHandler):
    @filter_check_params(["page_index", "page_size"])
    @filter_check_sign(config.get_value("sign_key"))
    def get_async(self, *args, **kwargs):
        """
        :description: 积分商品列表
        :last_editors: rigger
        """
        # 页码(从1开始)
        page_index = int(self.request_params["page_index"])
        # 每页多少条数据
        page_size = int(self.request_params["page_size"])

        # TODO 执行业务
        goods_list,goods_count = GoodsModel().get_dict_page_list(field="id,goods_icon,goods_inventory,goods_name,goods_integral,goods_code",page_index=page_index-1,page_size=page_size,where="status = 1",order_by="release_time desc")
        if goods_list and config.get_value("is_inventory",0):
            goods_list = self.get_goods_inventory_list(goods_list)
        
        ret_model = {
            "goods_list": goods_list,
            "has_next": True if math.ceil(goods_count/page_size) > page_index else False
        }

        # 输出模型
        return self.reponse_json_success(ret_model)

    def get_goods_inventory_list(self,goods_list):
        """
        :description: 获取奖品列表对应库存(如果使用自己库存，必须重写此方法)
        :param goods_list
        :return goods_list 奖品列表
        :last_editors: Kangwenbin
        """
        raise NotImplemented


class GoodsExchangeHandle(SevenBaseHandler):

    @filter_check_params(["user_id", "user_nick", "avatar", "goods_id", "goods_count", "total_integral"])
    @filter_check_sign(config.get_value("sign_key"))
    def post_async(self, *args, **kwargs):
        """
        :description: 商品兑换
        :last_editors: rigger
        """
        # 兑换用户id
        user_id = self.request_params["user_id"]
        # 昵称
        user_nick = self.request_params["user_nick"]
        # 头像
        avator = self.request_params["avator"]
        # 商品id
        goods_id = self.request_params["goods_id"]
        # 兑换数量
        goods_count = self.request_params["goods_count"]
        # 所需总积分
        total_integral = self.request_params["total_integral"]
        
        # 数据库连接
        db_transaction = DbTransaction(db_config_dict=config.get_value("db_seven_shell"))
        goods_conn = GoodsModel(db_transaction=db_transaction)

        # TODO 执行业务
        goods_model = goods_conn.get_dict_by_id(goods_id,"goods_code,goods_inventory,goods_integral")
        if not goods_model:
            return self.reponse_json_error("无法获取商品信息")

        # 验证积分总额
        if total_integral != goods_model["goods_integral"] * goods_count:
            return self.reponse_json_error("数据错误")

        is_inventory = config.get_value("is_inventory",0)
        if is_inventory:
            if self.goods_exchange(user_id,goods_model["goods_code"],goods_count,total_integral):
                # 添加兑换记录
                exchange_entity = Exchange()
                exchange_entity.order_id = self.create_order_number()
                exchange_entity.goods_id = goods_id
                exchange_entity.user_id = user_id
                exchange_entity.nick_name = user_nick
                exchange_entity.avator = avator
                exchange_entity.goods_integral = total_integral
                exchange_entity.goods_count = goods_count
                exchange_entity.goods_code = goods_model["goods_code"]
                exchange_entity.add_time = TimeHelper.get_now_timestamp()
                ret = ExchangeModel().add_entity(exchange_entity)
                if ret > 0:
                    return self.reponse_json_success("兑换成功")

        else:
            # 验证库存
            if goods_model["goods_inventory"] <= goods_count:
                return self.reponse_json_error("库存不足")

            # 验证用户积分
            if not self.user_check(user_id,total_integral):
                return self.reponse_json_error("用户积分不足")

            # 写入数据库
            order_id = self.create_order_number()
            exchenge_conn = ExchangeModel(db_transaction=db_transaction)
            inventory_conn = InventoryRecordModel(db_transaction=db_transaction)
            db_transaction.begin_transaction()
            # 修改奖品库存
            goods_conn.update_table("goods_inventory = goods_inventory - %s", where="id = %s and goods_inventory-%s >= 0",params=[goods_count,goods_id,goods_count])
            # 创建库存修改记录
            inventory_entity = InventoryRecord()
            inventory_entity.goods_id = goods_id
            inventory_entity.order_id = order_id
            inventory_entity.user_id = user_id
            inventory_entity.change_inventory = 0 - goods_count
            inventory_entity.add_time = TimeHelper.get_now_timestamp()
            inventory_conn.add_entity(inventory_entity)
            # 创建兑换记录
            exchange_entity = Exchange()
            exchange_entity.order_id = order_id
            exchange_entity.goods_id = goods_id
            exchange_entity.user_id = user_id
            exchange_entity.nick_name = user_nick
            exchange_entity.avator = avator
            exchange_entity.goods_integral = total_integral
            exchange_entity.goods_count = goods_count
            exchange_entity.goods_code = goods_model["goods_code"]
            exchange_entity.add_time = TimeHelper.get_now_timestamp()
            exchenge_conn.add_entity(exchange_entity)
            result = db_transaction.commit_transaction()
            if not result:
                return self.reponse_json_error("兑换失败[001]")
            
            if self.user_deal(goods_model["goods_code"],self.request_params):
                return self.reponse_json_success("兑换成功")
            else:
                self.logger_error.error(f"用户兑换商品失败，参数：user_id：{user_id},goods_id：{goods_id},goods_count：{goods_count},total_integral：{total_integral},goods_code：{goods_model['goods_code']}")
                return self.reponse_json_error("兑换失败[002]")
                
        # 输出模型
        self.reponse_json_error("兑换失败[003]")

    
    def goods_exchange(self,user_id,goods_code,goods_count,total_integral):
        """
        :description: 兑换流程(如果使用自己库存，必须重写此方法)
        :param user_id 用户id
        :param goods_code 商品编码
        :param goods_count 兑换数量
        :param total_integral 所需积分
        :return True 兑换成功 False 兑换失败
        :last_editors: Kangwenbin
        """
        raise NotImplemented
    
    def user_check(self,user_id,total_integral):
        """
        :description: 验证用户状态已经积分等(必须重写)
        :param user_id 用户id
        :param total_integral 所需积分
        :return True 兑换成功 False 兑换失败
        :last_editors: Kangwenbin
        """
        raise NotImplemented

    def user_deal(self,goods_code,params):
        """
        :description: 兑换用户所需处理，扣除积分等(必须重写)
        :param user_id 用户id
        :param total_integral 所需积分
        :return True 兑换成功 False 兑换失败
        :last_editors: Kangwenbin
        """
        raise NotImplemented

class ExchangeListHandle(SevenBaseHandler):

    @filter_check_params(["goods_id", "page_index", "page_size"])
    @filter_check_sign(config.get_value("sign_key"))
    def get_async(self, *args, **kwargs):
        """
        :description: 兑换列表
        :last_editors: rigger
        """
        # 商品id
        goods_id = int(self.request_params["goods_id"])
        # 页码(从1开始)
        page_index = int(self.request_params["page_index"])

        page_size = int(self.request_params["page_size"])

        # TODO 执行业务
        exchange_list = ExchangeModel().get_dict_page_list(field="nick_name,avator,add_time",page_index=page_index-1,page_size=page_size,where="goods_id = %s",order_by="add_time desc",params=goods_id)

        # 输出模型
        return self.reponse_json_success(exchange_list)
