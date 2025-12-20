<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { formatNumber } from '~/utils/formatNumber'
import 'swiper/css'

const props = defineProps({
  houses: {
    type: Array,
    required: true,
  },
  title: {
    type: String,
    default: 'Деревянные дома',
  },
  initialHouseId: {
    type: Number,
    default: undefined,
  },
})

const selectHouseIndex = ref(0)
const selectedHouse = computed(() => props.houses[selectHouseIndex.value])

// Функция для установки индекса на основе houseId
const setHouseIndex = (houseId) => {
  if (houseId) {
    const index = props.houses.findIndex((house) => house.id === houseId)
    if (index !== -1) {
      selectHouseIndex.value = index
    }
  }
}

// Устанавливаем начальный индекс при монтировании или изменении prop
onMounted(() => {
  if (props.initialHouseId) {
    setHouseIndex(props.initialHouseId)
  }
})

watch(() => props.initialHouseId, (newId) => {
  if (newId) {
    setHouseIndex(newId)
  }
})

const swiperBreakpoints = {
  0: {
    slidesPerView: 2,
    spaceBetween: 12,
  },
  640: {
    slidesPerView: 2,
    spaceBetween: 14,
  },
  1024: {
    slidesPerView: 2,
    spaceBetween: 16,
  },
}

const decSelectHouseIndex = () => {
  if (selectHouseIndex.value > 0) {
    selectHouseIndex.value--
  } else {
    selectHouseIndex.value = props.houses.length - 1
  }
}

const addSelectHouseIndex = () => {
  if (selectHouseIndex.value === props.houses.length - 1) {
    selectHouseIndex.value = 0
  } else {
    selectHouseIndex.value++
  }
}
</script>

<template>
  <section class="house_typ" style="padding-top: 63px" data-section="wooden">
    <div class="container">
      <div class="row">
        <div class="col-12 col-sm-6">
          <div class="d-flex justify-content-between align-items-center">
            <h4 class="section_name">{{ title }}</h4>
            <div class="d-flex container_icon align-items-center gap-2">
              <div class="circle-left" @click="decSelectHouseIndex"></div>
              <div style="display: flex; flex-direction: column; align-items: center; gap: 0.5rem">
                <p class="house__name">{{ selectedHouse?.name }}</p>
                <div class="d-flex gap-2">
                  <div
                    v-for="(house, index) in houses"
                    :key="house.id"
                    class="house_point"
                    :class="{ active: index === selectHouseIndex }"
                    @click="selectHouseIndex = index"
                  ></div>
                </div>
              </div>
              <div class="circle-right" @click="addSelectHouseIndex"></div>
            </div>
          </div>
        </div>
      </div>

      <div class="card_house__wrapper">
        <div v-for="(house, index) in houses" :key="house.id">
          <Transition name="fade" mode="out-in">
            <div v-show="selectHouseIndex === index" class="card_house">
              <div class="row">
                <!-- Фотографии слева -->
                <div class="col-12 col-sm-6">
                  <div class="row">
                    <div class="col-12">
                      <div
                        class="house__image"
                        :style="{ backgroundImage: `url(${house.img})` }"
                      ></div>
                    </div>
                  </div>
                  <div class="row row_swiper">
                    <div class="col-12 swiper__wrapper" style="position: relative">
                      <Swiper
                        class="house-swiper"
                        :slides-per-view="2"
                        :space-between="16"
                        :breakpoints="swiperBreakpoints"
                      >
                        <SwiperSlide
                          v-for="(card, cardIndex) in house.photo_gallery_set"
                          :key="cardIndex"
                        >
                          <div class="photogalery__card">
                            <div
                              class="photogalery__image"
                              :style="{ backgroundImage: `url(${card.img})` }"
                            ></div>
                            <div class="photogalery__name">{{ card.name }}</div>
                          </div>
                        </SwiperSlide>
                      </Swiper>
                    </div>
                  </div>
                </div>

                <!-- Информация справа -->
                <div class="col-12 col-sm-6">
                  <div class="row d-none d-sm-flex" style="margin-bottom: 64px">
                    <div class="col-12">
                      <div class="house__name_description">Стоимость</div>
                      <div
                        v-for="(cost, costIndex) in house.price_set"
                        :key="costIndex"
                        class="row_cost"
                      >
                        <div class="house__text_description">{{ cost.name }}</div>
                        <div class="house__text_description">
                          {{ formatNumber(cost.cost) + ' р.' }}
                        </div>
                      </div>
                      <div
                        v-for="(cost, costIndex) in house.special_price_set"
                        :key="`special-${costIndex}`"
                        class="row_cost"
                      >
                        <div class="house__text_description">{{ cost.name }}</div>
                        <div class="house__text_description">
                          {{ formatNumber(cost.cost) + ' р.' }}
                        </div>
                      </div>
                    </div>
                  </div>

                  <div class="row" style="margin-bottom: 31px">
                    <div class="col-6">
                      <div class="house__name_description">Описание</div>
                      <div class="house__text_description">{{ house.description }}</div>
                    </div>
                    <div class="col-6">
                      <div class="house__name_description">Доступность</div>
                      <div class="house__text_description">
                        <p
                          v-for="(availability, availIndex) in house.availability_set"
                          :key="availIndex"
                        >
                          {{ availability.name }}
                        </p>
                      </div>
                    </div>
                  </div>

                  <div class="row">
                    <div class="col-6">
                      <div class="house__name_description">Удобства</div>
                      <div class="house__text_description">{{ house.conveniences }}</div>
                    </div>
                    <div class="col-6">
                      <div class="house__name_description">Включено в проживание</div>
                      <div class="house__text_description">{{ house.include }}</div>
                    </div>
                  </div>

                  <div class="row" style="margin-top: 31px">
                    <div class="col-6">
                      <a :href="'/booking/?room-type=' + house?.travelLineId">
                        <button class="toBooking">забронировать</button>
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </Transition>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.house_point {
  height: 8px;
  width: 8px;
  border-radius: 50%;
  background-color: transparent;
  border: 1px #005d4b solid;
}

