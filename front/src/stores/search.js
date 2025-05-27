import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchVideosFromYoutube } from '@/services/youtube'

export const useSearchStore = defineStore('search', () => {
  const videos = ref([])

  const fetchVideos = async (query) => {
    const result = await fetchVideosFromYoutube(query)
    videos.value = result
  }

  return { videos, fetchVideos }
})