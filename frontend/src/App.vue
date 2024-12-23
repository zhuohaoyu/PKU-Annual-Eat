<template>
  <div class="min-h-screen bg-gray-50">
    <ConfigForm @report-generated="handleReportGenerated" v-if="!report" />
    <ConsumptionReport v-else :report-data="report" @back="report = null" />
  </div>
</template>

<script>
import ConfigForm from './components/ConfigForm.vue'
import ConsumptionReport from './components/ConsumptionReport.vue'

export default {
  name: 'App',
  components: {
    ConfigForm,
    ConsumptionReport
  },
  data() {
    return {
      report: null
    }
  },
  methods: {
    handleReportGenerated(data) {
      this.report = data
    }
  }
}
</script> 