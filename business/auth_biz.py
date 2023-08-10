#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: ~/Projects/rab_fastapi_auth/business/auth_biz
# @DATE: 2023/07/30 周日
# @TIME: 20:20:21
#
# @DESCRIPTION: 认证业务逻辑


import hashlib
from fastapi import HTTPException, status, Depends

from external.rab_fastapi_auth.controller import auth as external_rab_fastapi_auth_controller_auth
from external.rab_fastapi_auth.models.User import User
from external.rab_fastapi_auth.models.Error import UserNotFoundException, UsernameOrPasswordErrorException
from external.rab_fastapi_auth.business import token_biz


def _verify_password(plain_password: str, hashed_password: str):
    """
    @description: 校验密码
    @param {str} plain_password: 明文密码
    @param {str} hashed_password: 密文密码
    @return {bool} 是否匹配
    """
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

async def do_login(username: str, password: str, session, redis):
    """
    @description: 登录
    @param {str} username: 用户名
    @param {str} password: 密码
    @return {User} 用户
    """
    # 1. 查询用户
    user = session.query(User).filter(User.username == username).first()
    # 2. 校验
    # 2.1 用户不存在
    if not user:
        raise UserNotFoundException()
    # 2.2 密码错误
    if not _verify_password(password, user.hashed_password):
        raise UsernameOrPasswordErrorException()
    # 3. 生成 token 令牌
    access_token = token_biz.encode_token(user)
    # 4. 将令牌存储到 Redis 中
    access_token, masked_user_info = await token_biz.save_token_to_redis(access_token, user, redis)
    return access_token, masked_user_info

async def do_logout(token: str, redis):
    """
    @description: 登出
    @param {type}
    @return:
    """
    # 1. 删除 Redis 中的 Token
    await redis.delete(token)
    # 2. 返回
    return
