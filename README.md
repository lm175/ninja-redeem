# ninja-redeem
忍者必须死3礼包码兑换网页逆向api接口

## 礼包码兑换

    from ninja_redeem import redeem_code

    res = redeem_code(
        uid=634431781,
        code='ut26nbww',
    )
    print(res.json())

## uid查询
使用requests库进行的api调用

    from ninja_redeem import query_uid

    user_info = query_uid(634431781)
    print(user_info)