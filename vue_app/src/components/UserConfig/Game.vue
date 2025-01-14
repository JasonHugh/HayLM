<template>
    <t-navbar title="趣学" :fixed="true">
        <template #right>
            <!-- <t-switch :value="is_enable" @change="enable"></t-switch> -->
            <t-button size="extra-small" theme="primary" variant="outline" v-if="is_enable" @click="disable_game">退出趣学</t-button>
            <t-button size="extra-small" disabled theme="primary" variant="text" v-if="!is_enable">选择游戏即可启用</t-button>
        </template>
    </t-navbar>
    <main>
        <div class="example-search">
            <t-search v-model="search_text" :clearable="true" shape="round" placeholder="请输入关键字" @change="search"></t-search>
        </div>
        <div style="padding: 0 16px">
            <t-swiper :autoplay="true" height="180px" :navigation="{ type: 'dots-bar' }" @change="handleChange">
                <t-swiper-item v-for="(item, index) in banner_games" :key="index" @click="showDetail(item)">
                    <t-image fit="contain" :src="API_URL + '/image/' + item.banner_path"></t-image>
                </t-swiper-item>
            </t-swiper>
        </div>
        <t-pull-down-refresh
            v-model="refreshing"
            :loading-bar-height="66"
            :loading-texts="['下拉刷新', '松开刷新', '正在刷新', '刷新完成']"
            @refresh="handleRefresh"
            @scrolltolower="handleScrolltolower"
        >
            <t-cell-group>
                <t-cell v-for="(item, index) in games" :key="index" :title="item.title" :description="item.short_desc" align="top" @click="showDetail(item)">
                    <template #leftIcon>
                        <t-image 
                            class="image-container" 
                            :src="API_URL + '/image/' + item.icon_path" 
                            shape="round" 
                            fit="cover"
                            position="center"
                            :style="{ width: '64px', height: '64px' }" />
                    </template>
                    <template #rightIcon v-if="item.id == game_id">
                        <t-tag theme="success">已选择</t-tag>
                    </template>
                    <template #note v-if="item.is_vip">
                        <t-badge count="VIP" shape="ribbon" />
                    </template>
                </t-cell>
            </t-cell-group>
        </t-pull-down-refresh>
        <t-dialog
            v-if="isShowDetail"
            v-model:visible="isShowDetail"
            :title="select_game.title"
            :content="select_game.desc"
            cancel-btn="取消"
            confirm-btn="选择"
            @confirm="select"
            @cancel="cancel"
            :closeOnOverlayClick="true"
        >
            <template #top>
                <t-image fit="contain" :src="API_URL + '/image/' + select_game.banner_path"></t-image>
            </template>
        </t-dialog>
    </main>
</template>
  
<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router'
const router = useRouter()

const API_URL = process.env.VITE_API_URL
const userInfo = ref()

const is_enable = ref(false);
const game_id = ref(0);

const disable_game = () => {
  axios.post(API_URL+'/user/disable_game', {
    headers: {
      'accept': 'application/json',
    }
  }).then(response => {
    if(response.data.success){
      router.push('/game');
    }else{
      console.error(response.data.message);
    }
  })
  .catch(error => {
    console.error(error);
  });
}

const search_text = ref('');
const search = (val: string) => {
  console.log('change: ', val);
};


const banner_games = ref([])
const games = ref([])
const loadGames = async () => {
    axios.get(API_URL+'/games', {
      headers: {
        'accept': 'application/json',
      }
    }).then(response => {
      if(response.data.success){
        if(response.data.data.games != null){
          games.value = response.data.data.games;
          banner_games.value = games.value.filter((item: any) => item.is_banner == true)
          console.log(banner_games.value)
        }
      }else{
        console.error(response.data.message);
      }
    })
    .catch(error => {
      console.error(error);
    });
  }
const handleChange = (index: number, context: any) => {
//   console.log('基础示例,页数变化到》》》', index, context);
};

const refreshing = ref(false);
const handleRefresh = (value: any) => {
  refreshing.value = true;
  setTimeout(() => {
    refreshing.value = false;
  }, 1000);
};
const handleScrolltolower = () => {
  console.log('触底');
};

const select_game = ref();
const isShowDetail = ref(false);
const showDetail = (game) => {
  isShowDetail.value = true;
  select_game.value = game;
};

const select = () => {
  axios.post(API_URL+'/user/enable_game/'+select_game.value.id, {
    headers: {
      'accept': 'application/json',
    }
  }).then(response => {
    if(response.data.success){
      router.push('/game');
    }else{
      console.error(response.data.message);
    }
  })
  .catch(error => {
    console.error(error);
  });
};

const cancel = () => {
  console.log('dialog: cancel');
};

const loadUserInfo = () => {
  axios.get(API_URL+'/user/getConfig', {
    headers: {
      'accept': 'application/json',
    }
  }).then(response => {
    if(response.data.success){
      userInfo.value = response.data.data.config;
      is_enable.value = userInfo.value.game_enable;
      if(is_enable.value){
        game_id.value = userInfo.value.game_id;
      }
      console.log(userInfo.value)
    }else{
      console.error(response.data.message);
    }
  })
  .catch(error => {
    console.error(error);
  });
}
onMounted(() => {
  // check if user logged
  const token = localStorage.getItem('token');
  if(token == null){
    router.push({ path: "/login" });
  }else{
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }
  loadUserInfo()
  loadGames()
})
</script>

<style lang="less">
.example-search {
  background-color: var(--bg-color-demo, #fff);
  padding: 8px 16px;
}
.group {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  padding: 0 16px 140px 16px;
  .item {
    width: 47%;
    margin-bottom: 16px;
  }
}
</style>