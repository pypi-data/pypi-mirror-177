
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class InventoryRecordModel(BaseModel):
    def __init__(self, db_connect_key='db_seven_shell', sub_table=None, db_transaction=None, context=None):
        super(InventoryRecordModel, self).__init__(InventoryRecord, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class InventoryRecord:

    def __init__(self):
        super(InventoryRecord, self).__init__()
        self.id = 0  # 
        self.goods_id = 0  # 奖品id
        self.order_id = ""  # 兑换id
        self.user_id = ""  # 操作人
        self.change_inventory = 0  # 库存变更数量
        self.remark = ""  # 备注
        self.add_time = 0  # 添加时间戳

    @classmethod
    def get_field_list(self):
        return ['id', 'goods_id', 'order_id', 'user_id', 'change_inventory', 'remark', 'add_time']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "inventory_record_tb"
    