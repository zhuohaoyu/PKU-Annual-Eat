<template>
  <div class="flex justify-between items-center p-4 bg-white border border-gray-100 
              rounded-lg hover:border-gray-200 transition-colors">
    <div class="min-w-0">
      <div class="font-medium text-gray-900 truncate">{{ transaction.MERCNAME.trim() }}</div>
      <div class="text-sm text-gray-500 mt-0.5">{{ formatDate(transaction.OCCTIME) }}</div>
      <div class="text-xs text-gray-400 mt-1.5 line-clamp-2">{{ story }}</div>
    </div>
    <div class="flex flex-col items-end ml-4">
      <div class="text-lg font-semibold text-gray-900">
        ¥{{ Math.abs(parseFloat(transaction.TRANAMT)).toFixed(2) }}
      </div>
      <div class="text-xs text-gray-500 mt-1">
        {{ getTimeOfDay(transaction.OCCTIME) }}
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  transaction: {
    type: Object,
    required: true
  },
  story: {
    type: String,
    required: true
  }
})

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getTimeOfDay = (dateStr) => {
  const date = new Date(dateStr)
  const hours = date.getHours()
  if (hours < 12) {
    return '上午'
  } else if (hours < 18) {
    return '下午'
  } else {
    return '晚上'
  }
}
</script> 