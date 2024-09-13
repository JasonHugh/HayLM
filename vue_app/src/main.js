// import './assets/main.css'
import 'tdesign-mobile-vue/es/style/index.css';

import { createMemoryHistory, createRouter } from 'vue-router'
import { createApp, onMounted } from 'vue'
import TDesign from 'tdesign-mobile-vue';
import App from './App.vue'
import ChatHistory from './components/ChatHistory.vue';
import UserConfig from './components/UserConfig.vue';
import Login from './components/Login.vue';
import Chat from './components/Chat.vue';

const routes = [
    {
        path: '/',
        name: 'history', 
        component: ChatHistory
    },
    { 
        name: 'config', 
        path: '/config', 
        component: UserConfig 
    },
    { 
        name: 'login', 
        path: '/login', 
        component: Login 
    },
    { 
        name: 'chat', 
        path: '/chat', 
        component: Chat 
    },
]

const router = createRouter({
    history: createMemoryHistory(),
    routes
})

createApp(App).use(TDesign).use(router).mount('#app')