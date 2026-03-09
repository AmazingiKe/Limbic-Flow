"""
Markdown 渲染器
"""

import re
from typing import Dict


class MarkdownRenderer:
    """简单 Markdown 渲染器"""
    
    def __init__(self):
        self.handlers = {
            'h1': self.render_h1,
            'h2': self.render_h2,
            'h3': self.render_h3,
            'p': self.render_p,
            'code': self.render_code,
            'list': self.render_list,
            'link': self.render_link,
            'bold': self.render_bold,
            'italic': self.render_italic,
        }
    
    def render(self, md: str) -> str:
        """渲染 Markdown"""
        html = md
        
        # 代码块
        html = re.sub(r'```(\w+)?\n(.*?)```', 
                     r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
        
        # 行内代码
        html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
        
        # 标题
        html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        
        # 粗体
        html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html)
        
        # 斜体
        html = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', html)
        
        # 链接
        html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
        
        # 列表
        html = re.sub(r'^- (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        
        # 段落
        html = re.sub(r'\n\n', r'</p><p>', html)
        
        return f'<div class="markdown">{html}</div>'
    
    def render_h1(self, text): return f'<h1>{text}</h1>'
    def render_h2(self, text): return f'<h2>{text}</h2>'
    def render_h3(self, text): return f'<h3>{text}</h3>'
    def render_p(self, text): return f'<p>{text}</p>'
    def render_code(self, text): return f'<code>{text}</code>'
    def render_list(self, items): return f'<ul>{"".join(f"<li>{i}</li>" for i in items)}</ul>'
    def render_link(self, text, url): return f'<a href="{url}">{text}</a>'
    def render_bold(self, text): return f'<strong>{text}</strong>'
    def render_italic(self, text): return f'<em>{text}</em>'
