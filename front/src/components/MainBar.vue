<template>
  <div class="top-bar">
    <!-- 검색창 가운데 -->
    <div class="search-bar">
      <input
        v-model="searchKeyword"
        placeholder="검색어를 입력해 주세요."
        class="search-input"
        type="text"
        @keyup.enter="goSearch"
      />
      <span class="search-icon" @click="goSearch">🔍</span>
    </div>

    <!-- 우측 버튼 -->
    <div class="top-buttons">
      <v-btn
        v-if="isLogin"
        variant="plain"
        text
        @click="$router.push('/mypage')"
      >마이페이지</v-btn>

      <v-btn
        v-else
        variant="plain"
        text
        @click="$router.push('/signup')"
      >회원가입</v-btn>

      <v-btn
        class="login-btn"
        v-if="!isLogin"
        @click="$router.push('/login')"
      >로그인</v-btn>

      <v-btn
        class="login-btn"
        v-else
        @click="logout"
      >로그아웃</v-btn>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'
import { storeToRefs } from 'pinia'

const router = useRouter()
const accountStore = useAccountStore()
const { isLogin } = storeToRefs(accountStore)

const searchKeyword = ref('')

const goSearch = () => {
  if (searchKeyword.value.trim()) {
    router.push({ name: 'search', query: { q: searchKeyword.value } })
  }
}

const logout = () => {
  accountStore.logOut()
  delete axios.defaults.headers.common['Authorization']
  router.push('/')
}
</script>

<style scoped>
.top-bar {
  position: relative;
  width: 100%;
  max-width: 1024px;
  margin-top: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
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
  font-size: 16px;
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
.top-buttons {
  color: white;
  position: absolute;
  right: -300px;
  display: flex;
  gap: 8px;
  align-items: center;
}
.login-btn {
  background-color: white;
  color: black;
  border-radius: 12px;
  font-weight: 500;
  height: 36px;
  margin-left: 5px;
}
.top-buttons .v-btn {
  font-size: 16px; 
}
</style>
