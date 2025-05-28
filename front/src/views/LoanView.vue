<template>
  <div class="page-background">
    <NavBar />
    <v-container>
      <div class="d-flex justify-space-between align-center mb-4">
        <h1 class="text-h5 my-3"><strong>💸 전세자금 대출상품</strong></h1>
        <v-btn @click="fetchRecommendedLoans"  class="text-white" style="background-color: #016291;">
          🤖 내 또래가 고른 전세대출 보러가기
        </v-btn>
      </div>

      <v-row>
        <v-col
          v-for="loan in loanProducts"
          :key="loan.id"
          cols="12"
          md="6"
          lg="3"
        >
          <v-card
            class="mb-4 fixed-card"
            style="background-color: #ffffff; color: #003E5C; max-width: 300px;"
            elevation="0.1"

          >
            <!-- ❤️🤍 위시리스트 버튼 -->
            <div
              class="wishlist-emoji"
              @click.stop="toggleWishlist(loan)"
            >
              {{ wishlist.has(loan.id) ? '❤️' : '🤍' }}
            </div>

            <v-card-title>
              <strong v-html="formatTitle(loan.fin_prdt_nm)"></strong>
            </v-card-title>
            <v-card-subtitle>
              {{ loan.kor_co_nm }}
            </v-card-subtitle>
            <v-card-text>
              <p><strong>최대 한도:</strong> {{ loan.loan_lmt || '정보 없음' }}</p>
              <p><strong>최저 금리:</strong> {{ loan.min_lend_rate !== null ? loan.min_lend_rate + '%' : '정보 없음' }}</p>
            </v-card-text>

            <v-card-actions>
              <v-spacer />
              <v-btn @click="openDetail(loan)" variant="outlined">
                
                <strong>상세 정보 보기</strong>
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>

      </v-row>

      <!-- 상세 팝업 -->
      <v-dialog v-model="showDialog" max-width="700px">
        <v-card class="pa-6">
          <v-card-title><strong> 💰 {{ detail?.fin_prdt_nm }}</strong></v-card-title>
          <v-card-text v-if="detail" style="line-height: 1.8">
            <p><strong>은행:</strong> {{ detail.kor_co_nm }}</p>
            <p><strong>가입 방법:</strong> {{ detail.join_way }}</p>
            <p><strong>대출 한도:</strong> {{ detail.loan_lmt || '없음' }}</p>
            <p><strong>중도상환수수료:</strong> {{ detail.erly_rpay_fee }}</p>
            <p><strong>인지세:</strong> {{ detail.loan_inci_expn }}</p>
            <p><strong>연체이자율:</strong> {{ detail.dly_rate }}</p>
          </v-card-text>

          <v-card-text>
            <h4 class="text-subtitle-1 mb-4" ><strong>🔍 해당 상품의 예상 상환 금액 조회하기</strong></h4>
            <v-text-field
              variant="outlined"
              v-model="loanAmount"
              label="대출금액 (원)"
              type="number"
            />
            <v-text-field
              variant="outlined"
              v-model="months"
              label="상환 기간 (개월)"
              type="number"
            />
            <v-btn
              class="mt-2 text-white"
              style="background-color: #016291;"
              @click="fetchSimulation"
            >
              조회하기
            </v-btn>
          </v-card-text>

          <v-card-text v-if="deduplicatedResults.length">
            <h4 class="text-subtitle-1 mt-4 mb-2" style="border-bottom: 2px solid #003E5C; padding-bottom: 4px;"><strong>💡 상환 시뮬레이션 결과</strong></h4>
            <v-table>
              <thead>
                <tr>
                  <th>상환방식</th>
                  <th>최저금리(%)</th>
                  <th>총 상환금액</th>
                  <th>원금</th>
                  <th>총 이자</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="result in deduplicatedResults" :key="result.option_id">
                  <td>{{ result.rpay_type_nm }}</td>
                  <td>{{ result.lend_rate_min }}</td>
                  <td>{{ formatCurrency(result['총 상환금액']) }}</td>
                  <td>{{ formatCurrency(result['원금']) }}</td>
                  <td>{{ formatCurrency(result['총 이자']) }}</td>
                </tr>
              </tbody>
            </v-table>
          </v-card-text>

          <v-card-actions>
            <v-spacer />
            <v-btn
              class="mt-2 text-white"
              style="background-color: #016291;"
              @click="showDialog = false"
            >
              닫기
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- 추천 팝업 -->
      <v-dialog v-model="showRecommendDialog" max-width="800px">
        <v-card class="pa-6" style="background-color: #f2f4f5; color: #003E5C;">
          <v-card-title class="text-h6">
            <strong>🎯 당신에게 맞는 대출상품 추천</strong>
          </v-card-title>

          <v-card-text v-if="recommendLoading" class="text-center my-6">
            <v-progress-circular indeterminate color="primary" />
            <div class="mt-2">맞춤형 추천을 불러오는 중입니다...</div>
          </v-card-text>

          <v-card-text
            v-else-if="recommendedLoans.length"
            class="mt-4"
            style="line-height: 1.8;"
          >
            <v-row>
              <v-col
                v-for="loan in recommendedLoans"
                :key="loan.id"
                cols="12"
                md="6"
              >
                <v-card
                  class="mb-3"
                  outlined
                  style="background-color: #ffffff; color: #003E5C;"
                >
                  <v-card-title>
                    <strong>{{ loan.fin_prdt_nm }}</strong>
                  </v-card-title>
                  <v-card-subtitle>
                    {{ loan.kor_co_nm }}
                  </v-card-subtitle>
                  <v-card-text>
                    <p><strong>최대 한도:</strong> {{ loan.loan_lmt ?? '정보 없음' }}</p>
                    <p><strong>최저 금리:</strong> {{ loan.min_lend_rate ?? 'N/A' }}%</p>
                    <p class="mt-2 text-caption text-blue-darken-2">
                      🔍 이 상품은 당신의 소득, 자산, 나이 등을 고려해 추천되었어요.
                    </p>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>

          <v-card-actions>
            <v-spacer />
            <v-btn
              class="mt-2 text-white"
              style="background-color: #016291;"
              @click="showRecommendDialog = false"
            >
              닫기
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

    </v-container>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import NavBar from '@/components/NavBar.vue'

