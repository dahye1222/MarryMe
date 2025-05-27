import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const token = ref(localStorage.getItem('token') || null)

  const isLogin = computed(() => !!token.value)

  const logIn = async (payload) => {
    const { username, password } = payload
    try {
      const res = await axios.post('http://127.0.0.1:8000/api/auth/login/', {
        username,
        password
      })
      token.value = res.data.key
      localStorage.setItem('token', token.value)
      axios.defaults.headers.common.Authorization = `Token ${token.value}`
      console.log(' 로그인 성공:', res.data)
    } catch (err) {
      console.error(' 로그인 실패:', err.response?.data || err.message)
    }
  }

  const logOut = () => {
    token.value = null
    localStorage.removeItem('token')
    delete axios.defaults.headers.common.Authorization
    console.log(' 로그아웃 완료')
  }

  return { token, isLogin, logIn, logOut }
}, {
  persist: true 
})
