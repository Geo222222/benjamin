import { useMemo, useState } from 'react';

type NavItem = { key: string; label: string; glyph: string };
type ClientRow = {
  id: string;
  name: string;
  status: string;
  mandate: string;
  aum: string;
  mtd: string;
  ytd: string;
  inception: string;
  drawdown: string;
  risk: string;
  last: string;
  account: string;
  custodian: string;
  cash: string;
  deployed: string;
};

type SurfaceSpec = {
  title: string;
  question: string;
  sources: string[];
  actions: string[];
  metrics: Array<[string, string]>;
  items: Array<[string, string, string]>;
};

const navItems: NavItem[] = [
  { key: 'command', label: 'Command', glyph: '⌂' },
  { key: 'clients', label: 'Clients', glyph: '◎' },
  { key: 'accounts', label: 'Accounts', glyph: '▤' },
  { key: 'capital', label: 'Capital', glyph: '◈' },
  { key: 'markets', label: 'Markets / ZLJ', glyph: '⌁' },
  { key: 'cases', label: 'Investment Cases', glyph: '◇' },
  { key: 'decisions', label: 'Decisions / Benjamin', glyph: '◉' },
  { key: 'execution', label: 'Execution / The Hand', glyph: '▣' },
  { key: 'risk', label: 'Risk / Watchman', glyph: '⬡' },
  { key: 'strategies', label: 'Strategies', glyph: '⌗' },
  { key: 'intelligence', label: 'Intelligence / Calibration', glyph: '◌' },
  { key: 'book', label: 'Book / Evidence', glyph: '▧' },
  { key: 'compliance', label: 'Compliance', glyph: '✓' },
  { key: 'operations', label: 'Operations', glyph: '⚙' },
  { key: 'system', label: 'System', glyph: '◍' },
  { key: 'owner-command', label: 'Owner Command', glyph: '⊕' },
  { key: 'reports', label: 'Reports', glyph: '▥' },
  { key: 'audit', label: 'Audit & History', glyph: '↺' },
  { key: 'governance', label: 'Settings & Governance', glyph: '⚙' },
];

const clients: ClientRow[] = [
  { id: 'BEN-000184', name: 'Robert M.', status: 'Active', mandate: 'BM-SCALP-01', aum: '$28,491.72', mtd: '+3.42%', ytd: '+17.81%', inception: '+28.93%', drawdown: '-7.21%', risk: '31%', last: '10:42:12 AM', account: 'ACC-000184-01', custodian: 'IBKR', cash: '$22,108.49', deployed: '$6,383.23' },
  { id: 'BEN-000185', name: 'Sarah K.', status: 'Active', mandate: 'BM-SCALP-01', aum: '$15,783.41', mtd: '+2.18%', ytd: '+12.47%', inception: '+19.32%', drawdown: '-6.14%', risk: '24%', last: '10:41:58 AM', account: 'ACC-000185-01', custodian: 'IBKR', cash: '$11,954.11', deployed: '$3,829.30' },
  { id: 'BEN-000186', name: 'James L.', status: 'Active', mandate: 'BM-SCALP-03', aum: '$42,103.09', mtd: '+4.11%', ytd: '+21.33%', inception: '+33.88%', drawdown: '-8.17%', risk: '34%', last: '10:42:05 AM', account: 'ACC-000186-01', custodian: 'IBKR', cash: '$25,674.22', deployed: '$16,428.87' },
  { id: 'BEN-000187', name: 'Linda P.', status: 'Active', mandate: 'BM-REV-02', aum: '$11,226.00', mtd: '-0.64%', ytd: '+4.22%', inception: '+6.77%', drawdown: '-9.53%', risk: '28%', last: '10:40:47 AM', account: 'ACC-000187-01', custodian: 'IBKR', cash: '$9,021.31', deployed: '$2,204.69' },
  { id: 'BEN-000188', name: 'Michael T.', status: 'Active', mandate: 'BM-SCALP-01', aum: '$63,552.19', mtd: '+1.92%', ytd: '+15.69%', inception: '+24.11%', drawdown: '-6.48%', risk: '29%', last: '10:42:14 AM', account: 'ACC-000188-01', custodian: 'IBKR', cash: '$39,874.51', deployed: '$23,677.68' },
  { id: 'BEN-000189', name: 'Jennifer W.', status: 'Onboarding', mandate: 'BM-SCALP-01', aum: '$0.00', mtd: '—', ytd: '—', inception: '—', drawdown: '—', risk: '0%', last: '09:22:31 AM', account: 'ACC-000189-01', custodian: 'IBKR', cash: '$0.00', deployed: '$0.00' },
  { id: 'BEN-000190', name: 'David R.', status: 'Active', mandate: 'BM-SCALP-03', aum: '$9,871.33', mtd: '+2.77%', ytd: '+11.02%', inception: '+14.31%', drawdown: '-5.12%', risk: '21%', last: '10:41:49 AM', account: 'ACC-000190-01', custodian: 'Schwab', cash: '$7,803.12', deployed: '$2,068.21' },
  { id: 'BEN-000191', name: 'Amanda C.', status: 'Active', mandate: 'BM-MOM-01', aum: '$19,442.87', mtd: '+3.95%', ytd: '+18.77%', inception: '+25.66%', drawdown: '-6.90%', risk: '27%', last: '10:41:37 AM', account: 'ACC-000191-01', custodian: 'Fidelity', cash: '$15,180.64', deployed: '$4,262.23' },
];

