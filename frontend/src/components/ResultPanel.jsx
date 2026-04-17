import ScoreRing from './ScoreRing.jsx'
import SkillGrid from './SkillGrid.jsx'

export default function ResultPanel({ data }) {
  const { match_score, matched_skills, soft_matched, missing_skills, extra_skills, jd_skills, resume_skills } = data

  return (
    <section style={{ marginTop: 64, animation: 'fadeUp 0.4s ease both' }}>
      <style>{`@keyframes fadeUp { from { opacity:0; transform:translateY(20px); } to { opacity:1; transform:translateY(0); } }`}</style>

      <div style={{ display: 'grid', gridTemplateColumns: '220px 1fr', gap: 32, marginBottom: 48, alignItems: 'center' }}>
        <ScoreRing score={match_score} />
        <div>
          <h2 style={{ fontFamily: 'var(--serif)', fontSize: 32, fontWeight: 900, lineHeight: 1.1, marginBottom: 12 }}>
            {scoreLabel(match_score)}
          </h2>
          <p style={{ color: 'var(--muted)', fontSize: 13, lineHeight: 1.7, maxWidth: 480 }}>
            {scoreDescription(match_score, missing_skills.length)}
          </p>
          <div style={{ display: 'flex', gap: 24, marginTop: 20 }}>
            <Stat value={jd_skills.length} label="JD skills" />
            <Stat value={matched_skills.length} label="exact match" color="var(--accent)" />
            <Stat value={soft_matched.length} label="soft match" color="var(--soft)" />
            <Stat value={missing_skills.length} label="missing" color="var(--miss)" />
          </div>
        </div>
      </div>

      <div style={{ height: 1, background: 'var(--border)' }} />

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32, marginTop: 40 }}>
        <SkillGrid title="Matched" subtitle="exact" skills={matched_skills} color="var(--accent)" prefix="+" />
        <SkillGrid title="Missing" subtitle="priority to learn" skills={missing_skills} color="var(--miss)" prefix="-" />
      </div>

      {soft_matched.length > 0 && (
        <div style={{ marginTop: 32 }}>
          <div style={{ display: 'flex', alignItems: 'baseline', gap: 10, marginBottom: 12 }}>
            <span style={{ fontSize: 11, fontWeight: 500, letterSpacing: '1px', textTransform: 'uppercase', color: 'var(--soft)' }}>Semantic Matches</span>
            <span style={{ fontSize: 11, color: 'var(--muted)' }}>similar concepts matched via SBERT cosine similarity</span>
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {soft_matched.map((m, i) => (
              <div key={i} style={{
                padding: '6px 12px', borderRadius: 6, fontSize: 12, color: 'var(--soft)',
                background: 'rgba(66,180,245,0.06)', border: '1px solid rgba(66,180,245,0.2)',
                display: 'flex', alignItems: 'center', gap: 8,
              }}>
                <span style={{ color: 'var(--text)' }}>{m.jd_skill}</span>
                <span style={{ color: 'var(--muted)' }}>←</span>
                <span>{m.resume_skill}</span>
                <span style={{ background: 'rgba(66,180,245,0.15)', padding: '1px 6px', borderRadius: 4, fontSize: 10 }}>
                  {(m.score * 100).toFixed(0)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {extra_skills.length > 0 && (
        <div style={{ marginTop: 32 }}>
          <div style={{ fontSize: 11, fontWeight: 500, letterSpacing: '1px', textTransform: 'uppercase', color: 'var(--muted)', marginBottom: 10 }}>
            Additional Skills <span style={{ fontWeight: 400, textTransform: 'none', letterSpacing: 0 }}>— in resume, not in this JD</span>
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
            {extra_skills.slice(0, 20).map((s, i) => (
              <span key={i} style={{
                padding: '4px 10px', background: 'var(--surface)', border: '1px solid var(--border)',
                borderRadius: 4, fontSize: 11, color: 'var(--muted)',
              }}>{s}</span>
            ))}
          </div>
        </div>
      )}

      <div style={{ height: 1, background: 'var(--border)', marginTop: 48 }} />
      <p style={{ marginTop: 20, fontSize: 11, color: 'var(--muted)', lineHeight: 1.6 }}>
        Method: spaCy PhraseMatcher + ESCO taxonomy for extraction / Sentence-BERT (all-MiniLM-L6-v2) for semantic similarity / Threshold: 0.65 cosine
      </p>
    </section>
  )
}

function Stat({ value, label, color = 'var(--text)' }) {
  return (
    <div>
      <div style={{ fontSize: 28, fontFamily: 'var(--serif)', fontWeight: 900, color, lineHeight: 1 }}>{value}</div>
      <div style={{ fontSize: 11, color: 'var(--muted)', marginTop: 2, letterSpacing: '0.5px' }}>{label}</div>
    </div>
  )
}

function scoreLabel(score) {
  if (score >= 85) return 'Strong match.'
  if (score >= 65) return 'Good fit, some gaps.'
  if (score >= 40) return 'Partial match.'
  return 'Significant skill gap.'
}

function scoreDescription(score, missingCount) {
  if (score >= 85) return `Your profile aligns well with this role. ${missingCount} skills could strengthen your application further.`
  if (score >= 65) return `You cover most requirements. Closing ${missingCount} skill gaps would make you a strong candidate.`
  if (score >= 40) return `You have a foundation, but ${missingCount} key skills are missing. Target these before applying.`
  return `This role requires skills you haven't developed yet. Use the missing skills below as a learning roadmap.`
}