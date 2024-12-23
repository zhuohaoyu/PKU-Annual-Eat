<template>
  <div class="max-w-4xl mx-auto p-4 space-y-5">
    <!-- Header Section - More prominent and shareable -->
    <div class="bg-gradient-to-br from-white to-blue-50/30 rounded-2xl p-8 text-center border border-blue-100/50 shadow-sm">
      <h1 class="text-3xl sm:text-4xl font-bold bg-gradient-to-r from-blue-900 via-blue-700 to-blue-800 bg-clip-text text-transparent">
        百鲸大学食堂消费年度报告
      </h1>
      <p class="text-gray-600 mt-3 text-base">{{ formatDateRange() }}</p>
    </div>

    <!-- Key Metrics Grid - More visual impact -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
      <!-- Total Spending -->
      <div class="bg-gradient-to-br from-white to-blue-50/30 rounded-2xl p-6 border border-blue-100/50">
        <div class="flex items-center gap-4">
          <div class="p-3 bg-blue-100/50 rounded-xl">
            <span class="text-2xl">💰</span>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500">年度总消费</p>
            <p class="text-2xl font-bold text-gray-900 mt-1">
              ¥{{ reportData.summary.total_amount.toFixed(1) }}
            </p>
            <div class="flex items-center gap-1.5 mt-2">
              <span class="text-sm text-gray-500">≈</span>
              <span class="text-sm font-medium text-blue-700">
                {{ Math.floor(reportData.summary.total_amount / 15) }}碗拉面
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Transaction Count -->
      <div class="bg-gradient-to-br from-white to-amber-50/30 rounded-2xl p-6 border border-amber-100/50">
        <div class="flex items-center gap-4">
          <div class="p-3 bg-amber-100/50 rounded-xl">
            <span class="text-2xl">🍽️</span>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500">打卡次数</p>
            <p class="text-2xl font-bold text-gray-900 mt-1">
              {{ reportData.summary.total_transactions }}次
            </p>
            <p class="text-sm font-medium text-amber-700 mt-2">
              日均 {{ getAveragePerDay().toFixed(1) }}次
            </p>
          </div>
        </div>
      </div>

      <!-- Average Cost -->
      <div class="bg-gradient-to-br from-white to-emerald-50/30 rounded-2xl p-6 border border-emerald-100/50">
        <div class="flex items-center gap-4">
          <div class="p-3 bg-emerald-100/50 rounded-xl">
            <span class="text-2xl">📊</span>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500">平均消费</p>
            <p class="text-2xl font-bold text-gray-900 mt-1">
              ¥{{ getAveragePerMeal().toFixed(1) }}
            </p>
            <p class="text-sm font-medium text-emerald-700 mt-2">
              每次消费
            </p>
          </div>
        </div>
      </div>

      <!-- Explored Locations -->
      <div class="bg-gradient-to-br from-white to-purple-50/30 rounded-2xl p-6 border border-purple-100/50">
        <div class="flex items-center gap-4">
          <div class="p-3 bg-purple-100/50 rounded-xl">
            <span class="text-2xl">📍</span>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500">探索窗口</p>
            <p class="text-2xl font-bold text-gray-900 mt-1">
              {{ reportData.summary.total_categories }}个
            </p>
            <p class="text-sm font-medium text-purple-700 mt-2">
              {{ getExplorerText() }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Analysis Grid -->
    <div class="grid grid-cols-1 gap-4">
      <!-- Time Distribution and Top Locations Row -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <!-- Time Distribution - Matched height with Top Locations -->
        <div class="bg-white rounded-2xl border border-gray-100/80 overflow-hidden">
          <div class="p-4 border-b border-gray-100">
            <h3 class="text-lg font-bold text-gray-900 flex items-center gap-2">
              <span>📊</span>就餐时间分布
            </h3>
          </div>
          <div class="p-4">
            <div class="h-[340px]">
              <EatingTimeHeatmap :transactions="reportData.transactions" />
            </div>
          </div>
        </div>
        
        <!-- Top Locations - More compact -->
        <div class="bg-gradient-to-br from-white to-purple-50/30 rounded-2xl border border-purple-100/50 overflow-hidden">
          <div class="p-4 border-b border-purple-100/50">
            <h3 class="text-lg font-bold text-gray-900 flex items-center gap-2">
              <span>🏆</span>年度打卡地标
            </h3>
          </div>
          <div class="p-3">
            <div class="grid grid-cols-1 gap-2">
              <div v-for="(location, index) in getTopLocations()" :key="location.name" 
                   class="flex items-center justify-between p-3 bg-white/50 rounded-xl border border-purple-100/30 hover:bg-white/80 transition-colors">
                <div class="flex items-center gap-2 min-w-0">
                  <span class="flex-shrink-0 text-lg">{{ getRankEmoji(index) }}</span>
                  <div class="truncate">
                    <div class="text-sm font-bold text-gray-900 truncate">{{ location.name }}</div>
                    <div class="text-xs text-gray-500 mt-0.5">{{ location.visits }}次光顾</div>
                  </div>
                </div>
                <div class="text-sm font-bold text-purple-700 ml-2">
                  ¥{{ location.amount.toFixed(1) }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Location Distribution (Full Width) -->
      <div class="bg-white rounded-2xl border border-gray-100/80 overflow-hidden">
        <div class="p-5 border-b border-gray-100">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-bold text-gray-900 flex items-center gap-2">
                <span>🗺️</span>就餐地点分布
              </h3>
              <p class="text-sm text-gray-500 mt-1">{{ getLocationText() }}</p>
            </div>
          </div>
        </div>
        <div class="p-4">
          <div class="h-[600px]">
            <LocationAnalysis :transactions="reportData.transactions" />
          </div>
        </div>
      </div>
    </div>

    <!-- Unusual Transactions -->
    <div class="bg-white rounded-2xl border border-gray-100/80 overflow-hidden">
      <div class="p-5 border-b border-gray-100">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-lg font-bold text-gray-900 flex items-center gap-2">
              <span>✨</span>难忘时刻
            </h3>
            <p class="text-sm text-gray-500 mt-1">这些时刻，值得被记住</p>
          </div>
        </div>
      </div>
      <div class="p-4">
        <UnusualTransactions 
          :transactions="reportData.transactions"
          :special-transactions="reportData.special_transactions" 
        />
      </div>
    </div>

    <!-- Footer - More prominent -->
    <div class="text-center space-y-2 py-6">
      <div class="inline-flex items-center gap-2 text-sm bg-gray-50 px-4 py-2 rounded-full">
        <span>✨</span>
        <span class="text-gray-600 font-medium">今年的故事写在这里，明年的精彩还在继续</span>
      </div>
      <p class="text-xs text-gray-400 mt-4">
        <a href="https://scholar.google.com/citations?user=zVYE7-UAAAAJ" 
           target="_blank"
           rel="noopener noreferrer" 
           class="inline-flex items-center gap-1.5 text-gray-400 hover:text-gray-600 transition-colors">
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 24a7 7 0 1 1 0-14 7 7 0 0 1 0 14Zm0-24L0 9.5l4.838 3.94A8 8 0 0 1 12 9a8 8 0 0 1 7.162 4.44L24 9.5 12 0Z"/>
          </svg>
          <span>Google Scholar</span>
        </a>
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import EatingTimeHeatmap from './EatingTimeHeatmap.vue'
import LocationAnalysis from './LocationAnalysis.vue'
import UnusualTransactions from './UnusualTransactions.vue'

const props = defineProps({
  reportData: {
    type: Object,
    required: true
  }
})

// Date utility functions
const dateRange = computed(() => {
  const dates = props.reportData.transactions
    .map(t => new Date(t.OCCTIME))
    .sort((a, b) => a - b)
  
  return {
    start: dates[0],
    end: dates[dates.length - 1],
    // Calculate days between including both start and end dates
    totalDays: Math.ceil((dates[dates.length - 1] - dates[0]) / (1000 * 60 * 60 * 24)) + 1
  }
})

// Formatting functions
const formatDateRange = () => {
  const { start, end } = dateRange.value
  return `${start.getFullYear()}年${start.getMonth() + 1}月 - ${end.getFullYear()}年${end.getMonth() + 1}月`
}

// Analysis functions with improved calculations
const getAveragePerDay = () => {
  const totalTransactions = props.reportData.summary.total_transactions
  return totalTransactions / dateRange.value.totalDays
}

const getAveragePerMeal = () => {
  const totalAmount = props.reportData.summary.total_amount
  const totalTransactions = props.reportData.summary.total_transactions
  return totalAmount / totalTransactions
}

// Update header text to show correct year
const reportYear = computed(() => dateRange.value.end.getFullYear())

// Analysis functions
const getExplorerText = () => {
  const count = props.reportData.summary.total_categories
  if (count >= 20) return "探索达人 🏆"
  if (count >= 15) return "美食家 🌟"
  if (count >= 10) return "初级探索者 🎯"
  return "��续探索"
}

const getTimeHabitText = () => {
  const transactions = props.reportData.transactions
  const morningCount = transactions.filter(t => new Date(t.OCCTIME).getHours() < 10).length
  const eveningCount = transactions.filter(t => new Date(t.OCCTIME).getHours() >= 18).length
  
  if (morningCount > eveningCount) return "早起是你的标签"
  if (eveningCount > morningCount) return "夜生活爱好者"
  return "作息规律的食客"
}

const getLocationText = () => {
  const locations = getTopLocations()
  const favoritePlace = locations[0]?.name
  return favoritePlace ? `${favoritePlace}是你最爱的去处` : "遍览校园美食"
}

// Location analysis
const getTopLocations = () => {
  const locationStats = {}
  
  props.reportData.transactions.forEach(trans => {
    if (trans.TRANAMT >= 0) return
    
    const location = trans.MERCNAME.trim()
    if (!locationStats[location]) {
      locationStats[location] = {
        name: location,
        amount: 0,
        visits: 0
      }
    }
    locationStats[location].amount += Math.abs(parseFloat(trans.TRANAMT))
    locationStats[location].visits++
  })

  return Object.values(locationStats)
    .sort((a, b) => b.amount - a.amount)
    .slice(0, 5)
}

const getRankEmoji = (index) => {
  const emojis = ['🥇', '🥈', '🥉', '✨', '🌟']
  return emojis[index]
}
</script> 