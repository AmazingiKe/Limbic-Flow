from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from limbic_flow.pipeline import LimbicFlowPipeline

app = FastAPI(title="Limbic-Flow API", description="计算精神病学引擎 API")

# 初始化 Limbic-Flow 管道
pipeline = LimbicFlowPipeline()

# 请求模型
class InputRequest(BaseModel):
    user_input: str
    context: Optional[Dict[str, Any]] = None

# 响应模型
class LimbicFlowResponse(BaseModel):
    response: str
    emotional_state: Dict[str, Any]
    memories: list

@app.post("/process", response_model=LimbicFlowResponse)
async def process_input(request: InputRequest):
    """
    处理用户输入并返回响应
    
    Args:
        request: 包含用户输入和上下文的请求
    
    Returns:
        LimbicFlowResponse: 包含响应、情绪状态和记忆的响应
    """
    try:
        result = pipeline.process_input(request.user_input, request.context)
        return LimbicFlowResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理请求时出错: {str(e)}")

@app.get("/health")
async def health_check():
    """
    健康检查端点
    
    Returns:
        Dict[str, str]: 健康状态
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)