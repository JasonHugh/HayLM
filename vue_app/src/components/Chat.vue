<template>
  <t-navbar title="聊天" :fixed="true"></t-navbar>
  <div ref="scrollRef" class="mainBox">
    <t-list>
      <t-cell v-for="item in responseList" :key="item.id" :title="item.role + '&nbsp;&nbsp;&nbsp;' + item.create_time" :description="item.content" align="top" @click="playAudio">
          <template #leftIcon>
              <t-avatar shape="circle" image="https://tdesign.gtimg.com/mobile/demos/avatar1.png" v-show="item.role=='assistant'" />
              <t-avatar shape="circle" image="https://tdesign.gtimg.com/mobile/demos/avatar4.png" v-show="item.role=='user'" />
          </template>
      </t-cell>
    </t-list>
    <t-loading theme="dots" size="40px" style="height: 100px;position: fixed;bottom: 130px;left: 50%;margin-left: -20px;" v-show="isLoading" />
    <t-row style="height: 100px;position: fixed;bottom: 50px;padding: 0 10px;">
      <t-col span="4" style="width: 80px;height: 80px;">
        <t-button :theme="theme" :disabled="isLoading" size="large" :icon="chatIcon" shape="circle" @click="recording" style="width: 80px;height: 80px;"></t-button>
      </t-col>
      <t-col span="12" style="width: calc(100vw - 120px);margin-left: 10px;margin-top: 13px;">
        <t-input v-model="chatInput" placeholder="请输入内容" borderless style="border: 1px solid rgba(220, 220, 220, 1);border-radius: 6px;padding: 10px;">
          <template #suffix>
            <t-button theme="primary" size="small" @click="send" :disabled="isLoading"> 发送 </t-button>
          </template>
        </t-input>
      </t-col>
    </t-row>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, h, nextTick } from 'vue';
import { Message, Toast } from 'tdesign-mobile-vue';
import axios from 'axios';
import { MicrophoneIcon, StopIcon } from 'tdesign-icons-vue-next';
import { useRouter } from 'vue-router'
const router = useRouter()

const chatIcon = () => {
  if(isRecording.value){
    return h(StopIcon, { size: '80px' })
  }else{
    return h(MicrophoneIcon, { size: '50px' })
  }
};
const theme = ref("primary")
const isRecording = ref(false)
const audioChunks = ref([]);
const mediaRecorder = ref();
const responseList = ref([]);
const scrollRef = ref()
const isLoading = ref(false)
const playingAudio = ref()
const chatInput = ref("")

const playAudio = () => {
  if(playingAudio.value.paused){
    playingAudio.value.play();
  }else{
    playingAudio.value.pause();
    playingAudio.value.currentTime = 0;
  }
}
const send = () => {
  if(playingAudio.value){
    console.log("stop audio")
    playingAudio.value.pause();
  }
  isLoading.value = true;
  new Promise((resolve) => {
    axios.post(encodeURI(import.meta.env.VITE_API_URL+'/chat/response?user_input='+chatInput.value), {
      headers: {
        'accept': 'application/json',
        'Content-Type': 'multipart/form-data'
      }
    }).then(response => {
      chatInput.value = ""
      if(response.data.success){
        responseList.value.push(...response.data.data.histories) 
        
        // scroll to bottom after DOM loading done
        nextTick(()=>{
          scrollRef.value.scrollTo({
            top: document.getElementsByClassName('t-list')[0].scrollHeight
          })
        })

        // play audio
        axios.get(import.meta.env.VITE_API_URL+'/chat/audio?audio_path='+response.data.data.audio_path, {
          'responseType': 'blob'
        }).then(response => {
          if(response.data){
            const audioUrl = URL.createObjectURL(new Blob([response.data]));
            playingAudio.value = new Audio(audioUrl);
            playingAudio.value.play();
          }else{
            console.error(response.data);
            Toast("网络错误")
          }
        })
        .catch(error => {
          console.error(error);
          Toast(error)
          isLoading.value = false;
        }).then(() => {
          isLoading.value = false;
        });
      }else{
        console.error(response.data.message);
        Toast(response.data.message);
        isLoading.value = false;
      }
    })
    .catch(error => {
      console.error(error);
      Toast(error)
    });
    resolve(responseList);
  });
}
const recording = async () => {
  if(playingAudio.value){
    console.log("stop audio")
    playingAudio.value.pause();
  }
  if(isRecording.value){
    console.log("stop recording")
    isRecording.value = false
    theme.value = "primary"
    mediaRecorder.value.stop();
    mediaRecorder.value.onstop = () => {
      isLoading.value = true;
      const audioBlob = new Blob(audioChunks.value, { 'type' : 'audio/wav' });
      // request api
      const formData = new FormData();
      formData.append('wav', audioBlob, 'recording.wav');
      new Promise((resolve) => {
        // axios.post(import.meta.env.VITE_API_URL+'/chat/response?user_input=hi', {
        axios.post(import.meta.env.VITE_API_URL+'/chat/response', formData, {
          headers: {
            'accept': 'application/json',
            'Content-Type': 'multipart/form-data'
          }
        }).then(response => {
          if(response.data.success){
            responseList.value.push(...response.data.data.histories) 
            
            // scroll to bottom after DOM loading done
            nextTick(()=>{
              scrollRef.value.scrollTo({
                top: document.getElementsByClassName('t-list')[0].scrollHeight
              })
            })

            // play audio
            axios.get(import.meta.env.VITE_API_URL+'/chat/audio?audio_path='+response.data.data.audio_path, {
              'responseType': 'blob'
            }).then(response => {
              if(response.data){
                const audioUrl = URL.createObjectURL(new Blob([response.data]));
                playingAudio.value = new Audio(audioUrl);
                playingAudio.value.play();
              }else{
                console.error(response.data);
                Toast(response.data);
              }
            })
            .catch(error => {
              console.error(error);
              Toast(error)
              isLoading.value = false;
            }).then(() => {
              isLoading.value = false;
            });
          }else{
            console.error(response.data.message);
            Toast(response.data.message);
            isLoading.value = false;
          }
        })
        .catch(error => {
          console.error(error);
          Toast(error)
          isLoading.value = false;
        });
        resolve(responseList);
      });
    };
  }else{
    // init recorder
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder.value = new MediaRecorder(stream);

    audioChunks.value = []
    console.log("start recording")
    mediaRecorder.value.ondataavailable = e => {
      audioChunks.value.push(e.data);
    };
    mediaRecorder.value.start();
    isRecording.value = true;
    theme.value = "default"
  }
}
onMounted(async ()=>{
  // check if user logged
  const token = localStorage.getItem('token');
  if(token == null){
      router.push({ path: "/login" });
  }else{
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }
  
  // scroll to bottom after DOM loading done
  nextTick(()=>{
    scrollRef.value.scrollTo({
      top: document.getElementsByClassName('t-list')[0].scrollHeight
    })
  })

})
</script>
<style scoped>
.mainBox{
  top:48px;
  margin-bottom: 40px;
  position: relative;
  height: calc(100vh - 48px - 200px);
  overflow-y: scroll;
}
</style>