<template>
  <div class="grid gap-6">
    <!-- Early Birds -->
    <div v-if="earlyBirds.length > 0">
      <h4 class="font-medium text-gray-700 mb-3 flex items-center gap-2">
        <span>🌅</span> 早起冠军
        <span class="text-sm text-gray-500">早起的年轻人值得表扬</span>
      </h4>
      <div class="space-y-3">
        <TransactionCard 
          v-for="trans in earlyBirds" 
          :key="trans.OCCTIME"
          :transaction="trans"
          :story="'早起的鸟儿有虫吃，早起的学生...有包子吃！'"
        />
      </div>
    </div>

    <!-- Night Owls -->
    <div v-if="nightOwls.length > 0">
      <h4 class="font-medium text-gray-700 mb-3 flex items-center gap-2">
        <span>🌙</span> 夜宵达人
        <span class="text-sm text-gray-500">夜生活才刚刚开始</span>
      </h4>
      <div class="space-y-3">
        <TransactionCard 
          v-for="trans in nightOwls" 
          :key="trans.OCCTIME"
          :transaction="trans"
          :story="'夜宵是一天中最快乐的解压方式'"
        />
      </div>
    </div>

    <!-- Big Spenders -->
    <div v-if="bigSpenders.length > 0">
      <h4 class="font-medium text-gray-700 mb-3 flex items-center gap-2">
        <span>💸</span> 大手笔
        <span class="text-sm text-gray-500">这顿吃得很豪横</span>
      </h4>
      <div class="space-y-3">
        <TransactionCard 
          v-for="trans in bigSpenders" 
          :key="trans.OCCTIME"
          :transaction="trans"
          :story="getBigSpenderStory(trans)"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import TransactionCard from './TransactionCard.vue'

const props = defineProps({
  transactions: {
    type: Array,
    required: true
  },
  specialTransactions: {
    type: Object,
    default: () => ({
      early_birds: [],
      night_owls: [],
      big_spenders: []
    })
  }
})

const earlyBirds = computed(() => props.specialTransactions?.early_birds || [])
const nightOwls = computed(() => props.specialTransactions?.night_owls || [])
const bigSpenders = computed(() => props.specialTransactions?.big_spenders || [])

const getBigSpenderStory = (trans) => {
  const amount = Math.abs(parseFloat(trans.TRANAMT))
  return `相当于${Math.floor(amount/15)}碗兰州拉面的战斗力`
}
</script> 