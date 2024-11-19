<template>
  <t-navbar title="登录" :fixed="true"></t-navbar>
  <main>
    <t-form
      ref="form"
      :data="formData"
      :rules="rules"
      reset-type="initial"
      show-error-message
      label-align="left"
      scroll-to-first-error="auto"
      @reset="register"
      @submit="login"
    >
    <t-form-item label="用户名" name="username">
      <t-input v-model="formData.username" borderless placeholder="请输入内容"></t-input>
      </t-form-item>
      <t-form-item label="密码" name="password">
        <t-input v-model="formData.password" borderless type="password" :clearable="false" placeholder="请输入内容">
          <template #suffixIcon>
            <BrowseOffIcon />
          </template>
        </t-input>
      </t-form-item>
      <div class="button-group">
        <t-button theme="primary" type="submit" size="large">登录</t-button>
        <t-button theme="default" variant="base" type="reset" size="large">注册</t-button>
      </div>
    </t-form>
  </main>
</template>
<script lang="ts" setup>
import { useRouter, useRoute } from 'vue-router'
const router = useRouter()
import { Message, Toast } from 'tdesign-mobile-vue';
import { ref, reactive, defineProps, toRefs, onMounted } from 'vue';
import { BrowseOffIcon } from 'tdesign-icons-vue-next';
import axios from 'axios';
  
const API_URL = process.env.VITE_API_URL

const formData = reactive({
  username: '',
  password: ''
});

const rules = {
  username: [{ pattern: /^[a-zA-Z0-9_-]{3,16}$/, message: '长度3-16个字符，只允许英文字符/数字/_/-' }],
  password: [{ validator: (val: String) => val.length > 2, message: '长度大于2个字符' }],
};

const register = () => {
  router.push({ path: "/register" });
};

const login = (e: any) => {
  if(e.validateResult === true){
    axios.post(API_URL+'/login', {grant_type:'password',username: formData.username,password: formData.password,client_id:'',client_secret:''}, {
      headers: {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }).then(response => {
      localStorage.setItem('token', response.data.access_token);
      router.push({ path: "/" });
    }).catch(error => {
      console.error(error)
      Toast(error);
    });
  }
};

</script>
<style lang="less" scoped>
.box {
  width: 100%;
  display: flex;
  justify-content: space-between;
}
.upload {
  --td-upload-grid-columns: 3;
}
.textarea {
  height: 100px;
  width: 100%;
}
.button-group {
  background-color: var(--bg-color-demo, #fff);
  box-sizing: border-box;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  position: relative;
  border-bottom: 0.5px solid #e7e7e7;

  .t-button {
    height: 32px;
    flex: 1;

    &:not(:last-child) {
      flex: 1;
      margin-right: 16px;
    }
  }
}
</style>
