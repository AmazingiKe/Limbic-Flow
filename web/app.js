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
    isTyping: false
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
    sidebarEmotion: document.getElementById('sidebar-emotion'),
    btnSettings: document.getElementById('btn-settings'),
    btnEmotion: document.getElementById('btn-emotion'),
    closeSettings: document.getElementById('close-settings'),
    closeEmotion: document.getElementById('close-emotion'),
    saveConfig: document.getElementById('save-config'),
    resetEmotion: document.getElementById('reset-emotion'),
    personality: document.getElementById('personality'),
    pathology: document.getElementById('pathology'),
    provider: document.getElementById('llm-provider'),
    model: document.getElementById('llm-model'),
    apiKey: document.getElementById('llm-api-key')
};

// 情绪图标映射
const emotionIcons = {
    joy: '😊',
    sadness: '😢',
    anger: '😠',
    fear: '😨',
    surprise: '😲',
    disgust: '🤢',
    neutral: '😐',
    love: '❤️',
    anxiety: '😰'
};

// GIF 反应
const gifReactions = {
    positive: ['👍', '❤️', '😊', '🎉', '✨'],
    negative: ['😔', '💔', '😞', '😢'],
    thinking: ['🤔', '💭', '🧐'],
    surprised: ['😮', '😲', '🎉']
};

// 初始化
function init() {
    loadConfig();
    setupEventListeners();
    updateEmotionDisplay();
}

// 事件监听
function setupEventListeners() {
    // 发送消息
    elements.sendBtn.addEventListener('click', sendMessage);
    elements.input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // 输入框自动调整高度
    elements.input.addEventListener('input', autoResize);

    // 侧边栏
    elements.btnSettings.addEventListener('click', () => openSidebar('settings'));
    elements.btnEmotion.addEventListener('click', () => openSidebar('emotion'));
    elements.closeSettings.addEventListener('click', () => closeSidebar('settings'));
    elements.closeEmotion.addEventListener('click', () => closeSidebar('emotion'));
    elements.overlay.addEventListener('click', closeAllSidebars);

    // 保存配置
    elements.saveConfig.addEventListener('click', saveConfig);
    elements.resetEmotion.addEventListener('click', resetEmotion);
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

    // 隐藏欢迎画面
    if (elements.welcome) {
        elements.welcome.style.display = 'none';
    }

    // 添加用户消息
    addMessage(text, 'user');

    // 清空输入框
    elements.input.value = '';
    elements.input.style.height = 'auto';

    // 显示打字动画
    showTyping();

    // 更新情绪
    updateEmotionFromText(text);

    // 模拟 AI 响应
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
        <div class="message-avatar">${sender === 'user' ? '👤' : '🧠'}</div>
        <div class="message-content">
            <div class="message-bubble">${escapeHtml(text)}</div>
            <span class="message-time">${getTime()}</span>
        </div>
    `;

    elements.chat.appendChild(messageEl);
    scrollToBottom();
}

// 显示打字动画
function showTyping() {
    state.isTyping = true;
    const typingEl = document.createElement('div');
    typingEl.className = 'message ai';
    typingEl.id = 'typing-indicator';
    typingEl.innerHTML = `
        <div class="message-avatar">🧠</div>
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
    if (typingEl) {
        typingEl.remove();
    }
    state.isTyping = false;
}

// 生成响应
function generateResponse(userText) {
    const responses = [
        "我理解你的感受。让我想想...",
        "这是一个很有趣的话题。你为什么会这么认为呢？",
        "我明白你的意思了。",
        "感谢你分享这些。你希望我怎样帮助你？",
        "我在这里倾听。继续说吧。",
        "这让我有了新的思考角度。",
        "我感受到了你的情绪。",
        "让我们一起探讨这个问题。"
    ];

    const response = responses[Math.floor(Math.random() * responses.length)];
    addMessage(response, 'ai');

    // 根据用户输入更新情绪
    updateEmotionFromText(userText);
}

