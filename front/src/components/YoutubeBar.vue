
<template>
  <div class="nav-bar">
    <!-- 로고 -->
    <img src="@/assets/mini-logo.png" alt="logo" class="logo" @click="$router.push('/')" />

    <!-- 메뉴 -->
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

    <!-- 로그인/회원가입 or 마이페이지/로그아웃 -->
    <div class="auth-buttons">
      <span
        class="menu-item"
        v-if="isLogin"
        @click="$router.push('/mypage')"
      >마이페이지</span>

      <v-btn
        class="login-btn"
        v-if="!isLogin"
        @click="$router.push('/login')"
      >로그인</v-btn>

      <v-btn
        class="login-btn"
        v-if="!isLogin"
        @click="$router.push('/signup')"
      >회원가입</v-btn>

      <v-btn
        class="login-btn"
        v-if="isLogin"
        @click="logout"
      >로그아웃</v-btn>
    </div>
  </div>
</template>

<script setup>
import { useAccountStore } from '@/stores/accounts'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import axios from 'axios'

const router = useRouter()
const accountStore = useAccountStore()
const { isLogin } = storeToRefs(accountStore)

const logout = () => {
  accountStore.logOut()
  delete axios.defaults.headers.common['Authorization']
  router.push('/')
}
</script>

<style scoped>
.nav-bar {
  background-color: #003E5C;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 32px;
  color: white;
  font-size: 15px;
  gap: 16px;
}

.logo {
  height: 48px;
  cursor: pointer;
}

.menu-items {
  display: flex;
  gap: 24px;
  flex-grow: 1;
  justify-content: center;
}

.menu-item {
  cursor: pointer;
  transition: opacity 0.2s ease;
}
.menu-item:hover {
  opacity: 0.7;
}

.auth-buttons {
  display: flex;
  gap: 12px;
  align-items: center;
}

.login-btn {
  background-color: white;
  color: black;
  border-radius: 999px;
  font-weight: 500;
  padding: 4px 16px;
  font-size: 14px;
  height: 36px;
}
</style>
