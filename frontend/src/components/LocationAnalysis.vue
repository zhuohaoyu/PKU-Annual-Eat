<template>
  <div class="h-full" ref="chartContainer"></div>
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

const chartContainer = ref(null)
let chart = null

// Updated modern color palette
const LOCATION_GROUPS = ['燕南', '家园', '农园', '新勺园', '成府园', '医学部', '松林', '佟园', '学一', '学五', '德园']
const GROUP_COLORS = {
  '燕南': '#60a5fa',    // Dimmed blue
  '家园': '#4ade80',    // Dimmed green
  '农园': '#fbbf24',    // Dimmed yellow
  '新勺园': '#f472b6',  // Dimmed pink
  '成府园': '#f97316',  // Dimmed orange
  '医学部': '#818cf8',  // Dimmed indigo
  '松林': '#a855f7',    // Dimmed purple
  '佟园': '#ec4899',    // Dimmed fuchsia
  '学一': '#14b8a6',    // Dimmed teal
  '学五': '#22c55e',    // Dimmed emerald
  '德园': '#ef4444',    // Dimmed red
  '其他': '#94a3b8'     // Dimmed gray
}

const processData = (transactions) => {
  const locationStats = {}
  
  transactions.forEach(trans => {
    if (trans.TRANAMT >= 0) return
    
    const location = trans.MERCNAME.trim()
    let group = '其他'
    
    for (const prefix of LOCATION_GROUPS) {
      if (location.startsWith(prefix)) {
        group = prefix
        break
      }
    }
    
    if (!locationStats[group]) {
      locationStats[group] = {
        name: group,
        value: 0,
        children: {},
        itemStyle: {
          color: GROUP_COLORS[group],
          borderRadius: 10,
          borderWidth: 2,
          borderColor: '#ffffff'
        }
      }
    }
    
    if (!locationStats[group].children[location]) {
      locationStats[group].children[location] = {
        name: location,
        value: 0,
        amount: 0,
        itemStyle: {
          color: GROUP_COLORS[group],
          borderRadius: 8,
          borderWidth: 2,
          borderColor: '#ffffff'
        }
      }
    }
    
    locationStats[group].children[location].value++
    locationStats[group].children[location].amount += Math.abs(parseFloat(trans.TRANAMT))
    locationStats[group].value++
  })

  return {
    name: '就餐地点',
    children: Object.values(locationStats).map(group => ({
      name: group.name,
      value: group.value,
      itemStyle: group.itemStyle,
      children: Object.values(group.children).map(loc => ({
        name: loc.name,
        value: loc.value,
        amount: loc.amount,
        itemStyle: loc.itemStyle
      }))
    }))
  }
}

const createVisualization = () => {
  if (!chartContainer.value) return

  const data = processData(props.transactions)
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        const value = params.value
        const amount = params.data.amount
        if (amount !== undefined) {
          return `${params.name}<br/>
                 <span class="font-medium">${value}次</span> 消费<br/>
                 共计 <span class="font-medium">¥${amount.toFixed(1)}</span>`
        }
        return `${params.name}<br/>${value}次消费`
      },
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderWidth: 1,
      borderColor: '#e2e8f0',
      padding: [8, 12],
      textStyle: { 
        fontSize: 12,
        color: '#1f2937'
      }
    },
    series: [{
      type: 'sunburst',
      data: [data],
      radius: ['20%', '90%'],
      itemStyle: {
        borderWidth: 2,
        borderColor: '#ffffff',
        opacity: 0.85
      },
      label: {
        rotate: 'tangential',
        minAngle: 15,
        fontSize: 11,
        color: '#ffffff',
        fontWeight: 500,
        textBorderWidth: 2,
        textBorderColor: 'rgba(0, 0, 0, 0.2)'
      },
      emphasis: {
        focus: 'ancestor',
        itemStyle: {
          opacity: 0.95,
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.2)'
        }
      },
      levels: [
        {},
        {
          r0: '20%',
          r: '45%',
          label: {
            rotate: 'tangential',
            fontSize: 12,
            fontWeight: 600
          },
          itemStyle: {
            borderWidth: 2,
            opacity: 0.9
          }
        },
        {
          r0: '45%',
          r: '90%',
          label: {
            rotate: 'tangential',
            fontSize: 11,
            fontWeight: 500
          },
          itemStyle: {
            borderWidth: 1.5,
            opacity: 0.85
          }
        }
      ]
    }]
  }

  if (chart) chart.dispose()
  chart = echarts.init(chartContainer.value)
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