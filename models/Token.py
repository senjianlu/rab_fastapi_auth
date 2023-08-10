#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: ~/Projects/rab_fastapi_auth/models/Token
# @DATE: 2023/07/30 周日
# @TIME: 17:16:28
#
# @DESCRIPTION: Token 模型


from pydantic import BaseModel


class Token(BaseModel):
    """
    @description: Token 模型
    """

    # 访问令牌
    access_token: str
    # 令牌类型
    token_type: str