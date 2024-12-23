<template>
  <div class="relative h-full" ref="heatmapContainer">
    <!-- Overlay Legend -->
    <div class="absolute top-2 right-2 text-xs text-gray-500 bg-white/90 px-2 py-1 rounded-md shadow-sm border border-gray-100">
      <div class="flex items-center gap-1.5">
        <span class="w-2 h-2 rounded-sm bg-blue-700"></span>高频时段
        <span class="w-2 h-2 rounded-sm bg-blue-300"></span>低频时段
      </div>
    </div>
  </div>
</template>

<script setup>
import * as echarts from 'echarts'
import { onMounted, onUnmounted, ref, watch } from 'vue'

const props = defineProps({
  transactions: {
    type: Array,
    required: true
  }
})

const heatmapContainer = ref(null)
let chart = null

// Create 30-minute time slots
const createTimeSlots = () => {
  const slots = []
  for (let hour = 6; hour < 22; hour++) {
    slots.push(`${hour.toString().padStart(2, '0')}:00`)
    slots.push(`${hour.toString().padStart(2, '0')}:30`)
  }
  return slots
}

const analyzeTransactions = (transactions) => {
  // 32 slots (16 hours * 2 slots per hour)
  const frequencyMatrix = Array(32).fill().map(() => Array(12).fill(0))
  const halfHourlyStats = Array(32).fill(0)
  
  transactions.forEach(trans => {
    if (trans.TRANAMT >= 0) return
    
    const date = new Date(trans.OCCTIME)
    const hour = date.getHours()
    const minutes = date.getMinutes()
    const month = date.getMonth()

    if (hour >= 6 && hour < 22) {
      // Calculate slot index (2 slots per hour)
      const timeSlotIndex = (hour - 6) * 2 + (minutes >= 30 ? 1 : 0)
      frequencyMatrix[timeSlotIndex][month]++
      halfHourlyStats[timeSlotIndex]++
    }
  })

  const peakSlots = halfHourlyStats
    .map((count, index) => ({ 
      time: createTimeSlots()[index], 
      count 
    }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 3)

  return {
    data: frequencyMatrix.flatMap((row, timeIndex) => 
      row.map((value, monthIndex) => [monthIndex, timeIndex, value])
    ),
    peakSlots
  }
}

const createVisualization = () => {
  if (!heatmapContainer.value) return

  const { data, peakSlots } = analyzeTransactions(props.transactions)
  
  const option = {
    grid: {
      top: '8%',
      left: '8%',
      right: '4%',
      bottom: '15%',
      containLabel: true
    },
    tooltip: {
      position: 'top',
      formatter: (params) => {
        const slots = createTimeSlots()
        return `${slots[params.value[1]]} ${params.value[0] + 1}月<br/>
               <span class="font-medium">${params.value[2]}次</span>就餐记录`
      },
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderWidth: 1,
      borderColor: '#e2e8f0',
      padding: [4, 8],
      textStyle: { fontSize: 12 }
    },
    xAxis: {
      type: 'category',
      data: Array.from({length: 12}, (_, i) => `${i + 1}月`),
      splitArea: { show: true },
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        fontSize: 11,
        margin: 8,
        color: '#64748b'
      }
    },
    yAxis: {
      type: 'category',
      data: createTimeSlots(),
      splitArea: { show: true },
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        fontSize: 11,
        margin: 8,
        color: '#64748b',
        formatter: (value) => value.endsWith(':00') ? value.split(':')[0] : ''
      }
    },
    visualMap: {
      min: 0,
      max: Math.max(...data.map(item => item[2])),
      calculable: false,
      orient: 'horizontal',
      left: 'center',
      bottom: '5%',
      itemWidth: 10,
      itemHeight: 80,
      text: ['高', '低'],
      textStyle: { 
        color: '#64748b',
        fontSize: 11
      },
      inRange: {
        // New darker color scheme with white background
        color: [
          '#ffffff',                    // Pure white for zero
          '#e2e8f0',                    // Light gray-blue
          '#bfdbfe',                    // Light blue
          '#60a5fa',                    // Medium blue
          '#3b82f6',                    // Blue
          '#2563eb',                    // Medium dark blue
          '#1d4ed8',                    // Dark blue
          '#1e40af'                     // Darker blue
        ]
      }
    },
    series: [{
      name: '就餐频次',
      type: 'heatmap',
      data: data,
      label: {
        show: true,
        formatter: (params) => params.value[2] || '',
        fontSize: 11,
        fontWeight: 500,
        color: (params) => {
          // Adjusted threshold for better text contrast
          return params.value[2] > 10 ? '#ffffff' : '#1e3a8a'
        }
      },
      itemStyle: {
        borderWidth: 1,
        borderColor: '#ffffff'
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 8,
          shadowColor: 'rgba(37, 99, 235, 0.25)'
        }
      }
    }],
    backgroundColor: '#ffffff'
  }

  if (chart) chart.dispose()
  chart = echarts.init(heatmapContainer.value)
  chart.setOption(option)
}

// Handle window resize
const handleResize = () => {
  if (chart) chart.resize()
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
  createVisualization()
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (chart) chart.dispose()
})

watch(() => props.transactions, createVisualization, { deep: true })
</script> 