.house_point.active {
  background-color: #005d4b;
}

.house_point:hover {
  cursor: pointer;
}

.row_swiper {
  margin-top: 24px;
}

:global(.house-swiper) {
  width: 100%;
}

:global(.house-swiper .swiper-wrapper) {
  align-items: stretch;
}

:global(.house-swiper .swiper-slide) {
  height: auto;
  width: auto;
}

.card_house__wrapper {
  position: relative;
  min-height: 770px;
  margin-top: 34px;
}

.card_house {
  position: absolute;
  height: 100%;
  width: 100%;
  top: 0;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 1.2s ease-out;
}

.circle-left {
  width: 55px;
  height: 55px;
  border-radius: 50%;
  background-color: #005d4b;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/></svg>');
  background-repeat: no-repeat;
  background-position: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.circle-left:hover {
  background-color: #fff;
  border: 1px #005d4b solid;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23005d4b"><path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/></svg>');
}

.circle-right {
  width: 55px;
  height: 55px;
  border-radius: 50%;
  background-color: #005d4b;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>');
  background-repeat: no-repeat;
  background-position: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.circle-right:hover {
  background-color: #fff;
  border: 1px #005d4b solid;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23005d4b"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>');
}

.row_cost {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.row_cost:not(:last-child) {
  border-bottom: 1px #005d4b solid;
  padding-bottom: 14px;
}

.row_cost:not(:first-child) {
  padding-top: 14px;
}

.house__text_description {
  color: black;
  font-size: 15px;
  font-family: 'Lato', sans-serif;
  font-weight: 300;
  line-height: 20.33px;
}

.house__name_description {
  color: #003731;
  font-size: 17px;
  font-family: 'Lato', sans-serif;
  font-weight: 400;
  margin-bottom: 10px;
}

.photogalery__image {
  border-radius: 30px;
  width: 100%;
  height: 200px;
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
}

.photogalery__name {
  color: #032d28;
  font-size: 11px;
  font-family: 'Lato', sans-serif;
  font-weight: 400;
  display: flex;
  justify-content: center;
  padding: 19px 0px;
}

.photogalery__card {
  background-color: #fff;
  border-radius: 30px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.house__image {
  border-radius: 30px;
  width: 100%;
  height: 354px;
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
}

.house__name {
  width: 160px;
  display: flex;
  justify-content: center;
  color: #003731;
  font-size: 17px;
  font-family: 'Lato', sans-serif;
  font-weight: 400;
  margin-bottom: 0px;
}

.section_name {
  color: #003c30;
  font-size: 47px;
  font-family: 'Apoc Normal', serif;
  font-weight: 300;
}

.house_typ {
  background-color: #f5f3f1;
}

button.toBooking {
  background-color: rgba(0, 93, 75, 1);
  color: #fff;
  border: 0px;
  padding-left: 15px;
  padding-right: 15px;
  border-radius: 35px;
  cursor: pointer;
}

/* Bootstrap-подобные классы */
.container {
  width: 100%;
  padding-right: 15px;
  padding-left: 15px;
  margin-right: auto;
  margin-left: auto;
}

.row {
  display: flex;
  flex-wrap: wrap;
  margin-right: -15px;
  margin-left: -15px;
}

.col-12 {
  flex: 0 0 100%;
  max-width: 100%;
  padding-right: 15px;
  padding-left: 15px;
}

.col-6 {
  flex: 0 0 50%;
  max-width: 50%;
  padding-right: 15px;
  padding-left: 15px;
}

.d-flex {
  display: flex;
}

.justify-content-between {
  justify-content: space-between;
}

.align-items-center {
  align-items: center;
}

.gap-2 {
  gap: 0.5rem;
}

.d-none {
  display: none;
}

@media (min-width: 576px) {
  .col-sm-6 {
    flex: 0 0 50%;
    max-width: 50%;
  }

  .d-sm-flex {
    display: flex;
  }
}

@media (max-width: 1200px) {
  .section_name {
    font-size: 25px;
  }

  .circle-left {
    width: 35px;
    height: 35px;
  }

  .circle-right {
    width: 35px;
    height: 35px;
  }

  .house__image {
    width: 100%;
    height: 200px;
  }

  .photogalery__image {
    height: 130px;
  }

  .row_swiper {
    margin-top: 10px;
  }

  .photogalery__name {
    padding: 5px 0px;
  }

  .house__text_description {
    font-size: 12px;
    line-height: 15px;
  }

  .house__text_description p {
    margin-bottom: 0;
  }

  .house__name_description {
    margin-bottom: 0px;
    font-size: 15px;
  }
}
</style>

