<template>
  <div class="page-background">
    <NavBar />
    <v-container>
      <div class="d-flex justify-space-between align-center mb-4">
        <h1 class="text-h5 mb-4"><strong>📦 금융상품</strong></h1>
      </div>

      <!-- 버튼 토글 -->
      <div class="d-flex justify-center mb-6">
        <v-btn-toggle v-model="productType" mandatory>
          <v-btn value="deposit"><strong>예금상품 전체 보기</strong></v-btn>
          <v-btn value="saving"><strong>적금상품 전체 보기</strong></v-btn>
        </v-btn-toggle>
      </div>

      <!-- 추천 버튼 -->
      <div class="d-flex justify-end mb-4">
        <v-btn
          @click="fetchRecommended"
          class="text-white"
          style="background-color: #016291;"
        >
          🤖 당신에게 맞는 {{ productType === 'deposit' ? '예금' : '적금' }} 상품 추천받기
        </v-btn>
      </div>

      <!-- 카드 출력 -->
      <v-row align="stretch">
        <v-col
          v-for="product in displayedProducts"
          :key="product.id"
          cols="12"
          md="6"
          lg="3"
          class="d-flex"
        >
          <v-card
            class="mb-5 fixed-card"
            elevation="0.1"
            style="background-color: #ffffff; color: #003E5C; max-width: 100%; position: relative; flex: 1;"
          >
            <!-- ❤️🤍 위시리스트 버튼 -->
            <!-- <div
              class="wishlist-emoji"
              @click.stop="toggleWishlist(product)"
            >
              {{ wishlist.has(product.id) ? '❤️' : '🤍' }}
            </div> -->

            <v-card-title class="card-title">
              <strong v-html="formatTitle(product.fin_prdt_nm)"></strong>
            </v-card-title>
            <v-card-subtitle>{{ product.kor_co_nm }}</v-card-subtitle>

            <v-card-text>
              <div v-if="product.options && product.options.length">
                <h4
                  class="text-subtitle-2 mt-2 mb-2"
                  style="font-size: 1.5rem; border-bottom: 2px solid #003E5C; padding-bottom: 4px;"
                >
                  📈 기간별 금리
                </h4>
                <div
                  class="text-body-2 d-flex justify-space-between align-center mb-2"
                  v-for="(option, idx) in product.options"
                  :key="option.id"
                  style="font-size: 1.2rem; line-height: 0.8; margin-bottom: 1px;"
                >
                  <span @click.stop="openDetail(product, option)">
                    {{ option.save_trm }}개월: {{ option.intr_rate ?? 'N/A' }}%
                  </span>
                  <button
                    @click.stop="addToWishlistOption(option)"
                    class="wishlist-emoji-btn"
                    style="border: none; background: none; cursor: pointer; font-size: 1.4rem;"
                  >
                    {{ wishlist.has(`${productType}-${option.id}`) ? '❤️' : '🤍' }}
                  </button>
                </div>
              </div>
            </v-card-text>

            <v-card-actions>
              <v-spacer />
              <v-btn
                variant="outlined"
                @click="openDetail(product)"
              >
                <strong>상세 정보 보기</strong>
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>

      <!-- 상세 팝업 -->
      <v-dialog v-model="showDialog" max-width="600px">
        <v-card class="pa-6">
          <v-card-title class="d-flex justify-space-between align-center">
            <strong>{{ detail?.product_name }}</strong>
          </v-card-title>
          <v-card-text v-if="detail" style="line-height: 1.82">
            <p><strong>은행:</strong> {{ detail.bank_name }}</p>
            <p><strong>공시월:</strong> {{ detail.dcls_month }}</p>
            <p><strong>가입 방법:</strong> {{ detail.join_way }}</p>
            <p><strong>만기 후 이자율:</strong> {{ detail.mtrt_int }}</p>
            <p><strong>우대 조건:</strong> {{ detail.spcl_cnd }}</p>
            <p><strong>가입 대상:</strong> {{ detail.join_member }}</p>
            <p><strong>가입 제한:</strong> {{ detail.join_deny }}</p>
            <p><strong>최고 한도:</strong> {{ detail.max_limit ?? '없음' }}</p>
            <p><strong>기타 설명:</strong> {{ detail.etc_note }}</p>
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
      <!-- 추천 팝업 -->
      <v-dialog v-model="showRecommendDialog" max-width="800px">
        <v-card>
          <v-card-title class="text-h6">
            🎯 추천 {{ productType === 'deposit' ? '예금' : '적금' }} 상품
          </v-card-title>

          <v-card-text v-if="recommendLoading" class="text-center my-6">
            <v-progress-circular indeterminate color="primary" />
            <div class="mt-2">추천 상품을 불러오는 중입니다...</div>
          </v-card-text>

          <v-card-text v-else-if="recommendedOptions.length">
            <p class="text-caption text-blue-darken-2 mb-4">
              🔍 아래 추천은 당신의 나이, 자산, 성향 등을 고려한 결과입니다.
            </p>
            <v-row>
              <v-col
                v-for="(option, index) in recommendedOptions"
                :key="option.id"
                cols="12"
                md="6"
                lg="4"
              >
                <v-card class="mb-3" outlined style="position: relative; padding-top: 32px;">
                  <!-- ❤️ 하트 버튼 - 오른쪽 위 고정 -->
                  <button
                    @click.stop="addToWishlistOption(option)"
                    class="wishlist-emoji-btn"
                    style="
                      position: absolute;
                      top: 8px;
                      right: 8px;
                      border: none;
                      background: none;
                      cursor: pointer;
                      font-size: 1.4rem;
                    "
                  >
                    {{ wishlist.has(`${productType}-${option.id}`) ? '❤️' : '🤍' }}
                  </button>

                  <v-card-title>{{ index + 1 }}순위</v-card-title>
                  <v-card-subtitle>{{ option.fin_prdt_nm }} - {{ option.kor_co_nm }}</v-card-subtitle>
                  <v-card-text>
                    <p><strong>{{ option.save_trm }}개월 금리:</strong> {{ option.intr_rate2 ?? option.intr_rate ?? 'N/A' }}%</p>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>

          <v-card-actions>
            <v-spacer />
            <v-btn text @click="showRecommendDialog = false">닫기</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import NavBar from '@/components/NavBar.vue'