const surfaceSpecs: Record<string, SurfaceSpec> = {
  capital: {
    title: 'Capital',
    question: 'How is capital deployed across the enterprise?',
    sources: ['The Book · capital records', 'Custodians · balances', 'Benjamin · exposure intent'],
    actions: ['View capital detail', 'View liens / restrictions', 'Export report'],
    metrics: [['Client AUM', '$87.64M'], ['Principal capital', '$5.42M'], ['Cash', '$34.67M'], ['Deployed', '$58.39M']],
    items: [['Client accounts', '$87,642,193', '94.2% of enterprise capital'], ['Benjamin principal', '$5,421,883', '5.8% of enterprise capital'], ['Required reserves', '$8,100,000', 'Policy protected'], ['Available deployment', '$26,572,304', 'After reserves']],
  },
  markets: {
    title: 'Markets / ZLJ',
    question: 'What does ZLJ see in the market right now?',
    sources: ['ZLJ · market intelligence', 'Evidence vault · source lineage', 'Market-data quality plane'],
    actions: ['View market state', 'Open evidence', 'Subscribe / alert'],
    metrics: [['Regime', 'HIGH VOL'], ['Qualified feeds', '18 / 18'], ['Observed symbols', '426'], ['Stale inputs', '0']],
    items: [['SPX', '5,287.31', 'Regime: trend / liquid'], ['NASDAQ', '16,734.63', 'Volatility elevated'], ['BTC', '68,882.11', '24h liquidity healthy'], ['VIX', '22.41', 'Risk regime elevated']],
  },
  cases: {
    title: 'Investment Cases',
    question: 'What investment cases exist?',
    sources: ['ZLJ · evidence', 'Benjamin · interest signals', 'The Book · case history'],
    actions: ['Open case', 'Create case', 'Archive case', 'Compare case'],
    metrics: [['Open cases', '37'], ['Decision-ready', '12'], ['Needs evidence', '5'], ['Archived this month', '19']],
    items: [['CASE-AMD-042', 'AMD microstructure continuation', 'Decision-ready'], ['CASE-NVDA-031', 'NVDA momentum persistence', 'Active evidence'], ['CASE-AAPL-008', 'AAPL mean reversion', 'Needs evidence'], ['CASE-BTC-017', 'BTC liquidity expansion', 'Watch']],
  },
  decisions: {
    title: 'Decisions / Benjamin',
    question: 'What is Benjamin deciding and why?',
    sources: ['Benjamin · decisions', 'ZLJ · evidence', 'The Book · decision records'],
    actions: ['Open decision', 'Interrogate', 'Compare decisions', 'Export'],
    metrics: [['Decisions today', '8,412'], ['Trade intents', '7,391'], ['Abstentions', '97'], ['Awaiting governance', '924']],
    items: [['BEN-D-084921', 'BUY AMD · BM-SCALP-03', 'Confidence 0.81'], ['BEN-D-084920', 'NO TRADE NVDA', 'Spread / edge insufficient'], ['BEN-D-084919', 'REDUCE AAPL', 'Thesis decayed'], ['BEN-D-084918', 'HOLD CASH', 'No qualified edge']],
  },
  execution: {
    title: 'Execution / The Hand',
    question: 'What authorized actions are executing right now?',
    sources: ['The Hand · orders & fills', 'Broker / custodian', 'The Book · execution records'],
    actions: ['Open action', 'Cancel if authorized', 'Reconcile', 'Export execution'],
    metrics: [['Orders today', '9,625'], ['Filled', '8,751'], ['Partial', '612'], ['Avg slippage', '1.83 bps']],
    items: [['HAND-A-91221', 'BUY AMD 250 sh', 'Filled · IBKR'], ['HAND-A-91220', 'SELL NVDA 120 sh', 'Filled · IBKR'], ['HAND-A-91219', 'BUY AAPL 80 sh', 'Partial · Fidelity'], ['HAND-A-91218', 'CANCEL MSFT', 'Acknowledged']],
  },
  risk: {
    title: 'Risk / Watchman',
    question: 'What is Watchman approving, restricting, or blocking?',
    sources: ['Watchman · decisions', 'Benjamin · risk metrics', 'The Book · risk records'],
    actions: ['View Watchman log', 'Adjust governed limits', 'Run scenario', 'Export risk'],
    metrics: [['Risk utilization', '31%'], ['Daily loss', '14%'], ['Aggregate drawdown', '6.2%'], ['Accounts near limit', '22']],
    items: [['BEN-000184', 'NORMAL', '31% risk utilization'], ['BEN-000186', 'WATCH', '34% risk utilization'], ['BEN-000187', 'RESTRICTED', 'Drawdown threshold'], ['BEN-000190', 'NORMAL', '21% risk utilization']],
  },
  strategies: {
    title: 'Strategies',
    question: 'How are strategies performing?',
    sources: ['The Book · strategies', 'Benjamin · performance', 'Watchman · limits'],
    actions: ['Open strategy', 'View model detail', 'View attribution', 'Export'],
    metrics: [['Active', '12'], ['Shadow', '9'], ['Restricted', '2'], ['Demoted', '1']],
    items: [['EPX-SCALP-003', '+$742,118', 'Qualified · active'], ['EPX-SCALP-001', '+$301,552', 'Qualified · active'], ['EPX-REV-002', '+$129,914', 'Watch'], ['EPX-MOM-001', '+$84,667', 'Qualified · active']],
  },
  intelligence: {
    title: 'Intelligence / Calibration',
    question: 'How is Benjamin learning and calibrated?',
    sources: ['Benjamin · learning', 'ZLJ · data quality', 'The Book · calibration records'],
    actions: ['View model detail', 'Recalibrate candidate', 'Run backtest', 'Export'],
    metrics: [['Calibration score', '0.86'], ['Decision precision', '82.7%'], ['Drift alerts', '3'], ['Candidate models', '7']],
    items: [['Microstructure model 04', '0.89 calibrated', 'Directional liquid regime'], ['Regime classifier 02', '0.92 calibrated', 'All qualified feeds'], ['Slippage model 03', '0.81 calibrated', 'Review high-vol tail'], ['Reasoner policy 01', '0.84 calibrated', 'Shadow successor pending']],
  },
  book: {
    title: 'Book / Evidence',
    question: 'Can we reconstruct any material event from start to finish?',
    sources: ['The Book · records', 'Evidence vault · source objects', 'All producing organs'],
    actions: ['Search Book', 'View evidence', 'Export', 'Verify receipt'],
    metrics: [['Material records', '1.48M'], ['Broken lineage', '0'], ['Reconciliation breaks', '3'], ['Public disclosures', '12']],
    items: [['BOOK-991442', 'BEN-D-084921', 'Observation → Decision → Governance → Execution → Outcome'], ['BOOK-991441', 'HAND-A-91221', 'Execution reconciled'], ['BOOK-991440', 'WATCH-11822', 'Authorization verified'], ['BOOK-991439', 'ZLJ-P-22781', 'Prediction evaluated']],
  },
  compliance: {
    title: 'Compliance',
    question: 'Are we operating inside the current compliance posture?',
    sources: ['Compliance system', 'The Book · compliance records', 'Account mandates'],
    actions: ['Open alert', 'Run report', 'Acknowledge', 'Export'],
    metrics: [['Open alerts', '4'], ['Due reviews', '11'], ['Restricted accounts', '7'], ['Exceptions', '2']],
    items: [['KYC refresh', '11 accounts', 'Due within 30 days'], ['Mandate exception', 'BEN-000187', 'Under review'], ['Trade restriction', '2 instruments', 'Current policy'], ['Disclosure package', 'Q3', 'Draft']],
  },
  operations: {
    title: 'Operations',
    question: 'What operational issues require attention?',
    sources: ['Operations system', 'Custodian / broker', 'The Book · ops records'],
    actions: ['Resolve exception', 'Reconcile', 'View details', 'Export ops'],
    metrics: [['Exceptions', '9'], ['Reconciliation breaks', '3'], ['Pending transfers', '2'], ['SLA breaches', '0']],
    items: [['OPS-442', 'Account sync delayed', 'Investigating'], ['OPS-441', 'Transfer pending review', 'Owner action'], ['OPS-440', 'Receipt mismatch', 'Reconciliation'], ['OPS-439', 'Custodian heartbeat', 'Resolved']],
  },
  system: {
    title: 'System',
    question: 'Is every Epinnox organ healthy?',
    sources: ['Monitoring', 'System health', 'Deployment records'],
    actions: ['View detail', 'Restart governed service', 'View logs', 'Configure alerts'],
    metrics: [['ZLJ', 'OPERATIONAL'], ['Benjamin', 'OPERATIONAL'], ['Watchman', 'OPERATIONAL'], ['The Hand', 'OPERATIONAL']],
    items: [['The Book', 'OPERATIONAL', '0 integrity errors'], ['ZLJ market data', 'VALID', '18 qualified feeds'], ['Benjamin reasoner', 'OPERATIONAL', 'Decision latency normal'], ['The Hand adapters', 'OPERATIONAL', '3 providers healthy']],
  },
  'owner-command': {
    title: 'Owner Command',
    question: 'Ask Benjamin anything across the enterprise.',
    sources: ['Benjamin · reasoning', 'The Book · results', 'Authorized enterprise read models'],
    actions: ['Ask question', 'Save query', 'Open result', 'Schedule governed report'],
    metrics: [['Context domains', '14'], ['Freshness', '8 sec'], ['Open investigations', '3'], ['Protected claims', 'ENFORCED']],
    items: [['“Why did risk rise this morning?”', 'Ready', 'Evidence-bound answer'], ['“Which client accounts are near drawdown limits?”', 'Ready', 'Account-scoped'], ['“What changed in EPX-SCALP-003?”', 'Ready', 'Calibration + performance'], ['“Where are reconciliation breaks?”', 'Ready', 'Operations + Book']],
  },
  reports: {
    title: 'Reports',
    question: 'What governed reports can the enterprise produce?',
    sources: ['The Book · reports', 'All authorized read models'],
    actions: ['Generate report', 'Schedule', 'Download', 'Share'],
    metrics: [['Scheduled', '18'], ['Generated today', '31'], ['Client reports', '22'], ['Internal reports', '9']],
    items: [['Enterprise operating report', 'Daily', 'Internal'], ['Client account statement', 'Monthly', 'Client scoped'], ['Risk utilization report', 'Daily', 'Internal'], ['Calibration report', 'Weekly', 'Research / governance']],
  },
  audit: {
    title: 'Audit & History',
    question: 'What is the full audit trail?',
    sources: ['The Book · audit', 'Auth system', 'All producing organs'],
    actions: ['Search audit', 'Filter', 'Export', 'Inspect receipt'],
    metrics: [['Events today', '84,291'], ['Privileged changes', '7'], ['Failed checks', '0'], ['Unverified records', '0']],
    items: [['AUD-77492', 'Mandate changed · BEN-000190', 'Owner authorized'], ['AUD-77491', 'Watchman policy promoted', 'Governance receipt'], ['AUD-77490', 'Hand adapter version changed', 'Deployment receipt'], ['AUD-77489', 'Book verification completed', 'Valid']],
  },
  governance: {
    title: 'Settings & Governance',
    question: 'How do we configure and govern the enterprise?',
    sources: ['Governance system', 'The Book · governance records', 'Policy registry'],
    actions: ['Edit setting', 'Manage roles', 'Configure integrations', 'Save governed change'],
    metrics: [['Active policies', '43'], ['Roles', '9'], ['Integrations', '12'], ['Pending changes', '2']],
    items: [['Mandate templates', '6 active', 'Version controlled'], ['Watchman policy set', 'v14', 'Current'], ['Execution capability registry', '23 capabilities', '12 production-disabled'], ['Disclosure policy', 'v5', 'Current']],
  },
};

