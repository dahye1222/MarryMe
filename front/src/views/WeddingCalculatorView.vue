<template>
  <div>
    <NavBar />

    <v-container class="calculator-wrapper" fluid>
      <h1 class="text-h5 mb-6" style="color: white;"><strong>📋 결혼 비용 계산기</strong></h1>
      <div class="text-center mt-8" style="color: white; margin-bottom: 20px;">
        <strong>💡 예산 계산기 사용법</strong>
        <p>
          각 항목에 예상 비용을 입력하고,  💰 총 비용을 확인하세요. <br />
          저장버튼을 통해 💾 저장 및 예산 도우미 챗봇 🤖 을 통해 <br />
          결혼비용 예산에 관한 상담 및 질문도 가능합니다.
        </p>
      </div>

      <v-card
        v-for="(category, idx) in weddingCostCategories"
        :key="idx"
        class="mb-6 px-4 py-4"
        elevation="2"
      >
        <h2 class="text-h6 mb-2">📂 <strong>{{ category.category }}</strong></h2>

        <v-row v-if="form[category.category]" v-for="(item, iIdx) in category.items" :key="iIdx" class="align-center mb-3">
          <v-col cols="5">
            <strong>{{ item.label }}</strong>
            <div v-if="item.description" class="item-desc" v-html="item.description"></div>
          </v-col>

          <v-col cols="7">
            <v-text-field
              v-model="form[category.category][item.name]"
              :placeholder="item.placeholder || ''"
              type="number"
              variant="underlined"
              density="comfortable"
              hide-details
              class="input-field"
              :step="item.step"
              :min="item.min"
              :max="item.max"
              suffix="만원"
            />
          </v-col>
        </v-row>
      </v-card>

      <v-divider class="my-6" />

      <v-row class="mb-4" style="font-size: 18px;">
        <v-col cols="6" class="text-right font-weight-bold">총합</v-col>
        <v-col cols="6">{{ total }} 만원</v-col>
      </v-row>

      <div class="text-center mb-8">
        <v-btn
          color="#003E5C"
          variant="text"
          @click="saveBudget"
          style="text-decoration: underline; font-size: 16px;"
        >
          <strong>💾 예산 저장하기</strong>
        </v-btn>      
      </div>

      <!-- 💬 챗봇 모달 -->
      <v-dialog v-model="showChatbot" max-width="600" persistent>
        <v-card class="pa-6 d-flex flex-column" style="max-height: 80vh;">
          <div class="d-flex justify-space-between align-center mb-4">
            <h2 class="text-h6"><strong>💬 결혼 예산 도우미 챗봇</strong></h2>
            <v-btn
              variant="plain"
              style="min-width: 0; padding: 0; box-shadow: none;"
              @click="showChatbot = false"
            >
              <span style="font-size: 20px;">❌</span>
            </v-btn>
          </div>

          <!-- 채팅 메시지 영역 -->
          <div class="chat-window flex-grow-1 mb-4">
            <div v-for="(msg, index) in messages" :key="index" class="mb-2">
              <div
                :class="['chat-bubble', msg.from === 'user' ? 'user-msg' : 'bot-msg']"
              >
                {{ msg.text }}
              </div>
            </div>
          </div>

          <!-- 질문 입력 -->
          <div class="d-flex align-center">
            <v-text-field
              variant="outlined"
              v-model="question"
              placeholder="질문을 입력하세요"
              hide-details
              density="compact"
              class="flex-grow-1 mr-2"
              @keyup.enter="askChatbot"
            />
            <v-btn color="#003E5C"  @click="askChatbot" :loading="loading">전송</v-btn>

          </div>
        </v-card>
      </v-dialog>

      <!-- 챗봇 열기 버튼 (우측 하단) -->
      <v-btn
        class="chatbot-float-btn"
        @click="showChatbot = true"
        elevation="0"
        variant="plain"
        v-ripple="false"
        style="background-color: transparent; padding: 0; min-width: 0; border-radius: 0;"
      >
        <img src="@/assets/chatbot.png" alt="챗봇" class="chatbot-icon" />
      </v-btn>

      
      

