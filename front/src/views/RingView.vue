<template>
  <div>
    <NavBar />
    <v-container>
      <h1 class="text-h5 mb-6">💍 예물 & 금시세</h1>
      <v-row>
        <v-col cols="12" md="6">
          <JewelryMap />
        </v-col>
        <v-col cols="12" md="6">
          <PriceChart />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue'
import JewelryMap from '@/components/KakaoMap.vue'
import PriceChart from '@/components/GoldChart.vue'
</script>
