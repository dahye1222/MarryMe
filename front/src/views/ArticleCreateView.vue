<script setup>
import { useRouter } from 'vue-router'
import axios from 'axios'
import ArticleForm from '@/components/ArticleForm.vue'
import NavBar from '@/components/NavBar.vue'

const router = useRouter()

const createArticle = async (formData) => {
  const token = localStorage.getItem('token')  // 또는 pinia store에서 가져올 수도 있음

  if (!token) {
    alert('로그인이 필요합니다.')
    router.push('/login')
    return
  }

  try {
    await axios.post('/api/articles/', formData, {
      headers: {
        Authorization: `Token ${token}`  // Django REST Framework 기본 인증 방식
      }
    })
    alert('게시글이 등록되었습니다.')
    router.push('/board')
  } catch (error) {
    console.error('❌ 글 작성 실패:', error)
    alert('글 작성에 실패했습니다.')
  }
}
</script>

<template>
  <div>
    <NavBar />
    <v-container>
      <h1 class="text-h5 mb-4">✏️ 글 작성</h1>
      <ArticleForm @submit="createArticle" />
    </v-container>
  </div>
</template>

<style scoped>
</style>