// 从文本更新情绪
function updateEmotionFromText(text) {
    const textLower = text.toLowerCase();

    // 简单的情绪关键词检测
    const positiveWords = ['好', '开心', '喜欢', '棒', '谢谢', 'happy', 'good', 'great', 'love'];
    const negativeWords = ['难过', '生气', '伤心', 'bad', 'sad', 'angry', 'hate'];
    const excitedWords = ['哇', '太棒了', '激动', 'amazing', 'excited', 'wow'];

    let emotionChange = { pleasure: 0, arousal: 0 };

    positiveWords.forEach(word => {
        if (textLower.includes(word)) emotionChange.pleasure += 10;
    });

    negativeWords.forEach(word => {
        if (textLower.includes(word)) emotionChange.pleasure -= 10;
    });

    excitedWords.forEach(word => {
        if (textLower.includes(word)) {
            emotionChange.pleasure += 5;
            emotionChange.arousal += 15;
        }
    });

    // 应用变化
    state.emotion.pleasure = Math.max(0, Math.min(100, state.emotion.pleasure + emotionChange.pleasure));
    state.emotion.arousal = Math.max(0, Math.min(100, state.emotion.arousal + emotionChange.arousal));

    // 更新显示
    updateEmotionDisplay();
    updateAvatar();
}

// 更新情绪显示
function updateEmotionDisplay() {
    const emotionMain = document.getElementById('emotion-main');
    const emotionArousal = document.getElementById('emotion-arousal');
    const emotionDominance = document.getElementById('emotion-dominance');
    const emotionDopamine = document.getElementById('emotion-dopamine');

    if (emotionMain) emotionMain.textContent = Math.round(state.emotion.pleasure);
    if (emotionArousal) emotionArousal.textContent = Math.round(state.emotion.arousal);
    if (emotionDominance) emotionDominance.textContent = Math.round(state.emotion.dominance);
    if (emotionDopamine) emotionDopamine.textContent = Math.round(state.emotion.dopamine);

    // 更新头像
    updateAvatar();
}

// 更新头像
function updateAvatar() {
    const emotionIcon = getEmotionIcon();
    elements.avatar.textContent = emotionIcon;
}

// 获取情绪图标
function getEmotionIcon() {
    if (state.emotion.pleasure > 70) return '😊';
    if (state.emotion.pleasure < 30) return '😢';
    if (state.emotion.arousal > 70) return '😮';
    if (state.emotion.pleasure > 50 && state.emotion.arousal > 50) return '😄';
    return '🧠';
}

// 打开侧边栏
function openSidebar(type) {
    const sidebar = type === 'settings' ? elements.sidebarSettings : elements.sidebarEmotion;
    sidebar.classList.add('active');
    elements.overlay.classList.add('active');
}

// 关闭侧边栏
function closeSidebar(type) {
    const sidebar = type === 'settings' ? elements.sidebarSettings : elements.sidebarEmotion;
    sidebar.classList.remove('active');
    elements.overlay.classList.remove('active');
}

// 关闭所有侧边栏
function closeAllSidebars() {
    elements.sidebarSettings.classList.remove('active');
    elements.sidebarEmotion.classList.remove('active');
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
    closeAllSidebars();
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

// 重置情绪
function resetEmotion() {
    state.emotion = {
        pleasure: 50,
        arousal: 50,
        dominance: 50,
        dopamine: 50,
        cortisol: 50,
        serotonin: 50
    };
    updateEmotionDisplay();
    alert('情绪已重置！');
}

// 滚动到底部
function scrollToBottom() {
    elements.chat.scrollTop = elements.chat.scrollHeight;
}

// 获取时间
function getTime() {
    const now = new Date();
    return now.getHours().toString().padStart(2, '0') + ':' + 
           now.getMinutes().toString().padStart(2, '0');
}

// HTML 转义
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', init);
