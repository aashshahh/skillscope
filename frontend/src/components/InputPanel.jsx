import { useState } from 'react'

const SAMPLE_RESUME = `Aash Shah — ML Engineer
Skills: Python, PyTorch, scikit-learn, FastAPI, Docker, PostgreSQL, AWS, NLP, BERT, Git, React`

const SAMPLE_JD = `Senior ML Engineer — Acme AI
Requirements: Python, PyTorch, TensorFlow, Kubernetes, Spark, Airflow, AWS SageMaker, MLflow, PostgreSQL, communication, teamwork`

export default function InputPanel({ onAnalyze, loading }) {
  const [resume, setResume] = useState('')
  const [jd, setJd] = useState('')

  const canSubmit = resume.trim().length > 10 && jd.trim().length > 10 && !loading

  return (
    <section style={{ paddingTop: 56 }}>
      <div style={{ marginBottom: 48 }}>
        <h1 style={{
          fontFamily: 'var(--serif)', fontSize: 'clamp(36px, 6vw, 68px)',
          fontWeight: 900, lineHeight: 1.05, letterSpacing: '-1px', marginBottom: 16,
        }}>
          Know exactly what<br />
          <em style={{ color: 'var(--accent)', fontStyle: 'italic' }}>skills you're missing.</em>
        </h1>
        <p style={{ color: 'var(--muted)', fontSize: 14, maxWidth: 520, lineHeight: 1.7 }}>
          Paste your resume and a job description. SkillScope extracts skills using spaCy and ESCO taxonomy,
          then computes semantic similarity via Sentence-BERT to surface your exact gap.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginBottom: 16 }}>
        <TextArea label="Resume" placeholder="Paste your resume text here..." value={resume} onChange={setResume} />
        <TextArea label="Job Description" placeholder="Paste the job description here..." value={jd} onChange={setJd} />
      </div>

      <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
        <button onClick={() => onAnalyze(resume, jd)} disabled={!canSubmit} style={{
          padding: '12px 32px',
          background: canSubmit ? 'var(--accent)' : 'var(--border)',
          color: canSubmit ? 'var(--bg)' : 'var(--muted)',
          border: 'none', borderRadius: 6, fontFamily: 'var(--mono)',
          fontSize: 13, fontWeight: 500, cursor: canSubmit ? 'pointer' : 'not-allowed',
        }}>
          {loading ? 'Analyzing...' : 'Analyze gap'}
        </button>
        <button onClick={() => { setResume(SAMPLE_RESUME); setJd(SAMPLE_JD) }} style={{
          padding: '12px 20px', background: 'transparent', color: 'var(--muted)',
          border: '1px solid var(--border)', borderRadius: 6, fontFamily: 'var(--mono)',
          fontSize: 12, cursor: 'pointer',
        }}>
          Load sample
        </button>
        {loading && <span style={{ color: 'var(--muted)', fontSize: 12 }}>Extracting skills + computing embeddings...</span>}
      </div>
    </section>
  )
}

function TextArea({ label, placeholder, value, onChange }) {
  return (
    <div>
      <label style={{
        display: 'block', fontSize: 11, color: 'var(--muted)',
        letterSpacing: '1.5px', textTransform: 'uppercase', marginBottom: 8,
      }}>{label}</label>
      <textarea value={value} onChange={e => onChange(e.target.value)}
        placeholder={placeholder} rows={12}
        style={{
          width: '100%', background: 'var(--surface)', border: '1px solid var(--border)',
          borderRadius: 8, color: 'var(--text)', fontFamily: 'var(--mono)',
          fontSize: 12, lineHeight: 1.7, padding: '14px 16px', resize: 'vertical', outline: 'none',
        }}
        onFocus={e => e.target.style.borderColor = 'var(--accent)'}
        onBlur={e => e.target.style.borderColor = 'var(--border)'}
      />
    </div>
  )
}