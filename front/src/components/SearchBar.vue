<template>
  <div class="top-bar">
    <div class="search-bar">
      <input
        v-model="query"
        placeholder="검색어를 입력해 주세요."
        class="search-input"
        type="text"
        @keyup.enter="emitSearch"
      />
      <span class="search-icon" @click="emitSearch">🔍</span>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const emit = defineEmits(['search'])
const route = useRoute()
const query = ref(route.query.q || '')

const emitSearch = () => {
  if (query.value.trim()) {
    emit('search', query.value)
  }
}
</script>

<style scoped>
.top-bar {
  width: 100%;
  max-width: 1024px;
  margin: 0 auto 32px auto;
  display: flex;
  justify-content: center;
  align-items: center;
}

.search-bar {
  position: relative;
  max-width: 600px; /* 기존 400px보다 넓게 */
  width: 100%;
}

.search-input {
  width: 100%;
  padding: 16px 56px 16px 20px; /* 상하 여백 증가 */
  border-radius: 36px;
  border: none;
  outline: none;
  font-size: 21px; /* 텍스트 크기 증가 */
  background-color: white;
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.15);
}

.search-icon {
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 22px; /* 아이콘도 약간 키움 */
  cursor: pointer;
}
</style>
