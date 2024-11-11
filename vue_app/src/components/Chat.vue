<template>
  <t-navbar title="聊天" :fixed="true"></t-navbar>
  <div ref="scrollRef" class="mainBox">
    <t-list>
      <t-cell v-for="item in responseList" :key="item.id" :title="item.role + '&nbsp;&nbsp;&nbsp;' + item.create_time" :description="item.content" align="top" @click="playAudio(0)">
          <template #leftIcon>
              <t-avatar shape="circle" image="https://tdesign.gtimg.com/mobile/demos/avatar1.png" v-show="item.role=='assistant'" />
              <t-avatar shape="circle" image="https://tdesign.gtimg.com/mobile/demos/avatar4.png" v-show="item.role=='user'" />
          </template>
      </t-cell>
    </t-list>
    <t-loading theme="dots" size="40px" style="height: 100px;position: fixed;bottom: 130px;left: 50%;margin-left: -20px;" v-show="isLoading" />
    <t-row style="height: 100px;position: fixed;bottom: 50px;padding: 0 10px;">
      <t-col span="4" style="width: 80px;height: 80px;">
        <t-button :theme="theme" :disabled="isLoading" size="large" :icon="chatIcon" shape="circle" @touchstart="startRecording" @touchend="stopRecording" style="width: 80px;height: 80px;"></t-button>
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
import { EventSourcePolyfill } from 'event-source-polyfill';
import { MicrophoneIcon, StopIcon } from 'tdesign-icons-vue-next';
import { useRouter } from 'vue-router'
const router = useRouter()
const API_URL = import.meta.env.VITE_API_URL

// check if user logged
const token = localStorage.getItem('token');
if(token == null){
    router.push({ path: "/login" });
}else{
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

const chatIcon = () => {
  return h(MicrophoneIcon, { size: '50px' })
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
let audio_paths = []
let audio_urls = []
let isAudioEnd = false

const playAudio = (index) => {
  isAudioEnd = true
  if(!playingAudio.value || playingAudio.value.paused){
    playingAudio.value = new Audio(audio_urls[index]);
    playingAudio.value.onended = function() {
      if (index < audio_urls.length - 1) {
        playAudio(index + 1); 
      }
    };
    playingAudio.value.play();
  }else{
    playingAudio.value.pause();
    playingAudio.value.currentTime = 0;
  }
}


let eventSource: EventSourcePolyfill;
const send = () => {
  isAudioEnd = true
  audio_paths = []
  audio_urls = []
  if(eventSource != null){
    eventSource.close()
  }
  if(playingAudio.value){
    console.log("stop audio")
    playingAudio.value.pause();
  }
  isLoading.value = true;

  eventSource = new EventSourcePolyfill(API_URL+'/chat/response?user_input='+chatInput.value, {
    headers: {
      'Authorization': `Bearer ${token}`
    },
    withCredentials: true
  });
  eventSource.addEventListener("start", (e: MessageEvent) => {
    console.log('start', e.data)
    const data = JSON.parse(e.data)
    responseList.value.push(data)
    console.log("list", responseList.value);
    // scroll to bottom after DOM loading done
    nextTick(()=>{
      scrollRef.value.scrollTo({
        top: document.getElementsByClassName('t-list')[0].scrollHeight
      })
    })
  })
  let first = true
  eventSource.onopen = (e) => {
    console.log('open', e)
  }
  eventSource.onmessage = (e) => {
    console.log('message', e.data)
    const data = JSON.parse(e.data)
    audio_paths.push(data["audio_path"])
    if (first) {
      first = false;
      responseList.value.push(data)
      // play audio
      isAudioEnd = false
      playWebAudio()
    }else{
      responseList.value[responseList.value.length-1]["content"] += data["content"]
    }
    // scroll to bottom after DOM loading done
    nextTick(()=>{
      scrollRef.value.scrollTo({
        top: document.getElementsByClassName('t-list')[0].scrollHeight
      })
    })
  }
  eventSource.addEventListener("end", (e: MessageEvent) => {
    console.log('end', e.data)
    eventSource.close()

    responseList.value[responseList.value.length-1] = JSON.parse(e.data)
    chatInput.value = ""
    isLoading.value = false;
  })
  eventSource.onerror = (e) => {
    console.error('error', e)
    eventSource.close()
    isLoading.value = false;
    Toast("网络错误");
  }
}
const startRecording = async () => {
  isAudioEnd = true
  audio_paths = []
  audio_urls = []
  if(eventSource != null){
    eventSource.close()
  }
  if(playingAudio.value){
    console.log("stop audio")
    playingAudio.value.pause();
  }

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
const stopRecording = async () => {
  if(mediaRecorder.value == null) {
    await new Promise<void>((resolve) => {
      setTimeout(() => {
        resolve()
      }, 100)
    })
  }
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
      axios.post(API_URL+'/asr', formData, {
        headers: {
          'accept': 'application/json',
          'Content-Type': 'multipart/form-data'
        }
      }).then(response => {
        if(response.data.success){
          chatInput.value = response.data.data.text
          send()
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
}
const playWebAudio = async () => {
  while(true){
    console.log(isLoading.value)
    console.log(audio_paths)
    console.log(audio_paths.length)
    if((!isLoading.value && audio_paths.length == 0) || isAudioEnd){
      break;
    }
    const audioPath = audio_paths.shift();
    if(audioPath && (playingAudio.value == null || playingAudio.value.paused)){
      console.log("play audio", audioPath)
      await axios.get(API_URL+'/chat/audio?audio_path='+audioPath, {
        'responseType': 'blob'
      }).then(response => {
        if(response.data){
          const audioUrl = URL.createObjectURL(new Blob([response.data]));
          audio_urls.push(audioUrl)
          console.log(audioUrl)
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
    }else if(audioPath){
      audio_paths.unshift(audioPath)
    }

    await new Promise<void>((resolve) => {
      setTimeout(() => {
        resolve()
      }, 500)
    })
  }
}
onMounted(async ()=>{
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