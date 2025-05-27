<template>
  <div>
    <h2 class="text-subtitle-1">📈 금/은 시세 차트</h2>

    <!-- 금/은 선택 -->
    <v-btn-toggle v-model="metalType" mandatory class="mb-4">
      <v-btn value="gold">금</v-btn>
      <v-btn value="silver">은</v-btn>
    </v-btn-toggle>

    <!-- 날짜 선택 -->
    <v-row class="mb-6" align="center" justify="start">
      <v-col cols="12" sm="5">
        <v-text-field
          v-model="startDate"
          label="시작일"
          type="date"
          density="compact"
        />
      </v-col>
      <v-col cols="12" sm="5">
        <v-text-field
          v-model="endDate"
          label="종료일"
          type="date"
          density="compact"
        />
      </v-col>
    </v-row>

    <!-- 차트 -->
    <div class="chart-wrapper">
      <canvas :key="chartKey" ref="chartCanvas"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

const metalType = ref('gold')
const startDate = ref('2024-01-09')
const endDate = ref('2024-12-01')
const chartCanvas = ref(null)
const chartInstance = ref(null)
const chartKey = ref(0)
let isDrawing = false

const rawData = { gold: [], silver: [] }

async function loadJson() {
  const fetchJson = async (metal) => {
    const res = await fetch(`http://localhost:8000/api/gold-prices/metal-prices/?metal=${metal}`)
    if (!res.ok) throw new Error(`${metal} 가격 데이터를 불러오지 못했습니다.`)
    return await res.json()
  }

  rawData.gold = await fetchJson('gold')
  rawData.silver = await fetchJson('silver')

  rawData.gold.sort((a, b) => new Date(a.date || a.Date) - new Date(b.date || b.Date))
  rawData.silver.sort((a, b) => new Date(a.date || a.Date) - new Date(b.date || b.Date))

  console.log('✅ gold sample:', rawData.gold[0])
  console.log('✅ silver sample:', rawData.silver[0])
}

async function drawChart() {
  if (isDrawing) return
  isDrawing = true

  await nextTick()

  const canvas = chartCanvas.value
  if (!canvas || !canvas.getContext) {
    console.warn('⛔ canvas 또는 getContext 없음')
    isDrawing = false
    return
  }

  const ctx = canvas.getContext('2d')
  const dataSet = rawData[metalType.value]

  if (!dataSet || !dataSet.length || !startDate.value || !endDate.value) {
    console.warn('⛔ 데이터 또는 날짜 누락')
    isDrawing = false
    return
  }

  const filteredData = dataSet.filter(row => {
    const rowDate = new Date(row.date || row.Date)
    return rowDate >= new Date(startDate.value) && rowDate <= new Date(endDate.value)
  })

  const labels = filteredData.map(row => row.date || row.Date)
  const prices = filteredData.map(row => row.close_price ?? row['Close/Last']).filter(v => typeof v === 'number')

  if (!labels.length || !prices.length) {
    console.warn('⛔ 라벨 또는 가격 없음')
    isDrawing = false
    return
  }

  if (chartInstance.value) {
    try {
      chartInstance.value.destroy()
      chartInstance.value = null
      await new Promise(resolve => setTimeout(resolve, 30))
    } catch (e) {
      console.error('🧨 Chart destroy 실패:', e)
      isDrawing = false
      return
    }
  }

  try {
    chartInstance.value = new Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: `${metalType.value === 'gold' ? '금' : '은'} 가격`,
          data: prices,
          borderColor: metalType.value === 'gold' ? 'gold' : 'silver',
          borderWidth: 2,
          pointBackgroundColor: (_, idx) =>
            idx === prices.indexOf(Math.max(...prices)) ? 'red' :
            idx === prices.indexOf(Math.min(...prices)) ? 'blue' :
            metalType.value === 'gold' ? 'gold' : 'gray',
          tension: 0.3
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: ctx => `₩${ctx.parsed.y}`
            }
          }
        },
        scales: {
          y: { title: { display: true, text: '가격 (₩)' } },
          x: {
            title: { display: true, text: '날짜' },
            ticks: { maxTicksLimit: 5, autoSkip: true }
          }
        }
      }
    })
  } catch (e) {
    console.error('❌ Chart 생성 실패:', e)
  }

  isDrawing = false
}

watch([metalType, startDate, endDate], async () => {
  chartKey.value += 1
  await drawChart()
})

onMounted(async () => {
  await loadJson()
  await drawChart()
})
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 400px;
  position: relative;
}
canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>
