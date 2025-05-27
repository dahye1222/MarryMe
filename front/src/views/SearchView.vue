<template>
  <div>
    <NavBar />
  <v-container class="search-view-wrapper" fluid>

    <!-- 🔍 검색창 상단 추가 -->
    <div class="top-bar">
      <div class="search-bar">
        <input
          v-model="searchQuery"
          placeholder="검색어를 입력해 주세요."
          class="search-input"
          type="text"
          @keyup.enter="goSearch"
        />
        <span class="search-icon" @click="goSearch">🔍</span>
      </div>
    </div>

    <v-row>
      <v-col
        v-for="video in searchStore.videos"
        :key="video.id.videoId"
        cols="12"
        md="6"
        lg="4"
      >
        <v-card
          variant="outlined"
          class="mb-4"
          @click="goToDetail(video.id.videoId)"
          style="cursor: pointer; padding: 12px;"
        >
          <v-img :src="video.snippet.thumbnails.high.url" height="300px" />
          <v-card-title class="text-wrap">{{ video.snippet.title }}</v-card-title>
          <v-card-subtitle>
            {{ video.snippet.channelTitle }} <br />
            📅 {{ formatDate(video.snippet.publishedAt) }}
          </v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</div>

</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSearchStore } from '@/stores/search'
import NavBar from '@/components/NavBar.vue'

const route = useRoute()
const router = useRouter()
const searchStore = useSearchStore()
const searchQuery = ref(route.query.q || '')

const goSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({ name: 'search', query: { q: searchQuery.value } })
  }
}

watch(() => route.query.q, async (newQuery) => {
  if (newQuery) {
    searchQuery.value = newQuery
    await searchStore.fetchVideos(newQuery)
  }
}, { immediate: true })

onMounted(async () => {
  if (searchQuery.value) {
    await searchStore.fetchVideos(searchQuery.value)
  }
})
const goToDetail = (videoId) => {
  router.push({ name: 'videoDetail', params: { id: videoId } })
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('ko-KR')
}

</script>

<style scoped>
.search-view-wrapper {
  padding-top: 32px;
}

.top-bar {
  width: 100%;
  max-width: 1024px;
  margin: 0 auto 32px auto;
  display: flex;
  justify-content: center;
  align-items: center;
}

.search-bar {
  position: relative;
  max-width: 600px; /* 기존 400px보다 넓게 */
  width: 100%;
}

.search-input {
  width: 100%;
  padding: 16px 56px 16px 20px; /* 상하 여백 증가 */
  border-radius: 36px;
  border: none;
  outline: none;
  font-size: 21px; /* 텍스트 크기 증가 */
  background-color: white;
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.15);
}

.search-icon {
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 22px; /* 아이콘도 약간 키움 */
  cursor: pointer;
}
</style>
