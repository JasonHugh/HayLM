<template>
  <t-cell-group theme="card">
      <t-cell :left-icon="palette1" title="AI角色选择" :note="aiName" arrow hover @click="aiSelect = true" />
      <t-popup v-model="aiSelect" placement="bottom" style="height: 100vh;">
        <div class="header">
          <div class="btn btn--cancel" aria-role="button" @click="aiSelectCancel">取消</div>
          <div class="title">AI角色选择</div>
          <div class="btn btn--confirm" aria-role="button" @click="aiSelectComfirm">确定</div>
        </div>
        <t-list style="overflow-y: scroll;margin-top: 53px;height: calc(100vh - 53px);">
          <t-cell v-for="item in airoles" :right-icon="active(item.id)" :key="item.id" :title="item.ai_name" :description="item.profile" align="top" @click="aiSelectClick(item)">
            <template #leftIcon>
                <t-avatar shape="circle" :image="API_URL+'/image/'+item.avatar_path" />
            </template>
          </t-cell>
        </t-list>
        <t-overlay :visible="isShowConfirm" >
          <t-dialog
            v-model:visible="isShowConfirm"
            title=""
            content="更改AI角色将会清空所有陪伴记录，请谨慎操作！"
            cancel-btn="取消"
            confirm-btn="确认"
            @confirm="onAIConfirm"
            @cancel="onAICancel"
          ></t-dialog>
        </t-overlay>
      </t-popup>

      <t-cell :left-icon="palette" title="自定义AI角色" :note="aiCustomName" arrow hover @click="aiCustom = true" />
      <t-popup v-model="aiCustom" placement="bottom" style="height: 100vh;">
        <div class="header">
          <div class="btn btn--cancel" aria-role="button" @click="aiCustomCancel">取消</div>
          <div class="title">自定义AI角色</div>
          <div class="btn btn--cancel" aria-role="button">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div>
        </div>
        <t-form  style="overflow-y: scroll;margin-top: 53px;height: calc(100vh - 53px);"
          ref="form"
          :data="formData"
          :rules="rules"
          reset-type="initial"
          show-error-message
          label-align="left"
          :disabled="false"
          scroll-to-first-error="auto"
          @reset="onResetCustom"
          @submit="aiCustomComfirm"
        >
          <t-form-item label="AI名称" name="ai_name" help="输入你对AI的称呼，例如：悟空">
            <t-input v-model="formData.ai_name" borderless placeholder="请输入内容"></t-input>
          </t-form-item>
          <t-form-item label="AI角色" name="ai_role" help="输入希望AI扮演的角色，例如：《西游记》里的孙悟空">
            <t-input v-model="formData.ai_role" borderless placeholder="请输入内容"></t-input>
          </t-form-item>
          <t-form-item arrow label="AI音色" name="ai_timbre_name" content-align="right">
            <t-input
              v-model="formData.ai_timbre_name"
              borderless
              align="right"
              placeholder="请输入内容"
              @click="showTimbreBox = true"
            ></t-input>
            <t-popup v-model="showTimbreBox" placement="bottom">
              <t-picker
                :columns="timbreOptions"
                @confirm="onConfirmTimbre"
                @cancel="showTimbreBox = false"
              >
                <template #option="item">{{ item.label }}</template>
              </t-picker>
            </t-popup>
          </t-form-item>
          <t-form-item label="AI人设" name="ai_profile">
            <t-textarea
              v-model="formData.ai_profile"
              class="textarea"
              indicator
              :maxlength="300"
              placeholder="请输入AI的介绍，最多300字"
            ></t-textarea>
          </t-form-item>
          <div class="button-group">
            <t-button theme="primary" type="submit" size="large">提交</t-button>
            <t-button theme="default" variant="base" type="reset" size="large">重置</t-button>
          </div>
        </t-form>
        <t-overlay :visible="showDoubleConfirm" >
          <t-dialog
            v-model:visible="showDoubleConfirm"
            title=""
            content="更改AI角色将会清空所有陪伴记录，请谨慎操作！"
            cancel-btn="取消"
            confirm-btn="确认"
            @confirm="onDoubleConfirm"
            @cancel="onDoubleCancel"
          ></t-dialog>
        </t-overlay>
      </t-popup>
    </t-cell-group>
