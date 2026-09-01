import { useMemo, useState } from 'react';

type NavItem = {
  key: string;
  label: string;
  eyebrow: string;
};

type MetricRows = Array<[string, string]>;

const navItems: NavItem[] = [
  { key: 'overview', label: 'Overview', eyebrow: 'NOW' },
  { key: 'research', label: 'Research', eyebrow: 'EYES' },
  { key: 'portfolio', label: 'Portfolio', eyebrow: 'CAPITAL' },
  { key: 'decisions', label: 'Decisions', eyebrow: 'MIND' },
  { key: 'watchman', label: 'Watchman', eyebrow: 'GUARD' },
  { key: 'execution', label: 'Execution', eyebrow: 'HAND' },
  { key: 'evidence', label: 'Evidence', eyebrow: 'BOOK' },
  { key: 'participants', label: 'Participants', eyebrow: 'RIGHTS' },
  { key: 'reports', label: 'Reports', eyebrow: 'LEARN' },
  { key: 'covenant', label: 'Covenant', eyebrow: 'LAW' },
];

const snapshot = {
  asOf: '2026-09-01 13:59 CDT',
  capital: [
    ['Shadow NAV', '$103,821'],
    ['Cash', '$31,492'],
    ['Deployable', '$21,492'],
    ['Required reserves', '$10,000'],
  ] as MetricRows,
  risk: [
    ['Current drawdown', '-1.8%'],
    ['Max shadow drawdown', '-4.3%'],
    ['Largest position', '4.1%'],
    ['Watchman blocks', '1'],
  ] as MetricRows,
  research: [
    ['Observed assets', '42'],
    ['Active cases', '8'],
    ['Recommendations', '3'],
    ['Awaiting decision', '1'],
  ] as MetricRows,
  evidence: [
    ['Market data', 'VALID'],
    ['Big Book integrity', 'VALID'],
    ['Missing lineage', '0'],
    ['Unreviewed decisions', '2'],
  ] as MetricRows,
  cases: [
    { asset: 'XYZ', thesis: 'Normalized earnings mispricing', confidence: '0.71', action: 'ACCUMULATE', state: 'Awaiting Steward' },
    { asset: 'ABC', thesis: 'Balance-sheet recovery', confidence: '0.63', action: 'WATCH', state: 'Research active' },
    { asset: 'DEF', thesis: 'Demand slowdown risk', confidence: '0.78', action: 'REDUCE', state: 'Watchman review' },
  ],
  decisions: [
    { id: 'DEC-00381', asset: 'XYZ', steward: 'MODIFIED', watchman: 'PASS', intent: '2.5%', evidence: 'COMPLETE' },
    { id: 'DEC-00380', asset: 'DEF', steward: 'APPROVED', watchman: 'BLOCK', intent: '—', evidence: 'COMPLETE' },
    { id: 'DEC-00379', asset: 'ABC', steward: 'REJECTED', watchman: 'N/A', intent: '—', evidence: 'COMPLETE' },
  ],
};

function StatusPill({ value }: { value: string }) {
  const normalized = value.toLowerCase().replace(/\s+/g, '-');
  return <span className={`pill pill-${normalized}`}>{value}</span>;
}

function MetricGroup({ title, subtitle, values }: { title: string; subtitle: string; values: MetricRows }) {
  return (
    <section className="metric-card">
      <div className="section-heading">
        <div>
          <p className="kicker">{subtitle}</p>
          <h2>{title}</h2>
        </div>
      </div>
      <div className="metric-list">
        {values.map(([label, value]) => (
          <div className="metric-row" key={label}>
            <span>{label}</span>
            <strong>{value}</strong>
          </div>
        ))}
      </div>
    </section>
  );
}

