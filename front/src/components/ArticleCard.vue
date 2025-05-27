<template>
  <v-card @click="$router.push(`/board/${article.id}`)" style="cursor: pointer;">
    <v-card-title>{{ article.title }}</v-card-title>
    <v-card-subtitle>
      👤 {{ article.nickname }}
      <span v-if="article.gender === 'W'">예신님</span>
      <span v-else-if="article.gender === 'M'">예랑님</span>
      | 🕒 {{ article.created_at.slice(0, 16).replace('T', ' ') }}
    </v-card-subtitle>
    <v-card-text>{{ article.content.slice(0, 300) }}</v-card-text>
  </v-card>
</template>

<script setup>
defineProps({
  article: Object
})
</script>