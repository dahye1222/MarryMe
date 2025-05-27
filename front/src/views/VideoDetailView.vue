<template>
    <NavBar />
    <v-container class="video-detail-view">
    <SearchBar @search="goSearch" />
        <div class="py-6">
        <v-row justify="center">
            <v-col cols="12" md="8">
            <h1 class="text-h5 mb-4">
            <strong>
                <a
                :href="`https://www.youtube.com/watch?v=${videoId}`"
                target="_blank"
                rel="noopener noreferrer"
                style="text-decoration: none; color: inherit;"
                >
                {{ video?.snippet.title }}
                </a>
            </strong>
            </h1>
            <iframe
                v-if="videoId"
                :src="`https://www.youtube.com/embed/${videoId}`"
                width="100%"
                height="600"
                frameborder="0"
                allowfullscreen
            ></iframe>
            <p class="mt-4"><strong>채널명:</strong> {{ video?.snippet.channelTitle }}</p>
            <p><strong>업로드일:</strong> {{ formatDate(video?.snippet.publishedAt) }}</p>
            <p><strong>설명:</strong></p>
            <p>{{ video?.snippet.description }}</p>
            </v-col>
        </v-row>
        </div>
  </v-container>

    <div v-if="comments.length" class="mt-8">
    <h2 class="text-h6 mb-4" style="margin-left: 500px; ">💬 댓글</h2>

    <v-list>
        <v-list-item
        v-for="comment in comments"
        :key="comment.id"
        class="comment-item mb-4 px-4 py-3"
        >
        <v-list-item-content>
            <div class="comment-author font-weight-bold mb-1">
            {{ comment.snippet.topLevelComment.snippet.authorDisplayName }}
            </div>
            <div class="comment-text" v-html="comment.snippet.topLevelComment.snippet.textDisplay"></div>
        </v-list-item-content>
        </v-list-item>
    </v-list>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useRoute } from 'vue-router'
import SearchBar from '@/components/SearchBar.vue'
const route = useRoute()
const router = useRouter()

const goSearch = (query) => {
  router.push({ name: 'search', query: { q: query } })
}
import { useSearchStore } from '@/stores/search'
import NavBar from '@/components/NavBar.vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'
const accountStore = useAccountStore()


const searchStore = useSearchStore()
const videoId = route.params.id
const video = ref(null)
const fetchComments = async () => {
  try {
    const response = await axios.get(
      'https://www.googleapis.com/youtube/v3/commentThreads', {
        params: {
          part: 'snippet',
          videoId: videoId,
          key: 'AIzaSyArnrUGMeTOVnzZPR7JnAODzwmG0tV-QDo',
          maxResults: 20,  
          order: 'relevance'  
        }
      }
    )
    comments.value = response.data.items
  } catch (error) {
    console.error('댓글 불러오기 실패:', error)
  }
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('ko-KR')
}

onMounted(async () => {
  if (!videoId) return
  try {
    const response = await axios.get(
      `https://www.googleapis.com/youtube/v3/videos?part=snippet&id=${videoId}&key=AIzaSyArnrUGMeTOVnzZPR7JnAODzwmG0tV-QDo`
    )
    video.value = response.data.items[0]
  } catch (error) {
    console.error('영상 정보를 불러오는 데 실패했습니다:', error)
  }
})

const comments = ref([])

onMounted(async () => {
  if (!videoId) return

  try {
    const response = await axios.get(
      `https://www.googleapis.com/youtube/v3/videos?part=snippet&id=${videoId}&key=AIzaSyArnrUGMeTOVnzZPR7JnAODzwmG0tV-QDo`
    )
    video.value = response.data.items[0]
  } catch (error) {
    console.error('영상 정보 불러오기 실패:', error)
  }

  await fetchComments()
})

</script>
<style scoped>  
.search-view-wrapper {
  padding-top: 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.top-bar {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 32px;
}

.search-bar {
  position: relative;
  max-width: 400px;
  width: 100%;
}

.search-input {
  width: 100%;
  padding: 12px 48px 12px 16px;
  border-radius: 32px;
  border: none;
  outline: none;
  font-size: 14px;
  background-color: white;
  box-shadow: 0 0 4px rgba(0, 0, 0, 0.15);
}

.search-icon {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 18px;
  cursor: pointer;
}
.comment-item {
  border: 1px solid #ddd;
  border-radius: 12px;
  background-color: #fafafa;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: box-shadow 0.2s;
  margin-left: 500px;   
  margin-right: 500px;
}

.comment-item:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
}

.comment-author {
  color: #003e5c;
  font-size: 14px;
}

.comment-text {
  font-size: 14px;
  line-height: 1.5;
}
</style>
