// Limbic-Flow 现代聊天应用

// 全局状态
const state = {
    messages: [],
    emotion: {
        pleasure: 50,
        arousal: 50,
        dominance: 50,
        dopamine: 50,
        cortisol: 50,
        serotonin: 50
    },
    config: {
        personality: 'default',
        pathology: 'none',
        provider: 'mock',
        model: '',
        apiKey: ''
    },
    isTyping: false,
    lastMessageTime: Date.now(),
    autoCheckInterval: null
};

// DOM 元素
const elements = {
    chat: document.getElementById('chat'),
    input: document.getElementById('input'),
    sendBtn: document.getElementById('btn-send'),
    avatar: document.getElementById('avatar'),
    statusText: document.getElementById('status-text'),
    welcome: document.getElementById('welcome'),
    overlay: document.getElementById('overlay'),
    sidebarSettings: document.getElementById('sidebar-settings'),
    btnSettings: document.getElementById('btn-settings'),
    closeSettings: document.getElementById('close-settings'),
    saveConfig: document.getElementById('save-config'),
    personality: document.getElementById('personality'),
    pathology: document.getElementById('pathology'),
    provider: document.getElementById('llm-provider'),
    model: document.getElementById('llm-model'),
    apiKey: document.getElementById('llm-api-key')
};

// 初始化
function init() {
    loadConfig();
    loadChatHistory();
    setupEventListeners();
    updateAvatar();
    startAutoCheck();
}

// 自动检查 - 检测是否需要主动发消息
function startAutoCheck() {
    state.autoCheckInterval = setInterval(() => {
        checkAndInitiateConversation();
    }, 30000);
}

// 检查并主动发起对话
function checkAndInitiateConversation() {
    const now = Date.now();
    const gapMinutes = (now - state.lastMessageTime) / 60000;
    
    if (gapMinutes > 5 && !state.isTyping) {
        let responses = [];
        
        if (gapMinutes > 60) {
            responses = ["你好像忙很久了😴", "在干嘛呢？", "怎么不理我了💔"];
        } else if (gapMinutes > 30) {
            responses = ["有点无聊了...", "在干嘛呀", "陪我聊聊天嘛"];
        } else {
            responses = ["怎么突然安静了", "在忙什么？", "嗯？"];
        }
        
        const response = responses[Math.floor(Math.random() * responses.length)];
        
        showTyping();
        
        setTimeout(() => {
            hideTyping();
            addMessage(response, 'ai');
            state.emotion.pleasure = Math.max(20, state.emotion.pleasure - 5);
            updateAvatar();
        }, 1000 + Math.random() * 1500);
    }
}

// 事件监听
function setupEventListeners() {
    elements.sendBtn.addEventListener('click', sendMessage);
    elements.input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    elements.input.addEventListener('input', autoResize);
    elements.btnSettings.addEventListener('click', openSettings);
    elements.closeSettings.addEventListener('click', closeSettings);
    elements.overlay.addEventListener('click', closeSettings);
    elements.saveConfig.addEventListener('click', saveConfig);
}

// 自动调整输入框高度
function autoResize() {
    elements.input.style.height = 'auto';
    elements.input.style.height = Math.min(elements.input.scrollHeight, 120) + 'px';
}

// 发送消息
function sendMessage() {
    const text = elements.input.value.trim();
    if (!text) return;

    state.lastMessageTime = Date.now();

    if (elements.welcome) {
        elements.welcome.style.display = 'none';
    }

    addMessage(text, 'user');
    elements.input.value = '';
    elements.input.style.height = 'auto';

    showTyping();
    updateEmotionFromText(text);

    setTimeout(() => {
        hideTyping();
        generateResponse(text);
    }, 1000 + Math.random() * 1500);
}

// 添加消息
function addMessage(text, sender) {
    const messageEl = document.createElement('div');
    messageEl.className = `message ${sender}`;
    messageEl.innerHTML = `
        <div class="message-avatar">${sender === 'user' ? '👤' : '🦊'}</div>
        <div class="message-content">
            <div class="message-bubble">${escapeHtml(text)}</div>
            <span class="message-time">${getTime()}</span>
        </div>
    `;
    elements.chat.appendChild(messageEl);
    scrollToBottom();
    state.messages.push({ text, sender, time: Date.now() });
    saveChatHistory();
}

