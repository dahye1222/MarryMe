import axios from 'axios'
import apiKey from '@/config/apiKey.js' // YOUTUBE_API_KEY가 저장된 파일

const BASE_URL = 'https://www.googleapis.com/youtube/v3'

export const fetchVideosFromYoutube = async (query) => {
  try {
    const response = await axios.get(`${BASE_URL}/search`, {
      params: {
        key: apiKey.YOUTUBE_API_KEY,
        part: 'snippet',
        q: query,
        type: 'video',
        maxResults: 10,
      },
    })
    return response.data.items
  } catch (error) {
    console.error('YouTube API Error:', error)
    return []
  }
}