import { useMemo, useState } from 'react';

type NavItem = { key: string; label: string };

const navItems: NavItem[] = [
  { key: 'overview', label: 'Overview' },
  { key: 'capital', label: 'Capital Account' },
  { key: 'performance', label: 'Performance' },
  { key: 'activity', label: 'Activity' },
  { key: 'documents', label: 'Documents' },
  { key: 'proofs', label: 'Proof Center' },
  { key: 'profile', label: 'Profile & Access' },
  { key: 'support', label: 'Support' },
];

const participant = {
  displayName: 'Demo Participant',
  participantId: 'participant:9271',
  asOf: '2026-09-01 13:59 CDT',
  status: 'DEMO / SHADOW',
  account: [
    ['Capital contributed', '$25,000.00'],
    ['Participant equity', '$25,955.25'],
    ['Ownership units', '250.000'],
    ['Distributions to date', '$0.00'],
  ],
  performance: [
    ['Since shadow inception', '+3.82%'],
    ['Current period', '+1.14%'],
    ['Latest participant NAV', '$103.821 / unit'],
    ['Valuation status', 'SHADOW'],
  ],
  activity: [
    { date: '2026-09-01', type: 'Contribution proof', amount: '$25,000.00', status: 'DEMO', proof: 'RCP-DEMO-001' },
    { date: '2026-09-01', type: 'Unit allocation', amount: '250.000 units', status: 'DEMO', proof: 'RCP-DEMO-002' },
    { date: '2026-09-01', type: 'Statement generated', amount: '—', status: 'READY', proof: 'RCP-DEMO-003' },
  ],
  documents: [
    { title: 'Participation agreement', period: 'Current', status: 'Demo document', ref: 'AG-DEMO-229' },
    { title: 'Capital account statement', period: 'Sep 2026', status: 'Demo statement', ref: 'STMT-DEMO-001' },
    { title: 'Privacy & proof notice', period: 'Current', status: 'Available', ref: 'NOTICE-001' },
  ],
};

function Badge({ children, tone = 'neutral' }: { children: string; tone?: 'neutral' | 'good' | 'warn' }) {
  return <span className={`badge badge-${tone}`}>{children}</span>;
}

function StatGroup({ title, values }: { title: string; values: Array<[string, string]> }) {
  return (
    <section className="card stat-card">
      <p className="eyebrow">{title}</p>
      <div className="stat-list">
        {values.map(([label, value]) => (
          <div className="stat-row" key={label}>
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
      <section className="welcome-card">
        <div>
          <p className="eyebrow">FIRSTFRUITS · PARTICIPANT VIEW</p>
          <h1>Your participation, clearly accounted for.</h1>
          <p>
            This console is intentionally limited to your own demo participation, documents, and proofs. It does not expose Benjamin's private portfolio, research, other participants, or internal decision process.
          </p>
        </div>
        <div className="welcome-meta">
          <Badge tone="warn">DEMO / SHADOW</Badge>
          <span>{participant.participantId}</span>
          <span>As of {participant.asOf}</span>
        </div>
      </section>

      <div className="stat-grid">
        <StatGroup title="YOUR CAPITAL ACCOUNT" values={participant.account} />
        <StatGroup title="YOUR PERFORMANCE VIEW" values={participant.performance} />
      </div>

      <div className="two-column">
        <section className="card">
          <div className="section-head">
            <div>
              <p className="eyebrow">PARTICIPANT-SCOPED</p>
              <h2>Recent account activity</h2>
            </div>
            <button className="link-button">View all</button>
          </div>
          <div className="activity-list">
            {participant.activity.map((item) => (
              <div className="activity-item" key={item.proof}>
                <div>
                  <strong>{item.type}</strong>
                  <span>{item.date} · {item.proof}</span>
                </div>
                <div className="activity-right">
                  <strong>{item.amount}</strong>
                  <Badge tone={item.status === 'READY' ? 'good' : 'neutral'}>{item.status}</Badge>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="card proof-card">
          <p className="eyebrow">PROOF CENTER</p>
          <h2>Verify what belongs to you.</h2>
          <p>
            Participant proofs can establish your contribution, entitlement, statement lineage, or other authorized account facts without giving you unrestricted access to the Big Book.
          </p>
          <div className="proof-example">
            <span>Contribution accepted</span>
            <strong>$25,000.00</strong>
            <span>Agreement</span>
            <strong>AG-DEMO-229</strong>
            <span>Entitlement</span>
            <strong>250.000 units</strong>
            <span>Big Book proof</span>
            <strong className="mono">RCP-DEMO-001</strong>
          </div>
          <button className="primary-button">Open Proof Center</button>
        </section>
      </div>

      <section className="card">
        <div className="section-head">
          <div>
            <p className="eyebrow">DOCUMENTS YOU ARE ENTITLED TO RECEIVE</p>
            <h2>Documents & notices</h2>
          </div>
          <button className="link-button">Document center</button>
        </div>
        <div className="document-grid">
          {participant.documents.map((doc) => (
            <div className="document" key={doc.ref}>
              <div className="doc-icon">D</div>
              <div>
                <strong>{doc.title}</strong>
                <span>{doc.period} · {doc.ref}</span>
              </div>
              <Badge>{doc.status}</Badge>
            </div>
          ))}
        </div>
      </section>

      <section className="privacy-banner">
        <div>
          <p className="eyebrow">PRIVACY BY CONSTITUTION</p>
          <strong>Your access stops where another participant's rights begin.</strong>
        </div>
        <p>
          This surface receives a participant-specific read model. It is not a manager dataset with fields hidden in the browser.
        </p>
      </section>
    </>
  );
}

function ReservedSurface({ item }: { item: NavItem }) {
  return (
    <section className="card reserved">
      <p className="eyebrow">ACM-07.0 PARTICIPANT SURFACE</p>
      <h1>{item.label}</h1>
      <p>
        This participant-scoped surface is reserved for the next read-model slice. No manager-only data will be introduced here to make the screen feel complete.
      </p>
      <Badge tone="warn">DEMO / SHADOW ONLY</Badge>
    </section>
  );
}

export function App() {
  const [active, setActive] = useState('overview');
  const activeItem = useMemo(() => navItems.find((item) => item.key === active) ?? navItems[0], [active]);

  return (
    <div className="client-shell">
      <header className="header">
        <div className="brand">
          <div className="brand-mark">B</div>
          <div>
            <strong>Benjamin</strong>
            <span>Client Console</span>
          </div>
        </div>
        <div className="identity">
          <span className="identity-dot" />
          <div>
            <strong>{participant.displayName}</strong>
            <span>Participant-scoped session</span>
          </div>
        </div>
      </header>

      <nav className="tabs" aria-label="Client console navigation">
        {navItems.map((item) => (
          <button key={item.key} onClick={() => setActive(item.key)} className={active === item.key ? 'tab active' : 'tab'}>
            {item.label}
          </button>
        ))}
      </nav>

      <main>
        <div className="page-title-row">
          <div>
            <p className="crumb">Your account / {activeItem.label}</p>
          </div>
          <Badge tone="warn">NO LIVE CAPITAL</Badge>
        </div>
        <div className="page-grid">{active === 'overview' ? <Overview /> : <ReservedSurface item={activeItem} />}</div>
      </main>
    </div>
  );
}