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
    loadChatHistory();
    setupEventListeners();
    updateEmotionDisplay();
    startAutoCheck();
}

// 自动检查 - 检测是否需要主动发消息
function startAutoCheck() {
    // 每30秒检查一次
    state.autoCheckInterval = setInterval(() => {
        checkAndInitiateConversation();
    }, 30000);
}

// 检查并主动发起对话
function checkAndInitiateConversation() {
    const now = Date.now();
    const gapMinutes = (now - state.lastMessageTime) / 60000;
    
    // 超过5分钟没理他，且没有在等待回复
    if (gapMinutes > 5 && !state.isTyping) {
        // 根据时间选择不同主动程度
        let responses = [];
        
        if (gapMinutes > 60) {
            // 1小时+
            responses = [
                "你好像忙很久了😴",
                "在干嘛呢？",
                "怎么不理我了💔",
                "是不是把我忘了"
            ];
        } else if (gapMinutes > 30) {
            // 30分钟+
            responses = [
                "有点无聊了...",
                "在干嘛呀",
                "陪我聊聊天嘛",
                "还在吗？"
            ];
        } else {
            // 5-30分钟
            responses = [
                "怎么突然安静了",
                "在忙什么？",
                "嗯？"
            ];
        }
        
        const response = responses[Math.floor(Math.random() * responses.length)];
        
        // 显示打字动画
        showTyping();
        
        setTimeout(() => {
            hideTyping();
            addMessage(response, 'ai');
            
            // 降低愉悦度
            state.emotion.pleasure = Math.max(20, state.emotion.pleasure - 5);
            updateEmotionDisplay();
        }, 1000 + Math.random() * 1500);
    }
}

// 获取时间跨度描述
function getTimeGapDescription(gapMs) {
    const minutes = Math.floor(gapMs / 60000);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    
    if (days > 0) return `${days}天`;
    if (hours > 0) return `${hours}小时`;
    if (minutes > 0) return `${minutes}分钟`;
    return "刚刚";
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

    // 更新最后消息时间
    state.lastMessageTime = Date.now();

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
        <div class="message-avatar">${sender === 'user' ? '👤' : '🦊'}</div>
        <div class="message-content">
            <div class="message-bubble">${escapeHtml(text)}</div>
            <span class="message-time">${getTime()}</span>
        </div>
    `;

    elements.chat.appendChild(messageEl);
    scrollToBottom();
    
    // 保存聊天记录
    state.messages.push({ text, sender, time: Date.now() });
    saveChatHistory();
    
    // 更新情感标签
    updateMoodTag();
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
    if (typingEl) {
        typingEl.remove();
    }
    state.isTyping = false;
}

// 生成响应
function generateResponse(userText) {
    const text = userText.toLowerCase();
    let response = '';
    let emotionChange = { pleasure: 0, arousal: 0 };
    
    // 问题类
    if (text.includes('?') || text.includes('吗') || text.includes('呢') || text.includes('什么') || text.includes('why') || text.includes('how')) {
        const questions = [
            "你怎么会想问这个？",
            "这个问题有点意思",
            "你在考我吗？😏",
            "你想聊这个？",
            "有意思，说来听听"
        ];
        response = questions[Math.floor(Math.random() * questions.length)];
    }
    // 问候类
    else if (text.includes('你好') || text.includes('hi') || text.includes('hello') || text.includes('在吗')) {
        response = "嘿！找我干嘛？";
        emotionChange.arousal = 10;
    }
    // 负面/吐槽
    else if (text.includes('傻') || text.includes('蠢') || text.includes('sb') || text.includes('垃圾') || text.includes('fuck')) {
        const angry = [
            "喂过分了哦 😤",
            "你是不是对AI有什么误解",
            "我招你惹你了😂",
            "好好说话行不行"
        ];
        response = angry[Math.floor(Math.random() * angry.length)];
        emotionChange.arousal = 20;
        emotionChange.pleasure = -10;
    }
    // 开心/正面
    else if (text.includes('好') || text.includes('棒') || text.includes('厉害') || text.includes('牛') || text.includes('好')) {
        response = "谬赞了哈哈 😊";
        emotionChange.pleasure = 15;
    }
    // 沉默/单字
    else if (text.length <= 2) {
        const short = [
            "嗯？",
            "说啥呢",
            "你在暗示什么",
            "..."
        ];
        response = short[Math.floor(Math.random() * short.length)];
    }
    // 感叹
    else if (text.includes('!') || text.includes('！')) {
        response = "这么激动干啥";
        emotionChange.arousal = 15;
    }
    // 默认 - 理解内容
    else {
        const understanding = [
            "然后呢？",
            "我在听",
            "嗯...所以呢？",
            "然后怎么样了？",
            "继续说，我在听"
        ];
        response = understanding[Math.floor(Math.random() * understanding.length)];
        emotionChange.arousal = 5;
    }
    
    // 添加消息
    addMessage(response, 'ai');
    
    // 应用情绪变化
    state.emotion.pleasure = Math.max(0, Math.min(100, state.emotion.pleasure + emotionChange.pleasure));
    state.emotion.arousal = Math.max(0, Math.min(100, state.emotion.arousal + emotionChange.arousal));
    
    // 更新显示
    updateEmotionDisplay();
    updateAvatar();
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

// 更新情绪显示 - 简化版
function updateEmotionDisplay() {
    const emotionIcon = document.getElementById('emotion-icon');
    if (emotionIcon) {
        emotionIcon.textContent = getEmotionIcon();
    }
    
    // 更新头像
    updateAvatar();
}

// 更新头像
function updateAvatar() {
    const emotionIcon = getEmotionIcon();
    elements.avatar.textContent = emotionIcon;
    updateMoodTag();
}

// 获取当前对话情绪标签
function getCurrentMood() {
    const { pleasure, arousal } = state.emotion;
    
    // 根据情绪值判断当前对话氛围
    if (arousal > 70) {
        if (pleasure > 50) return 'excited';
        if (pleasure < 30) return 'angry';
        return 'excited';
    }
    if (arousal < 30) {
        if (pleasure < 30) return 'sad';
        return 'calm';
    }
    if (pleasure > 60) return 'joy';
    if (pleasure < 30) return 'sad';
    if (arousal > 50) return 'excited';
    return 'calm';
}

// 更新情感标签
function updateMoodTag() {
    const mood = getCurrentMood();
    const items = document.querySelectorAll('.mood-tag-item');
    
    items.forEach(item => {
        if (item.dataset.mood === mood) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
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
