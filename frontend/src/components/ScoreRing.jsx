import { useEffect, useState } from 'react'

const SIZE = 180, STROKE = 10, R = (SIZE - STROKE) / 2, CIRC = 2 * Math.PI * R

function scoreColor(score) {
  if (score >= 75) return 'var(--accent)'
  if (score >= 45) return 'var(--accent2)'
  return 'var(--miss)'
}

export default function ScoreRing({ score }) {
  const [animated, setAnimated] = useState(0)
  useEffect(() => { const t = setTimeout(() => setAnimated(score), 80); return () => clearTimeout(t) }, [score])
  const offset = CIRC - (animated / 100) * CIRC
  const color = scoreColor(score)
  return (
    <div style={{ position: 'relative', width: SIZE, height: SIZE, flexShrink: 0 }}>
      <svg width={SIZE} height={SIZE} style={{ transform: 'rotate(-90deg)' }}>
        <circle cx={SIZE/2} cy={SIZE/2} r={R} fill="none" stroke="var(--border)" strokeWidth={STROKE} />
        <circle cx={SIZE/2} cy={SIZE/2} r={R} fill="none" stroke={color} strokeWidth={STROKE}
          strokeLinecap="round" strokeDasharray={CIRC} strokeDashoffset={offset}
          style={{ transition: 'stroke-dashoffset 1s cubic-bezier(0.4,0,0.2,1)' }} />
      </svg>
      <div style={{
        position: 'absolute', inset: 0, display: 'flex',
        flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
      }}>
        <span style={{ fontFamily: 'var(--serif)', fontSize: 40, fontWeight: 900, color, lineHeight: 1 }}>
          {Math.round(score)}
        </span>
        <span style={{ fontSize: 11, color: 'var(--muted)', letterSpacing: '1px' }}>/ 100</span>
      </div>
    </div>
  )
}