function Overview() {
  return (
    <>
      <section className="hero-panel">
        <div>
          <p className="kicker">FIRSTFRUITS · SHADOW CAPITAL</p>
          <h1>What needs the manager's attention?</h1>
          <p className="hero-copy">
            One operating surface for research, judgment, constraint, execution evidence, and learning. No live client capital is represented here.
          </p>
        </div>
        <div className="hero-state">
          <span className="mode-badge">DEMO / SHADOW</span>
          <span>As of {snapshot.asOf}</span>
          <span>Capital acceptance: disabled</span>
        </div>
      </section>

      <div className="metrics-grid">
        <MetricGroup title="Capital" subtitle="TREASURY" values={snapshot.capital} />
        <MetricGroup title="Risk" subtitle="WATCHMAN" values={snapshot.risk} />
        <MetricGroup title="Research" subtitle="EPINNOX" values={snapshot.research} />
        <MetricGroup title="Evidence" subtitle="THE BIG BOOK" values={snapshot.evidence} />
      </div>

      <div className="content-grid">
        <section className="panel span-7">
          <div className="section-heading">
            <div>
              <p className="kicker">EPINNOX → STEWARD</p>
              <h2>Active investment cases</h2>
            </div>
            <button className="quiet-button">View research queue</button>
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Asset</th>
                  <th>Thesis</th>
                  <th>Confidence</th>
                  <th>Recommendation</th>
                  <th>State</th>
                </tr>
              </thead>
              <tbody>
                {snapshot.cases.map((item) => (
                  <tr key={item.asset}>
                    <td className="mono strong">{item.asset}</td>
                    <td>{item.thesis}</td>
                    <td>{item.confidence}</td>
                    <td><StatusPill value={item.action} /></td>
                    <td>{item.state}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="panel span-5">
          <div className="section-heading">
            <div>
              <p className="kicker">OPERATING HEALTH</p>
              <h2>Institution state</h2>
            </div>
          </div>
          <div className="health-stack">
            <div className="health-row"><span>Data plane</span><StatusPill value="VALID" /></div>
            <div className="health-row"><span>Watchman policy</span><StatusPill value="VALID" /></div>
            <div className="health-row"><span>Big Book integrity</span><StatusPill value="VALID" /></div>
            <div className="health-row"><span>Hand execution</span><StatusPill value="PENDING" /></div>
            <div className="health-row"><span>Client capital</span><StatusPill value="BLOCKED" /></div>
          </div>
          <div className="callout">
            <span className="callout-label">Constitutional reminder</span>
            <strong>Steward approval + Watchman block = no authorization.</strong>
          </div>
        </section>
      </div>

      <section className="panel">
        <div className="section-heading">
          <div>
            <p className="kicker">MIND → GUARD → AUTHORITY</p>
            <h2>Recent decisions</h2>
          </div>
          <button className="quiet-button">Open decision journal</button>
        </div>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Decision</th>
                <th>Asset</th>
                <th>Steward</th>
                <th>Watchman</th>
                <th>Authorized intent</th>
                <th>Evidence</th>
              </tr>
            </thead>
            <tbody>
              {snapshot.decisions.map((decision) => (
                <tr key={decision.id}>
                  <td className="mono">{decision.id}</td>
                  <td className="mono strong">{decision.asset}</td>
                  <td><StatusPill value={decision.steward} /></td>
                  <td><StatusPill value={decision.watchman} /></td>
                  <td>{decision.intent}</td>
                  <td><StatusPill value={decision.evidence} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </>
  );
}

function ReservedSurface({ item }: { item: NavItem }) {
  return (
    <section className="panel reserved-panel">
      <p className="kicker">ACM-07.0 SURFACE</p>
      <h1>{item.label}</h1>
      <p>
        The information boundary for this surface is reserved, but the first ACM-07 slice intentionally implements Overview before wiring authoritative read models.
      </p>
      <div className="callout">
        <span className="callout-label">Current source</span>
        <strong>Synthetic shadow fixture only — no live capital truth.</strong>
      </div>
    </section>
  );
}

export function App() {
  const [active, setActive] = useState('overview');
  const activeItem = useMemo(() => navItems.find((item) => item.key === active) ?? navItems[0], [active]);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-block">
          <div className="brand-mark">B</div>
          <div>
            <strong>Benjamin</strong>
            <span>Manager Console</span>
          </div>
        </div>

        <nav>
          {navItems.map((item) => (
            <button
              key={item.key}
              className={active === item.key ? 'nav-item active' : 'nav-item'}
              onClick={() => setActive(item.key)}
            >
              <span className="nav-eyebrow">{item.eyebrow}</span>
              <span>{item.label}</span>
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <span className="mode-badge">SHADOW</span>
          <p>No live money. No client admission.</p>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <p className="breadcrumb">Alabama Capital Management / {activeItem.label}</p>
          </div>
          <div className="operator-chip">
            <span className="operator-dot" />
            <span>Steward workspace</span>
          </div>
        </header>

        <div className="page-content">{active === 'overview' ? <Overview /> : <ReservedSurface item={activeItem} />}</div>
      </main>
    </div>
  );
}