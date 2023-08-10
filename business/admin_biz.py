#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: ~/Projects/rab_fastapi_auth/business/admin_biz
# @DATE: 2023/07/31 周一
# @TIME: 20:20:21
#
# @DESCRIPTION: Admin 业务逻辑


from external.rab_common import orm as external_rab_common_orm
from external.rab_fastapi_auth.models.User import User


def load_config_admin():
    """
    @description: 加载配置文件中的 Admin
    """
    # 1. 建立数据库连接
    session = external_rab_common_orm.init_db()
    # 2. 查询所有 Admin
    users = session.query(User).filter(User.is_admin == True).all()
    # 3. 配置文件中的 Admin
    is_config_admin_exist = False
    config_admin = User.init_config_admin()
    for user in users:
        # print(user.username, user.hashed_password)
        if user.username != config_admin.username or user.hashed_password != config_admin.hashed_password:
            session.delete(user)
        else:
            is_config_admin_exist = True
    # 4. 如果配置文件中的 Admin 不存在则创建
    if not is_config_admin_exist:
        session.add(config_admin)
    # 5. 提交事务
    session.commit()
    # 6. 关闭数据库连接
    session.close()
