"""
Obsidian 适配器

功能:
- 读取Obsidian vault中的笔记
- 同步情感元数据
- 双向同步
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import os
import json
import re
from pathlib import Path
import yaml


@dataclass
class ObsidianNote:
    """Obsidian笔记"""
    path: str
    title: str
    content: str
    frontmatter: Dict = field(default_factory=dict)
    links: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


@dataclass  
class LimbicMetadata:
    """Limbic-Flow情感元数据"""
    emotion: Dict[str, float] = field(default_factory=dict)
    neurotransmitters: Dict[str, float] = field(default_factory=dict)
    last_emotion_update: str = ""
    emotional_context: str = ""
    attachments: List[Dict] = field(default_factory=list)


class ObsidianAdapter:
    """
    Obsidian适配器
    
    使用:
    - 本地文件访问
    - YAML frontmatter 解析
    - 内部链接处理
    """
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.encoding = "utf-8"
        
        # 情感元数据键
        self.limbic_prefix = "limbic-flow"
    
    def get_all_notes(self, extension: str = ".md") -> List[ObsidianNote]:
        """获取所有笔记"""
        notes = []
        
        for md_file in self.vault_path.rglob(f"*{extension}"):
            try:
                note = self._read_note(md_file)
                notes.append(note)
            except Exception as e:
                print(f"Error reading {md_file}: {e}")
        
        return notes
    
    def _read_note(self, path: Path) -> ObsidianNote:
        """读取单个笔记"""
        with open(path, "r", encoding=self.encoding) as f:
            content = f.read()
        
        # 解析 frontmatter
        frontmatter = {}
        body = content
        
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter_str = parts[1]
                body = parts[2].strip()
                
                try:
                    frontmatter = yaml.safe_load(frontmatter_str) or {}
                except:
                    pass
        
        # 提取标题
        title = path.stem
        if body.startswith("# "):
            title = body.split("\n")[0].replace("# ", "")
        
        # 提取链接
        links = re.findall(r"\[\[([^\]]+)\]\]", body)
        
        # 提取标签
        tags = re.findall(r"#(\w+)", body)
        
        return ObsidianNote(
            path=str(path.relative_to(self.vault_path)),
            title=title,
            content=body,
            frontmatter=frontmatter,
            links=links,
            tags=tags
        )
    
    def get_emotion_metadata(self, note: ObsidianNote) -> Optional[LimbicMetadata]:
        """获取笔记的情感元数据"""
        if self.limbic_prefix not in note.frontmatter:
            return None
        
        limbic_data = note.frontmatter[self.limbic_prefix]
        
        return LimbicMetadata(
            emotion=limbic_data.get("emotion", {}),
            neurotransmitters=limbic_data.get("neurotransmitters", {}),
            last_emotion_update=limbic_data.get("last_emotion_update", ""),
            emotional_context=limbic_data.get("emotional_context", ""),
            attachments=limbic_data.get("attachments", [])
        )
    
    def add_emotion_metadata(
        self, 
        note: ObsidianNote,
        emotion: Dict[str, float],
        context: str = ""
    ) -> str:
        """添加情感元数据到笔记"""
        import datetime
        
        # 获取现有元数据
        if self.limbic_prefix in note.frontmatter:
            limbic_data = note.frontmatter[self.limbic_prefix]
        else:
            limbic_data = {}
        
        # 更新情感数据
        limbic_data["emotion"] = emotion
        limbic_data["last_emotion_update"] = datetime.datetime.now().isoformat()
        
        if context:
            limbic_data["emotional_context"] = context
        
        # 更新 frontmatter
        note.frontmatter[self.limbic_prefix] = limbic_data
        
        return self._serialize_note(note)
    
    def _serialize_note(self, note: ObsidianNote) -> str:
        """序列化笔记"""
        lines = []
        
        # 添加 frontmatter
        if note.frontmatter:
            lines.append("---")
            lines.append(yaml.dump(note.frontmatter, allow_unicode=True))
            lines.append("---")
            lines.append("")
        
        # 添加内容
        lines.append(note.content)
        
        return "\n".join(lines)
    
    def sync_emotions(
        self,
        emotion_state: Dict,
        notes: Optional[List[ObsidianNote]] = None
    ) -> Dict[str, str]:
        """
        同步情感状态到笔记
        
        Returns:
            Dict: {note_path: status}
        """
        if notes is None:
            notes = self.get_all_notes()
        
        results = {}
        
        for note in notes:
            try:
                # 检查是否需要更新
                metadata = self.get_emotion_metadata(note)
                
                if metadata is None or self._should_update(metadata, emotion_state):
                    # 添加元数据
                    serialized = self.add_emotion_metadata(
                        note,
                        emotion_state.get("pad", {}),
                        emotion_state.get("context", "")
                    )
                    
                    # 写回文件
                    full_path = self.vault_path / note.path
                    with open(full_path, "w", encoding=self.encoding) as f:
                        f.write(serialized)
                    
                    results[note.path] = "updated"
                else:
                    results[note.path] = "skipped"
                    
            except Exception as e:
                results[note.path] = f"error: {str(e)}"
        
        return results
    
    def _should_update(self, metadata: LimbicMetadata, emotion_state: Dict) -> bool:
        """判断是否应该更新"""
        import datetime
        
        # 超过1小时未更新
        if not metadata.last_emotion_update:
            return True
        
        try:
            last = datetime.datetime.fromisoformat(metadata.last_emotion_update)
            now = datetime.datetime.now()
            
            if (now - last).total_seconds() > 3600:
                return True
        except:
            pass
        
        return False
    
    def get_notes_by_emotion(
        self,
        emotion_filter: Dict[str, float],
        notes: Optional[List[ObsidianNote]] = None
    ) -> List[ObsidianNote]:
        """根据情感过滤笔记"""
        if notes is None:
            notes = self.get_all_notes()
        
        matching = []
        
        for note in notes:
            metadata = self.get_emotion_metadata(note)
            
            if metadata:
                # 检查情感匹配
                match = True
                for key, value in emotion_filter.items():
                    note_value = metadata.emotion.get(key, 0)
                    if abs(note_value - value) > 0.2:
                        match = False
                        break
                
                if match:
                    matching.append(note)
        
        return matching


# 示例
if __name__ == "__main__":
    # 注意: 需要实际的 vault 路径
    # adapter = ObsidianAdapter("/path/to/obsidian/vault")
    # notes = adapter.get_all_notes()
    print("Obsidian adapter ready")
    print("Usage: adapter = ObsidianAdapter('/path/to/vault')")