const router = useRouter()
const productType = ref('deposit')

const depositProducts = ref([])
const savingProducts = ref([])
const showDialog = ref(false)
const detail = ref(null)
const currentProduct = ref(null)
const wishlist = ref(new Set())
const isLoggedIn = ref(!!localStorage.getItem('token'))

const showRecommendDialog = ref(false)
const recommendLoading = ref(false)
const recommendedOptions = ref([])

const formatTitle = (title) => {
  const limit = 13.5
  if (title.length <= limit) return title
  return title.slice(0, limit) + '<br>' + title.slice(limit)
}


onMounted(async () => {
  try {
    const depositRes = await axios.get('https://marryme-4mqi.onrender.com/api/products/deposits/')
    depositProducts.value = depositRes.data
  } catch (err) {
    console.error('❌ 예금 데이터 오류:', err)
  }

  try {
    const savingRes = await axios.get('https://marryme-4mqi.onrender.com/api/products/savings/')
    savingProducts.value = savingRes.data
  } catch (err) {
    console.error('❌ 적금 데이터 오류:', err)
  }

  if (isLoggedIn.value) {
    try {
      const res = await axios.get('https://marryme-4mqi.onrender.com/api/accounts/mypage/', {
        headers: {
          Authorization: `Token ${localStorage.getItem('token')}`
        }
      })
      const depositOptionIds = res.data.wishlist_deposits_options.map(opt => opt.id)
      const savingOptionIds = res.data.wishlist_savings_options.map(opt => opt.id)
      wishlist.value = new Set([
        ...depositOptionIds.map(id => `deposit-${id}`),
        ...savingOptionIds.map(id => `saving-${id}`)
      ])
    } catch (err) {
      console.error('❌ 찜 목록 불러오기 실패:', err)
    }
  }
})

const displayedProducts = computed(() =>
  productType.value === 'deposit' ? depositProducts.value : savingProducts.value
)

const openDetail = async (product, option = null) => {
  const productId = product.id
  currentProduct.value = product

  try {
    const res = await axios.get(`https://marryme-4mqi.onrender.com/api/products/${productType.value}s/${productId}/`)
    detail.value = res.data
    showDialog.value = true
  } catch (err) {
    console.error('❌ 상세 정보 불러오기 실패:', err)
  }
}

const addToWishlistOption = async (option) => {
  if (!isLoggedIn.value) {
    alert('로그인이 필요합니다!')
    return
  }

  const key = `${productType.value}-${option.id}`
  const isWished = wishlist.value.has(key)

  const url = `https://marryme-4mqi.onrender.com/api/products/wishlist/${productType.value}-option/${option.id}/toggle/`

  try {
    await axios.post(url, {}, {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })

    if (isWished) {
      wishlist.value.delete(key)
      alert(`${option.save_trm}개월 이율이 찜 목록에서 제거되었습니다.`)
    } else {
      wishlist.value.add(key)
      alert(`${option.save_trm}개월 이율이 찜 목록에 추가되었습니다!`)
    }
  } catch (err) {
    console.error('❌ 찜 토글 실패:', err)
    alert('로그인이 필요합니다!')
  }
}


const fetchRecommended = async () => {
  if (!isLoggedIn.value) {
    alert('추천 기능은 로그인 후 이용 가능합니다.')
    return
  }

  recommendLoading.value = true
  const url = `https://marryme-4mqi.onrender.com/api/recommend/${productType.value}/`
  try {
    const res = await axios.get(url, {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })
    recommendedOptions.value = res.data
    showRecommendDialog.value = true
  } catch (err) {
    console.error('❌ 추천 실패:', err)
    alert('추천 정보를 불러오지 못했습니다. 로그인이 필요합니다!')
  } finally {
    recommendLoading.value = false
  }
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