</v-container>
    </div>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue'
import { ref, reactive, computed, onMounted } from 'vue'
import axios from 'axios'
import weddingCostCategories from '@/data/weddingCategories.js'

// 💾 예산 계산기
const form = reactive({})
const question = ref('')
const answer = ref('')
const loading = ref(false)
const showChatbot = ref(false)


const initializeForm = () => {
  weddingCostCategories.forEach(category => {
    form[category.category] = {}
    category.items.forEach(item => {
      form[category.category][item.name] = ''
    })
  })
}

const flattenForm = () => {
  const flat = {}
  for (const category of Object.values(form)) {
    for (const [key, value] of Object.entries(category)) {
      flat[key] = value === '' ? null : Number(value)
    }
  }
  return flat
}

const nestedForm = (flatData) => {
  const result = {}
  weddingCostCategories.forEach(category => {
    result[category.category] = {}
    category.items.forEach(item => {
      result[category.category][item.name] = flatData[item.name] ?? ''
    })
  })
  return result
}

onMounted(async () => {
  initializeForm()

  try {
    const res = await axios.get('/api/budget/')
    const nested = nestedForm(res.data)
    Object.assign(form, nested)
  } catch (e) {
    console.error('❌ 예산 불러오기 실패:', e)
  }
})

const total = computed(() => {
  let sum = 0
  for (const category of Object.values(form)) {
    for (const val of Object.values(category)) {
      sum += Number(val) || 0
    }
  }
  return sum
})

const saveBudget = async () => {
  try {
    const payload = flattenForm()
    await axios.patch('/api/budget/', payload)
    alert('✅ 예산이 저장되었습니다.')
  } catch (e) {
    console.error('❌ 저장 실패:', e.response?.data || e)
    alert('저장에 실패했습니다.')
  }
}
const messages = ref([])


// 💬 챗봇 질문
const askChatbot = async () => {
  const userQuestion = question.value?.trim()

  if (!userQuestion) {
    alert('질문을 입력해주세요.')
    return
  }

  messages.value.push({ from: 'user', text: userQuestion })
  question.value = ''  

  loading.value = true

  try {
    const res = await axios.post(
      '/api/budget/chat/',
      { question: userQuestion },  
      {
        headers: {
          Authorization: `Token ${localStorage.getItem('token')}`,
        },
      }
    )
    messages.value.push({ from: 'bot', text: res.data.answer })
  } catch (e) {
    console.error(e)
    messages.value.push({ from: 'bot', text: '❌ 챗봇 응답 중 오류가 발생했습니다.' })
  } finally {
    loading.value = false
  }
}

</script>

<style scoped>
.calculator-wrapper {
  background: linear-gradient(to bottom, #003E5C 45%, #ffffff);
  min-height: 100vh;
  color: black;
  padding-top: 32px;
}

.input-field input {
  text-align: right;
}

.item-desc {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
  white-space: pre-line;
}

.save-btn {
  padding: 10px 24px;
  border-radius: 999px;
  font-weight: bold;
}
.chatbot-float-btn {
  position: fixed;
  bottom: 120px;
  right: 32px;
  z-index: 999;
  background-color: transparent !important;
  box-shadow: none !important;
}

.v-dialog .v-card {
  border-radius: 16px;
}

.chat-window {
  overflow-y: auto;
  max-height: 400px;
  padding-right: 4px;
  border-radius: 24px;
}

.chat-bubble {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 24px; 
  word-wrap: break-word;
  line-height: 1.4;
}
.user-msg {
  background-color: #e0f7fa;
  align-self: flex-end;
  margin-left: auto;
  border-bottom-right-radius: 4px; 
}

.bot-msg {
  background-color: #eeeeee;
  align-self: flex-start;
  margin-right: auto;
  border-bottom-left-radius: 4px; 
}
.chatbot-icon {
  width: 120px;
  height: 120px;
  object-fit: contain;
  cursor: pointer;
  transform: scale(1.05);
  transition: transform 0.2s ease-in-out;
}
</style>
