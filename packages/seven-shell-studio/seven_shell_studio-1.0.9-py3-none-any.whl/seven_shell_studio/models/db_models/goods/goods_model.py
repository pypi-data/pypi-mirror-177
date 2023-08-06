
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class GoodsModel(BaseModel):
    def __init__(self, db_connect_key='db_seven_shell', sub_table=None, db_transaction=None, context=None):
        super(GoodsModel, self).__init__(Goods, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class Goods:

    def __init__(self):
        super(Goods, self).__init__()
        self.id = 0  # 
        self.goods_name = ""  # 商品名称
        self.goods_code = ""  # 商品编码
        self.goods_icon = ""  # 商品ICON
        self.goods_integral = 0  # 商品所需积分
        self.goods_detail = ""  # 商品详情图
        self.goods_inventory = 0  # 商品库存
        self.status = 0  # 状态 0 未发布 1 已发布 2 伪删除
        self.price = 0  # 商品价值
        self.add_time = 0  # 添加时间
        self.release_time = 0  # 发布时间

    @classmethod
    def get_field_list(self):
        return ['id', 'goods_name', 'goods_code', 'goods_icon', 'goods_integral', 'goods_detail', 'goods_inventory', 'status', 'price', 'add_time', 'release_time']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "goods_tb"
    