"""
FlowUs 适配器

功能:
- 读取FlowUs工作区中的页面
- 同步情感元数据
- 双向同步
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import requests
import time
import hashlib


@dataclass
class FlowUsPage:
    """FlowUs页面"""
    id: str
    title: str
    content: str
    blocks: List[Dict] = field(default_factory=list)
    children: List[str] = field(default_factory=list)


@dataclass
class FlowUsConfig:
    """FlowUs配置"""
    workspace_id: str
    token: str
    api_base: str = "https://api.flowus.com/v1"


class FlowUsAdapter:
    """
    FlowUs适配器
    
    使用FlowUs API进行操作
    """
    
    def __init__(self, config: FlowUsConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {config.token}",
            "Content-Type": "application/json"
        })
        
        # 速率限制
        self.rate_limit = 10  # 每秒请求数
        self.last_request = 0
    
    def _rate_limit(self):
        """速率限制"""
        now = time.time()
        elapsed = now - self.last_request
        
        if elapsed < (1.0 / self.rate_limit):
            time.sleep((1.0 / self.rate_limit) - elapsed)
        
        self.last_request = time.time()
    
    def get_page(self, page_id: str) -> FlowUsPage:
        """获取页面"""
        self._rate_limit()
        
        url = f"{self.config.api_base}/pages/{page_id}"
        
        response = self.session.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        return FlowUsPage(
            id=data["id"],
            title=data.get("title", ""),
            content=data.get("content", ""),
            blocks=data.get("blocks", []),
            children=data.get("children", [])
        )
    
    def get_pages(self, parent_id: Optional[str] = None) -> List[FlowUsPage]:
        """获取页面列表"""
        self._rate_limit()
        
        url = f"{self.config.api_base}/workspaces/{self.config.workspace_id}/pages"
        
        params = {}
        if parent_id:
            params["parent_id"] = parent_id
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        pages = []
        for item in data.get("items", []):
            pages.append(FlowUsPage(
                id=item["id"],
                title=item.get("title", ""),
                content=item.get("content", ""),
                blocks=item.get("blocks", []),
                children=item.get("children", [])
            ))
        
        return pages
    
    def update_page(self, page_id: str, content: str) -> bool:
        """更新页面内容"""
        self._rate_limit()
        
        url = f"{self.config.api_base}/pages/{page_id}"
        
        payload = {
            "content": content
        }
        
        response = self.session.patch(url, json=payload)
        
        return response.status_code == 200
    
    def add_emotion_property(
        self,
        page_id: str,
        emotion_data: Dict
    ) -> bool:
        """添加情感属性到页面"""
        import datetime
        
        # FlowUs使用属性块
        property_block = {
            "type": "property",
            "properties": {
                "limbic-flow": {
                    "emotion": emotion_data.get("pad", {}),
                    "neurotransmitters": emotion_data.get("neurotransmitters", {}),
                    "last_update": datetime.datetime.now().isoformat(),
                    "context": emotion_data.get("context", "")
                }
            }
        }
        
        # 获取当前页面
        page = self.get_page(page_id)
        
        # 添加属性块
        blocks = page.blocks + [property_block]
        
        return self.update_page(page_id, blocks)
    
    def sync_emotions(
        self,
        emotion_state: Dict,
        pages: Optional[List[FlowUsPage]] = None
    ) -> Dict[str, str]:
        """同步情感状态到页面"""
        if pages is None:
            pages = self.get_pages()
        
        results = {}
        
        for page in pages:
            try:
                success = self.add_emotion_property(page.id, emotion_state)
                results[page.id] = "updated" if success else "error"
            except Exception as e:
                results[page.id] = f"error: {str(e)}"
        
        return results
    
    def search_by_emotion(
        self,
        emotion_filter: Dict[str, float],
        pages: Optional[List[FlowUsPage]] = None
    ) -> List[FlowUsPage]:
        """根据情感搜索页面"""
        if pages is None:
            pages = self.get_pages()
        
        matching = []
        
        for page in pages:
            # 检查属性
            for block in page.blocks:
                if block.get("type") == "property":
                    props = block.get("properties", {})
                    if "limbic-flow" in props:
                        limbic = props["limbic-flow"]
                        emotion = limbic.get("emotion", {})
                        
                        match = True
                        for key, value in emotion_filter.items():
                            if abs(emotion.get(key, 0) - value) > 0.2:
                                match = False
                                break
                        
                        if match:
                            matching.append(page)
                            break
        
        return matching


class UnifiedMemoryGateway:
    """
    统一记忆网关
    
    同时支持Obsidian和FlowUs
    """
    
    def __init__(self):
        self.obsidian_adapter = None
        self.flowus_adapter = None
    
    def set_obsidian(self, vault_path: str):
        """设置Obsidian"""
        from .obsidian_adapter import ObsidianAdapter
        self.obsidian_adapter = ObsidianAdapter(vault_path)
    
    def set_flowus(self, config: FlowUsConfig):
        """设置FlowUs"""
        self.flowus_adapter = FlowUsAdapter(config)
    
    def get_all_notes(self) -> Dict[str, List]:
        """获取所有笔记"""
        notes = {"obsidian": [], "flowus": []}
        
        if self.obsidian_adapter:
            notes["obsidian"] = self.obsidian_adapter.get_all_notes()
        
        if self.flowus_adapter:
            notes["flowus"] = self.flowus_adapter.get_pages()
        
        return notes
    
    def sync_emotions(self, emotion_state: Dict) -> Dict:
        """同步情感到所有平台"""
        results = {}
        
        if self.obsidian_adapter:
            results["obsidian"] = self.obsidian_adapter.sync_emotions(emotion_state)
        
        if self.flowus_adapter:
            results["flowus"] = self.flowus_adapter.sync_emotions(emotion_state)
        
        return results
    
    def search_by_emotion(self, emotion_filter: Dict[str, float]) -> Dict:
        """跨平台情感搜索"""
        results = {}
        
        if self.obsidian_adapter:
            results["obsidian"] = self.obsidian_adapter.get_notes_by_emotion(emotion_filter)
        
        if self.flowus_adapter:
            results["flowus"] = self.flowus_adapter.search_by_emotion(emotion_filter)
        
        return results


# 示例
if __name__ == "__main__":
    # 配置
    # config = FlowUsConfig(workspace_id="xxx", token="xxx")
    # adapter = FlowUsAdapter(config)
    
    # 统一网关
    # gateway = UnifiedMemoryGateway()
    # gateway.set_obsidian("/path/to/vault")
    # gateway.set_flowus(config)
    
    print("FlowUs adapter ready")
    print("Usage: config = FlowUsConfig(workspace_id, token)")
    print("       adapter = FlowUsAdapter(config)")
