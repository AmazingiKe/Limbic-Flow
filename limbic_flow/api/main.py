import json
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from limbic_flow.pipeline import LimbicFlowPipeline

app = FastAPI(title="Limbic-Flow API", description="计算精神病学引擎 API")

# 默认单例，可通过 Depends 在测试中覆盖
_default_pipeline: Optional[LimbicFlowPipeline] = None


def get_pipeline() -> LimbicFlowPipeline:
    """依赖注入：返回 Pipeline 实例，便于单测或多配置替换。"""
    global _default_pipeline
    if _default_pipeline is None:
        _default_pipeline = LimbicFlowPipeline()
    return _default_pipeline


# 请求模型
class InputRequest(BaseModel):
    user_input: str
    context: Optional[Dict[str, Any]] = None


@app.post("/process")
async def process_input(
    request: InputRequest,
    pipeline: LimbicFlowPipeline = Depends(get_pipeline),
):
    """
    处理用户输入并返回动作流

    Args:
        request: 包含用户输入和上下文的请求

    Returns:
        Dict: 包含动作流的响应
    """
    try:
        action_generator = pipeline.process_input(request.user_input, request.context)
        actions = [action.to_dict() for action in action_generator]
        return {"actions": actions}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"处理请求时出错: {str(e)}")


@app.post("/process/stream")
async def process_input_stream(
    request: InputRequest,
    pipeline: LimbicFlowPipeline = Depends(get_pipeline),
):
    """
    处理用户输入并以 SSE 流式返回动作事件（ActionEvent）。
    每行格式: data: {json}\n\n
    """
    def event_generator():
        try:
            for action in pipeline.process_input(request.user_input, request.context):
                payload = json.dumps(action.to_dict(), ensure_ascii=False)
                yield f"data: {payload}\n\n"
        except Exception as e:
            yield f"data: {{\"error\": \"{str(e)}\"}}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


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