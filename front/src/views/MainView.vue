<template>
  <v-container class="main-wrapper" fluid>
    <TopBar />
    <MainMenu />

    <!-- ✅ 여백 확보 -->
    <div class="spacer" />

    <!-- ✅ 하단 링크 위젯 -->
    <div class="footer-links">
      <div
        v-for="link in linkWidgets"
        :key="link.title"
        class="footer-link-card"
      >
        <a
          :href="link.url"
          target="_blank"
          rel="noopener"
          class="footer-link-title"
        >
          <span class="footer-icon">{{ link.icon }}</span> {{ link.title }}
        </a>
        <div class="footer-link-desc">{{ link.desc }}</div>
      </div>
    </div>
  </v-container>
</template>

<script setup>
import TopBar from '@/components/MainBar.vue'
import MainMenu from '@/components/MainMenu.vue'

const linkWidgets = [
  {
    title: '신혼희망타운',
    icon: '🏡',
    url: 'https://www.lh.or.kr/menu.es?mid=a10402010200',
    desc: 'LH에서 제공하는 신혼희망타운 정보'
  },
  {
    title: '지역별 신혼부부 주거 복지 지원',
    icon: '📍',
    url: 'https://www.myhome.go.kr/hws/portal/main/getMgtMainYhsPage.do',
    desc: '지역 기반의 주거지원 정책'
  },
  {
    title: '신혼부부 혜택 정리 게시글',
    icon: '📝',
    url: 'https://brunch.co.kr/@dailynews/1919',
    desc: '다양한 혜택을 한눈에 보는 브런치 글'
  }
]

const openLink = (url) => {
  window.open(url, '_blank')
}
</script>

<style scoped>
.main-wrapper {
  min-height: 100vh;
  background: linear-gradient(to bottom, #003E5C 45%, #ffffff);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 24px;
}

/* 🔽 위와 하단 메뉴 사이 간격 */
.spacer {
  flex-grow: 1;
}

/* 🔗 하단 링크 */
.footer-links {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.footer-link-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  max-width: 220px;
}

.footer-link-title {
  font-size: 1.1rem;
  font-weight: bold;
  color: #003E5C;
  text-decoration: none;
  transition: color 0.2s ease;
}

.footer-link-title:hover {
  color: #FF69B4;
  text-decoration: underline;
}

.footer-icon {
  font-size: 2rem;
  display: block;
  margin-bottom: 4px;
}

.footer-link-desc {
  font-size: 0.9rem;
  color: #444;
  margin-top: 4px;
  line-height: 1.4;
}
</style>