</template>
<script lang="ts" setup>
  import { inject, ref, h, reactive } from 'vue'
  import { PaletteIcon, Palette1Icon, CheckIcon } from 'tdesign-icons-vue-next';
  import axios from 'axios';
  import { useRouter } from 'vue-router'
  const router = useRouter()
  const API_URL = inject('API_URL')
  const styledRole = ref(inject('styledRole',null))
  const userInfo = ref(inject('userInfo',null))
  const airoles = ref(inject('airoles',[]))
  const aiSelectItem = ref(inject('aiSelectItem',null))

  const palette = () => h(PaletteIcon);
  const palette1 = () => h(Palette1Icon);
  
  const aiSelect = ref(false)
  let aiSelectAudio = new Audio();

  const aiName = () => {
    console.log(styledRole)
    if(styledRole.value != null){
      return styledRole.value.ai_name
    }else{
      return ""
    }
  }
  const active = (id: number) => {
    if(aiSelectItem.value && aiSelectItem.value.id == id){
      return () => h(CheckIcon)
    }else{
      return null
    }
  }
  const aiSelectClick = async (item) => {
    aiSelectItem.value = item

    aiSelectAudio.pause();
    // play audio
    aiSelectAudio = new Audio(API_URL+'/audio/'+item.audio_path);
    aiSelectAudio.play();
  }
  const aiSelectCancel = () => {
    aiSelectAudio.pause();
    aiSelect.value = false;
    aiSelectItem.value = styledRole.value;
  }
  const isShowConfirm = ref(false)
  const aiSelectComfirm = () => {
    aiSelectAudio.pause();
    if(aiSelectItem.value && aiSelectItem.value.id != userInfo.value.styled_role_id){
      isShowConfirm.value = true;
    }else{
      aiSelect.value = false;
    }
  }

  const onAIConfirm = () => {
    aiSelect.value = false;
    isShowConfirm.value = false;
    if(aiSelectItem.value && aiSelectItem.value.id != userInfo.value.styled_role_id){
      // push to api
      axios.post(API_URL+'/user/updateStyledRole?styled_role_id='+aiSelectItem.value.id, {
        headers: {
          'accept': 'application/json',
          'Content-Type': 'application/json'
        }
      }).then(response => {
        if(response.data.success){
          console.log(response.data.data)
          userInfo.value.styled_role_id = aiSelectItem.value.id
          styledRole.value = aiSelectItem.value
        }else{
          console.error(response.data.message);
        }
      })
    }
  }
  const onAICancel = () => {
    aiSelect.value = false;
    isShowConfirm.value = false;
    aiSelectItem.value = styledRole.value;
  }

  
  
  const aiCustom = ref(false)
  let aiCustomAudio = new Audio();
  const aiCustomName = () => {
    console.log(userInfo.value)
    if(userInfo.value == null){
      return ""
    }
    formData.ai_name = userInfo.value.ai_name
    formData.ai_role = userInfo.value.ai_role
    formData.ai_timbre = userInfo.value.ai_timbre
    formData.ai_timbre_name = userInfo.value.ai_timbre_name
    formData.ai_tts_model = userInfo.value.ai_tts_model
    formData.ai_profile = userInfo.value.ai_profile
    if(userInfo.value.styled_role_id != null){
      return ""
    }
    return userInfo.value.ai_name
  }

  const formData = reactive({
    ai_name: '',
    ai_role: '',
    ai_timbre_name: '',
    ai_timbre: '',
    ai_tts_model: '',
    ai_profile: ''
  });
  const showTimbreBox = ref(false)
  const timbreOptions = () => {
    return [
      {
        label: '软萌童声',
        value: 'sambert-zhiying-v1'
      },
      {
        label: '诙谐男声',
        value: 'sambert-zhiming-v1'
      },
      {
        label: '知心姐姐',
        value: 'sambert-zhiyuan-v1'
      },
      {
        label: '自然男声',
        value: 'sambert-zhishuo-v1'
      },
      {
        label: '多种情感女声',
        value: 'sambert-zhimiao-emo-v1'
      }
    ];
  };

  const rules = {
    ai_name: [{ validator: (val: String) => val.length > 0, message: '不能为空' }],
    ai_role: [{ validator: (val: String) => val.length > 0, message: '不能为空' }],
    ai_timbre: [{ validator: (val: String) => val.length > 0, message: '不能为空' }],
    ai_timbre_name: [{ validator: (val: String) => val.length > 0, message: '不能为空' }],
    ai_tts_model: [{ validator: (val: String) => val.length > 0, message: '不能为空' }],
    ai_profile: [{ validator: (val: String) => val.length > 0, message: '不能为空' }]
  };

  const aiCustomCancel = () => {
    aiCustomAudio.pause();
    aiCustom.value = false;
  }
  const showDoubleConfirm = ref(false)
  const aiCustomComfirm = (context) => {
    if(context.validateResult === true){
      aiCustomAudio.pause();
      showDoubleConfirm.value = true;
    }
  }

  const onDoubleConfirm = () => {
    aiCustom.value = false;
    showDoubleConfirm.value = false;

    axios.post(API_URL+'/user/updateCustomAIRole', formData, {
      headers: {
        'accept': 'application/json',
        'Content-Type': 'application/json'
      }
    }).then(response => {
      if(response.data.success){
        console.log(response.data.data)
        userInfo.value.styled_role_id = null
        styledRole.value = null
        userInfo.value.ai_name = formData.ai_name
        userInfo.value.ai_role = formData.ai_role
        userInfo.value.ai_timbre = formData.ai_timbre
        userInfo.value.ai_timbre_name = formData.ai_timbre_name
        userInfo.value.ai_tts_model = formData.ai_tts_model
        userInfo.value.ai_profile = formData.ai_profile
      }else{
        console.error(response.data.message);
      }
    })
  }
  const onDoubleCancel = () => {
    aiSelect.value = false;
    isShowConfirm.value = false;
    aiSelectItem.value = styledRole.value;
  }

  const onConfirmTimbre = (val: string[], context: number[]) => {
    showTimbreBox.value = false;
    formData.ai_timbre_name = context['label'][0]
    formData.ai_timbre = val[0]
    formData.ai_tts_model = 'sambert'
    console.log(formData);
  };

  const onResetCustom = () => {
    console.log('onResetCustom');
  };

</script>
<style scoped lang="less">
.t-cell{
  background-color: rgba(239, 241, 243, 0.377);
}
.popup-demo {
  padding: 0 16px;
}

.header {
  display: flex;
  align-items: center;
  height: 116rpx;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background-color: #fff;
}

.title {
  flex: 1;
  text-align: center;
  font-weight: 600;
  font-size: 18px;
  color: var(--td-text-color-primary, rgba(0, 0, 0, 0.9));
  padding: 16px;
}

.btn {
  font-size: 16px;
  padding: 16px;
}

.btn--cancel {
  color: var(--td-text-color-secondary, rgba(0, 0, 0, 0.6));
}

.btn--confirm {
  color: #0052d9;
}
.textarea {
  height: 200px;
  width: 100%;
}
.button-group {
  background-color: var(--bg-color-demo, #fff);
  box-sizing: border-box;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  position: relative;

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
