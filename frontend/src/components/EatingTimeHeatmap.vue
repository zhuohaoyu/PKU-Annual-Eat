<template>
  <div class="h-full" ref="heatmapContainer"></div>
</template>

<script>
import * as echarts from 'echarts'
import { onMounted, onUnmounted, ref, watch } from 'vue'

export default {
  props: {
    transactions: {
      type: Array,
      required: true
    }
  },
  setup(props) {
    const heatmapContainer = ref(null)
    let chart = null

    const createTimeSlots = () => {
      const slots = []
      for (let hour = 6; hour < 22; hour++) {
        slots.push(`${hour.toString().padStart(2, '0')}:00`)
        slots.push(`${hour.toString().padStart(2, '0')}:30`)
      }
      return slots
    }

    const analyzeTransactions = (transactions) => {
      // Create a 32 (time slots) x 12 (months) matrix - now 2 slots per hour
      const frequencyMatrix = Array(32).fill().map(() => Array(12).fill(0))
      
      transactions.forEach(trans => {
        if (trans.TRANAMT >= 0) return
        
        const date = new Date(trans.OCCTIME)
        const hour = date.getHours()
        const minutes = date.getMinutes()
        const month = date.getMonth()

        // Only consider transactions between 6:00 and 22:00
        if (hour < 6 || hour >= 22) return
        
        // Calculate time slot index (2 slots per hour)
        const timeSlotIndex = (hour - 6) * 2 + Math.floor(minutes / 30)
        frequencyMatrix[timeSlotIndex][month]++
      })

      // Convert matrix to visualization data
      const visualData = []
      const allFrequencies = []

      frequencyMatrix.forEach((row, timeIndex) => {
        row.forEach((value, monthIndex) => {
          if (value > 0) allFrequencies.push(value)
          visualData.push([monthIndex, timeIndex, value])
        })
      })

      return {
        data: visualData,
        maxFrequency: Math.max(...allFrequencies),
        frequencies: allFrequencies.sort((a, b) => a - b)
      }
    }

    const createVisualization = () => {
      if (!heatmapContainer.value) return

      const { data, maxFrequency, frequencies } = analyzeTransactions(props.transactions)
      
      const getPercentileValue = (percentile) => {
        const index = Math.floor(frequencies.length * percentile)
        return frequencies[index] || 0
      }

      const option = {
        tooltip: {
          position: 'top',
          formatter: function (params) {
            const hour = Math.floor(params.value[1] / 2) + 6
            const minute = params.value[1] % 2 === 0 ? '00' : '30'
            return `${hour}:${minute} ${params.value[0] + 1}月<br/>
                   就餐次数: ${params.value[2]}次`
          },
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          borderWidth: 1,
          borderColor: '#e2e8f0',
          padding: 10,
          textStyle: {
            color: '#334155',
            fontSize: 14
          }
        },
        grid: {
          top: '10%',
          left: '8%',
          right: '5%',
          bottom: '25%'  // Increased bottom margin for visualMap
        },
        xAxis: {
          type: 'category',
          data: Array.from({length: 12}, (_, i) => `${i + 1}月`),
          splitArea: { show: true },
          axisLine: { lineStyle: { color: '#cbd5e1' } },
          axisTick: { show: false },
          axisLabel: {
            fontSize: 12,
            margin: 12
          }
        },
        yAxis: {
          type: 'category',
          data: createTimeSlots(),
          splitArea: { show: true },
          axisLine: { lineStyle: { color: '#cbd5e1' } },
          axisTick: { show: false },
          axisLabel: {
            fontSize: 12,
            margin: 12,
            formatter: (value) => {
              return value.endsWith(':00') ? value : ''  // Only show labels for full hours
            }
          }
        },
        visualMap: {
          min: 0,
          max: maxFrequency,
          calculable: true,
          orient: 'horizontal',
          left: 'center',
          bottom: '5%',
          itemWidth: 15,
          itemHeight: 120,
          text: ['高', '低'],
          dimension: 2,
          precision: 0,
          textStyle: { 
            color: '#475569',
            fontSize: 12
          },
          inRange: {
            color: [
              '#ffffff',
              '#93c5fd',
              '#3b82f6',
              '#1d4ed8',
              '#1e3a8a'
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
              return params.value[2] > getPercentileValue(0.4) ? '#fff' : '#1e3a8a'
            }
          },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(14, 165, 233, 0.3)'
            }
          }
        }]
      }

      if (chart) {
        chart.dispose()
      }

      chart = echarts.init(heatmapContainer.value)
      chart.setOption(option)
    }

    // Handle window resize
    const handleResize = () => {
      if (chart) {
        chart.resize()
      }
    }

    onMounted(() => {
      window.addEventListener('resize', handleResize)
      createVisualization()
    })

    onUnmounted(() => {
      window.removeEventListener('resize', handleResize)
      if (chart) {
        chart.dispose()
      }
    })

    watch(() => props.transactions, () => {
      createVisualization()
    }, { deep: true })

    return {
      heatmapContainer
    }
  }
}
</script> 