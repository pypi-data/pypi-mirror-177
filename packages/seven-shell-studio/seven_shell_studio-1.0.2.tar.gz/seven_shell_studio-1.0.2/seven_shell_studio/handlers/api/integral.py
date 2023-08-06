# -*- coding: utf-8 -*-
"""
:Author: ChenXiaolei
:Date: 2022-06-01 17:41:10
:LastEditTime: 2022-11-21 17:48:55
:LastEditors: Kangwenbin
:Description: 
"""
from seven_studio.handlers.studio_base import *
from seven_shell_studio.models.db_models.goods.goods_model import *
from seven_shell_studio.models.db_models.exchange.exchange_model_ex import *
from seven_shell_studio.models.db_models.inventory.inventory_record_model import *
class GoodsManageHandle(StudioBaseHandler):

    @filter_check_params(["goods_id"])
    @login_filter(True)
    def get_async(self, *args, **kwargs):
        """
        :description: 商品信息
        :last_editors: rigger
        """
        # 商品id
        goods_id = self.request_params["goods_id"]

        # TODO 执行业务
        goods_model = GoodsModel().get_dict_by_id(goods_id,field="id,goods_name,goods_code,goods_icon,goods_integral,goods_inventory,goods_detail,status")
        if not goods_model:
            return self.reponse_json_error("无法获取商品信息")
        
        if goods_model["goods_detail"]:
            goods_model["goods_detail"] = json.loads(goods_model["goods_detail"])

        # 输出模型
        self.reponse_json_success(goods_model)


    @filter_check_params(["goods_name", "goods_code", "goods_icon", "goods_integral", "goods_detail", "goods_inventory"])
    @login_filter(True)
    def post_async(self, *args, **kwargs):
        """
        :description: 商品添加
        :last_editors: rigger
        """
        # 商品名称
        goods_name = self.request_params["goods_name"]
        # 商品编码
        goods_code = self.request_params["goods_code"]
        # 商品ICON
        goods_icon = self.request_params["goods_icon"]
        # 商品所需积分
        goods_integral = self.request_params["goods_integral"]
        # 商品详情图
        goods_detail = self.request_params["goods_detail"]
        # 商品库存
        goods_inventory = self.request_params["goods_inventory"]
        # 状态 0 未发布 1 已发布
        status = self.request_params["status"]
        # 商品价值
        price = self.request_params["price"]

        # TODO 执行业务
        goods_entity = Goods()
        goods_entity.goods_name = goods_name
        goods_entity.goods_code = goods_code
        goods_entity.goods_icon = goods_icon
        goods_entity.goods_integral = goods_integral
        goods_entity.goods_detail = json.dumps(goods_detail)
        goods_entity.goods_inventory = goods_inventory
        goods_entity.status = status
        goods_entity.price = price
        goods_entity.add_time = TimeHelper.get_now_timestamp()
        if status == 1:
            goods_entity.release_time = TimeHelper.get_now_timestamp()
            
        ret = GoodsModel().add_entity(goods_entity)
        if ret>0:
            # 添加奖品库存记录
            inventory_record_entity = InventoryRecord()
            inventory_record_entity.goods_id = ret
            inventory_record_entity.order_id = ""
            inventory_record_entity.user_id = self.request_user_id()
            inventory_record_entity.change_inventory = goods_inventory
            inventory_record_entity.remark = "后台添加"
            inventory_record_entity.add_time = TimeHelper.get_now_timestamp()
            InventoryRecordModel().add_entity(inventory_record_entity)
            return self.reponse_json_success("提交成功")
        
        self.reponse_json_error("提交失败")


    @filter_check_params(["id", "goods_name", "goods_code", "goods_icon", "goods_integral", "goods_detail", "goods_inventory"])
    @login_filter(True)
    def put_async(self, *args, **kwargs):
        """
        :description: 商品修改
        :last_editors: rigger
        """
        # 奖品id
        id = self.request_params["id"]
        # 商品名称
        goods_name = self.request_params["goods_name"]
        # 商品编码
        goods_code = self.request_params["goods_code"]
        # 商品ICON
        goods_icon = self.request_params["goods_icon"]
        # 商品所需积分
        goods_integral = self.request_params["goods_integral"]
        # 商品详情图
        goods_detail = self.request_params["goods_detail"]
        # 商品库存
        goods_inventory = self.request_params["goods_inventory"]
        # 状态 0 未发布 1 已发布 2 伪删除
        status = self.request_params["status"]
        # 商品价值
        price = self.request_params["price"]

        db_transaction = DbTransaction(db_config_dict=config.get_value("db_seven_shell"))
        goods_conn = GoodsModel(db_transaction=db_transaction)
        inventory_conn = InventoryRecordModel(db_transaction=db_transaction)
        db_transaction.begin_transaction()

        # TODO 执行业务
        goods_model = goods_conn.get_dict_by_id(id,"goods_inventory")
        if not goods_model:
            return self.reponse_json_error("无法获取奖品信息")
        
        if goods_inventory < 0:
            return self.reponse_json_error("库存输入错误")

        # 库存变更量
        change_inventory = goods_model["goods_inventory"] - goods_inventory
        goods_conn.update_table("goods_name=%s,goods_code=%s,goods_icon=%s,goods_integral=%s,goods_detail=%s,status=%s,price=%s,goods_inventory=goods_inventory+%s,release_time=%s"
                                ,where="id = %s",params=[goods_name,goods_code,goods_icon,goods_integral,json.dumps(goods_detail),status,price,change_inventory,TimeHelper.get_now_timestamp(),id])

        # 添加库存记录
        inventory_record = InventoryRecord()
        inventory_record.goods_id = id
        inventory_record.order_id = ""
        inventory_record.user_id = self.request_user_id()
        inventory_record.change_inventory = 0 - change_inventory
        inventory_record.remark = "后台修改"
        inventory_record.add_time = TimeHelper.get_now_timestamp()
        inventory_conn.add_entity(inventory_record)
        
        if db_transaction.commit_transaction():
            return self.reponse_json_success("提交成功")
        
        self.reponse_json_error("提交失败")


    @filter_check_params(["goods_id_list"])
    @login_filter(True)
    def delete_async(self, *args, **kwargs):
        """
        :description: 商品删除
        :last_editors: rigger
        """
        # 需要删除的奖品id列表
        goods_id_list = self.request_params["goods_id_list"]

        if GoodsModel().update_table("status = 2","id in %s",(goods_id_list,)):
            return self.reponse_json_success("提交成功")

        self.reponse_json_error()


    @filter_check_params(["goods_id_list"])
    @login_filter(True)
    def patch_async(self, *args, **kwargs):
        """
        :description: 商品上下架
        :last_editors: rigger
        """
        # 需要上下架的id列表
        goods_id_list = self.request_params["goods_id_list"]

        goods_conn = GoodsModel()
        # TODO 执行业务
        for item in goods_id_list:
            goods_model = goods_conn.get_dict_by_id(item,"status")
            if not goods_model:
                continue
            
            if goods_model["status"] == 2:
                # 已删除的不进行上下架
                continue

            edit_status = 1 if goods_model["status"] == 0 else 0
            goods_conn.update_table("status = %s","id = %s",[edit_status,item])
        
        self.reponse_json_success()


