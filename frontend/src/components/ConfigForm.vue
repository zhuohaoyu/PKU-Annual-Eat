<template>
  <div class="min-h-screen flex items-center justify-center px-4">
    <div class="max-w-2xl w-full space-y-6 bg-white p-6 sm:p-8 rounded-2xl shadow-lg">
      <div>
        <h2 class="text-center text-3xl font-extrabold text-gray-900">
          百鲸大学食堂年度总结
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          输入你的账号信息，获取专属消费报告
        </p>
      </div>
      
      <!-- Credentials Guide -->
      <div class="bg-gradient-to-br from-white to-blue-50/30 rounded-xl border border-blue-100/50 p-5 space-y-4">
        <div class="flex items-center gap-3">
          <div class="p-2 bg-blue-100/50 rounded-lg">
            <span class="text-xl">📝</span>
          </div>
          <h3 class="text-lg font-bold text-gray-900">如何获取账号信息</h3>
        </div>

        <!-- Account Instructions -->
        <div class="space-y-2">
          <h4 class="font-medium text-gray-800 flex items-center gap-2">
            <span class="text-sm">1️⃣</span> 获取账号
          </h4>
          <div class="text-sm text-gray-600 space-y-1 ml-6">
            <p>1. 登录<a href="https://card.pku.edu.cn/user/user" target="_blank" class="text-blue-600 hover:text-blue-800 underline">校园卡网站</a></p>
            <p>2. 点击"账户管理"</p>
            <p>3. 在弹出的页面中找到并复制"账号"的值</p>
          </div>
        </div>

        <!-- Hallticket Instructions -->
        <div class="space-y-2">
          <h4 class="font-medium text-gray-800 flex items-center gap-2">
            <span class="text-sm">2️⃣</span> 获取 Hallticket
          </h4>
          <div class="text-sm text-gray-600 space-y-1 ml-6">
            <p>1. 按 F12 打开开发者工具，切换到 Network 标签页</p>
            <p>2. 刷新页面，找到GetCardInfoByAccountNoParm或任意XHR类型的请求</p>
            <p>3. 在 Cookies 选项卡中复制 hallticket 字段的值</p>
          </div>
        </div>

        <!-- Add to the Hallticket Instructions -->
        <div class="space-y-2">
          <h4 class="font-medium text-gray-800 flex items-center gap-2">
            <span class="text-sm">3️⃣</span> 获取 SessionId
          </h4>
          <div class="text-sm text-gray-600 space-y-1 ml-6">
            <p>1. 在同一个请求的 Cookie 中</p>
            <p>2. 找到并复制 ASP.NET_SessionId 的值</p>
          </div>
        </div>

        <!-- Add this after the Hallticket Instructions -->
        <div class="mt-4">
          <!-- Collapsible Header -->
          <button 
            @click="isGuideExpanded = !isGuideExpanded"
            class="w-full bg-blue-50/50 rounded-lg border border-blue-100/50 p-2.5 
                   flex items-center justify-between hover:bg-blue-50/70 transition-colors"
          >
            <div class="flex items-center gap-2">
              <span class="text-sm">💡</span>
              <span class="text-sm font-medium text-gray-700">查看详细获取教程</span>
            </div>
            <svg 
              class="w-4 h-4 text-gray-400 transition-transform duration-200"
              :class="{ 'rotate-180': isGuideExpanded }"
              viewBox="0 0 20 20" 
              fill="currentColor"
            >
              <path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"/>
            </svg>
          </button>

          <!-- Collapsible Content -->
          <div 
            v-show="isGuideExpanded"
            class="mt-3 bg-gradient-to-br from-white to-blue-50/30 rounded-xl border border-blue-100/50 p-5 space-y-6"
          >
            <!-- Chrome Section -->
            <div class="space-y-3">
              <h4 class="font-semibold text-gray-900 flex items-center gap-2 text-lg tracking-tight">
                Chrome 浏览器
              </h4>
              <div class="ml-7 space-y-2.5">
                <div class="text-sm leading-relaxed text-gray-600 space-y-1.5 ml-4 font-normal">
                  <p>1. 在校园卡网站，按 <kbd class="px-1.5 py-0.5 bg-gray-100 rounded text-xs font-mono">F12</kbd> （Mac用户按 <kbd class="px-1.5 py-0.5 bg-gray-100 rounded text-xs font-mono">Command</kbd> + <kbd class="px-1.5 py-0.5 bg-gray-100 rounded text-xs font-mono">Option</kbd> + <kbd class="px-1.5 py-0.5 bg-gray-100 rounded text-xs font-mono">I</kbd>） 打开开发者工具</p>
                  <p>2. 点击顶部的 <span class="font-medium text-gray-700">"Network"</span> 标签</p>
                  <p>3. 刷新页面（Windows 按 <kbd class="px-1.5 py-0.5 bg-gray-100 rounded text-xs font-mono">F5</kbd>，Mac 按 <kbd class="px-1.5 py-0.5 bg-gray-100 rounded text-xs font-mono">Command</kbd> + <kbd class="px-1.5 py-0.5 bg-gray-100 rounded text-xs font-mono">R</kbd>）</p>
                  <p>4. 在网络请求列表中找到任意一个请求</p>
                  <p>5. 点击请求，查看右侧 "Headers" 或 "标头" 中的 Cookie</p>
                  <p>6. 找到并复制 hallticket 的值（一串字母和数字）</p>
                  <p>7. 找到并复制 ASP.NET_SessionId 的值（一串字母和数字）</p>
                </div>
              </div>
            </div>

            <!-- Safari Section -->
            <div class="space-y-3 border-t border-blue-100/50 pt-6">
              <h4 class="font-semibold text-gray-900 flex items-center gap-2 text-lg tracking-tight">
                Safari 浏览器
              </h4>
              <div class="ml-7 space-y-2.5">
                <div class="text-sm leading-relaxed text-gray-600 space-y-1.5 ml-4 font-normal">
                  <p>1. 打开 Safari 的偏好设置（<kbd class="px-1.5 py-0.5 bg-gray-100 rounded text-xs font-mono">Command</kbd> + <kbd class="px-1.5 py-0.5 bg-gray-100 rounded text-xs font-mono">,</kbd>）</p>
                  <p>2. 切换到"高级"标签页</p>
                  <p>3. 勾选底部的"在菜单栏中显示开发菜单"</p>
                  <p>4. 关闭偏好设置</p>
                  <p>5. 点击顶部菜单栏的"开发" → "显示网页检查器"（或按 <kbd class="px-1.5 py-0.5 bg-gray-100 rounded text-xs font-mono">Command</kbd> + <kbd class="px-1.5 py-0.5 bg-gray-100 rounded text-xs font-mono">Option</kbd> + <kbd class="px-1.5 py-0.5 bg-gray-100 rounded text-xs font-mono">I</kbd>）</p>
                  <p>6. 点击顶部的 <span class="font-medium text-gray-700">"Network"</span> 标签</p>
                  <p>7. 刷新页面（<kbd class="px-1.5 py-0.5 bg-gray-100 rounded text-xs font-mono">Command</kbd> + <kbd class="px-1.5 py-0.5 bg-gray-100 rounded text-xs font-mono">R</kbd>）</p>
                  <p>8. 在请求列表中点击任意请求</p>
                  <p>9. 在右侧面板中找到 <span class="font-medium text-gray-700">"Headers"</span> → <span class="font-medium text-gray-700">"Request Headers"</span> → <span class="font-medium text-gray-700">"Cookie"</span></p>
                  <p>10. 找到并复制 hallticket 的值（一串字母和数字）</p>
                  <p>11. 找到并复制 ASP.NET_SessionId 的值（一串字母和数字）</p>
                </div>
              </div>
            </div>

            <!-- Tips Section with Safari-specific tips -->
            <div class="mt-6 bg-blue-50/70 rounded-lg p-4">
              <p class="font-medium text-blue-900 mb-3">💡 小贴士：</p>
              <ul class="space-y-2 text-sm text-blue-800">
                <li class="flex items-start gap-2">
                  <span class="font-medium">•</span>
                  <span class="font-normal">找不到 Network 标签？点击开发者工具右上角的更多标签 (<span class="font-mono">»</span>) 展开</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="font-medium">•</span>
                  <span class="font-normal">Safari 首次使用需要先启用开发菜单</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="font-medium">•</span>
                  <span class="font-normal">Cookie 内容较长时，可以双击选中 hallticket 的值后复制</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="font-medium">•</span>
                  <span class="font-normal">复制时不要包含引号，只需要引号内的内容</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="font-medium">•</span>
                  <span class="font-normal">在 Cookie 中，除了 hallticket，还需要复制 ASP.NET_SessionId 的值</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Security Notice -->
      <div class="bg-blue-50/70 border border-blue-100 rounded-xl p-4">
        <div class="flex gap-3">
          <div class="flex-shrink-0 text-blue-500">
            <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10 2a8 8 0 018 8c0 3.098-1.76 5.777-4.324 7.106a.5.5 0 01-.676-.676C13.777 14.76 16 12.098 16 9a6 6 0 10-12 0c0 3.098 2.223 5.76 4.324 7.106a.5.5 0 01-.676.676A7.963 7.963 0 012 10a8 8 0 018-8z"/>
            </svg>
          </div>
          <div>
            <div class="text-sm font-medium text-blue-900">数据安全说明</div>
            <div class="mt-1 text-sm text-blue-700 space-y-1">
              <p>• 仅处理数据用于生成报告，不会存储任何数据</p>
              <p>• 全部源代码已开源于 <a href="https://github.com/zhuohaoyu/PKU-Annual-Eat" class="underline hover:text-blue-900 transition-colors">GitHub</a></p>
              <p>• 如果担心安全问题，欢迎查看源码或自行部署使用</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Input Form -->
      <form class="space-y-6" @submit.prevent="submitForm">
        <div class="rounded-md space-y-4">
          <div>
            <label for="account" class="block text-sm font-medium text-gray-700">账号</label>
            <input
              id="account"
              v-model="formData.account"
              type="text"
              required
              class="mt-1 block w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg 
                     text-gray-900 placeholder-gray-400
                     focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 
                     transition-colors"
              placeholder="输入账号（6位数字）"
            >
          </div>
          
          <div>
            <label for="hallticket" class="block text-sm font-medium text-gray-700">Hallticket</label>
            <input
              id="hallticket"
              v-model="formData.hallticket"
              type="text"
              required
              class="mt-1 block w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg 
                     text-gray-900 placeholder-gray-400
                     focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 
                     transition-colors"
              placeholder="输入 hallticket（一串大写字母和数字组合）"
            >
          </div>

          <div>
            <label for="sessionId" class="block text-sm font-medium text-gray-700">ASP.NET_SessionId</label>
            <input
              id="sessionId"
              v-model="formData.sessionId"
              type="text"
              required
              class="mt-1 block w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg 
                     text-gray-900 placeholder-gray-400
                     focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 
                     transition-colors"
              placeholder="输入 ASP.NET_SessionId（一串小写字母和数字组合）"
            >
          </div>

          <div>
            <label for="year" class="block text-sm font-medium text-gray-700">选择年份</label>
            <select
              id="year"
              v-model="formData.year"
              class="mt-1 block w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg 
                     text-gray-900
                     focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 
                     transition-colors"
            >
              <option v-for="year in availableYears" :key="year" :value="year">
                {{ year }}年度报告
              </option>
            </select>
          </div>
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-lg
                 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700
                 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500
                 disabled:opacity-50 disabled:cursor-not-allowed
                 transition-colors duration-200"
        >
          {{ loading ? '获取中...' : '生成年度报告' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const isGuideExpanded = ref(false)
</script>

<script>
export default {
  data() {
    return {
      formData: {
        account: '',
        hallticket: '',
        sessionId: '',
        year: new Date().getFullYear()
      },
      loading: false
    }
  },
  computed: {
    availableYears() {
      const currentYear = new Date().getFullYear()
      return Array.from(
        { length: currentYear - 2019 }, 
        (_, i) => currentYear - i
      )
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
            sessionId: this.formData.sessionId,
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