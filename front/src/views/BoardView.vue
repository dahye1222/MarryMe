<template>
  <div>
    <NavBar />
    <v-container>
      <h1 class="text-h5 mb-4">📋 게시판</h1>
      <v-btn
        class="mb-4 underline-btn"
        variant="plain"
        color="primary"
        @click="$router.push('/board/create')"
      >
        ✏️ 글 작성
      </v-btn>
      <v-row>
        <v-col
          v-for="article in articles"
          :key="article.id"
          cols="12"
          md="6"
          lg="4"
        >
          <ArticleCard :article="article" />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import NavBar from '@/components/NavBar.vue'
import ArticleCard from '@/components/ArticleCard.vue'

const articles = ref([])

onMounted(async () => {
  try {
    const res = await axios.get('/api/articles/')
    console.log('🔥 받은 응답:', res.data)
    articles.value = Array.isArray(res.data) ? res.data : []
  } catch (err) {
    console.error('📛 API 요청 실패:', err)
  }
})

</script>

<style scoped>
</style>
