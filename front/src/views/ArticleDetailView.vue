<template>
  <div>
    <NavBar />
    <v-container>
      <h1 class="text-h5">{{ isEditing ? '📝 게시글 수정' : article.title }}</h1>

      <!-- 작성자 정보 -->
      <p class="mb-4">
        🕒 {{ article.created_at?.slice(0, 16).replace('T', ' ') }} |
        👤 {{ article.nickname }}
        <span v-if="article.gender === 'W'">예신님</span>
        <span v-else-if="article.gender === 'M'">예랑님</span>
      </p>

      <!-- 본문 -->
      <div v-if="!isEditing">
        <p>{{ article.content }}</p>
      </div>
      <div v-else>
        <v-text-field v-model="editForm.title" label="제목" />
        <v-textarea v-model="editForm.content" label="내용" rows="10" />
      </div>

      <!-- 본인 글일 경우에만 버튼 표시 -->
      <div v-if="article.username === currentUser?.username" class="my-4 d-flex gap-4">
        <v-btn color="primary" @click="isEditing ? updateArticle() : (isEditing = true)">
          {{ isEditing ? '💾 저장' : '✏️ 수정' }}
        </v-btn>
        <v-btn color="error" @click="deleteArticle">❌ 삭제</v-btn>
      </div>

      <!-- 댓글 목록 -->
      <CommentList :articleId="articleId" />
    </v-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import NavBar from '@/components/NavBar.vue'
import CommentList from '@/components/CommentList.vue'

const route = useRoute()
const router = useRouter()
const articleId = Number(route.params.id)

const article = ref({})
const editForm = ref({ title: '', content: '' })
const isEditing = ref(false)
const currentUser = ref(null)

// 게시글 상세 불러오기
const fetchArticle = async () => {
  const res = await axios.get(`/api/articles/${articleId}/`)
  article.value = res.data
  editForm.value.title = res.data.title
  editForm.value.content = res.data.content
}

// 현재 로그인 사용자 정보 가져오기
const fetchCurrentUser = async () => {
  const token = localStorage.getItem('token')
  if (!token) return

  const res = await axios.get('/api/accounts/user/', {
    headers: { Authorization: `Token ${token}` }
  })
  currentUser.value = res.data
}

// 게시글 수정
const updateArticle = async () => {
  try {
    const token = localStorage.getItem('token')
    await axios.patch(`/api/articles/${articleId}/`, {
      title: editForm.value.title,
      content: editForm.value.content
    }, {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    isEditing.value = false
    fetchArticle()
  } catch (err) {
    console.error('수정 실패:', err)
    alert('게시글 수정에 실패했습니다.')
  }
}

// 게시글 삭제
const deleteArticle = async () => {
  if (!confirm('정말 이 게시글을 삭제하시겠습니까?')) return
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`/api/articles/${articleId}/`, {
      headers: { Authorization: `Token ${token}` }
    })
    alert('삭제되었습니다.')
    router.push('/board')
  } catch (err) {
    console.error('삭제 실패:', err)
    alert('게시글 삭제에 실패했습니다.')
  }
}

onMounted(() => {
  fetchArticle()
  fetchCurrentUser()
})
</script>

<style scoped>
.gap-4 {
  gap: 16px;
}
</style>