const performancePoints = [4, 8, 6, 12, 9, 15, 13, 21, 18, 24, 20, 17, 26, 31, 28, 34, 30, 39, 46, 43, 51, 48, 57, 54, 63, 67, 61, 72, 78, 75, 82, 88, 84];

function LineChart({ compact = false }: { compact?: boolean }) {
  const width = compact ? 180 : 620;
  const height = compact ? 56 : 190;
  const max = Math.max(...performancePoints);
  const min = Math.min(...performancePoints);
  const points = performancePoints.map((value, index) => {
    const x = (index / (performancePoints.length - 1)) * width;
    const y = height - ((value - min) / (max - min || 1)) * (height - 16) - 8;
    return `${x},${y}`;
  }).join(' ');
  return (
    <svg className={compact ? 'sparkline' : 'line-chart'} viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Synthetic performance chart">
      {!compact && <><line x1="0" y1="45" x2={width} y2="45" /><line x1="0" y1="95" x2={width} y2="95" /><line x1="0" y1="145" x2={width} y2="145" /></>}
      <polyline points={points} fill="none" vectorEffect="non-scaling-stroke" />
    </svg>
  );
}

function Pill({ children, tone = 'good' }: { children: string; tone?: 'good' | 'warn' | 'bad' | 'muted' }) {
  return <span className={`pill pill-${tone}`}><i />{children}</span>;
}

