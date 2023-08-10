#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: ~/Projects/rab_fastapi_auth/controller/auth
# @DATE: 2023/07/30 周日
# @TIME: 17:27:04
#
# @DESCRIPTION: 认证控制器


import jwt
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from external.rab_common import config as external_rab_common_config
from external.rab_fastapi_auth.business import admin_biz
from external.rab_fastapi_auth.business import auth_biz
from external.rab_fastapi_auth.business import token_biz
from external.rab_fastapi_auth.models.User import User
from external.rab_fastapi_auth.models.Error import UserNotFoundException, UsernameOrPasswordErrorException, TokenInvalidException, TokenExpiredException, TokenNotExistsException, TokenIllegalException


# FastAPI 风格相关配置
FASTAPI_AUTH_STYLE_CONFIG = external_rab_common_config.CONFIG["external"]["rab_fastapi_auth"]["style"]
# FastAPI 认证路由相关配置
FASTAPI_AUTH_ROUTER_CONFIG = external_rab_common_config.CONFIG["external"]["rab_fastapi_auth"]["router"]
# OAuth2 密码模式
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl=FASTAPI_AUTH_ROUTER_CONFIG["token"])
# FastAPI 认证路由
ROUTER = APIRouter(
    prefix=FASTAPI_AUTH_ROUTER_CONFIG["prefix"],
    tags=["auth"]
)


async def _get_current_user(request: Request, token: str = Depends(OAUTH2_SCHEME)):
    """
    @description: 获取当前用户
    @param {str} token: 访问令牌
    @return {dict} 用户信息
    """
    # 1. 根据令牌解码
    try:
        decoded_token_info = token_biz.decode_token(token)
    except jwt.exceptions.DecodeError:
        raise TokenIllegalException()
    except jwt.exceptions.ExpiredSignatureError:
        raise TokenExpiredException()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token 解码出现未知错误！")
    # 2. 从 Redis 中获取用户信息
    try:
        user_info = await token_biz.get_user_info_from_redis(token, request.app.state.redis)
    except TokenNotExistsException:
        raise TokenNotExistsException()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token 对应的数据解析出现未知错误！")
    # 3. 对比用户信息
    if decoded_token_info["id"] != user_info["id"] or decoded_token_info["sub"] != user_info["username"]:
        raise TokenInvalidException()
    return User(**user_info)


@ROUTER.on_event("startup")
async def startup():
    # 1. 加载配置文件中的 Admin
    admin_biz.load_config_admin()
    print("FastAPI - 认证路由 - 配置文件 Admin 加载完成。")

@ROUTER.middleware("http")
async def handle_response_style(request: Request, call_next):
    """
    @description: 截取所有请求，并修改 response 的格式风格
    """
    response_style = FASTAPI_AUTH_STYLE_CONFIG["response"]
    # 1. Ant Design Pro 风格
    if response_style == "antd":
        response = await call_next(request)
        # 1.1 正常响应
        if response.status_code == 200:
            advance_response = response.body
            del advance_response["code"]
            del advance_response["msg"]
            del advance_response["data"]
            return {"success": True, "data": response.body["data"], code: response.body["code"], message: response.body["msg"], **advance_response}
        # 1.2 失败响应
        else:
            return {"success": False, "data": response.body["data"], errorCode: response.body["code"], errorMessage: response.body["msg"]}
    else:
        return await call_next(request)
    

@ROUTER.post('/login')
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        current_user = await auth_biz.do_login(form_data.username, form_data.password, request.app.state.session)
        return {"code": 200, "msg": "登录成功", "data": {"token": access_token, "user": current_user_info}, "access_token": access_token, "token_type": "bearer"}
    except UserNotFoundException:
        raise UserNotFoundException
    except UsernameOrPasswordErrorException:
        raise UsernameOrPasswordErrorException
    except Exception as e:
        raise HTTPException(status_code=401, detail="登录出现未知错误！")

@ROUTER.get('/me')
async def get_me(current_user: User = Depends(_get_current_user)):
    return {"code": 200, "msg": "获取用户信息成功", "data": current_user}

@ROUTER.get('/token')
async def get_token(token: str = Depends(OAUTH2_SCHEME)):
    return { "code": 200, "msg": "获取 Token 成功", "data": {"token": token}}

@ROUTER.post('/logout')
async def logout(request: Request, token: str = Depends(OAUTH2_SCHEME)):
    try:
        await auth_biz.do_logout(token, request.app.state.redis)
        return {"code": 200, "msg": "登出成功", "data": {}}
    except Exception as e:
        raise HTTPException(status_code=401, detail="登出出现未知错误！")
