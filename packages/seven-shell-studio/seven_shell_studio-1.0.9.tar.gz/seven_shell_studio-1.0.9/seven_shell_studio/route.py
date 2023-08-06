import seven_shell_studio.handlers.api.integral as integral

def seven_studio_route():
    return [
        (r"/api/integral/exchange_list", integral.ExchangeListHandle), # 兑换列表 
        (r"/api/integral/goods_list", integral.GoodsListHandle), # 商品列表 
        (r"/api/integral/goods_manage", integral.GoodsManageHandle), # 商品信息/商品添加/商品修改/商品删除/商品上下架 
    ]