class ExchangeListHandle(StudioBaseHandler):
    @filter_check_params(["page_index", "page_size"])
    @login_filter(True)
    def get_async(self, *args, **kwargs):
        """
        :description: 兑换列表
        :last_editors: rigger
        """
        # 页码(从1开始)
        page_index = self.request_params["page_index"]
        #
        page_size = self.request_params["page_size"]
        # 商品名称搜索
        sel_goods_name = self.request_params.get("sel_goods_name", None)
        # 用户昵称搜索
        sel_user_nick = self.request_params.get("sel_user_nick", None)
        # 用户id搜索
        sel_user_id = self.request_params.get("sel_user_id", None)
        # 时间戳搜索(开始)
        sel_begin_time = self.request_params.get("sel_begin_time", None)
        # 时间戳搜索(结束)
        sel_end_time = self.request_params.get("sel_end_time", None)

        # TODO 执行业务
        condition = "1=1"
        param_list = []

        if sel_goods_name:
            condition += " and b.goods_name like %s"
            param_list.append(f"%{sel_goods_name}%")

        if sel_user_nick:
            condition += " and a.nick_name like %s"
            param_list.append(f"%{sel_user_nick}%")

        if sel_user_id:
            condition += " and a.user_id = %s"
            param_list.append(sel_user_id)

        if sel_begin_time:
            condition += " and a.add_time >= %s"
            param_list.append(sel_begin_time)

        if sel_end_time:
            condition += " and a.add_time <= %s"
            param_list.append(sel_end_time)

        # 获取兑换列表
        exchange_list,exchange_count = ExchangeModelEx().get_exchange_page_list(condition,"a.order_id,a.goods_id,b.goods_name,a.goods_icon,a.user_id,a.nick_name,a.goods_integral,a.goods_code,a.goods_count,a.add_time",
                            limit = f"{(page_index-1)*page_size},{page_size}",params=param_list)
        
        ret_model = {
            "count":exchange_count,
            "model_list":exchange_list
        }

        return self.reponse_json_success(ret_model)


class GoodsListHandle(StudioBaseHandler):

    @filter_check_params(["page_index", "page_size"])
    def get_async(self, *args, **kwargs):
        """
        :description: 商品列表
        :last_editors: rigger
        """
        # 页码(1开始)
        page_index = self.request_params["page_index"]
        #
        page_size = self.request_params["page_size"]
        # 奖品名称搜索
        sel_goods_name = self.request_params.get("sel_goods_name", None)
        # 奖品状态 0 未发布 1 已发布
        sel_status = self.request_params.get("sel_status", None)
        # 奖品积分区间(开始)
        sel_integral_begin = self.request_params.get(
            "sel_integral_begin", None)
        # 奖品积分区间(结束)
        sel_integral_end = self.request_params.get("sel_integral_end", None)
        # 奖品编码搜索
        sel_goods_code = self.request_params.get("sel_goods_code", None)

        # TODO 执行业务
        condition = "1=1"
        param_list = []

        if sel_goods_name:
            condition += " and goods_name like %s"
            param_list.append(f"%{sel_goods_name}%")

        if sel_status:
            condition += " and status = %s"
            param_list.append(sel_status)

        if sel_integral_begin:
            condition += " and goods_integral >= %s"
            param_list.append(sel_integral_begin)

        if sel_integral_end:
            condition += " and goods_integral <= %s"
            param_list.append(sel_integral_end)

        if sel_goods_code:
            condition += " and goods_code like %s"
            param_list.append(f"%{sel_goods_code}%")

        # 获取奖品列表
        goods_list,goods_count = GoodsModel().get_dict_page_list(field="id,goods_name,goods_code,goods_icon,goods_integral,goods_inventory,status,add_time",
                                    page_index=page_index-1,page_size=page_size,where=condition,order_by="id desc",params=param_list)
        
        ret_model = {
            "count":goods_list,
            "model_list":goods_count
        }

        return self.reponse_json_success(ret_model)

