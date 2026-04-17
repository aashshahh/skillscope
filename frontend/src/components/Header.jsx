export default function Header() {
  return (
    <header style={{
      borderBottom: '1px solid var(--border)', padding: '0 24px', height: 64,
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      position: 'sticky', top: 0,
      background: 'rgba(10,10,8,0.92)', backdropFilter: 'blur(12px)', zIndex: 100,
    }}>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 10 }}>
        <span style={{ fontFamily: 'var(--serif)', fontSize: 22, fontWeight: 900, color: 'var(--accent)', letterSpacing: '-0.5px' }}>
          SkillScope
        </span>
        <span style={{ color: 'var(--muted)', fontSize: 12 }}>/ skill gap analysis</span>
      </div>
      <nav style={{ display: 'flex', gap: 24, alignItems: 'center' }}>
        <a href="https://github.com/aashshahh/skillscope" target="_blank" rel="noopener noreferrer"
          style={{ color: 'var(--muted)', textDecoration: 'none', fontSize: 12 }}>
          GitHub
        </a>
        <a href="https://github.com/aashshahh/skillscope#readme" target="_blank" rel="noopener noreferrer"
          style={{ color: 'var(--muted)', textDecoration: 'none', fontSize: 12 }}>
          Docs
        </a>
      </nav>
    </header>
  )
}