function Metric({ label, value, sub }: { label: string; value: string; sub?: string }) {
  return <div className="metric"><span>{label}</span><strong>{value}</strong>{sub && <small>{sub}</small>}</div>;
}

function CommandOverview({ onOpenClients, onOpenAccounts }: { onOpenClients: () => void; onOpenAccounts: () => void }) {
  return (
    <div className="screen-stack">
      <section className="section-frame command-frame">
        <header className="frame-title"><span>1.</span><h1>Command Overview</h1><Pill>DESIGN / SHADOW</Pill></header>
        <div className="metric-strip six">
          <Metric label="Total client AUM" value="$87,642,193" sub="+$1,284,771 · 1.48%" />
          <Metric label="Benjamin principal capital" value="$5,421,883" sub="+$87,543 · 1.64%" />
          <Metric label="Total capital" value="$93,064,076" sub="+$1,372,314 · 1.50%" />
          <Metric label="Capital deployed" value="$58,391,772" sub="62.77%" />
          <Metric label="Total cash" value="$34,672,304" sub="37.23%" />
          <Metric label="Daily P&L (net)" value="$1,284,771" sub="1.48%" />
        </div>

        <div className="command-grid">
          <article className="panel chart-panel span-5">
            <div className="panel-head"><div><span>Fleet Performance (Net)</span><strong>All managed accounts + principal</strong></div><div className="range-tabs"><b>1D</b><b>1W</b><b>1M</b><b className="active">ALL</b></div></div>
            <LineChart />
            <div className="chart-axis"><span>Apr 15</span><span>Apr 29</span><span>May 13</span></div>
          </article>
          <article className="panel span-3">
            <div className="panel-head"><span>Accounts Summary</span><button onClick={onOpenAccounts}>OPEN</button></div>
            <div className="donut-wrap"><div className="donut"><strong>512</strong><span>accounts</span></div><ul><li><i className="c-good" />Active <b>487</b></li><li><i className="c-warn" />Onboarding <b>11</b></li><li><i className="c-yellow" />Restricted <b>7</b></li><li><i className="c-bad" />Attention <b>7</b></li></ul></div>
          </article>
          <article className="panel span-4">
            <div className="panel-head"><span>Risk Overview</span><button>VIEW</button></div>
            <div className="risk-bars">
              <div><span>Risk Utilization</span><b>31%</b><i><em style={{ width: '31%' }} /></i></div>
              <div><span>Daily Loss</span><b>14%</b><i><em style={{ width: '14%' }} /></i></div>
              <div><span>Drawdown (Aggregate)</span><b>6.2%</b><i><em style={{ width: '26%' }} /></i></div>
              <div><span>Largest Concentration</span><b>8.4%</b><i><em style={{ width: '42%' }} /></i></div>
              <div><span>Accounts Near Limits</span><b>22</b><i><em style={{ width: '18%' }} /></i></div>
            </div>
          </article>
        </div>

        <div className="command-grid lower-grid">
          <article className="panel span-3"><div className="panel-head"><span>Decisions Today</span></div><strong className="big-number">8,412</strong><div className="mini-list"><span>Authorized <b>7,391</b></span><span>Blocked / restricted <b>924</b></span><span>Abstained <b>97</b></span></div><LineChart compact /></article>
          <article className="panel span-3"><div className="panel-head"><span>Execution Today</span></div><div className="mini-list"><span>Orders <b>9,625</b></span><span>Filled <b>8,751</b></span><span>Partial <b>612</b></span><span>Rejected <b>262</b></span><span>Avg slippage <b>1.83 bps</b></span></div></article>
          <article className="panel span-3"><div className="panel-head"><span>Top Strategies (MTD Net)</span></div><div className="strategy-bars">{[['EPX-SCALP-003','$742,118','86%'],['EPX-SCALP-001','$301,552','64%'],['EPX-REV-002','$129,914','42%'],['EPX-MOM-001','$84,667','31%']].map(([name,val,w]) => <div key={name}><span>{name}</span><i><em style={{width:w}} /></i><b>{val}</b></div>)}</div></article>
          <article className="panel span-3"><div className="panel-head"><span>Alerts & Exceptions</span></div><div className="alert-list"><span>Accounts near daily loss limit <b>4</b></span><span>Accounts near drawdown limit <b>6</b></span><span>Data quality degraded <b>1</b></span><span>Reconciliation exceptions <b>3</b></span><span>Withdrawals pending review <b>2</b></span></div><button className="view-all" onClick={onOpenClients}>VIEW ALL →</button></article>
        </div>
      </section>

      <ClientsOverview onOpenClient={onOpenClients} embedded />
    </div>
  );
}

