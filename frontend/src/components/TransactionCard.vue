<template>
  <div class="flex justify-between items-center p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
    <div>
      <div class="font-medium">{{ transaction.MERCNAME.trim() }}</div>
      <div class="text-sm text-gray-500">{{ formatDate(transaction.OCCTIME) }}</div>
      <div class="text-xs text-gray-400 mt-1">{{ story }}</div>
    </div>
    <div class="text-lg font-semibold text-gray-900">
      ¥{{ Math.abs(parseFloat(transaction.TRANAMT)).toFixed(2) }}
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
</script> 