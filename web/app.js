// Limbic-Flow Chat Frontend - ChatGPT Style

const API_BASE = 'http://localhost:8001';
const CONFIG_KEY = 'limbic_flow_config';

class ChatApp {
    constructor() {
        this.chatContainer = document.getElementById('chat-container');
        this.messageInput = document.getElementById('message-input');
        this.sendBtn = document.getElementById('send-btn');
        
        // 设置相关
        this.personalitySelect = document.getElementById('personality');
        this.pathologySelect = document.getElementById('pathology');
        this.llmProviderSelect = document.getElementById('llm-provider');
        this.llmModelInput = document.getElementById('llm-model');
        this.llmApiKeyInput = document.getElementById('llm-api-key');
        this.llmBaseUrlInput = document.getElementById('llm-base-url');
        this.saveConfigBtn = document.getElementById('save-config-btn');
        
        this.resetBtn = document.getElementById('reset-btn');
        this.newChatBtn = document.getElementById('new-chat-btn');
        
        // 加载保存的配置
        this.loadConfig();
        
        // 绑定事件
        this.saveConfigBtn.addEventListener('click', () => this.saveConfig());
        
        this.init();
    }
    
    // 从 localStorage 加载配置
    loadConfig() {
        try {
            const saved = localStorage.getItem(CONFIG_KEY);
            if (saved) {
                const config = JSON.parse(saved);
                this.personalitySelect.value = config.personality || 'default';
                this.pathologySelect.value = config.pathology || 'none';
                this.llmProviderSelect.value = config.llmProvider || 'mock';
                this.llmModelInput.value = config.llmModel || '';
                this.llmApiKeyInput.value = config.llmApiKey || '';
                this.llmBaseUrlInput.value = config.llmBaseUrl || '';
                
                console.log('配置已加载:', config);
            }
        } catch (e) {
            console.error('加载配置失败:', e);
        }
    }
    
    // 保存配置到 localStorage
    saveConfig() {
        const config = {
            personality: this.personalitySelect.value,
            pathology: this.pathologySelect.value,
            llmProvider: this.llmProviderSelect.value,
            llmModel: this.llmModelInput.value,
            llmApiKey: this.llmApiKeyInput.value,
            llmBaseUrl: this.llmBaseUrlInput.value,
        };
        
        try {
            localStorage.setItem(CONFIG_KEY, JSON.stringify(config));
            console.log('配置已保存:', config);
            
            // 同时发送到后端
            this.updateConfig();
            this.updateLLMConfig(config);
            
            alert('配置已保存！');
        } catch (e) {
            console.error('保存配置失败:', e);
            alert('保存失败: ' + e.message);
        }
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
        
        // 新对话按钮
        this.newChatBtn.addEventListener('click', () => this.newChat());
        
        // 欢迎页元素
        this.welcomeScreen = this.chatContainer.querySelector('.welcome-screen');
        
        // 定期获取情绪状态
        this.updateEmotionDisplay();
        setInterval(() => this.updateEmotionDisplay(), 3000);
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
    
    async updateLLMConfig(config) {
        try {
            await fetch(`${API_BASE}/llm-config`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    provider: config.llmProvider,
                    model: config.llmModel,
                    api_key: config.llmApiKey,
                    base_url: config.llmBaseUrl
                })
            });
        } catch (error) {
            console.error('Error updating LLM config:', error);
        }
    }
    
    newChat() {
        // 清空聊天记录
        this.chatContainer.innerHTML = '';
        
        // 恢复欢迎页
        this.chatContainer.innerHTML = `
            <div class="welcome-screen">
                <div class="welcome-icon">🧠</div>
                <h2>我是 Limbic-Flow</h2>
                <p>一个有点情绪化的 AI，可以当我是个有感情的朋友~</p>
            </div>
        `;
        this.welcomeScreen = this.chatContainer.querySelector('.welcome-screen');
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