function ClientsOverview({ onOpenClient, embedded = false }: { onOpenClient: () => void; embedded?: boolean }) {
  const [query, setQuery] = useState('');
  const filtered = clients.filter((client) => `${client.id} ${client.name}`.toLowerCase().includes(query.toLowerCase()));
  return (
    <section className="section-frame">
      <header className="frame-title"><span>{embedded ? '2.' : ''}</span><h1>Clients Overview</h1><div className="header-actions"><button>FILTERS</button><button>EXPORT</button></div></header>
      <div className="filter-row"><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search clients…" /><select><option>Status · All</option></select><select><option>Mandate · All</option></select><select><option>Risk · All</option></select><select><option>Location · All</option></select></div>
      <div className="table-wrap"><table><thead><tr><th>Client ID</th><th>Client name</th><th>Status</th><th>Mandate</th><th>AUM (USD)</th><th>MTD (Net %)</th><th>YTD (Net %)</th><th>Since inception</th><th>Max DD</th><th>Risk</th><th>Last activity</th></tr></thead><tbody>{filtered.map((client) => <tr key={client.id} onClick={onOpenClient} className="click-row"><td className="mono accent">{client.id}</td><td>{client.name}</td><td><Pill tone={client.status === 'Active' ? 'good' : 'warn'}>{client.status}</Pill></td><td>{client.mandate}</td><td className="positive">{client.aum}</td><td className={client.mtd.startsWith('-') ? 'negative' : 'positive'}>{client.mtd}</td><td className="positive">{client.ytd}</td><td className="positive">{client.inception}</td><td>{client.drawdown}</td><td>{client.risk}</td><td>{client.last}</td></tr>)}</tbody><tfoot><tr><td colSpan={2}>TOTAL / AVERAGE</td><td>{filtered.length}</td><td>—</td><td>$87,642,193</td><td className="positive">+2.96%</td><td className="positive">+16.84%</td><td className="positive">+24.17%</td><td>-6.45%</td><td>31%</td><td>—</td></tr></tfoot></table></div>
    </section>
  );
}

