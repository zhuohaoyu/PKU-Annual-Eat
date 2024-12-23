<template>
  <div class="h-full" ref="chartContainer"></div>
</template>

<script>
import * as echarts from 'echarts'
import { onMounted, ref, watch } from 'vue'

export default {
  props: {
    transactions: {
      type: Array,
      required: true
    }
  },
  setup(props) {
    const chartContainer = ref(null)
    let chart = null

    const LOCATION_GROUPS = ['燕南', '家园', '农园', '勺园', '成府园', '医学部', '松林', '佟园', '学一', '学五']
    const GROUP_COLORS = {
      '燕南': '#E6B8AF',
      '家园': '#B6D7A8',
      '农园': '#9FC5E8',
      '勺园': '#D5A6BD',
      '成府园': '#FFD966',
      '医学部': '#A2C4C9',
      '松林': '#B4A7D6',
      '佟园': '#E6B89C',
      '学一': '#F9CB9C',
      '学五': '#A4C2F4',
      '其他': '#D9D9D9'
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
              color: GROUP_COLORS[group]
            }
          }
        }
        
        if (!locationStats[group].children[location]) {
          locationStats[group].children[location] = {
            name: location,
            value: 0,
            amount: 0,
            itemStyle: {
              color: GROUP_COLORS[group]
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

    const initChart = () => {
      const data = processData(props.transactions)
      
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: (params) => {
            const value = params.data.value
            const amount = params.data.amount
            if (amount !== undefined) {
              return `${params.name}<br/>
                     <span style="display:inline-block;margin-right:4px">就餐次数:</span>${value}次<br/>
                     <span style="display:inline-block;margin-right:4px">消费金额:</span>¥${amount.toFixed(1)}`
            }
            return `${params.name}<br/>就餐次数: ${value}次`
          },
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          borderWidth: 1,
          borderColor: '#e2e8f0',
          padding: [6, 8],
          textStyle: {
            fontSize: 11,
            lineHeight: 16
          }
        },
        series: {
          type: 'sunburst',
          data: [data],
          radius: ['15%', '90%'],
          center: ['50%', '50%'],
          itemStyle: {
            borderRadius: 5,
            borderWidth: 1.5,
            borderColor: '#fff'
          },
          label: {
            rotate: 'tangential',
            minAngle: 12,
            fontSize: 9,
            lineHeight: 12,
            color: '#1f2937'
          },
          levels: [
            {},
            {
              r0: '15%',
              r: '40%',
              itemStyle: {
                borderWidth: 1.5
              },
              label: {
                rotate: 'tangential',
                fontSize: 10,
                fontWeight: 500,
                padding: 3,
                color: '#1f2937'
              }
            },
            {
              r0: '40%',
              r: '90%',
              label: {
                align: 'right',
                fontSize: 9,
                padding: 2,
                color: '#374151'
              }
            }
          ]
        }
      }

      chart = echarts.init(chartContainer.value)
      chart.setOption(option)
      
      window.addEventListener('resize', () => {
        chart.resize()
      })
    }

    onMounted(() => {
      initChart()
    })

    watch(() => props.transactions, () => {
      if (chart) {
        chart.dispose()
      }
      initChart()
    })

    return {
      chartContainer
    }
  }
}
</script> 