// Limbic-Flow Chat Frontend - Simplified

const API_BASE = 'http://localhost:8001';
const CONFIG_KEY = 'limbic_flow_config';

class ChatApp {
    constructor() {
        this.chatContainer = document.getElementById('chat-container');
        this.messageInput = document.getElementById('message-input');
        this.sendBtn = document.getElementById('send-btn');
        
        // Panels
        this.settingsPanel = document.getElementById('settings-panel');
        this.emotionPanel = document.getElementById('emotion-panel');
        
        // Settings elements
        this.personalitySelect = document.getElementById('personality');
        this.pathologySelect = document.getElementById('pathology');
        this.llmProviderSelect = document.getElementById('llm-provider');
        this.llmModelInput = document.getElementById('llm-model');
        this.llmApiKeyInput = document.getElementById('llm-api-key');
        this.llmBaseUrlInput = document.getElementById('llm-base-url');
        
        // Buttons
        this.toggleSettingsBtn = document.getElementById('toggle-settings');
        this.toggleEmotionBtn = document.getElementById('toggle-emotion');
        this.closeSettingsBtn = document.getElementById('close-settings');
        this.closeEmotionBtn = document.getElementById('close-emotion');
        this.saveConfigBtn = document.getElementById('save-config-btn');
        this.resetBtn = document.getElementById('reset-btn');
        
        // Load saved config
        this.loadConfig();
        
        // Bind events
        this.bindEvents();
    }
    
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
            }
        } catch (e) {
            console.error('加载配置失败:', e);
        }
    }
    
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
            this.updateConfig();
            this.updateLLMConfig(config);
            alert('配置已保存！');
            this.closePanels();
        } catch (e) {
            alert('保存失败: ' + e.message);
        }
    }
    
    bindEvents() {
        // Send message
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Auto resize input
        this.messageInput.addEventListener('input', () => {
            this.messageInput.style.height = 'auto';
            this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 200) + 'px';
        });
        
        // Toggle panels
        this.toggleSettingsBtn.addEventListener('click', () => this.toggleSettings());
        this.toggleEmotionBtn.addEventListener('click', () => this.toggleEmotion());
        this.closeSettingsBtn.addEventListener('click', () => this.closePanels());
        this.closeEmotionBtn.addEventListener('click', () => this.closePanels());
        
        // Save & Reset
        this.saveConfigBtn.addEventListener('click', () => this.saveConfig());
        this.resetBtn.addEventListener('click', () => this.resetEmotion());
        
        // Welcome screen
        this.welcomeScreen = this.chatContainer.querySelector('.welcome-screen');
        
        // Poll emotion
        this.updateEmotionDisplay();
        setInterval(() => this.updateEmotionDisplay(), 3000);
    }
    
    toggleSettings() {
        this.settingsPanel.classList.toggle('active');
        this.emotionPanel.classList.remove('active');
    }
    
    toggleEmotion() {
        this.emotionPanel.classList.toggle('active');
        this.settingsPanel.classList.remove('active');
    }
    
    closePanels() {
        this.settingsPanel.classList.remove('active');
        this.emotionPanel.classList.remove('active');
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
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;
        
        // Hide welcome
        if (this.welcomeScreen) {
            this.welcomeScreen.style.display = 'none';
        }
        
        // Add user message
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        this.messageInput.style.height = 'auto';
        
        // Loading
        const loadingMsg = this.addLoadingMessage();
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
            loadingMsg.remove();
            
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
            
            this.updateEmotionDisplay();
        } catch (error) {
            console.error('Error:', error);
            loadingMsg.remove();
            this.addMessage('连接失败，请确保后端服务正在运行', 'bot');
        }
        
        this.scrollToBottom();
    }
    
    addMessage(content, sender) {
        const div = document.createElement('div');
        div.className = `message ${sender}`;
        div.innerHTML = `
            <div class="avatar">${sender === 'bot' ? '🧠' : '👤'}</div>
            <div class="content">${this.escapeHtml(content)}</div>
        `;
        this.chatContainer.appendChild(div);
        this.scrollToBottom();
    }
    
    addLoadingMessage() {
        const div = document.createElement('div');
        div.className = 'message bot';
        div.innerHTML = `
            <div class="avatar">🧠</div>
            <div class="content">
                <div class="typing"><span></span><span></span><span></span></div>
            </div>
        `;
        this.chatContainer.appendChild(div);
        this.scrollToBottom();
        return div;
    }
    
    async updateEmotionDisplay() {
        try {
            const response = await fetch(`${API_BASE}/emotion/current`);
            const data = await response.json();
            const emotion = data.emotion || {};
            
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
            this.closePanels();
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

document.addEventListener('DOMContentLoaded', () => {
    new ChatApp();
});
