<template>
  <t-navbar title="聊天记录" :fixed="true">
    <template #right>
      <t-icon name="calendar" size="24px" @click="visible = true" />
    </template>
  </t-navbar>
  <t-calendar v-model:visible="visible" @select="handleSelect" :min-date="minDate" :max-date="maxDate" :confirmBtn=null></t-calendar>
  <main>
  <t-pull-down-refresh v-model="refreshing" @refresh="onRefresh" style="overflow-y: scroll;">
    <t-list :async-loading="loading" @scroll="onScroll">
      <t-swipe-cell v-for="item in listPull">
        <t-cell :key="item.id" :title="item.role + '&nbsp;&nbsp;&nbsp;' + item.create_time" :description="item.content" align="top">
            <template #leftIcon>
                <t-avatar shape="circle" image="https://tdesign.gtimg.com/mobile/demos/avatar1.png" v-show="item.role=='assistant'" />
                <t-avatar shape="circle" image="https://tdesign.gtimg.com/mobile/demos/avatar4.png" v-show="item.role=='user'" />
            </template>
        </t-cell>
        <template #right>
          <div class="btn delete-btn" @click="handleDelete(item.id)">删除</div>
        </template>
      </t-swipe-cell>
    </t-list>
  </t-pull-down-refresh>
  </main>
  </template>
  
  <script lang="ts" setup>
  import { ref, onMounted, toRaw, nextTick } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router'
  const router = useRouter()

  const MAX_DATA_LEN = 60;
  const sessionId = 1;

  const visible = ref(false);
  const minDate = new Date(2024, 0, 1);
  const maxDate = new Date();
  const selectDate = ref(new Date());
  const handleSelect = (val: Date) => {
    selectDate.value = val
    onRefresh()
  };
  
  function getDateString(date: Date): string {
      const year = date.getFullYear().toString().padStart(4, '0');
      const month = (date.getMonth() + 1).toString().padStart(2, '0');
      const day = date.getDate().toString().padStart(2, '0');
      return `${year}-${month}-${day}`;
  }
  const loadData = (data: any, isRefresh?: Boolean) => {
    return new Promise((resolve) => {
      axios.get(import.meta.env.VITE_API_URL+'/chat/history?session_id='+sessionId+'&date='+getDateString(selectDate.value), {
        headers: {
          'accept': 'application/json',
        }
      }).then(response => {
        if(response.data.success){
          if(response.data.data.history != null){
            if (isRefresh) {
              data.value = response.data.data.history;
            } else {
              data.value = response.data.data.history;
            }
            // scroll to bottom after DOM loading done
            nextTick(()=>{
              document.getElementsByClassName('t-pull-down-refresh')[0].scrollTo({
                top: document.getElementsByClassName('t-list')[0].scrollHeight
              })
            })
          }else{
            data.value = []
          }
        }else{
          console.error(response.data.message);
        }
      })
      .catch(error => {
        console.error('There was an error!', error);
      });
      resolve(data);
    });
  };
  
  const listPull = ref([] as Array<any>);
  const loading = ref('');
  const refreshing = ref(false);
  
  const onLoadPull = (isRefresh?: Boolean) => {
    if ((listPull.value.length >= MAX_DATA_LEN && !isRefresh) || loading.value) {
      return;
    }
    loading.value = 'loading';
    loadData(listPull, isRefresh).then(() => {
      loading.value = '';
      refreshing.value = false;
    });
  };
  
  const onRefresh = () => {
    refreshing.value = true;
    onLoadPull(true);
  };
  
  const onScroll = (scrollBottom: number) => {
    if (scrollBottom < 1) {
      onLoadPull();
    }
  };
  const handleDelete = (historyId: number)=>{
    new Promise((resolve) => {
      axios.delete(import.meta.env.VITE_API_URL+'/chat/history/delete?history_id='+historyId, {
        headers: {
          'accept': 'application/json',
        }
      }).then(response => {
        if(response.data.success){
          console.log("delete success");
          onLoadPull();
        }else{
          console.error(response.data.message);
        }
      })
      .catch(error => {
        console.error(error);
      });
    });
  }
  
  onMounted(() => {
    const token = localStorage.getItem('token');
    if(token == null){
        router.push({ path: "/login" });
    }else{
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      onLoadPull();
    }
  });
  
  </script>
  <style scoped>
  .btn-wrapper {
    height: 100%;
  }

  .btn {
    display: inline-flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    padding: 0 16px;
    color: white;
    font-size: 14px;
  }

  .delete-btn {
    background-color: #e34d59;
  }
  </style>
  