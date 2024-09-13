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
  { value: 'config', label: '设置', icon: 'user' },
]);

const jump = (value: String) => {
  if(value == 'history'){
    router.push({ path: "/" });
  }else if(value == 'chat'){
    router.push({ path: "/chat" });
  }else if(value == 'config'){
    router.push({ path: "/config" });
  }
}
</script>