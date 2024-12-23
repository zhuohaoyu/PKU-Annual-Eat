// Option 2: Using our backend as a proxy
const baseUrl = '/api/proxy/card'

export async function fetchTransactions(account, hallticket, startDate, endDate) {
  const params = new URLSearchParams({
    sdate: startDate,
    edate: endDate,
    account: account,
  })

  try {
    const response = await fetch(`/api/proxy/card?${params.toString()}`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'hallticket': hallticket
      }
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || 'Failed to fetch transactions')
    }

    const data = await response.json()
    
    // The PKU card system returns data in {rows: [...]} format
    const transactions = data.rows || []
    return processTransactions(transactions)
  } catch (error) {
    throw new Error(`获取数据失败: ${error.message}`)
  }
}

function processTransactions(data) {
  if (!Array.isArray(data)) {
    throw new Error('Invalid data format')
  }

  // Filter dining transactions (negative amounts)
  const diningTransactions = data.filter(t => t.TRANAMT < 0)

  // Calculate summary
  const summary = {
    total_amount: Math.abs(diningTransactions.reduce((sum, t) => sum + t.TRANAMT, 0)).toFixed(2),
    total_transactions: diningTransactions.length,
    total_categories: new Set(diningTransactions.map(t => t.MERCNAME.trim())).size
  }

  return {
    transactions: diningTransactions,
    summary
  }
} 