function ClientDetail({ onBack }: { onBack: () => void }) {
  const client = clients[0];
  return (
    <section className="section-frame">
      <header className="frame-title"><span>B</span><h1>Client Detail — {client.id} ({client.name})</h1><button onClick={onBack}>BACK TO CLIENTS</button></header>
      <div className="client-identity-strip"><div><span>{client.id}</span><strong>{client.name}</strong></div><div><span>Status</span><strong className="positive">Active</strong></div><div><span>Mandate</span><strong>{client.mandate}</strong></div><div><span>Opened</span><strong>Jan 18, 2027</strong><small>405 days</small></div><div><span>Custodian</span><strong>Interactive Brokers</strong><small>USD account</small></div><div><span>AUM</span><strong>{client.aum}</strong></div><div><span>MTD (Net)</span><strong className="positive">{client.mtd}</strong></div><div><span>YTD (Net)</span><strong className="positive">{client.ytd}</strong></div><div><span>Since inception</span><strong className="positive">{client.inception}</strong></div></div>
      <div className="detail-tabs"><b className="active">Overview</b><b>Account</b><b>Performance</b><b>Positions</b><b>Activity</b><b>Decisions</b><b>Risk</b><b>Documents</b><b>Book</b><b>Communications</b></div>
      <div className="detail-grid">
        <article className="panel detail-chart"><div className="panel-head"><span>Equity Curve (Net)</span><div className="range-tabs"><b>1D</b><b>1W</b><b>1M</b><b>3M</b><b>YTD</b><b>1Y</b><b className="active">ALL</b></div></div><LineChart /><div className="chart-axis"><span>Jan ’27</span><span>Mar ’27</span><span>May ’27</span></div></article>
        <article className="panel capital-summary"><div className="panel-head"><span>Capital Summary</span></div>{[['Starting Capital','$25,000.00'],['Net Deposits','$5,000.00'],['Net Withdrawals','$1,500.00'],['Gross Trading P&L','$4,182.31'],['Fees (Advisory)','-$1,092.41'],['Trading Costs (Est.)','-$983.18'],['Net Investment Result','$3,491.72'],['Current Equity','$28,491.72']].map(([a,b],i)=><div className={i===7?'summary-row total':'summary-row'} key={a}><span>{a}</span><strong className={b.startsWith('-')?'negative':''}>{b}</strong></div>)}</article>
        <article className="panel risk-snapshot"><div className="panel-head"><span>Risk Snapshot</span></div><div className="risk-ring"><strong>31%</strong><span>risk utilization</span></div><div className="mini-list"><span>Daily loss utilization <b>14%</b></span><span>Drawdown (this account) <b>-5.21%</b></span><span>Max drawdown <b>-7.21%</b></span><span>Exposure <b>22.47%</b></span><span>Watchman status <b className="positive">NORMAL</b></span></div></article>
        <article className="panel positions-panel"><div className="panel-head"><span>Current Positions</span><button>VIEW FULL POSITIONS →</button></div><table><thead><tr><th>Symbol</th><th>Strategy</th><th>Qty</th><th>Market Value</th><th>Unrealized P&L</th><th>% Equity</th></tr></thead><tbody><tr><td>NVDA</td><td>EPX-SCALP-003</td><td>120</td><td>$3,842.40</td><td className="positive">+$312.48</td><td>13.49%</td></tr><tr><td>AMD</td><td>EPX-SCALP-003</td><td>250</td><td>$2,912.00</td><td className="positive">+$185.25</td><td>10.22%</td></tr><tr><td>AAPL</td><td>EPX-SCALP-001</td><td>80</td><td>$1,658.40</td><td className="positive">+$96.32</td><td>5.82%</td></tr></tbody></table></article>
        <article className="panel activity-panel"><div className="panel-head"><span>Recent Activity</span><button>VIEW ALL ACTIVITY →</button></div><div className="timeline"><div><time>10:42 AM</time><span>Sold NVDA 120 sh</span><b className="positive">+$156.72</b></div><div><time>10:38 AM</time><span>Bought AMD 250 sh</span><b>—</b></div><div><time>10:31 AM</time><span>Watchman blocked order (position limit)</span><b className="negative">Blocked</b></div><div><time>10:26 AM</time><span>Sold AAPL 80 sh</span><b className="positive">+$96.32</b></div><div><time>10:19 AM</time><span>Bought NVDA 100 sh</span><b>—</b></div></div></article>
      </div>
    </section>
  );
}

