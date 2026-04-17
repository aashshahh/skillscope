export default function SkillGrid({ title, subtitle, skills, color, prefix }) {
  if (skills.length === 0) return (
    <div>
      <GridHeader title={title} subtitle={subtitle} color={color} />
      <p style={{ color: 'var(--muted)', fontSize: 12, marginTop: 12 }}>None</p>
    </div>
  )
  return (
    <div>
      <GridHeader title={title} subtitle={subtitle} color={color} count={skills.length} />
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginTop: 12 }}>
        {skills.map((s, i) => (
          <span key={i} style={{
            padding: '5px 11px', borderRadius: 5, fontSize: 12,
            color: color, fontFamily: 'var(--mono)',
            background: `color-mix(in srgb, ${color} 7%, transparent)`,
            border: `1px solid color-mix(in srgb, ${color} 20%, transparent)`,
            animation: `fadeIn 0.3s ease ${i * 0.03}s both`,
          }}>
            <span style={{ opacity: 0.5, marginRight: 4 }}>{prefix}</span>{s}
          </span>
        ))}
      </div>
      <style>{`@keyframes fadeIn { from { opacity:0; transform:scale(0.9); } to { opacity:1; transform:scale(1); } }`}</style>
    </div>
  )
}

function GridHeader({ title, subtitle, color, count }) {
  return (
    <div style={{ display: 'flex', alignItems: 'baseline', gap: 8, borderBottom: '1px solid var(--border)', paddingBottom: 10 }}>
      <span style={{ fontSize: 11, fontWeight: 500, letterSpacing: '1.5px', textTransform: 'uppercase', color }}>{title}</span>
      {count !== undefined && (
        <span style={{ fontSize: 10, padding: '1px 7px', borderRadius: 10, color,
          background: `color-mix(in srgb, ${color} 10%, transparent)` }}>{count}</span>
      )}
      <span style={{ fontSize: 11, color: 'var(--muted)', marginLeft: 'auto' }}>{subtitle}</span>
    </div>
  )
}