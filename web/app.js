const API = 'http://localhost:8001';
const CHAT_KEY = 'limbic_chat';
const CONFIG_KEY = 'limbic_config';

const App = {
    chat: document.getElementById('chat'),
    input: document.getElementById('input'),
    sendBtn: document.getElementById('btn-send'),
    sidebarSettings: document.getElementById('sidebar-settings'),
    sidebarEmotion: document.getElementById('sidebar-emotion'),
    overlay: document.getElementById('overlay'),
    
    init() {
        this.loadConfig();
        this.loadChat();
        this.bindEvents();
        this.pollEmotion();
    },
    
    loadConfig() {
        try {
            const cfg = JSON.parse(localStorage.getItem(CONFIG_KEY));
            if (cfg) {
                document.getElementById('personality').value = cfg.personality || 'default';
                document.getElementById('pathology').value = cfg.pathology || 'none';
                document.getElementById('llm-provider').value = cfg.llmProvider || 'mock';
                document.getElementById('llm-model').value = cfg.llmModel || '';
                document.getElementById('llm-api-key').value = cfg.llmApiKey || '';
            }
        } catch(e) { console.log(e); }
    },
    
    loadChat() {
        try {
            const msgs = JSON.parse(localStorage.getItem(CHAT_KEY));
            if (msgs && msgs.length > 0) {
                msgs.forEach(m => this.appendMsg(m.content, m.sender));
            }
        } catch(e) { console.log(e); }
    },
    
    saveChat() {
        const msgs = [];
        this.chat.querySelectorAll('.message').forEach(el => {
            msgs.push({
                content: el.querySelector('.content').textContent,
                sender: el.classList.contains('user') ? 'user' : 'bot'
            });
        });
        localStorage.setItem(CHAT_KEY, JSON.stringify(msgs.slice(-50)));
    },
    
    bindEvents() {
        this.sendBtn.addEventListener('click', () => this.send());
        this.input.addEventListener('keydown', e => {
            if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); this.send(); }
        });
        this.input.addEventListener('input', () => {
            this.input.style.height = 'auto';
            this.input.style.height = Math.min(this.input.scrollHeight, 120) + 'px';
        });
        
        document.getElementById('btn-settings').onclick = () => this.openSidebar('settings');
        document.getElementById('btn-emotion').onclick = () => this.openSidebar('emotion');
        document.getElementById('close-settings').onclick = () => this.closeSidebar();
        document.getElementById('close-emotion').onclick = () => this.closeSidebar();
        this.overlay.onclick = () => this.closeSidebar();
        
        document.getElementById('save-config').onclick = () => this.saveConfig();
        document.getElementById('reset-emotion').onclick = () => this.resetEmotion();
    },
    
    openSidebar(type) {
        this.sidebarSettings.classList.remove('active');
        this.sidebarEmotion.classList.remove('active');
        if (type === 'settings') this.sidebarSettings.classList.add('active');
        else this.sidebarEmotion.classList.add('active');
        this.overlay.classList.add('active');
    },
    
    closeSidebar() {
        this.sidebarSettings.classList.remove('active');
        this.sidebarEmotion.classList.remove('active');
        this.overlay.classList.remove('active');
    },
    
    async send() {
        const text = this.input.value.trim();
        if (!text) return;
        
        this.appendMsg(text, 'user');
        this.input.value = '';
        this.input.style.height = 'auto';
        
        const loading = this.appendLoading();
        
        try {
            const res = await fetch(`${API}/process`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    user_input: text,
                    context: {
                        personality: document.getElementById('personality').value,
                        pathology: document.getElementById('pathology').value
                    }
                })
            });
            const data = await res.json();
            loading.remove();
            
            const reply = data.actions?.filter(a => a.action === 'message').map(a => a.content).join('') || '...';
            this.appendMsg(reply, 'bot');
        } catch(e) {
            loading.remove();
            this.appendMsg('连接失败', 'bot');
        }
        
        this.saveChat();
        this.pollEmotion();
    },
    
    appendMsg(text, sender) {
        const div = document.createElement('div');
        div.className = `message ${sender}`;
        div.innerHTML = `<div class="avatar">${sender === 'bot' ? '🧠' : '👤'}</div><div class="content">${this.escape(text)}</div>`;
        this.chat.appendChild(div);
        this.chat.scrollTop = this.chat.scrollHeight;
    },
    
    appendLoading() {
        const div = document.createElement('div');
        div.className = 'message bot';
        div.innerHTML = `<div class="avatar">🧠</div><div class="content"><div class="typing"><span></span><span></span><span></span></div></div>`;
        this.chat.appendChild(div);
        this.chat.scrollTop = this.chat.scrollHeight;
        return div;
    },
    
    async pollEmotion() {
        try {
            const res = await fetch(`${API}/emotion/current`);
            const data = await res.json();
            const e = data.emotion || {};
            this.updateBar('pleasure', e.pleasure);
            this.updateBar('arousal', e.arousal);
            this.updateBar('dominance', e.dominance);
            this.updateBar('dopamine', e.dopamine);
            this.updateBar('cortisol', e.cortisol);
        } catch(e) {}
        setTimeout(() => this.pollEmotion(), 3000);
    },
    
    updateBar(key, val) {
        const v = parseFloat(val) || 0;
        const pct = (v + 1) * 50;
        document.getElementById(`bar-${key}`).style.width = `${Math.min(100, Math.max(0, pct))}%`;
        document.getElementById(`val-${key}`).textContent = Math.round(v * 100);
    },
    
    async saveConfig() {
        const cfg = {
            personality: document.getElementById('personality').value,
            pathology: document.getElementById('pathology').value,
            llmProvider: document.getElementById('llm-provider').value,
            llmModel: document.getElementById('llm-model').value,
            llmApiKey: document.getElementById('llm-api-key').value
        };
        localStorage.setItem(CONFIG_KEY, JSON.stringify(cfg));
        
        try {
            await fetch(`${API}/config`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({personality: cfg.personality, pathology: cfg.pathology})
            });
        } catch(e) {}
        
        alert('已保存');
        this.closeSidebar();
    },
    
    async resetEmotion() {
        try {
            await fetch(`${API}/emotion/reset`, {method: 'POST'});
            this.appendMsg('情绪已重置~', 'bot');
            this.saveChat();
        } catch(e) {}
        this.closeSidebar();
    },
    
    escape(t) {
        const d = document.createElement('div');
        d.textContent = t;
        return d.innerHTML;
    }
};

document.addEventListener('DOMContentLoaded', () => App.init());
