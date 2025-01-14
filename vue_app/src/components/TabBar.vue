<template>
  <t-tab-bar v-model="value" theme="tag" :split="false">
    <t-tab-bar-item v-for="item in list" :key="item.value" :value="item.value" @click="jump(item.value)">
      {{ item.label }}
      <template #icon>
        <t-icon :name="item.icon" />
      </template>
    </t-tab-bar-item>
  </t-tab-bar>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Icon as TIcon } from 'tdesign-icons-vue-next';
import { useRouter, useRoute } from 'vue-router'
const router = useRouter()
const route = useRoute()

const value = ref('history');
const list = ref([
  { value: 'history', label: '历史', icon: 'history' },
  { value: 'chat', label: '聊天', icon: 'chat' },
  { value: 'game', label: '趣学', icon: 'sonic' },
  { value: 'config', label: '设置', icon: 'user' },
]);

const jump = (value: String) => {
  switch (value) {
    case 'history':
      router.push({ path: "/" });
      break;
    case 'chat':
      router.push({ path: "/chat" });
      break;
    case 'game':
      router.push({ path: "/game" });
      break;
    case 'config':
      router.push({ path: "/config" });
      break;
    default:
      break;
  }
}
</script>