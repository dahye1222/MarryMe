<template>
  <div>
    <h2 class="text-subtitle-1">📍 지역별 금은방 검색</h2>
    <v-select v-model="selectedProvince" :items="mapInfo.map(r => r.name)" label="광역시/도" class="mb-2" />
    <v-select
      v-model="selectedDistrict"
      :items="filteredDistricts"
      label="시/군/구"
      class="mb-2"
      :disabled="!selectedProvince"
    />
    <v-btn color="primary" @click="searchJewelryStores">금은방 찾기</v-btn>
    <div id="map" style="width: 100%; height: 400px;"></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import mapJson from '@/assets/data.json'

const selectedProvince = ref(null)
const selectedDistrict = ref(null)
const mapInfo = ref(mapJson.mapInfo)

const filteredDistricts = computed(() => {
  const region = mapInfo.value.find(r => r.name === selectedProvince.value)
  return region?.countries || []
})

let kakaoMap = null
const markers = ref([])

function initKakaoMap() {
  const container = document.getElementById('map')
  kakaoMap = new window.kakao.maps.Map(container, {
    center: new window.kakao.maps.LatLng(37.5665, 126.9780),
    level: 5
  })
}

function searchJewelryStores() {
  const keyword = `${selectedProvince.value} ${selectedDistrict.value} 금은방`
  const ps = new kakao.maps.services.Places()

  markers.value.forEach(marker => marker.setMap(null))
  markers.value = []

  let openInfoWindow = null
  const bounds = new kakao.maps.LatLngBounds()

  ps.keywordSearch(keyword, (data, status) => {
    if (status !== kakao.maps.services.Status.OK) {
      alert('검색 결과 없음')
      return
    }

    data.forEach(place => {
      const pos = new kakao.maps.LatLng(place.y, place.x)
      const marker = new kakao.maps.Marker({
        map: kakaoMap,
        position: pos
      })

      const infowindow = new kakao.maps.InfoWindow({
        content: `
          <div style="
            padding: 10px 12px;
            font-size: 13px;
            line-height: 1.6;
            max-width: 300px;
            min-width: 200px;
            min-height: 140px;
            white-space: normal;
            word-break: break-word;
            box-sizing: border-box;
          ">
            <div style="font-weight: bold; margin-bottom: 8px;">${place.place_name}</div>
            <div>📍 ${place.address_name || '주소 정보 없음'}</div>
            <div>📞 ${place.phone || '전화번호 없음'}</div>
            <a href="https://map.naver.com/v5/search/${encodeURIComponent(place.place_name)}"
              target="_blank"
              style="color: #0B84FF; display: inline-block; margin-top: 8px; text-decoration: underline;">
              🔍 네이버 플레이스에서 보기
            </a>
          </div>
        `
      })

      kakao.maps.event.addListener(marker, 'click', () => {
        if (openInfoWindow) openInfoWindow.close()
        infowindow.open(kakaoMap, marker)
        openInfoWindow = infowindow
      })

      markers.value.push(marker)
      bounds.extend(pos)
    })

    kakaoMap.setBounds(bounds)
  })
}

onMounted(async () => {
  if (!window.kakao || !window.kakao.maps) {
    console.log('카카오맵 스크립트 동적 로드 시작')
    await new Promise((resolve, reject) => {
      const script = document.createElement('script')
      script.src = 'https://dapi.kakao.com/v2/maps/sdk.js?appkey=a071a72ee9d1089b0146695f228fdbaa&autoload=false&libraries=services'
      script.onload = () => {
        console.log('카카오맵 스크립트 로드 완료')
        window.kakao.maps.load(resolve)
      }
      script.onerror = (e) => {
        console.error('카카오맵 스크립트 로드 실패', e)
        reject(e)
      }
      document.head.appendChild(script)
    })
  }
  console.log('카카오맵 초기화')
  initKakaoMap()
})
</script>
