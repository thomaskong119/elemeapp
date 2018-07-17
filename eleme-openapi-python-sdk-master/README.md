# Python SDK 接入指南 & CHANGELOG

## 接入指南
    1. 安装eleme sdk依赖包,引入依赖
    2. 利用sdk.config 模块初始化设置沙箱环境，key,secret,调用config.set_log 设置自己的log处理方式。如果是企业应用还需设置callback_url
    3. 利用sdk.oauth 模块完成oauth授权测试
    4. 利用sdk.api 模块完成接口调用测试
    5. 启动sdk自带的server 帮助完成接收饿了么推送消息业务,以及授权测试
    6. 上线前将config.py中初始值sandbox,key和secret以及callback_url填为正式环境


## 代码示例(以调用ShopService为例)


### 企业应用

  - 第一步 安装sdk 包,引入模块
  sudo pip install eleme.openapi.python.sdk

```python
    from sdk.oauth.oauth_client import OAuthClient
    from sdk.apis.shop_service import ShopService
    from sdk.config import Config
```
 
  - 第二步  实例化一个config,设置自己的日志处理方式 实例化一个oauth2.0客户端授权模式的授权对象

```python
    config = Config(True, key, secret, call_back_url)
    # 自己的日志处理方式,必须有info 和error 方法
    class MyLog:
        def info(self, log):
            print (u"my info log:{}".format(log))

        def error(self, log):
            print (u"my error log:{}".format(log))

    config.set_log(MyLog())
    oauth_client = OAuthClient(config)
```

  - 第三步 获取生成授权url

```python
    auth_url = oauth_client.get_auth_url(state, scope)
```

  - 第四步 在授权url中同意授权后，会跳转到CALLBACK_URL的页面，在通过链接上的参数，获取授权码code


  - 第五️步 通过code获取token对象,此步获取到的token对象可在有效期内一直使用，不用每次调用前都去获取一次，建议应用授权一次后存放到全局缓存中

```python
    token = oauth_client.get_token_by_code(code)
```

  - 第六步 实例化远程调用的client对象

```python
    rpc_client = RpcClient(config, token)
```

  - 第七步 实例化一个服务对象

```python
    shop_service = ShopService(rpc_client)
```

  - 第八步 调用服务方法，获取资源数据

```python
    shop = shop_service.get_shop(123456)
```

  - 第九步 如果token过期，通过refresh_token换取新的token

```python
    refresh_token = token["refresh_token"]
    token = oauth_client.get_token_by_refresh_token(refresh_token, scope)
```

### 个人应用

  - 第一步 安装sdk 包,引入模块
    sudo pip install eleme.openapi.python.sdk

```python
    from sdk.oauth.oauth_client import OAuthClient
    from sdk.apis.shop_service import ShopService
    from sdk.protocol.rpc_client import RpcClient
    from sdk.config import Config
```

  - 第二步 实例化config对象，实例化一个oauth2.0客户端授权模式的授权对象

```python
    config = Config(True, key, secret)
    # 自己的日志处理方式,必须有info 和error 方法
    class MyLog:
        def info(self, log):
            print (u"my info log:{}".format(log))

        def error(self, log):
            print (u"my error log:{}".format(log))

    config.set_log(MyLog())
    oauth_client = OAuthClient(config)
```

  - 第三️步 获取token对象,此步获取到的token对象可在有效期内一直使用，不用每次调用前都去获取一次，建议应用授权一次后存放到全局缓存中

```python
    token = oauth_client.get_token_in_client_credentials()
```

  - 第四步 实例化远程调用的client对象

```python
    rpc_client = RpcClient(config, token)
```

  - 第五步 实例化一个服务对象

```python
    shop_service = ShopService(rpc_client)
```

  - 第六步 调用服务方法，获取资源数据

```python
    shop = shop_service.get_shop(123456)
```


### Server 使用方式

 - 第一步 安装sdk 包,引入模块
    sudo pip install eleme.openapi.python.sdk

 - 第二步 引入依赖

```python
    from sdk.config import Config
    from server.global_config import Global
    from server.start_up import boot_start
```
 - 第三步 初始化config对象,并将config对象设置到Global中

```python
    config = Config(True, key, secret, call_back_url)
    # 自己的日志处理方式,必须有info 和error 方法
    class MyLog:
        def info(self, log):
            print (u"my info log:{}".format(log))

        def error(self, log):
            print (u"my error log:{}".format(log))

    config.set_log(MyLog())
    Global(config)
```

 - 第四步 启动服务
 启动服务后 会监听三个localtion
    1. get  /listenMessage  响应饿了么平台的url校检
    2. post /listenMessage  接收饿了么平台的消息推送
    3. get  /callback       授权回调地址，处理授权逻辑
    4. post /getInfo        获取当前的用户信息和店铺信息

```python
    boot_start(port)
```




## CHANGELOG:
### [1.18.5]
Release Date : 2018-7-13
- [Feature] 订单评论服务新增接口

### [1.18.4]
Release Date : 2018-7-6
- [Feature] 内容服务新增接口
- [Feature] 商品服务新增接口

### [1.18.3]
Release Date : 2018-6-28
- [Feature] 内容服务新增接口
- [Feature] 商品服务新增接口
- [Feature] 订单服务新增接口
- [Feature] 店铺装修服务新增接口
- [Feature] 店铺服务新增接口

