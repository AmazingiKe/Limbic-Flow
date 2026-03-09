"""
API 文档生成
"""

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def generate_docs(app: FastAPI, title: str = "Limbic-Flow API"):
    """生成 API 文档"""
    
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=title,
        version="0.5.0",
        description="有情绪的 AI 助手 API",
        routes=app.routes,
    )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def custom_docs(app: FastAPI):
    """自定义 API 文档"""
    
    @app.get("/docs")
    async def custom_docs():
        return {"message": "访问 /docs 查看 API 文档"}
    
    return app
