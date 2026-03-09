// Limbic-Flow Chat Frontend - ChatGPT Style

const API_BASE = 'http://localhost:8001';

class ChatApp {
    constructor() {
        this.chatContainer = document.getElementById('chat-container');
        this.messageInput = document.getElementById('message-input');
        this.sendBtn = document.getElementById('send-btn');
        this.personalitySelect = document.getElementById('personality');
        this.pathologySelect = document.getElementById('pathology');
        this.resetBtn = document.getElementById('reset-btn');
        
        // 绑定切换事件
        this.personalitySelect.addEventListener('change', () => this.updateConfig());
        this.pathologySelect.addEventListener('change', () => this.updateConfig());
        
        this.init();
    }
    
    init() {
        // 绑定发送事件
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // 自动调整输入框高度
        this.messageInput.addEventListener('input', () => {
            this.messageInput.style.height = 'auto';
            this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 200) + 'px';
        });
        
        this.resetBtn.addEventListener('click', () => this.resetEmotion());
        
        // 初始欢迎消息
        this.welcomeScreen = this.chatContainer.querySelector('.welcome-screen');
        
        // 定期获取情绪状态
        this.updateEmotionDisplay();
        setInterval(() => this.updateEmotionDisplay(), 3000);
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;
        
        // 隐藏欢迎页
        if (this.welcomeScreen) {
            this.welcomeScreen.style.display = 'none';
        }
        
        // 添加用户消息
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        this.messageInput.style.height = 'auto';
        
        // 显示加载状态
        const loadingMsg = this.addLoadingMessage();
        
        // 滚动到底部
        this.scrollToBottom();
        
        try {
            const response = await fetch(`${API_BASE}/process`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_input: message,
                    context: {
                        personality: this.personalitySelect.value,
                        pathology: this.pathologySelect.value
                    }
                })
            });
            
            const data = await response.json();
            console.log('API Response:', data);
            
            // 移除加载消息
            loadingMsg.remove();
            
            // 添加机器人回复
            if (data.actions && data.actions.length > 0) {
                const botResponse = data.actions
                    .filter(a => a.action === 'message')
                    .map(a => a.content)
                    .join('');
                
                if (botResponse) {
                    this.addMessage(botResponse, 'bot');
                } else {
                    this.addMessage('抱歉，出了点问题...', 'bot');
                }
            } else {
                this.addMessage('抱歉，出了点问题...', 'bot');
            }
            
            // 更新情绪显示
            this.updateEmotionDisplay();
            
        } catch (error) {
            console.error('Error:', error);
            loadingMsg.remove();
            this.addMessage('连接失败，请确保后端服务正在运行', 'bot');
        }
        
        this.scrollToBottom();
    }
    
    addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const avatar = sender === 'bot' ? '🧠' : '👤';
        
        messageDiv.innerHTML = `
            <div class="avatar">${avatar}</div>
            <div class="content">${this.escapeHtml(content)}</div>
        `;
        
        this.chatContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    addLoadingMessage() {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot';
        messageDiv.innerHTML = `
            <div class="avatar">🧠</div>
            <div class="content">
                <div class="typing">
                    <span></span><span></span><span></span>
                </div>
            </div>
        `;
        
        this.chatContainer.appendChild(messageDiv);
        this.scrollToBottom();
        
        return messageDiv;
    }
    
    async updateEmotionDisplay() {
        try {
            const response = await fetch(`${API_BASE}/emotion/current`);
            const data = await response.json();
            
            const emotion = data.emotion || {};
            
            // 更新进度条
            this.updateBar('pleasure', emotion.pleasure);
            this.updateBar('arousal', emotion.arousal);
            this.updateBar('dominance', emotion.dominance);
            this.updateBar('dopamine', emotion.dopamine);
            this.updateBar('cortisol', emotion.cortisol);
            
        } catch (error) {
            console.error('Error fetching emotion:', error);
        }
    }
    
    updateBar(key, value) {
        const bar = document.getElementById(`bar-${key}`);
        const valueEl = document.getElementById(`value-${key}`);
        
        if (bar && valueEl) {
            // 转换到 0-100%
            const percentage = ((parseFloat(value) || 0) + 1) * 50;
            bar.style.width = `${Math.min(100, Math.max(0, percentage))}%`;
            valueEl.textContent = Math.round((parseFloat(value) || 0) * 100);
        }
    }
    
    async updateConfig() {
        try {
            await fetch(`${API_BASE}/config`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    personality: this.personalitySelect.value,
                    pathology: this.pathologySelect.value
                })
            });
        } catch (error) {
            console.error('Error updating config:', error);
        }
    }
    
    async resetEmotion() {
        try {
            await fetch(`${API_BASE}/emotion/reset`, { method: 'POST' });
            this.addMessage('情绪已重置~', 'bot');
            this.updateEmotionDisplay();
        } catch (error) {
            console.error('Error resetting emotion:', error);
        }
    }
    
    scrollToBottom() {
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// 启动应用
document.addEventListener('DOMContentLoaded', () => {
    new ChatApp();
});
