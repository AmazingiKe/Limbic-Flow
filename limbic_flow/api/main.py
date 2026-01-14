from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from limbic_flow.pipeline import LimbicFlowPipeline

app = FastAPI(title="Limbic-Flow API", description="计算精神病学引擎 API")

# 初始化 Limbic-Flow 管道
pipeline = LimbicFlowPipeline()

# 请求模型
class InputRequest(BaseModel):
    user_input: str
    context: Optional[Dict[str, Any]] = None

@app.post("/process")
async def process_input(request: InputRequest):
    """
    处理用户输入并返回动作流
    
    Args:
        request: 包含用户输入和上下文的请求
    
    Returns:
        Dict: 包含动作流的响应
    """
    try:
        # 获取动作生成器
        action_generator = pipeline.process_input(request.user_input, request.context)
        
        # 收集所有动作
        actions = []
        for action in action_generator:
            actions.append(action.to_dict())
            
        return {"actions": actions}
    except Exception as e:
        import traceback
        traceback.print_exc()
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