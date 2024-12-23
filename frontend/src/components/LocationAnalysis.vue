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
  },
  chartType: {
    type: String,
    default: 'sunburst'
  }
})

const chartContainer = ref(null)
let chart = null

// Updated location groups and colors
const LOCATION_GROUPS = [
  '燕南', '家园', '农园', '新勺园', '成府园', '医学部', '松林', 
  '佟园', '学一', '学五', '德园', '跃二', '馨园', '快乐食间'
]

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
  '跃二': '#0ea5e9',    // Dimmed sky blue
  '馨园': '#d946ef',    // Dimmed pink-purple
  '快乐食间': '#06b6d4', // Dimmed cyan
  '其他': '#94a3b8'     // Dimmed gray
}

const processData = (transactions) => {
  const locationStats = {}
  
  transactions.forEach(trans => {
    if (trans.TRANAMT >= 0) return
    
    const location = trans.MERCNAME.trim()
    let group = '其他'
    
    for (const prefix of LOCATION_GROUPS) {
      if (location.includes(prefix)) {
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

const createSunburstVisualization = () => {
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
      }
    },
    series: [{
      type: 'sunburst',
      data: [data],
      radius: ['20%', '90%'],
      itemStyle: {
        borderWidth: 2,
        borderColor: '#ffffff'
      },
      label: {
        rotate: 'tangential',
        minAngle: 15,
        fontSize: 11,
        color: '#ffffff',
        fontWeight: 500
      },
      levels: [
        {},
        {
          r0: '20%',
          r: '45%',
          label: { rotate: 'tangential' }
        },
        {
          r0: '45%',
          r: '90%',
          label: { rotate: 'tangential' }
        }
      ]
    }]
  }

  if (chart) chart.dispose()
  chart = echarts.init(chartContainer.value)
  chart.setOption(option)
}

const createBarVisualization = () => {
  if (!chartContainer.value) return
  
  // Process data for bar chart - no filtering, just amount aggregation
  const locationStats = []
  props.transactions.forEach(trans => {
    if (trans.TRANAMT >= 0) return  // Only keep consumption records
    
    const location = trans.MERCNAME.trim()
    locationStats.push({
      name: location,
      amount: Math.abs(parseFloat(trans.TRANAMT))
    })
  })

  // Aggregate by exact location name
  const aggregatedStats = locationStats.reduce((acc, curr) => {
    if (!acc[curr.name]) {
      acc[curr.name] = {
        name: curr.name,
        amount: 0,
        visits: 0
      }
    }
    acc[curr.name].amount += curr.amount
    acc[curr.name].visits++
    return acc
  }, {})

  // Sort by amount (ascending)
  const sortedData = Object.values(aggregatedStats)
    .sort((a, b) => a.amount - b.amount)

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: (params) => {
        const data = params[0]
        const stats = sortedData[params.dataIndex]
        return `${data.name}<br/>
                消费 <span class="font-medium">¥${data.value.toFixed(1)}</span><br/>
                共计 <span class="font-medium">${stats.visits}次</span>`
      }
    },
    grid: {
      left: '20%',      // Reduced from 25% to 20%
      right: '5%',      // Reduced from 8% to 5%
      bottom: '3%',
      top: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      axisLabel: {
        color: '#64748b',
        formatter: (value) => `¥${value.toFixed(0)}`,
        fontSize: 11
      },
      splitLine: {
        show: true,
        lineStyle: {
          color: '#e2e8f0',
          type: 'dashed'
        }
      }
    },
    yAxis: {
      type: 'category',
      data: sortedData.map(item => item.name),
      axisLabel: {
        color: '#64748b',
        fontSize: 11,
        width: 150,       // Reduced from 180 to 150
        overflow: 'break',
        interval: 0,
        align: 'right',
        padding: [0, 4, 0, 0], // Reduced padding from 8 to 4
        lineHeight: 12,
        formatter: (value) => {
          // Format long names to multiple lines with shorter segments
          if (value.length > 10) {  // Reduced from 12 to 10 characters per line
            const parts = value.match(/.{1,10}/g)
            return parts.join('\n')
          }
          return value
        }
      },
      axisTick: {
        show: false
      },
      axisLine: {
        show: true,
        lineStyle: {
          color: '#e2e8f0'
        }
      }
    },
    series: [{
      name: '消费金额',
      type: 'bar',
      data: sortedData.map(item => item.amount),
      barWidth: '70%',    // Increased from 60% to 70%
      itemStyle: {
        color: '#60a5fa',
        borderRadius: 2
      },
      label: {
        show: true,
        position: 'right',
        formatter: (params) => `¥${params.value.toFixed(1)}`,
        fontSize: 11,
        color: '#64748b',
        distance: 3,      // Reduced from 5 to 3
        padding: [0, 0, 0, 2]  // Reduced padding
      }
    }]
  }

  if (chart) chart.dispose()
  chart = echarts.init(chartContainer.value)
  chart.setOption(option)
}

// Update the visualization creation logic
const createVisualization = () => {
  if (props.chartType === 'bar') {
    createBarVisualization()
  } else {
    createSunburstVisualization()
  }
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
watch(() => props.chartType, createVisualization)
</script> 