// 显示打字动画
function showTyping() {
    state.isTyping = true;
    const typingEl = document.createElement('div');
    typingEl.className = 'message ai';
    typingEl.id = 'typing-indicator';
    typingEl.innerHTML = `
        <div class="message-avatar">🦊</div>
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;
    elements.chat.appendChild(typingEl);
    scrollToBottom();
}

// 隐藏打字动画
function hideTyping() {
    const typingEl = document.getElementById('typing-indicator');
    if (typingEl) typingEl.remove();
    state.isTyping = false;
}

// 生成响应
function generateResponse(userText) {
    const text = userText.toLowerCase();
    let response = '';
    let emotionChange = { pleasure: 0, arousal: 0 };
    
    if (text.includes('?') || text.includes('吗') || text.includes('呢') || text.includes('什么')) {
        const questions = ["你怎么会想问这个？", "这个问题有点意思", "你在考我吗？😏"];
        response = questions[Math.floor(Math.random() * questions.length)];
    }
    else if (text.includes('你好') || text.includes('hi') || text.includes('hello') || text.includes('在吗')) {
        response = "嘿！找我干嘛？";
        emotionChange.arousal = 10;
    }
    else if (text.includes('傻') || text.includes('蠢') || text.includes('sb') || text.includes('垃圾')) {
        const angry = ["喂过分了哦 😤", "你是不是对AI有什么误解", "我招你惹你了😂"];
        response = angry[Math.floor(Math.random() * angry.length)];
        emotionChange.arousal = 20;
        emotionChange.pleasure = -10;
    }
    else if (text.includes('好') || text.includes('棒') || text.includes('厉害') || text.includes('牛')) {
        response = "谬赞了哈哈 😊";
        emotionChange.pleasure = 15;
    }
    else if (text.length <= 2) {
        const short = ["嗯？", "说啥呢", "你在暗示什么", "..."];
        response = short[Math.floor(Math.random() * short.length)];
    }
    else if (text.includes('!') || text.includes('！')) {
        response = "这么激动干啥";
        emotionChange.arousal = 15;
    }
    else {
        const understanding = ["然后呢？", "我在听", "嗯...所以呢？", "继续说，我在听"];
        response = understanding[Math.floor(Math.random() * understanding.length)];
        emotionChange.arousal = 5;
    }
    
    addMessage(response, 'ai');
    state.emotion.pleasure = Math.max(0, Math.min(100, state.emotion.pleasure + emotionChange.pleasure));
    state.emotion.arousal = Math.max(0, Math.min(100, state.emotion.arousal + emotionChange.arousal));
    updateAvatar();
}

// 从文本更新情绪
function updateEmotionFromText(text) {
    const textLower = text.toLowerCase();
    let emotionChange = { pleasure: 0, arousal: 0 };

    const positiveWords = ['好', '开心', '喜欢', '棒', '谢谢', 'happy', 'good', 'great', 'love'];
    const negativeWords = ['难过', '生气', '伤心', 'bad', 'sad', 'angry', 'hate'];
    const excitedWords = ['哇', '太棒了', '激动', 'amazing', 'excited', 'wow'];

    positiveWords.forEach(word => { if (textLower.includes(word)) emotionChange.pleasure += 10; });
    negativeWords.forEach(word => { if (textLower.includes(word)) emotionChange.pleasure -= 10; });
    excitedWords.forEach(word => { if (textLower.includes(word)) { emotionChange.pleasure += 5; emotionChange.arousal += 15; } });

    state.emotion.pleasure = Math.max(0, Math.min(100, state.emotion.pleasure + emotionChange.pleasure));
    state.emotion.arousal = Math.max(0, Math.min(100, state.emotion.arousal + emotionChange.arousal));
    updateAvatar();
}

// 更新头像
function updateAvatar() {
    elements.avatar.textContent = getEmotionIcon();
}

// 获取情绪图标
function getEmotionIcon() {
    const { pleasure, arousal } = state.emotion;
    if (arousal > 70) { if (pleasure > 60) return '🤩'; if (pleasure > 30) return '😤'; if (pleasure < 30) return '😫'; return '🤪'; }
    if (arousal > 50) { if (pleasure > 60) return '😄'; if (pleasure > 30) return '😊'; if (pleasure < 30) return '😒'; return '🙂'; }
    if (arousal > 30) { if (pleasure > 60) return '😊'; if (pleasure > 30) return '🙂'; if (pleasure < 30) return '😔'; return '😐'; }
    if (arousal < 30) { if (pleasure > 60) return '😌'; if (pleasure > 30) return '😌'; if (pleasure < 30) return '😴'; return '😌'; }
    return '🙂';
}

// 打开设置
function openSettings() {
    elements.sidebarSettings.classList.add('active');
    elements.overlay.classList.add('active');
}

// 关闭设置
function closeSettings() {
    elements.sidebarSettings.classList.remove('active');
    elements.overlay.classList.remove('active');
}

// 保存配置
function saveConfig() {
    state.config.personality = elements.personality.value;
    state.config.pathology = elements.pathology.value;
    state.config.provider = elements.provider.value;
    state.config.model = elements.model.value;
    state.config.apiKey = elements.apiKey.value;
    localStorage.setItem('limbic-flow-config', JSON.stringify(state.config));
    alert('配置已保存！');
    closeSettings();
}

// 加载配置
function loadConfig() {
    const saved = localStorage.getItem('limbic-flow-config');
    if (saved) {
        state.config = JSON.parse(saved);
        elements.personality.value = state.config.personality;
        elements.pathology.value = state.config.pathology;
        elements.provider.value = state.config.provider;
        elements.model.value = state.config.model;
        elements.apiKey.value = state.config.apiKey;
    }
}

// 保存聊天记录
function saveChatHistory() {
    localStorage.setItem('limbic-chat-history', JSON.stringify(state.messages));
    localStorage.setItem('limbic-emotion', JSON.stringify(state.emotion));
    localStorage.setItem('limbic-last-time', state.lastMessageTime.toString());
}

// 加载聊天记录
function loadChatHistory() {
    try {
        const messages = localStorage.getItem('limbic-chat-history');
        const emotion = localStorage.getItem('limbic-emotion');
        const lastTime = localStorage.getItem('limbic-last-time');
        
        if (messages) {
            const msgs = JSON.parse(messages);
            if (msgs.length > 0) {
                if (elements.welcome) elements.welcome.style.display = 'none';
                msgs.forEach(msg => addMessage(msg.text, msg.sender));
            }
        }
        if (emotion) state.emotion = JSON.parse(emotion);
        if (lastTime) state.lastMessageTime = parseInt(lastTime);
    } catch (e) { console.log('加载历史记录失败:', e); }
}

// 滚动到底部
function scrollToBottom() {
    elements.chat.scrollTop = elements.chat.scrollHeight;
}

// 获取时间
function getTime() {
    const now = new Date();
    return now.getHours().toString().padStart(2, '0') + ':' + now.getMinutes().toString().padStart(2, '0');
}

// HTML 转义
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', init);
