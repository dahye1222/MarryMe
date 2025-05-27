<!-- components/MainMenu.vue -->
<template>
  <div class="logo-section">
    <img src="@/assets/marryme-logo.png" alt="logo" class="logo-img" />

    <div class="text-menus">
      <span class="menu-item" @click="$router.push('/products')">💰 예/적금 추천</span>
      <span class="menu-item" @click="$router.push('/loans')">💳 대출 찾기</span>
      <span class="menu-item" @click="$router.push('/calculator')">📋 결혼비용계산기</span>
      <span class="menu-item" @click="$router.push('/weddingring')">💍 예물 & 금시세</span>
      <span class="menu-item" @click="$router.push('/board')">📓 결혼이야기</span>
    </div>
  </div>
</template>

<script setup></script>

<style scoped>
.logo-section {
  text-align: center;
  margin-top: 48px;
}
.logo-img {
  width: 400px;
  height: auto;
}
.text-menus {
  margin-top: 36px;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 36px;
}
.menu-item {
  position: relative;
  font-weight: 500;
  color: white;
  cursor: pointer;
  font-size: 20px;
  transition: opacity 0.2s;
}
.menu-item::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 0%;
  height: 2px;
  background-color: white;
  transition: width 0.3s ease;
}
.menu-item:hover::after {
  width: 100%;
}
.menu-item:hover {
  opacity: 0.8;
}
</style>
