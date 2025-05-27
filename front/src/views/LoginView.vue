<template>
  <v-container class="login-container">
    <h1 class="text-h5 mb-6">로그인</h1>

    <v-form @submit.prevent="handleLogin">
      <div class="field-label">아이디</div>
      <v-text-field
        v-model="username"
        variant="underlined"
        placeholder="아이디를 입력하세요"
        bg-color="transparent"
        hide-details
        density="comfortable"
        required
      />

      <div class="field-label">비밀번호</div>
      <v-text-field
        v-model="password"
        variant="underlined"
        type="password"
        placeholder="비밀번호를 입력하세요"
        bg-color="transparent"
        hide-details
        density="comfortable"
        required
      />

      <v-btn variant="outlined" type="submit" color="primary" class="mt-6">로그인</v-btn>
    </v-form>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

const router = useRouter()
const accountStore = useAccountStore()

const username = ref('')
const password = ref('')

const handleLogin = async () => {
  const payload = {
    username: username.value,
    password: password.value,
  }

  await accountStore.logIn(payload)

  if (accountStore.isLogin) {
    router.push('/')
  } else {
    alert('로그인 실패. 아이디 또는 비밀번호를 확인하세요.')
  }
}
</script>

<style scoped>
.login-container {
  max-width: 500px;
  margin: 0 auto;
  padding-top: 64px;
}

.field-label {
  font-weight: 500;
  margin-top: 20px;
  margin-bottom: 4px;
  color: #333;
}
</style>
