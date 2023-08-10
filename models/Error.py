#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: ~/Projects/rab_fastapi_auth/models/Error.py
# @DATE: 2023/08/02 周三
# @TIME: 13:55:07
#
# @DESCRIPTION: 自定义错误


from fastapi import HTTPException, status


class UserNotFoundException(HTTPException):
    """
    @description: 用户不存在
    """

    def __init__(self, status_code=status.HTTP_401_UNAUTHORIZED, detail="用户不存在！"):
        super().__init__(
            status_code=status_code,
            detail=detail
        )

class UsernameOrPasswordErrorException(HTTPException):
    """
    @description: 用户名或密码错误
    """

    def __init__(self, status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误！"):
        super().__init__(
            status_code=status_code,
            detail=detail
        )

class TokenNotExistsException(HTTPException):
    """
    @description: Token 不存在
    """

    def __init__(self, status_code=status.HTTP_401_UNAUTHORIZED, detail="Token 不存在！"):
        super().__init__(
            status_code=status_code,
            detail=detail
        )

class TokenIllegalException(HTTPException):
    """
    @description: Token 不合法
    """

    def __init__(self, status_code=status.HTTP_401_UNAUTHORIZED, detail="Token 不合法，无法解析！"):
        super().__init__(
            status_code=status_code,
            detail=detail
        )

class TokenInvalidException(HTTPException):
    """
    @description: Token 无效
    """

    def __init__(self, status_code=status.HTTP_401_UNAUTHORIZED, detail="Token 无效，携带数据不一致！"):
        super().__init__(
            status_code=status_code,
            detail=detail
        )

class TokenExpiredException(HTTPException):
    """
    @description: Token 已过期
    """

    def __init__(self, status_code=status.HTTP_401_UNAUTHORIZED, detail="Token 已过期！"):
        super().__init__(
            status_code=status_code,
            detail=detail
        )
