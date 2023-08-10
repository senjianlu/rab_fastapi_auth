#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: ~/Projects/rab_fastapi_auth/models/User
# @DATE: 2023/07/25 周二
# @TIME: 11:20:09
#
# @DESCRIPTION: 代理节点 Container 模型


import uuid
import hashlib
from enum import Enum
from typing import Union
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer

from external.rab_common import config as external_rab_common_config
from external.rab_common import orm as external_rab_common_orm


# FastAPI Login 相关配置
FASTAPI_AUTH_USER_CONFIG = external_rab_common_config.CONFIG["external"]["rab_fastapi_auth"]["user"]
# ORM 基类 Base
ORM_BASE = external_rab_common_orm.Base


def _hash_password(password: str) -> str:
    """
    @description: 密码加密
    @param {type}
    password: 密码
    @return:
    """
    return hashlib.sha256(password.encode()).hexdigest()
    

class User(ORM_BASE):
    """
    @description: 用户模型
    """

    # === 表名 ===
    __tablename__ = FASTAPI_AUTH_USER_CONFIG["table_name"]
    # === 表结构 ===
    # === 基础信息 ===
    id = Column(String(32), primary_key=True, comment="用户 ID")
    username = Column(String(255), nullable=False, unique=True, comment="用户名")
    password = Column(String(255), nullable=False, comment="密码")
    hashed_password = Column(String(255), nullable=False, comment="加密后的密码")
    is_disabled = Column(Boolean, nullable=False, default=False, comment="是否禁用")
    is_admin = Column(Boolean, nullable=False, default=False, comment="是否管理员")
    # === 额外信息 ===
    nickname = Column(String(255), nullable=True, comment="昵称")
    # === 创建者和更新者信息 ===
    created_by = Column(String(255), nullable=True, comment="创建者 ID")
    created_by_name = Column(String(255), nullable=True, comment="创建者名称")
    created_at = Column(DateTime, nullable=True, comment="创建时间")
    updated_by = Column(String(255), nullable=True, comment="更新者 ID")
    updated_by_name = Column(String(255), nullable=True, comment="更新者名称")
    updated_at = Column(DateTime, nullable=True, comment="更新时间")

    def __init__(self, id: str=None, username: str=None, password: str=None, is_disabled: bool=False, is_admin: bool=False, nickname: str=None):
        """
        @description: 初始化
        @param {type}
        username: 用户名
        password: 密码
        is_disabled: 是否禁用
        is_admin: 是否管理员
        nickname: 昵称
        @return:
        """
        self.id = uuid.uuid4().hex if not id else id
        self.username = username
        self.password = password
        self.hashed_password = _hash_password(password) if password else None
        self.is_disabled = is_disabled
        self.is_admin = is_admin
        self.nickname = nickname

    @staticmethod
    def init_config_admin():
        """
        @description: 初始化管理员
        @param {type}
        @return:
        """
        config_admin_username = FASTAPI_AUTH_USER_CONFIG["admin"]["username"]
        config_admin_password = FASTAPI_AUTH_USER_CONFIG["admin"]["password"]
        admin = User(None, config_admin_username, config_admin_password, is_admin=True, nickname="管理员")
        return admin