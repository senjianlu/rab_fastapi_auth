#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: ~/Projects/rab_fastapi_auth/business/token_biz
# @DATE: 2023/07/31 周一
# @TIME: 20:56:34
#
# @DESCRIPTION: Token 业务逻辑


import jwt
import json
from datetime import datetime, timedelta

from external.rab_common import config as external_rab_common_config
from external.rab_fastapi_auth.models.User import User
from external.rab_fastapi_auth.models.Error import TokenIllegalException, TokenInvalidException, TokenNotExistsException


# FastAPI Login 相关配置
FASTAPI_AUTH_TOKEN_CONFIG = external_rab_common_config.CONFIG["external"]["rab_fastapi_auth"]["token"]


def encode_token(user: User, secret_key: str=None, algorithm: str=None):
    """
    @description: 编码 Token
    @param {User} user: 用户
    @param {str} secret_key: 密钥
    @param {str} algorithm: 算法
    @return {str} Token
    """
    access_token_expire_seconds = FASTAPI_AUTH_TOKEN_CONFIG["access_token_expire_seconds"]
    payload = {
        "id": user.id,
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(seconds=access_token_expire_seconds)
    }
    secret_key = secret_key or FASTAPI_AUTH_TOKEN_CONFIG["secret_key"]
    algorithm = algorithm or FASTAPI_AUTH_TOKEN_CONFIG["algorithm"]
    return jwt.encode(payload, secret_key, algorithm=algorithm)

def decode_token(token: str, secret_key: str=None, algorithm: str=None):
    """
    @description: 解码 Token
    @param {type}
    @return:
    """
    secret_key = secret_key or FASTAPI_AUTH_TOKEN_CONFIG["secret_key"]
    algorithm = algorithm or FASTAPI_AUTH_TOKEN_CONFIG["algorithm"]
    return jwt.decode(token, secret_key, algorithms=[algorithm])

async def save_token_to_redis(access_token: str, current_user: User, redis):
    """
    @description: 将 Token 保存到 Redis 中
    @param {str} token: Token
    @param {User} current_user: 当前用户
    @param {Redis} redis: Redis
    @return:
    """
    # 1. 删除 User 中的密码
    masked_user_info = current_user.__dict__
    del masked_user_info["_sa_instance_state"]
    del masked_user_info["password"]
    del masked_user_info["hashed_password"]
    del masked_user_info["created_by"]
    del masked_user_info["created_by_name"]
    del masked_user_info["created_at"]
    del masked_user_info["updated_by"]
    del masked_user_info["updated_by_name"]
    del masked_user_info["updated_at"]
    # 2. 将 Token 存储到 Redis 中
    await redis.set(access_token, json.dumps(masked_user_info), ex=FASTAPI_AUTH_TOKEN_CONFIG["access_token_expire_seconds"])
    # 3. 返回
    return access_token, masked_user_info

async def get_user_info_from_redis(access_token: str, redis):
    """
    @description: 从 Redis 中获取用户信息
    @param {str} access_token: 访问令牌
    @param {Redis} redis: Redis
    @return {dict} 用户信息
    """
    # 1. 从 Redis 中获取用户信息
    user_info_str = await redis.get(access_token)
    # 2. 判断用户信息是否存在
    if not user_info_str:
        raise TokenNotExistsException()
    # 3. 返回用户信息
    return json.loads(user_info_str)
