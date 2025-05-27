<template>
  <v-container class="signup-container">
    <h1 class="text-h5 mb-6">회원가입</h1>

    <v-form @submit.prevent="submitSignup">
      <div class="field-label">아이디</div>
      <v-text-field v-model="form.username" variant="underlined" placeholder="아이디를 입력하세요" bg-color="transparent" hide-details density="comfortable" required />

      <div class="field-label">닉네임</div>
      <v-text-field v-model="form.nickname" variant="underlined" placeholder="닉네임을 입력하세요" bg-color="transparent" hide-details density="comfortable" required />

      <div class="field-label">비밀번호</div>
      <v-text-field v-model="form.password" type="password" variant="underlined" placeholder="비밀번호를 입력하세요" bg-color="transparent" hide-details density="comfortable" required />

      <div class="field-label">비밀번호 확인</div>
      <v-text-field
        v-model="passwordCheck"
        type="password"
        variant="underlined"
        placeholder="비밀번호를 다시 입력하세요"
        :error="passwordCheck && form.password !== passwordCheck"
        error-messages="비밀번호가 일치하지 않습니다."
        bg-color="transparent"
        hide-details
        density="comfortable"
        required
      />

      <div class="field-label">이메일</div>
      <v-text-field v-model="form.email" type="email" variant="underlined" placeholder="이메일을 입력하세요" bg-color="transparent" hide-details density="comfortable" required />

      <div class="field-label">생년월일</div>
      <v-text-field v-model="form.birthdate" type="date" variant="underlined" bg-color="transparent" hide-details density="comfortable" required />

      <div class="field-label">성별</div>
      <v-select v-model="form.gender" :items="['남성', '여성']" variant="underlined" placeholder="성별을 선택하세요" bg-color="transparent" hide-details density="comfortable" required />

      <div class="field-label">연소득 (만원)</div>
      <v-text-field v-model="form.salary" type="number" variant="underlined" placeholder="예: 5000" bg-color="transparent" hide-details density="comfortable" required />

      <div class="field-label">자산 (만원)</div>
      <v-text-field v-model="form.wealth" type="number" variant="underlined" placeholder="예: 20000" bg-color="transparent" hide-details density="comfortable" required />

      <div class="field-label">프로필 이미지 (선택)</div>
      <v-file-input
        v-model="form.profile_img"
        accept="image/*"
        show-size
        hide-details
        density="comfortable"
        bg-color="transparent"
        variant="underlined"
        prepend-icon="mdi-camera"
        label="이미지 업로드"
        style="max-width: 300px;"
        class="file-button"
      />

      <v-btn variant="outlined" type="submit" color="primary" class="mt-6">회원가입</v-btn>
    </v-form>
  </v-container>
</template>

<script setup>
import { reactive, ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const passwordCheck = ref('')

const form = reactive({
  username: '',
  nickname: '',
  password: '',
  email: '',
  birthdate: '',
  gender: '',
  salary: '',
  wealth: '',
  profile_img: null,
})

const submitSignup = async () => {
  console.log("🔍 username 값:", form.username) 
  if (form.password !== passwordCheck.value) {
    alert('비밀번호가 일치하지 않습니다.')
    return
  }

  const formData = new FormData()
  formData.append('username', form.username)
  formData.append('nickname', form.nickname)
  formData.append('password1', form.password)
  formData.append('password2', passwordCheck.value)
  formData.append('email', form.email)

  // 날짜 형식 오류 방지
  formData.append('birth_date', new Date(form.birthdate).toISOString().slice(0, 10))

  formData.append('gender', form.gender === '남성' ? 'M' : 'W')
  formData.append('salary', form.salary)
  formData.append('wealth', form.wealth)

if (form.profile_img && form.profile_img instanceof File) {
  formData.append('profile_img', form.profile_img)
} else if (form.profile_img && form.profile_img.length > 0) {
  formData.append('profile_img', form.profile_img[0])
}

  try {
    const res = await axios.post('http://127.0.0.1:8000/api/auth/registration/', formData)
    console.log('회원가입 성공:', res.data)
    alert('회원가입이 완료되었습니다!')
    router.push('/')
  } catch (err) {
    console.error('회원가입 실패:', err.response?.data || err.message)
    alert('회원가입 실패: ' + (err.response?.data?.detail || '다시 시도해 주세요.'))
  }
}
</script>


<style scoped>
.signup-container {
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
