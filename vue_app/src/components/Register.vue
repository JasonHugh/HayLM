<template>
  <t-navbar title="设备注册" :fixed="false">
  </t-navbar>
    <t-form
      ref="form"
      :data="formData"
      :rules="rules"
      reset-type="initial"
      show-error-message
      label-align="left"
      scroll-to-first-error="auto"
      @submit="register"
    >
      <t-form-item label="用户名" name="name">
        <t-input v-model="formData.name" borderless placeholder="请输入用户名"></t-input>
      </t-form-item>
      <t-form-item label="密码" name="password">
        <t-input v-model="formData.password" borderless type="password" :clearable="false" placeholder="请输入密码">
          <template #suffixIcon>
            <BrowseOffIcon />
          </template>
        </t-input>
      </t-form-item>
      <t-form-item label="手机号" name="phone">
        <t-input tips="手机号用于重置密码" v-model="formData.phone" borderless placeholder="请输入手机号"></t-input>
      </t-form-item>
      <t-form-item label="SN" name="SN">
        <t-input tips="请在产品卡中查看SN码" v-model="formData.SN" borderless placeholder="请输入SN码"></t-input>
      </t-form-item>
      <div class="button-group">
        <t-button theme="primary" type="submit" size="large">注册</t-button>
      </div>
    </t-form>
</template>
<script lang="ts" setup>
import { useRouter, useRoute } from 'vue-router'
const router = useRouter()
import { Message, Toast } from 'tdesign-mobile-vue';
import { ref, reactive, defineProps, toRefs, onMounted } from 'vue';
import { BrowseOffIcon } from 'tdesign-icons-vue-next';
import axios from 'axios';
  
const formData = reactive({
  name: '',
  password: '',
  phone: '',
  SN: ''
});

const rules = {
  name: [{ validator: (val: String) => /^[a-zA-Z0-9_-]{3,16}$/.test(val), message: '长度3-16个字符，只允许英文字符/数字/_/-' }],
  password: [{ validator: (val: String) => val.length > 6, message: '长度大于6个字符' }],
  phone: [{ validator: (val: String) => /^1[3-9]\d{9}$/.test(val), message: '请输入正确的手机号' }],
  SN: [{ validator: (val: String) => (val !== '') && (val.length == 11), message: '请输入11位SN码' }],
};

const register = (e: any) => {
  if(e.validateResult === true){
    axios.post(import.meta.env.VITE_API_URL+'/api/register', formData, {
      headers: {
        'accept': 'application/json'
      }
    }).then(response => {
      if (response.data.success) {
        localStorage.setItem('token', response.data.access_token);
        router.push({ path: "/config" });
      }else{
        console.error(response.data.message)
        Toast(response.data.message);
      }
    }).catch(error => {
      console.error(error)
      Toast("注册失败");
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
