<template>
  <t-navbar title="设置" :fixed="true"></t-navbar>
  <main>
    <AiConfig />
    <t-cell-group theme="card" style="margin-top: 10px;">
      <t-cell :left-icon="app" title="教育智能体" arrow />
    </t-cell-group>
    <t-cell-group theme="card" style="margin-top: 10px;">
      <t-cell :left-icon="user" title="个人信息" arrow />
      <t-cell :left-icon="rootlist" title="陪伴报告" arrow />
      <t-cell :left-icon="rollback" title="退出登陆" arrow @click="logout" />
    </t-cell-group>
  </main>
</template>

<script lang="ts" setup>
  import { h, onMounted, ref, provide } from 'vue';
  import { UserIcon, RollbackIcon, AppIcon, PaletteIcon, Palette1Icon, RootListIcon, CheckIcon } from 'tdesign-icons-vue-next';
  import axios from 'axios';
  import { useRouter } from 'vue-router'
  const router = useRouter()
  import AiConfig from './AiConfig.vue';

  const API_URL = process.env.VITE_API_URL
  provide('API_URL', API_URL)

  const app = () => h(AppIcon);
  const user = () => h(UserIcon);
  const rollback = () => h(RollbackIcon);
  const rootlist = () => h(RootListIcon);

  const userInfo = ref()
  provide('userInfo', userInfo)
  const styledRole = ref()
  provide('styledRole', styledRole)
  const aiSelectItem = ref()
  provide('aiSelectItem', aiSelectItem)

  const loadUserInfo = () => {
    axios.get(API_URL+'/user/getConfig', {
      headers: {
        'accept': 'application/json',
      }
    }).then(response => {
      if(response.data.success){
        userInfo.value = response.data.data.config;
        styledRole.value = response.data.data.styled_role;
        if(styledRole.value){
          aiSelectItem.value = styledRole.value
        }
        console.log(userInfo.value)
        console.log(styledRole.value)
      }else{
        console.error(response.data.message);
      }
    })
    .catch(error => {
      console.error(error);
    });
  }

  const airoles = ref([])
  provide('airoles', airoles)
  const loadAIRoles = async () => {
    axios.get(API_URL+'/airoles', {
      headers: {
        'accept': 'application/json',
      }
    }).then(response => {
      if(response.data.success){
        if(response.data.data.ai_roles != null){
          airoles.value = response.data.data.ai_roles;
          console.log(airoles.value.push(response.data.data.ai_roles[1]))
        }
      }else{
        console.error(response.data.message);
      }
    })
    .catch(error => {
      console.error(error);
    });
  }
  const logout = () => {
    localStorage.removeItem('token');
    router.push({ path: "/login" });
  }
  onMounted(() => {
    // check if user logged
    const token = localStorage.getItem('token');
    if(token == null){
        router.push({ path: "/login" });
    }else{
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }
    loadUserInfo()
    loadAIRoles()
  })
</script>

<style>
</style>