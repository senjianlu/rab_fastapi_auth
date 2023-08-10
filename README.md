# rab_fastapi_login
## 依赖
1. 依赖于 `rab_common` 模块的数据库连接。

## 配置片段
```toml
# 外部模块
[external]
  [external.rab_fastapi_auth]
    [external.rab_fastapi_auth.token]
    # Secret Key，生成方式: openssl rand -hex 32
    secret_key = "my_secret_key"
    # Token 过期时间，单位: 秒
    access_token_expire_seconds = 3600
    # 计算 Token 时使用的算法
    algorithm = "HS256"
    [external.rab_fastapi_auth.router]
    # 路由前缀
    prefix = "/auth"
    # Token 认证路由
    token = "auth/login"
    [external.rab_fastapi_auth.user]
    # 表名
    table_name = "fastapi_auth_user"
      [external.rab_fastapi_auth.user.admin]
      # 管理员用户名
      username = "admin"
      # 管理员密码
      password = "admin"
```