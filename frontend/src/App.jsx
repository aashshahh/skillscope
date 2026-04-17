import { useState } from 'react'
import Header from './components/Header.jsx'
import InputPanel from './components/InputPanel.jsx'
import ResultPanel from './components/ResultPanel.jsx'
import axios from 'axios'

const API = import.meta.env.VITE_API_URL || ''

export default function App() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function analyze(resumeText, jdText) {
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const res = await axios.post(`${API}/api/v1/analyze/text`, {
        resume_text: resumeText,
        jd_text: jdText,
      })
      setResult(res.data)
    } catch (e) {
      setError(e.response?.data?.detail || 'Analysis failed. Is the API running?')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Header />
      <main style={{ flex: 1, maxWidth: 1100, margin: '0 auto', width: '100%', padding: '0 24px 80px' }}>
        <InputPanel onAnalyze={analyze} loading={loading} />
        {error && (
          <div style={{
            marginTop: 24, padding: '14px 20px',
            background: 'rgba(245,66,66,0.08)', border: '1px solid rgba(245,66,66,0.3)',
            borderRadius: 8, color: '#f54242', fontSize: 13,
          }}>
            {error}
          </div>
        )}
        {result && <ResultPanel data={result} />}
      </main>
    </div>
  )
}