function AccountsOverview() {
  return (
    <section className="section-frame">
      <header className="frame-title"><span>4.</span><h1>Accounts Overview</h1><div className="header-actions"><button>COLUMNS</button><button>EXPORT</button></div></header>
      <div className="filter-row"><input placeholder="Search accounts…" /><select><option>Status · All</option></select><select><option>Custodian · All</option></select><select><option>Mandate · All</option></select><select><option>Risk · All</option></select><button>More Filters</button></div>
      <div className="table-wrap"><table><thead><tr><th>Account ID</th><th>Client ID</th><th>Client name</th><th>Custodian</th><th>Mandate</th><th>AUM (USD)</th><th>Cash</th><th>Deployed</th><th>Risk %</th><th>Status</th><th>Last sync</th></tr></thead><tbody>{clients.map(client => <tr key={client.account}><td className="mono accent">{client.account}</td><td className="mono accent">{client.id}</td><td>{client.name}</td><td>{client.custodian}</td><td>{client.mandate}</td><td className="positive">{client.aum}</td><td>{client.cash}</td><td>{client.deployed}</td><td>{client.risk}</td><td><Pill tone={client.status==='Active'?'good':'warn'}>{client.status}</Pill></td><td>{client.last}</td></tr>)}</tbody></table></div>
      <div className="account-summary-grid"><article className="panel"><div className="panel-head"><span>Accounts by Status</span></div><div className="donut-wrap"><div className="donut"><strong>512</strong><span>total</span></div><ul><li><i className="c-good" />Active <b>487</b></li><li><i className="c-warn" />Onboarding <b>11</b></li><li><i className="c-yellow" />Restricted <b>7</b></li><li><i className="c-bad" />Closed <b>7</b></li></ul></div></article><article className="panel"><div className="panel-head"><span>AUM by Custodian</span></div><div className="horizontal-bars">{[['Interactive Brokers','$62.41M','92%'],['Fidelity','$15.82M','48%'],['Schwab','$6.71M','26%'],['Other','$2.70M','12%']].map(([a,b,w])=><div key={a}><span>{a}</span><i><em style={{width:w}} /></i><b>{b}</b></div>)}</div></article><article className="panel"><div className="panel-head"><span>AUM by Mandate</span></div><div className="donut-wrap"><div className="donut mandate"><strong>$87.64M</strong><span>total</span></div><ul><li><i className="c-good" />BM-SCALP-01 <b>$58.21M</b></li><li><i className="c-warn" />BM-SCALP-03 <b>$18.93M</b></li><li><i className="c-yellow" />BM-REV-02 <b>$6.72M</b></li><li><i className="c-blue" />BM-MOM-01 <b>$3.79M</b></li></ul></div></article></div>
    </section>
  );
}

