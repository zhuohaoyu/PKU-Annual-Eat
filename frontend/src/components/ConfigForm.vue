<template>
  <div class="min-h-screen flex items-center justify-center px-4">
    <div class="max-w-md w-full space-y-6 bg-white p-6 sm:p-8 rounded-lg shadow-lg">
      <div>
        <h2 class="text-center text-3xl font-extrabold text-gray-900">
          百鲸大学食堂年度总结
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          输入你的账号信息，获取专属消费报告
        </p>
      </div>
      
      <!-- Security Notice -->
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-blue-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-blue-800">隐私说明</h3>
            <div class="mt-2 text-xs text-blue-700 space-y-1">
              <p>• 我们不会存储任何用户凭据</p>
              <p>• 本项目完全开源，可以在 <a href="https://github.com/zhuohaoyu/PKU-Annual-Eat" target="_blank" class="font-medium underline">GitHub</a> 查看源码</p>
              <p>• 如果担心安全问题，欢迎自行部署使用</p>
            </div>
          </div>
        </div>
      </div>
      
      <form class="space-y-6" @submit.prevent="submitForm">
        <div class="rounded-md space-y-4">
          <div>
            <label for="account" class="block text-sm font-medium text-gray-700">账号</label>
            <input
              id="account"
              v-model="formData.account"
              type="text"
              required
              class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="请输入账号"
            >
          </div>
          
          <div>
            <label for="hallticket" class="block text-sm font-medium text-gray-700">Hallticket</label>
            <input
              id="hallticket"
              v-model="formData.hallticket"
              type="text"
              required
              class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="请输入hallticket"
            >
          </div>

          <div>
            <label for="year" class="block text-sm font-medium text-gray-700">选择年份</label>
            <select
              id="year"
              v-model="formData.year"
              required
              class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            >
              <option v-for="year in availableYears" :key="year" :value="year">
                {{ year }}年
              </option>
            </select>
          </div>
        </div>

        <div>
          <button
            type="submit"
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            :disabled="loading"
          >
            <span v-if="loading" class="absolute left-0 inset-y-0 flex items-center pl-3">
              <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            {{ loading ? '生成中...' : '生成我的年度总结' }}
          </button>
        </div>
      </form>

      <!-- Instructions -->
      <div class="bg-gray-50 rounded-lg p-4 text-sm text-gray-600">
        <p class="font-medium text-gray-700 mb-2">如何获取账号和 Hallticket？</p>
        <p class="mb-2 text-xs">详细教程请参考：<a href="https://github.com/KingRayCao/PKU-Annual-Eat#使用方法" target="_blank" class="text-indigo-600 hover:text-indigo-800 font-medium">使用教程</a></p>
        <div class="space-y-2 text-xs">
          <p class="font-medium text-gray-700">简要步骤：</p>
          <ol class="list-decimal list-inside space-y-1">
            <li>登录<a href="https://card.pku.edu.cn/user/user" target="_blank" class="text-indigo-600 hover:text-indigo-800 mx-1">校园卡网站</a></li>
            <li>点击"账号管理"获取账号</li>
            <li>按 F12 打开开发者工具，切换到 Network 标签页</li>
            <li>刷新页面 (Ctrl+R)</li>
            <li>找到 GetCardInfoByAccountNoParm 请求</li>
            <li>在 Cookies 中找到 hallticket 的值</li>
          </ol>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      formData: {
        account: '',
        hallticket: '',
        year: new Date().getFullYear()
      },
      loading: false
    }
  },
  computed: {
    availableYears() {
      const currentYear = new Date().getFullYear()
      return [currentYear - 1, currentYear]
    }
  },
  methods: {
    async submitForm() {
      this.loading = true
      try {
        const year = this.formData.year
        const startDate = `${year}-01-01`
        const endDate = year === new Date().getFullYear() 
          ? new Date().toISOString().split('T')[0]  // Current date for current year
          : `${year}-12-31`  // End of year for past years

        const response = await fetch('/api/report', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({
            account: this.formData.account,
            hallticket: this.formData.hallticket,
            sdate: startDate,
            edate: endDate
          })
        })
        const data = await response.json()
        if (response.ok) {
          this.$emit('report-generated', data)
        } else {
          alert('获取数据失败：' + data.error)
        }
      } catch (error) {
        alert('发生错误：' + error.message)
      } finally {
        this.loading = false
      }
    }
  }
}
</script> 