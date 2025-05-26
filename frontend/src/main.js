import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import VueCookies from 'vue-cookies'
import './style.css'
import App from './App.vue'
import pinia from "./stores";
import router from './router'

const app=createApp(App)
app.use(ElementPlus)
app.use(pinia)
app.use(router)
app.config.globalProperties.VueCookies = VueCookies;
app.mount('#app')