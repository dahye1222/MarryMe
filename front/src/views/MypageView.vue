<template>
  <div>
    <NavBar />
    <v-container>
      <h1 class="text-h5 mb-4">👤 마이페이지</h1>

      <v-row>
        <!-- 왼쪽: 프로필 정보 -->
        <v-col cols="12" md="4" class="text-center">
          <v-avatar size="200" class="mb-4">
            <img
              :src="getProfileImgUrl(profileImage)"
              alt="프로필 이미지"
              class="avatar-img"
            />
          </v-avatar>
          <div class="text-h6">
            {{ profile.nickname }}
            <span v-if="profile.gender === 'W'">예신님</span>
            <span v-else-if="profile.gender === 'M'">예랑님</span>
            환영합니다!
          </div>
          <div class="mt-2">연소득: {{ profile.salary.toLocaleString() }}만원</div>
          <div>자산: {{ profile.wealth.toLocaleString() }}만원</div>
        </v-col>

        <!-- 오른쪽: 위시리스트 -->
        <v-col cols="12" md="8">
          <div class="mb-4">
            <h3 class="text-subtitle-1">⭐ 예금 옵션 위시리스트</h3>
            <v-card class="pa-4 my-2" v-if="profile.wishlist_deposits_options.length">
              <v-list>
                <v-list-item
                  v-for="item in profile.wishlist_deposits_options"
                  :key="item.id"
                >
                  <v-list-item-content>
                    <v-list-item-title>
                      {{ item.deposit_product.kor_co_nm }} - {{ item.deposit_product.fin_prdt_nm }}
                    </v-list-item-title>
                    <v-list-item-subtitle>
                      {{ item.save_trm }}개월 | 금리: {{ item.intr_rate ?? 'N/A' }}%
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-card>
            <v-alert type="info" v-else>마음에 드는 예금 옵션을 담아보세요!</v-alert>
          </div>

          <div class="mb-4">
            <h3 class="text-subtitle-1">⭐ 적금 옵션 위시리스트</h3>
            <v-card class="pa-4 my-2" v-if="profile.wishlist_savings_options.length">
              <v-list>
                <v-list-item
                  v-for="item in profile.wishlist_savings_options"
                  :key="item.id"
                >
                  <v-list-item-content>
                    <v-list-item-title>
                      {{ item.saving_product.kor_co_nm }} - {{ item.saving_product.fin_prdt_nm }}
                    </v-list-item-title>
                    <v-list-item-subtitle>
                      {{ item.save_trm }}개월 | 금리: {{ item.intr_rate ?? 'N/A' }}%
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-card>
            <v-alert type="info" v-else>마음에 드는 적금 옵션을 담아보세요!</v-alert>
          </div>

          <div class="mb-4">
            <h3 class="text-subtitle-1">⭐ 대출상품 위시리스트</h3>
            <v-card class="pa-4 my-2" v-if="profile.wishlist_loans.length">
              <v-list>
                <v-list-item
                  v-for="item in profile.wishlist_loans"
                  :key="item.id"
                >
                  <v-list-item-content>
                    <v-list-item-title>
                      {{ item.kor_co_nm }} - {{ item.fin_prdt_nm }}
                    </v-list-item-title>
                    <v-list-item-subtitle>
                      {{ item.loan_lmt ? `최대 한도: ${item.loan_lmt}` : '한도 정보 없음' }} |
                      최저 금리: {{ item.min_lend_rate ?? 'N/A' }}%
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-card>
            <v-alert type="info" v-else>마음에 드는 대출 상품을 담아보세요!</v-alert>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import axios from 'axios'
import NavBar from '@/components/NavBar.vue'

const profile = ref({
  nickname: '',
  gender: '',
  salary: 0,
  wealth: 0,
  profile_img: '',
  wishlist_deposits_options: [],
  wishlist_savings_options: [],
  wishlist_loans: [],
})

const getProfileImgUrl = (path) => {
  if (!path) return '/default_profile.png'
  // 로컬 asset이거나 data URI인 경우
  if (path.startsWith('http') || path.startsWith('data:')) return path
  return `https://marryme-4mqi.onrender.com${path}`  // /media/... 등 처리
}

onMounted(async () => {
  try {
    const res = await axios.get('https://marryme-4mqi.onrender.com/api/accounts/mypage/', {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`,
      },
    })
    profile.value = res.data
  } catch (err) {
    console.error('❌ 마이페이지 불러오기 실패:', err)
    alert('로그인이 필요합니다.')
  }
})

const profileImage = computed(() => {
  if (profile.value.profile_img) {
    return profile.value.profile_img
  }
  if (profile.value.gender === 'W') {
    return new URL('@/assets/default_woman.png', import.meta.url).href
  }
  if (profile.value.gender === 'M') {
    return new URL('@/assets/default_man.png', import.meta.url).href
  }
  return new URL('@/assets/default_profile.png', import.meta.url).href
})
</script>

<style scoped>
.text-subtitle-1 {
  font-weight: bold;
  font-family: 'SUIT-Regular', sans-serif;
}
@font-face {
  font-family: 'SUIT-Regular';
  src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_suit@1.0/SUIT-Regular.woff2') format('woff2');
  font-weight: normal;
  font-style: normal;
}

.text-h6, .h1 {
  font-family: 'SUIT-Regular', sans-serif;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}
</style>
 