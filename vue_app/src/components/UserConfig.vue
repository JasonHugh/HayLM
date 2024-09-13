<template>
  <div>
    <button @click="startRecording">开始录音</button>
    <button @click="stopRecording" :disabled="!isRecording">停止录音</button>
  </div>
</template>
 
<script>
export default {
  data() {
    return {
      isRecording: false,
      mediaRecorder: null,
      audioChunks: []
    };
  },
  methods: {
    async startRecording() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

        const audioCtx = new AudioContext();
        const analyser = audioCtx.createAnalyser();
        const mediaStreamSource = audioCtx.createMediaStreamSource(stream);
        mediaStreamSource.connect(analyser);
        
        this.mediaRecorder = new MediaRecorder(stream, {type: 'audio/webm'});
        this.mediaRecorder.ondataavailable = e => {
          this.audioChunks.push(e.data);
        };
        this.mediaRecorder.start();
        this.isRecording = true;

 
        // 开始监测静音
    
        // 分析麦克风输入
        const checkMute = () => {
          // 设置阈值和分析时间长度
          const threshold = 0.05; // 根据需要调整这个阈值
          const interval = 500; // 检查的时间间隔（毫秒
          setTimeout(() => {
            console.log('开始检测');
              const array = new Uint8Array(analyser.frequencyBinCount);
              analyser.getByteTimeDomainData(array);
      
              // 计算平均音量
              const average = array.reduce((a, b) => a + b) / array.length;
              console.log(average)
      
              // 如果平均音量低于阈值，则停止录音
              if (average < threshold) {
                stopRecording();
                audioStream.getTracks().forEach(track => track.stop());
                console.log('录音已停止因为超过静音阈值');
              } else if(this.isRecording){
                // 如果音量高于阈值，则继续监测
                checkMute()
              }
          }, interval)
        };
        checkMute()
      } catch (err) {
        console.error('录音失败：', err);
      }
    },
    stopRecording() {
      this.mediaRecorder.stop();
      this.mediaRecorder.onstop = () => {
        const audioBlob = new Blob(this.audioChunks, { 'type' : 'audio/ogg; codecs=opus' });
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audio.play();
        this.audioChunks = []; // 重置音频块数组以备下次录音
      };
      this.isRecording = false;
    },
    createSoundMeter(audioCtx) {
      const soundMeter = audioCtx.createScriptProcessor(2048, 1, 1);
      soundMeter.onaudioprocess = (e) => {
        const inputBuffer = e.inputBuffer;
        const volume = Math.max(...inputBuffer.getChannelData(0));
        soundMeter.volume = volume;
      };
      return soundMeter;
    },
  },
};
</script>