<template>
  <div class="space-y-5">
    <!-- Early Birds -->
    <div v-if="earlyBirds.length > 0 && earliestTransaction" 
         class="bg-gradient-to-br from-white to-amber-50/30 rounded-2xl p-6 border border-amber-100/50">
      <div class="flex items-center gap-4 mb-4">
        <div class="p-3 bg-amber-100/50 rounded-xl">
          <span class="text-2xl">🌅</span>
        </div>
        <div class="flex-1">
          <h4 class="text-lg font-bold text-gray-900">早起冠军</h4>
          <div class="flex items-center gap-2 mt-1">
            <span class="text-sm text-gray-500">最早的一笔消费发生在</span>
            <span class="text-sm font-medium text-amber-700">
              {{ formatTime(earliestTransaction?.OCCTIME) }}
            </span>
          </div>
        </div>
      </div>
      
      <div class="grid gap-3">
        <TransactionCard 
          v-for="trans in earlyBirds" 
          :key="trans.OCCTIME"
          :transaction="trans"
          :story="getEarlyBirdStory(trans)"
          :stats="{
            timeComparison: getTimeComparison(trans),
            amountComparison: getAmountComparison(trans),
            streak: getVisitStreak(trans)
          }"
        />
      </div>
    </div>

    <!-- Night Owls -->
    <div v-if="nightOwls.length > 0"
         class="bg-gradient-to-br from-white to-blue-50/30 rounded-2xl p-6 border border-blue-100/50">
      <div class="flex items-center gap-4 mb-4">
        <div class="p-3 bg-blue-100/50 rounded-xl">
          <span class="text-2xl">🌙</span>
        </div>
        <div class="flex-1">
          <h4 class="text-lg font-bold text-gray-900">夜宵达人</h4>
          <div class="flex items-center gap-2 mt-1">
            <span class="text-sm text-gray-500">最晚的一笔消费发生在</span>
            <span class="text-sm font-medium text-blue-700">
              {{ formatTime(latestTransaction?.OCCTIME) }}
            </span>
          </div>
        </div>
      </div>

      <div class="grid gap-3">
        <TransactionCard 
          v-for="trans in nightOwls" 
          :key="trans.OCCTIME"
          :transaction="trans"
          :story="getNightOwlStory(trans)"
          :stats="{
            timeComparison: getTimeComparison(trans),
            amountComparison: getAmountComparison(trans),
            companionCount: getCompanionCount(trans)
          }"
        />
      </div>
    </div>

    <!-- Big Spenders -->
    <div v-if="bigSpenders.length > 0"
         class="bg-gradient-to-br from-white to-emerald-50/30 rounded-2xl p-6 border border-emerald-100/50">
      <div class="flex items-center gap-4 mb-4">
        <div class="p-3 bg-emerald-100/50 rounded-xl">
          <span class="text-2xl">💸</span>
        </div>
        <div class="flex-1">
          <h4 class="text-lg font-bold text-gray-900">大手笔时刻</h4>
        </div>
      </div>

      <div class="grid gap-3">
        <TransactionCard 
          v-for="trans in bigSpenders" 
          :key="trans.OCCTIME"
          :transaction="trans"
          :story="getBigSpenderStory(trans)"
          :stats="{
            amountComparison: getAmountComparison(trans),
            percentile: getAmountPercentile(trans),
            context: getSpendingContext(trans)
          }"
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

// Add a filter function
const filterTransaction = (trans) => {
  if (!trans) return false
  // Filter out water control records
  if (trans.MERCNAME.includes('医学部学生区水控')) {
    return false
  }
  return true
}

// First get all valid transactions, then find earliest/latest
const validTransactions = computed(() => {
  return props.transactions.filter(filterTransaction)
})

// Update the computed properties
const earlyBirds = computed(() => {
  // Get all valid transactions and sort by time of day
  return validTransactions.value
    .filter(trans => trans.TRANAMT < 0)  // Only consumption records
    .sort((a, b) => {
      // Extract hours and minutes for comparison
      const timeA = new Date(a.OCCTIME)
      const timeB = new Date(b.OCCTIME)
      // Convert to minutes since midnight for easy comparison
      const minutesA = timeA.getHours() * 60 + timeA.getMinutes()
      const minutesB = timeB.getHours() * 60 + timeB.getMinutes()
      return minutesA - minutesB  // Sort by time of day
    })
    .slice(0, 3)  // Take top 3 earliest by time of day
})

