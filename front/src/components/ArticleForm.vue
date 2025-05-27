<template>
  <v-form @submit.prevent="handleSubmit">
    <v-text-field
      v-model="form.title"
      label="제목"
      required
    />
    <v-textarea
      v-model="form.content"
      label="내용"
      rows="10"
      required
    />
    <v-btn type="submit" color="primary">등록</v-btn>
  </v-form>
</template>

<script setup>
import { reactive } from 'vue'

const emit = defineEmits(['submit'])

const form = reactive({
  title: '',
  content: ''
})

const handleSubmit = () => {
  emit('submit', {
    title: form.title,
    content: form.content
  })

  // 전송 후 초기화 (선택사항)
  form.title = ''
  form.content = ''
}
</script>

<style scoped>
</style>