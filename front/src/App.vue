<template>
  <v-app class="app-background">
    <router-view />
  </v-app>
</template>

<script setup>

</script>

<style>

@font-face {
  font-family: 'SUIT';
  src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_suit@1.0/SUIT-Regular.woff2') format('woff2');
  font-weight: normal;
  font-style: normal;
}

* {
  font-family: 'SUIT', sans-serif !important;
}

.app-background {
  min-height: 100vh;
  background: linear-gradient(
    to bottom,
    /* #003E5C,  */
    #ffffff
  );
}

</style>