// Update earliest transaction computation
const earliestTransaction = computed(() => {
  if (!validTransactions.value || validTransactions.value.length === 0) return null
  
  // Find the transaction with earliest time of day
  return validTransactions.value
    .filter(trans => trans.TRANAMT < 0)
    .reduce((earliest, current) => {
      const earliestTime = new Date(earliest.OCCTIME)
      const currentTime = new Date(current.OCCTIME)
      const earliestMinutes = earliestTime.getHours() * 60 + earliestTime.getMinutes()
      const currentMinutes = currentTime.getHours() * 60 + currentTime.getMinutes()
      
      return currentMinutes < earliestMinutes ? current : earliest
    })
})

// Update the night owls computation
const nightOwls = computed(() => {
  // Get all valid transactions and sort by time of day (descending)
  return validTransactions.value
    .filter(trans => trans.TRANAMT < 0)  // Only consumption records
    .sort((a, b) => {
      // Extract hours and minutes for comparison
      const timeA = new Date(a.OCCTIME)
      const timeB = new Date(b.OCCTIME)
      // Convert to minutes since midnight for easy comparison
      const minutesA = timeA.getHours() * 60 + timeA.getMinutes()
      const minutesB = timeB.getHours() * 60 + timeB.getMinutes()
      return minutesB - minutesA  // Sort by time of day descending
    })
    .slice(0, 3)  // Take top 3 latest by time of day
})

// Update latest transaction computation
const latestTransaction = computed(() => {
  if (!validTransactions.value || validTransactions.value.length === 0) return null
  
  // Find the transaction with latest time of day
  return validTransactions.value
    .filter(trans => trans.TRANAMT < 0)
    .reduce((latest, current) => {
      const latestTime = new Date(latest.OCCTIME)
      const currentTime = new Date(current.OCCTIME)
      const latestMinutes = latestTime.getHours() * 60 + latestTime.getMinutes()
      const currentMinutes = currentTime.getHours() * 60 + currentTime.getMinutes()
      
      return currentMinutes > latestMinutes ? current : latest
    })
})

// Get big spenders (keep original logic but with filter)
const bigSpenders = computed(() => {
  const spenders = props.specialTransactions?.big_spenders || []
  return spenders.filter(filterTransaction)
})

// Helper functions for time formatting
const formatTime = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleTimeString('zh-CN', { 
    hour: '2-digit', 
    minute: '2-digit',
    hour12: false 
  })
}

// Story generation functions with variations
const getEarlyBirdStory = (trans) => {
  const hour = new Date(trans.OCCTIME).getHours()
  const stories = [
    `这天${hour}点，你开启了新的一天`,
    `这是一天的第一笔消费`,
    `一天从这里开始`
  ]
  return stories[Math.floor(Math.random() * stories.length)]
}

const getNightOwlStory = (trans) => {
  const hour = new Date(trans.OCCTIME).getHours()
  const stories = [
    `夜深人静的${hour}点，这里还有你的身影`,
    `这个深夜，你和美食相伴`,
    `深夜食堂，总有温暖的故事`
  ]
  return stories[Math.floor(Math.random() * stories.length)]
}

const getBigSpenderStory = (trans) => {
  const amount = Math.abs(parseFloat(trans.TRANAMT))
  const noodles = Math.floor(amount/15)
  return `这顿饭的价格相当于${noodles}碗兰州拉面，想必是和朋友们的欢聚时光`
}

// Statistics calculation functions
const getTimeComparison = (trans) => {
  const hour = new Date(trans.OCCTIME).getHours()
  const avgHour = 12 // You can calculate this from all transactions
  return Math.abs(hour - avgHour)
}

const getAmountComparison = (trans) => {
  const amount = Math.abs(parseFloat(trans.TRANAMT))
  const avgAmount = 15 // You can calculate this from all transactions
  return (amount / avgAmount).toFixed(1)
}

const getMaxSpendingMultiple = () => {
  if (!bigSpenders.value.length) return 0
  const maxAmount = Math.max(...bigSpenders.value.map(t => Math.abs(parseFloat(t.TRANAMT))))
  const avgAmount = 15 // You can calculate this from all transactions
  return (maxAmount / avgAmount).toFixed(1)
}

// Additional context functions
const getVisitStreak = (trans) => {
  // Calculate consecutive days of early visits
  return Math.floor(Math.random() * 5) + 1 // Placeholder
}

const getCompanionCount = (trans) => {
  const amount = Math.abs(parseFloat(trans.TRANAMT))
  return Math.floor(amount / 15) // Estimate based on average meal cost
}

const getAmountPercentile = (trans) => {
  // Calculate spending percentile
  return 95 + Math.floor(Math.random() * 5) // Placeholder
}

const getSpendingContext = (trans) => {
  const date = new Date(trans.OCCTIME)
  const isWeekend = date.getDay() === 0 || date.getDay() === 6
  return isWeekend ? '周末聚餐' : '工作日大餐'
}
</script> 