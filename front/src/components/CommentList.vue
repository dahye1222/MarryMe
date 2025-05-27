<template>
  <div>
    <h2 class="mt-6 text-h6">💬 댓글</h2>
    <v-list>
      <v-list-item
        v-for="comment in sortedComments"
        :key="comment.id"
      >
        <v-list-item-content>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span>
              {{ comment.nickname }}       
              <span v-if="comment.gender === 'W'">예신님</span>   
              <span v-else-if="comment.gender === 'M'">예랑님</span> |
              {{ comment.content }}
            </span>
            <div style="display: flex; align-items: center; gap: 8px;">
              <span class="text-caption">[🕒 {{ comment.created_at.slice(0, 16).replace('T', ' ') }}]</span>
              <!-- ✅ 본인 댓글만 삭제 버튼 표시 -->
              <v-btn
                v-if="comment.user === currentUserId"
                icon
                size="small"
                @click="deleteComment(comment.id)"
                variant="plain"
                class="no-bg-btn"
              >
                <span style="font-size: 18px;">❌</span>
              </v-btn>
            </div>
          </div>
        </v-list-item-content>
      </v-list-item>
    </v-list>

    <!-- ✅ 댓글과 입력창 사이 구분선 -->
    <v-divider class="my-4" />

    <!-- ✅ 댓글 입력창 간격 조정 -->
    <v-row class="mt-4 comment-box" align="center">
      <v-col cols="10">
        <v-textarea
          v-model="newComment"
          label="댓글을 입력하세요"
          variant="underlined"
          rows="2"
          auto-grow
          max-rows="4"
          hide-details
          style="max-height: 100px;"
        />
      </v-col>
      <v-col cols="2" class="text-end">
        <v-btn color="primary" @click="postComment">등록</v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, watch, computed, onMounted } from 'vue'
import axios from 'axios'

const props = defineProps({
  articleId: Number
})

const comments = ref([])
const newComment = ref('')
const currentUserId = ref(null) // ✅ 현재 로그인 유저 ID 저장

// ✅ 오래된 댓글부터 정렬된 목록
const sortedComments = computed(() => {
  return [...comments.value].sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
})

const fetchComments = async () => {
  const res = await axios.get(`/api/articles/${props.articleId}/comments/`)
  comments.value = res.data
}

const postComment = async () => {
  if (!newComment.value) return

  const token = localStorage.getItem('token')
  if (!token) {
    alert('로그인 후 댓글을 작성할 수 있습니다.')
    return
  }

  try {
    await axios.post(`/api/articles/${props.articleId}/comments/`, {
      content: newComment.value
    }, {
      headers: {
        Authorization: `Token ${token}`
      }
    })

    newComment.value = ''
    fetchComments()
  } catch (error) {
    console.error('❌ 댓글 작성 실패:', error.response?.data || error.message)
    alert('댓글 작성에 실패했습니다.')
  }
}

const deleteComment = async (commentId) => {
  const token = localStorage.getItem('token')
  if (!token) {
    alert('로그인 후 삭제할 수 있습니다.')
    return
  }

  if (!confirm('정말 이 댓글을 삭제하시겠습니까?')) return

  try {
    await axios.delete(`/api/articles/comments/${commentId}/`, {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    fetchComments()
  } catch (error) {
    console.error('❌ 댓글 삭제 실패:', error.response?.data || error.message)
    alert('댓글 삭제에 실패했습니다.')
  }
}

// ✅ 로그인한 사용자 ID 가져오기
const fetchCurrentUser = async () => {
  const token = localStorage.getItem('token')
  if (!token) return

  try {
    const res = await axios.get('/api/accounts/user/', {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    currentUserId.value = res.data.id
  } catch (err) {
    console.error('유저 정보 가져오기 실패:', err)
  }
}

onMounted(() => {
  fetchCurrentUser()
})

watch(() => props.articleId, fetchComments, { immediate: true })
</script>

<style scoped>
.no-bg-btn {
  box-shadow: none;
  background-color: transparent !important;
  min-width: 0;
  padding: 0;
}
.comment-box {
  margin-bottom: 16px;
}
</style>