function OperationalSurface({ spec }: { spec: SurfaceSpec }) {
  return (
    <section className="section-frame operational-surface">
      <header className="frame-title"><span>•</span><div><h1>{spec.title}</h1><p>{spec.question}</p></div><Pill>DESIGN / SHADOW</Pill></header>
      <div className="metric-strip four">{spec.metrics.map(([label,value])=><Metric key={label} label={label} value={value} />)}</div>
      <div className="surface-grid">
        <article className="panel span-8"><div className="panel-head"><span>Current operational view</span><button>REFRESH</button></div><div className="surface-list">{spec.items.map(([name,value,note])=><div key={name}><strong>{name}</strong><span>{value}</span><small>{note}</small></div>)}</div></article>
        <article className="panel span-4"><div className="panel-head"><span>Authoritative inputs</span></div><ul className="source-list">{spec.sources.map(source=><li key={source}>{source}</li>)}</ul><div className="panel-head action-title"><span>Available destinations</span></div><div className="action-stack">{spec.actions.map(action=><button key={action}>{action}</button>)}</div></article>
      </div>
    </section>
  );
}

export function App() {
  const [active, setActive] = useState('command');
  const activeItem = useMemo(() => navItems.find(item => item.key === active), [active]);

  const openClientDetail = () => setActive('client-detail');
  const renderScreen = () => {
    if (active === 'command') return <CommandOverview onOpenClients={() => setActive('clients')} onOpenAccounts={() => setActive('accounts')} />;
    if (active === 'clients') return <ClientsOverview onOpenClient={openClientDetail} />;
    if (active === 'client-detail') return <ClientDetail onBack={() => setActive('clients')} />;
    if (active === 'accounts') return <AccountsOverview />;
    const spec = surfaceSpecs[active];
    return spec ? <OperationalSurface spec={spec} /> : null;
  };

  return (
    <div className="command-shell">
      <aside className="sidebar">
        <div className="brand-block"><div className="brand-shield">B</div><div><strong>BENJAMIN COMMAND</strong><span>EPINNOX OWNER / MANAGER</span></div></div>
        <nav>{navItems.map(item => <button key={item.key} className={active === item.key || (active === 'client-detail' && item.key === 'clients') ? 'nav-item active' : 'nav-item'} onClick={() => setActive(item.key)}><span className="nav-glyph">{item.glyph}</span><span>{item.label}</span></button>)}</nav>
        <div className="sidebar-footer"><span>ENVIRONMENT</span><strong><i />DESIGN / SHADOW</strong><small>No live client capital is represented.</small></div>
      </aside>
      <main className="workspace">
        <header className="topbar"><div className="top-title">OWNER / MANAGER EXPERIENCE <span>— {active === 'client-detail' ? 'CLIENT DETAIL' : activeItem?.label.toUpperCase()}</span></div><div className="organ-status"><span><i />ZLJ</span><span><i />BENJAMIN</span><span><i />WATCHMAN</span><span><i />THE HAND</span><span><i />THE BOOK</span></div><button className="owner-chip"><b>DJ</b><span>Founder / Owner</span>⌄</button></header>
        <div className="ticker"><span>MARKET REGIME: HIGH VOLATILITY</span><b>VIX 22.41 ▲ 1.32</b><b>SPX 5,287.31 ▲ 0.81%</b><b>NASDAQ 16,734.63 ▲ 1.21%</b><b>BTC 68,882.11 ▲ 0.67%</b></div>
        <div className="workspace-scroll">{renderScreen()}</div>
      </main>
    </div>
  );
}