### [1.17.3]
Release Date : 2018-6-22
- [Feature] 店铺服务新增接口

### [1.17.2]
Release Date : 2018-6-08
- [Feature] 活动服务新增接口
- [Feature] 活动服务下线接口
- [Feature] 订单服务新增接口
- [Feature] 订单服务下线接口

### [1.16.2]
Release Date : 2018-5-18
- [Feature] 商品服务新增接口

### [1.16.1]
Release Date : 2018-5-11
- [Feature] 新增授权码换取OpenId接口
- [Feature] 活动服务新增若干接口

### [1.15.0]
Release Date : 2018-3-23

- [Feature] 新增若干新服务

### [1.14.1]
Release Date : 2018-2-2

- [Feature] 订单评论服务增加若干接口
- [Feature] 活动服务增加定向送红包接口
- [Feature] 新增服务市场服务

### [1.13.0]
Release Date : 2018-1-5

- [Feature] 商品服务新增根据店铺 Id 查询商品接口

### [1.12.0]
Release Date : 2017-12-29

- [Feature] 店铺服务新增设置是否支持预定单及预定天数接口

### [1.11.0]
Release Date : 2017-12-24

- [Feature] 订单服务新增出餐和评价骑手接口
- [Feature] 订单评论服务新增新版回复评论接口

### [1.10.0]
Release Date : 2017-11-21

- [Feature] 新增众包查询配送费接口

### [1.9.0]
Release Date : 2017-10-27

- [Feature] 新增了代金券和零元试吃的活动接口

### [v1.8.0]
    Release Date : 2017-09-22


- [feature] 新增活动服务相关接口，具体参见openapi活动文档
- [feature] 订单增加索赔相关的接口，具体参见openapi订单文档
- [feature] 商品接口增加 set_order_packing_fee 设置餐盒费接口
- [feature] 增加ugc评价服务，具体参见openapi ugc文档



### [v1.7.0]
    Release Date : 2017-08-03


- [feature] 新增user,shop,finance特权接口



### [v1.6.0]
    Release Date : 2017-07-07


- [feature] 新增两个金融接口。eleme.finance.queryBalance 和 eleme.finance.queryBalanceLog
- [feature] 新增接口 eleme.product.item.getItemIdsHasActivityByShopId
- [feature] 修改包含实体 OItem 的接口，属性 specs,多返回活动标识字段activityLevel

### [v1.5.0]

    Release Date : 2017-05-27

- [Feature] 在订单服务中增加了若干订单操作的轻量接口
- [Feature] 在店铺服务中增加了 eleme.shop.setOnlineRefund 设置是否支持在线退单

### [v1.4.0]

    Release Date : 2017-05-23

- [feature] 在商户服务中增加了 eleme.user.getPhoneNumber 获取当前授权帐号的手机号
- [feature] 在订单服务中增加了 eleme.order.getUnreplyReminders 获取店铺未回复的催单；eleme.order.getUnprocessOrders 查询店铺未处理订单；eleme.order.getCancelOrders 查询店铺未处理的取消单；eleme.order.getRefundOrders 查询店铺未处理的退单；eleme.order.getAllOrders 查询全部订单这五个新接口
- [feature] 在商品服务中增加了 eleme.product.item.getItemByShopIdAndExtendCode 根据商品扩展码获取商品；eleme.product.item.getItemsByShopIdAndBarCode 根据条形码获取商品

### [v1.3.0]

    Release Date : 2017-05-12

- [feature] 在商品服务中增加了 eleme.product.item.batchUpdatePrices 批量修改商品价格的接口
- [feature] 在订单服务中增加了 eleme.order.cancelDelivery 取消呼叫配送和 eleme.order.callDelivery 呼叫配送这两个接口
- [feature] 在订单服务中修改了 OOrder 类的定义，增加了一个 List<OActivity> 的属性。
- [feature] 在商品服务中增加了 eleme.product.category.getShopCategoriesWithChildren 查询店铺商品分类，包含二级分类；eleme.product.category.getCategoryWithChildren 查询商品分类详情，包含二级分类；eleme.product.category.createCategoryWithChildren 添加商品分类，支持二级分类；eleme.product.category.updateCategoryWithChildren 更新商品分类，包含二级分类；eleme.product.category.setCategoryPositionsWithChildren 设置二级分类排序这五个接口。

### [v1.2.0]

    Release Date : 2017-05-05

- [feature] 增加签约服务;
- [feature] 订单服务中新增了 eleme.order.replyReminder eleme.order.getCommodities eleme.order.mgetCommodities eleme.order.getRefundOrder eleme.order.mgetRefundOrders
- [feature] 增加接口查询商品后台分类 eleme.product.category.getBackCategory

### [v1.1.1]

    Release Date : 2017-04-28

- [bugfix] 为和老版本使用习惯保持一致,RpcClient(config,token) 中的token含义由access_token改为含有access_token 属性的json串

### [v1.1.0]

    Release Date : 2017-04-25

- [feature] 1.增加ugc服务;2.订单服务增加确认送达接口;3.shop服务增加设置送达时间接口;4.product服务增加 批量沽清置满接口

### [v1.0.1]

    Release Date : 2017-04-11

- [feature] 1.文档优化;2.修改回调页面图标

### [v1.0.0]

    Release Date : 2017-04-07

- [feature] eleme sdk











