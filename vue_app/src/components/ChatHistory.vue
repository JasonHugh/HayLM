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
      <t-notice-bar visible content="今日没有聊天记录" :prefix-icon="false" v-show="isEmpty"/>
      <t-swipe-cell v-for="(item, index) in listPull" :key="item.id">
        <div v-if="item.role=='user'">
          <t-cell :title="item.role + '&nbsp;&nbsp;&nbsp;' + item.create_time" :description="item.content" align="top">
              <template #leftIcon>
                  <t-avatar shape="circle" image="https://tdesign.gtimg.com/mobile/demos/avatar4.png" />
              </template>
          </t-cell>
          <t-cell :title="listPull[index+1].role + '&nbsp;&nbsp;&nbsp;' + listPull[index+1].create_time" :description="listPull[index+1].content" align="top" v-if="listPull[index+1]!=null">
              <template #leftIcon>
                  <t-avatar shape="circle" image="https://tdesign.gtimg.com/mobile/demos/avatar1.png"/>
              </template>
          </t-cell>
        </div>
        <template #right>
          <div class="btn delete-btn" @click="handleDelete(index, item.id)">删除</div>
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
  const API_URL = process.env.VITE_API_URL

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
      axios.get(API_URL+'/chat/history?session_id='+sessionId+'&date='+getDateString(selectDate.value), {
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

        loading.value = '';
        refreshing.value = false;
        if(listPull.value.length == 0){
          isEmpty.value = true
        }else{
          isEmpty.value = false
        }
      })
      .catch(error => {
        console.error('There was an error!', error);
        if(error.response.status == 401){
          router.push({ path: "/login" });
        }
      });
      resolve(data);
    });
  };
  
  const listPull = ref([] as Array<any>);
  const loading = ref('');
  const refreshing = ref(false);
  const isEmpty = ref(false)

  const listItem = (index) => {
    console.log(index)
    console.log(listPull.value.length)
    return listPull.value[index]
  }
  
  const onLoadPull = (isRefresh?: Boolean) => {
    if ((listPull.value.length >= MAX_DATA_LEN && !isRefresh) || loading.value) {
      return;
    }
    loading.value = 'loading';
    loadData(listPull, isRefresh);
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
  const handleDelete = (index: number, id: number)=>{
    let historyIdList = []
    historyIdList.push(id)
    if(listPull.value[index+1]!=null){
      historyIdList.push(listPull.value[index+1].id)
    }
    console.log(historyIdList)
    new Promise((resolve) => {
      axios.delete(API_URL +'/chat/history/delete', {data: historyIdList}).then(response => {
        if(response.data.success){
          console.log("delete success");
          // remove from list
          listPull.value.splice(index,2)
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
    // localStorage.removeItem('token');
    const token = localStorage.getItem('token');
    if(token == null){
        router.push({ path: "/login" });
    }else{
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      onLoadPull();
    }
    if(listPull.value.length == 0){
      isEmpty.value = true
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
  