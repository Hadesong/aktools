# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/9/28 15:05
Desc: 主程序入口文件
"""
import os
import sys

# 添加 package 查找路径，该行必须在前面，否则不能导入相关的模块
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import akshare
import aktools
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from aktools.core.api import app_core, templates
from aktools.datasets import get_favicon_path, get_homepage_html
from aktools.login import app_user_login
from aktools.utils import get_latest_version
from aktools.schema.version import VersionBase

favicon_path = get_favicon_path(file="favicon.ico")
html_path = get_homepage_html(file="homepage.html")


app = FastAPI()


@app.middleware("http")
async def add_cache_control_header(request, call_next):
    """ 将函数注册为 HTTP 中间件,用于拦截所有http请求,并设置缓存控制头 """
    response = await call_next(request)
    response.headers["Cache-Control"] = "max-age=86400" #3600一小时 86400一天
    return response



origins = ["*"]  # 此处设置可以访问的协议，IP和端口信息

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(app_core, prefix="/aaappi", tags=["数据接口"])
app.include_router(app_user_login, prefix="/auth", tags=["登录接口"])

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8080)