const loanProducts = ref([])
const detail = ref(null)
const repaymentResults = ref([])
const loanAmount = ref('')
const months = ref('')
const showDialog = ref(false)

const showRecommendDialog = ref(false)
const recommendedLoans = ref([])
const recommendLoading = ref(false)

const wishlist = ref(new Set())

const formatTitle = (title) => {
  const limit = 13.5
  if (title.length <= limit) return title
  return title.slice(0, limit) + '<br>' + title.slice(limit)
}
// 찜 토글
const toggleWishlist = async (loan) => {
  const isWished = wishlist.value.has(loan.id)
  const url = `https://marryme-4mqi.onrender.com/api/products/wishlist/loans/${loan.id}/toggle/`

  try {
    await axios.post(url, {}, {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })

    if (isWished) {
      wishlist.value.delete(loan.id)
      alert('찜에서 제거되었습니다.')
    } else {
      wishlist.value.add(loan.id)
      alert('찜 목록에 추가되었습니다!')
    }
  } catch (err) {
    console.error('❌ 찜 토글 실패:', err)
    alert('로그인이 필요합니다!')
  }
}

// 추천 불러오기
const fetchRecommendedLoans = async () => {
  recommendLoading.value = true
  try {
    const res = await axios.get('https://marryme-4mqi.onrender.com/api/recommend/loans/', {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })
    recommendedLoans.value = res.data
    showRecommendDialog.value = true
  } catch (err) {
    console.error('❌ 추천 로딩 실패:', err)
    alert('추천 기능은 로그인 후 이용 가능합니다.')
  } finally {
    recommendLoading.value = false
  }
}

// 대출 전체 조회 + 찜 목록 로딩
onMounted(async () => {
  try {
    const res = await axios.get('https://marryme-4mqi.onrender.com/api/products/loans/')
    loanProducts.value = res.data
  } catch (err) {
    console.error('❌ 대출상품 전체 조회 실패:', err)
  }

  try {
    const res = await axios.get('https://marryme-4mqi.onrender.com/api/accounts/mypage/', {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })
    wishlist.value = new Set(res.data.wishlist_loans.map(loan => loan.id))
  } catch (err) {
    console.error('❌ 찜 목록 조회 실패:', err)
  }
})

const openDetail = async (loan) => {
  try {
    const res = await axios.get(`https://marryme-4mqi.onrender.com/api/products/loans/${loan.id}/`)
    detail.value = res.data.product
    repaymentResults.value = []
    loanAmount.value = ''
    months.value = ''
    showDialog.value = true
  } catch (err) {
    console.error('❌ 상세 정보 조회 실패:', err)
  }
}

const fetchSimulation = async () => {
  if (!loanAmount.value || !months.value) {
    alert('대출금액과 기간을 입력해주세요!')
    return
  }

  try {
    const res = await axios.get(`https://marryme-4mqi.onrender.com/api/products/loans/${detail.value.id}/`, {
      params: {
        loan_amount: loanAmount.value,
        months: months.value
      }
    })
    repaymentResults.value = res.data.repayment_simulation
  } catch (err) {
    console.error('❌ 시뮬레이션 실패:', err)
  }
}

const deduplicatedResults = computed(() => {
  const seen = new Map()
  for (const result of repaymentResults.value) {
    const name = result.rpay_type_nm
    const rate = result.lend_rate_min
    if (seen.has(name)) {
      if (rate < seen.get(name).lend_rate_min) {
        seen.set(name, result)
      }
    } else {
      seen.set(name, result)
    }
  }
  return Array.from(seen.values())
})

const formatCurrency = (val) => {
  return Number(val).toLocaleString() + '원'
}
</script>

<style scoped>
.page-background {
  background-color: #F2F4F5; /* 진한 파란 배경 */
  min-height: 100vh;
  padding-bottom: 32px; /* 여백 보존 */
}

.fixed-card {
  min-height: 250px;
  background-color: #ffffff; /* 카드 흰색 */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
}

.wishlist-emoji {
  position: absolute;
  top: 8px;
  right: 12px;
  font-size: 24px;
  cursor: pointer;
  user-select: none;
}
</style>
