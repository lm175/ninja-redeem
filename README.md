# ninja-redeem
基于selenium的浏览器自动化程序，提供了忍3官网的礼包码接口

## 礼包码兑换
可以用`RedeemCode`类中定义的方法`redeem_for_user`方法

    from ninja_redeem import RedeemCode

    redeem = RedeemCode("此处为礼包码")
    tip_msg = redeem.redeem_for_user("此处为uid")
    print(tip_msg)

基于`RedeemCode`创建实例对象时会同时创建一个webdriver对象，批量化操作时尽量避免反复创建。

模块中提供了`redeem_for_users`函数，可通过异步协程提高运行效率

    import asyncio
    from ninja_redeem import redeem_for_users

    asyncio.run(redeem_for_users(
        "此处为礼包码",
        ["100000000", "100000001", "100000002"],
        3   # 创建3个协程
    ))


## uid查询
使用requests库进行的api调用

    from ninja_redeem import serch_uid

    user_info = serch_uid(634431781)
    print(user_info)