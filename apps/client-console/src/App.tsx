import { useMemo, useState } from 'react';
import {
  clientActivity,
  clientDecisions,
  clientEvidence,
  clientProjectionStatus,
  clientProjections,
  type ClientViewMode,
} from './client-projection';

type PageKey = 'capital' | 'participation' | 'performance' | 'activity' | 'benjamin' | 'responsibility' | 'protection' | 'executions' | 'book' | 'statements';
type NavItem = { key: PageKey; label: string; glyph: string; group: string };

const navItems: NavItem[] = [
  { key: 'capital', label: 'My Capital', glyph: '⌂', group: 'My Money' },
  { key: 'participation', label: 'My Participation', glyph: '◎', group: 'My Money' },
  { key: 'performance', label: 'Performance', glyph: '⌁', group: 'My Money' },
  { key: 'activity', label: 'Activity', glyph: '◇', group: 'My Money' },
  { key: 'benjamin', label: 'Benjamin', glyph: '◉', group: 'Management' },
  { key: 'responsibility', label: 'Responsibility', glyph: '▣', group: 'Management' },
  { key: 'protection', label: 'Watchman Protection', glyph: '⬡', group: 'Management' },
  { key: 'executions', label: 'Executions', glyph: '▤', group: 'Evidence' },
  { key: 'book', label: 'The Book', glyph: '▧', group: 'Evidence' },
  { key: 'statements', label: 'Statements & Documents', glyph: '▥', group: 'Evidence' },
];

function Topbar({ page, mode, setMode }: { page: PageKey; mode: ClientViewMode; setMode: (mode: ClientViewMode) => void }) {
  const item = navItems.find((entry) => entry.key === page)!;
  return <header className="cc-top">
    <div><div className="cc-eyebrow">Benjamin Capital Management / Client Console / Synthetic Contract Preview</div><h1>{item.label}</h1><p>{page === 'capital' ? 'See the capital Benjamin is responsible for managing for you, without exposing company-private intelligence or another participant’s records.' : 'This view is a privacy-scoped projection of the same capital structure, responsibility, decision, governance, execution, and evidence model used by the manager console.'}</p></div>
    <div className="cc-switcher" aria-label="Preview client identity"><button className={mode === 'INDIVIDUAL_OWNER' ? 'active' : ''} onClick={() => setMode('INDIVIDUAL_OWNER')}>Individual owner</button><button className={mode === 'POOLED_PARTICIPANT' ? 'active' : ''} onClick={() => setMode('POOLED_PARTICIPANT')}>Pooled participant</button></div>
  </header>;
}

function Sidebar({ page, setPage }: { page: PageKey; setPage: (page: PageKey) => void }) {
  const groups = [...new Set(navItems.map((item) => item.group))];
  return <aside className="cc-sidebar"><div className="cc-brand"><div className="cc-brand-mark">B</div><div><strong>BENJAMIN</strong><small>Client Capital</small></div></div><nav className="cc-nav">{groups.map((group) => <div key={group} style={{display:'contents'}}><div className="cc-nav-label">{group}</div>{navItems.filter((item) => item.group === group).map((item) => <button key={item.key} className={page === item.key ? 'active' : ''} onClick={() => setPage(item.key)}><span>{item.glyph}</span><span>{item.label}</span></button>)}</div>)}</nav><div className="cc-side-foot">Product mode <b>{clientProjectionStatus.productMode}</b><br/>Synthetic data <b>YES</b><br/>Other participant PII <b>HIDDEN</b><br/>Live money movement <b>OFF</b></div></aside>;
}

function Metric({ label, value, note, tone }: { label: string; value: string; note: string; tone?: 'positive' | 'negative' }) {
  return <article className="cc-card cc-metric"><span>{label}</span><strong className={tone === 'positive' ? 'cc-positive' : tone === 'negative' ? 'cc-negative' : ''}>{value}</strong><small>{note}</small></article>;
}

function CapitalHome({ mode }: { mode: ClientViewMode }) {
  const projection = clientProjections[mode];
  return <>
    <section className="cc-card cc-hero"><div className="cc-hero-grid"><div><div className="cc-eyebrow" style={{color:'#75dcff'}}>YOUR CAPITAL / YOUR AUTHORIZED VIEW</div><h2>{projection.currentValue} <em>managed under responsibility</em></h2><p>{mode === 'INDIVIDUAL_OWNER' ? 'You own the entire economic structure shown here. Benjamin manages inside the authority defined for your structure; custody remains external/client-owned in this preview.' : `You own a ${projection.economicInterestPct}% economic interest in ${projection.structureName}. Benjamin manages the shared pool under one Responsibility; your private records remain separate from other participants.`}</p></div><div className="cc-hero-side"><span>Capital structure</span><strong>{projection.structureName}</strong><span>Your role</span><strong>{projection.mode.replaceAll('_',' ')}</strong><span>Reporting scope</span><strong>{projection.reportingScope}</strong><span>Watchman</span><strong><b>{projection.watchmanStatus}</b></strong></div></div></section>
    <section className="cc-grid metrics"><Metric label="Current value" value={projection.currentValue} note="Your economic capital projection"/><Metric label="Net gain / loss" value={projection.netGainLoss} note="After preview contributions before full accounting backend" tone="positive"/><Metric label="Cash / liquidity" value={projection.cashShare} note="Your account or economic share"/><Metric label="Invested / deployed" value={projection.investedShare} note="Your account or economic share"/></section>
    <section className="cc-grid two">
      <article className="cc-card"><div className="cc-card-head"><div><h2>Where your money stands</h2><p>Capital ownership and Benjamin management are separate concepts.</p></div><span className="cc-status good">SCOPED TO YOU</span></div><div className="cc-detail"><span>Contributed capital</span><strong>{projection.contributedCapital}</strong></div><div className="cc-detail"><span>Distributions / withdrawals</span><strong>{projection.distributedCapital}</strong></div><div className="cc-detail"><span>Fees allocated to you</span><strong>{projection.fees}</strong></div><div className="cc-detail"><span>Economic interest</span><strong>{projection.economicInterestPct}%</strong></div><div className="cc-detail"><span>Custody</span><strong>{projection.custodyLabel}</strong></div></article>
      <article className="cc-card"><div className="cc-card-head"><div><h2>What Benjamin is responsible for</h2><p>The current Responsibility governs the money logic.</p></div><span className="cc-status good">VERSION {projection.responsibilityVersion}</span></div><div className="cc-detail"><span>Responsibility</span><strong>{projection.responsibilityName}</strong></div><div className="cc-detail"><span>Primary objective</span><strong>{projection.primaryObjective}</strong></div><div className="cc-detail"><span>Maximum drawdown</span><strong>{projection.maxDrawdown}</strong></div><div className="cc-detail"><span>Minimum liquidity</span><strong>{projection.minLiquidity}</strong></div><div className="cc-detail"><span>Benjamin autonomy</span><strong>{projection.autonomy}</strong></div></article>
    </section>
    <div className="cc-banner"><b>Client truth rule:</b> this frontend will ultimately be calculated from Book/accounting records and authorized projections. It will not invent performance from Benjamin’s forecasts, and pooled participants will never inherit another participant’s private information.</div>
  </>;
}

function Participation({ mode }: { mode: ClientViewMode }) {
  const p = clientProjections[mode];
  return <><section className="cc-card cc-hero"><div className="cc-hero-grid"><div><div className="cc-eyebrow" style={{color:'#75dcff'}}>OWNERSHIP / ECONOMIC RIGHTS</div><h2>{p.economicInterestPct}% <em>{mode === 'INDIVIDUAL_OWNER' ? 'ownership' : 'economic interest'}</em></h2><p>{mode === 'INDIVIDUAL_OWNER' ? 'Your structure is individually owned in this preview, so your economic view is the whole structure.' : 'Your participation entitles you to your economic share and permitted structure reporting. It does not give you access to another participant’s private records or unilateral trading authority over the pool.'}</p></div><div className="cc-hero-side"><span>Participant id</span><strong>{p.participantId}</strong><span>Relationship id</span><strong>{p.relationshipId}</strong><span>Structure</span><strong>{p.structureId}</strong><span>Scope</span><strong>{p.reportingScope}</strong></div></div></section><section className="cc-grid two"><article className="cc-card"><div className="cc-card-head"><div><h2>Your economic ledger</h2><p>The future accounting backend must make every allocation reproducible.</p></div><span className="cc-status warn">BACKEND PENDING</span></div><div className="cc-detail"><span>Contributions</span><strong>{p.contributedCapital}</strong></div><div className="cc-detail"><span>Current interest value</span><strong>{p.currentValue}</strong></div><div className="cc-detail"><span>Net gain / loss</span><strong className="cc-positive">{p.netGainLoss}</strong></div><div className="cc-detail"><span>Fees</span><strong>{p.fees}</strong></div><div className="cc-detail"><span>Distributions</span><strong>{p.distributedCapital}</strong></div></article><article className="cc-card"><div className="cc-card-head"><div><h2>Your rights vs shared authority</h2></div></div><div className="cc-list"><div className="cc-list-row"><b>✓</b><span>View your economic interest and capital activity</span><small>YES</small></div><div className="cc-list-row"><b>✓</b><span>View permitted portfolio/Benjamin activity affecting you</span><small>YES</small></div><div className="cc-list-row"><b>×</b><span>View another participant’s private records</span><small>NO</small></div><div className="cc-list-row"><b>×</b><span>Inject unilateral trade instructions into a shared pool</span><small>NO</small></div><div className="cc-list-row"><b>×</b><span>Withdraw another participant’s capital</span><small>NO</small></div></div></article></section></>;
}

function Performance({ mode }: { mode: ClientViewMode }) {
  const p=clientProjections[mode];
  return <><section className="cc-grid metrics"><Metric label="Opening contributed capital" value={p.contributedCapital} note="Preview basis"/><Metric label="Current value" value={p.currentValue} note="Authorized projection"/><Metric label="Net gain / loss" value={p.netGainLoss} note="Not a guaranteed return" tone="positive"/><Metric label="Fees" value={p.fees} note="Allocated to your interest"/></section><section className="cc-grid two"><article className="cc-card"><div className="cc-card-head"><div><h2>Performance decomposition</h2><p>The final backend will distinguish market P&L, realized/unrealized P&L, fees, cash flows, and participant allocation.</p></div><span className="cc-status warn">CONTRACT</span></div>{['Contributions / redemptions','Realized P&L','Unrealized P&L','Fees and costs','Distributions','Ending capital'].map((item,index)=><div className="cc-list-row" key={item}><b>{index+1}</b><span>{item}</span><small>Book-derived later</small></div>)}</article><article className="cc-card"><div className="cc-card-head"><div><h2>What performance will never mean</h2></div></div><div className="cc-privacy"><strong>Forecast ≠ earned return</strong><p>ZLJ intelligence or Benjamin expected benefit cannot be displayed as account performance. Only reconciled accounting outcomes belong here.</p></div><div className="cc-privacy" style={{marginTop:9}}><strong>Pool return ≠ your private cash flow</strong><p>Participant-level statements must account for when you entered/exited and the units/capital interest you actually owned.</p></div></article></section></>;
}

function Activity() {
  return <section className="cc-card"><div className="cc-card-head"><div><h2>Activity affecting your capital</h2><p>Decisions, governance, execution, and accounting are separate event types.</p></div><span className="cc-status warn">SYNTHETIC</span></div><table className="cc-table"><thead><tr><th>Reference</th><th>Type</th><th>Activity</th><th>Result / status</th></tr></thead><tbody>{clientActivity.map(([ref,type,action,status])=><tr key={ref}><td><strong>{ref}</strong></td><td>{type}</td><td>{action}</td><td>{status}</td></tr>)}</tbody></table></section>;
}

function BenjaminView() {
  return <><section className="cc-card cc-hero"><div className="cc-hero-grid"><div><div className="cc-eyebrow" style={{color:'#75dcff'}}>BENJAMIN / MONEY LOGIC</div><h2>What path did Benjamin choose <em>for this capital?</em></h2><p>Clients receive understandable capital-decision explanations, not proprietary model internals or raw ZLJ engineering data. The explanation still preserves the mandate, alternatives, and institutional chain.</p></div><div className="cc-hero-side"><span>Selected preview</span><strong>INCREASE BTC SPOT EXPOSURE</strong><span>Futures understanding</span><strong>USED AS INFORMATION</strong><span>Futures execution</span><strong>DISABLED</strong><span>Watchman</span><strong><b>PENDING</b></strong></div></div></section><section className="cc-card"><div className="cc-card-head"><div><h2>Decisions affecting your money</h2><p>Why a path was selected or rejected.</p></div><span className="cc-status warn">SYNTHETIC</span></div><table className="cc-table"><thead><tr><th>Path</th><th>Status</th><th>Explanation</th></tr></thead><tbody>{clientDecisions.map(([path,status,reason])=><tr key={path}><td><strong>{path}</strong></td><td>{status}</td><td>{reason}</td></tr>)}</tbody></table></section><div className="cc-banner"><b>Transparency boundary:</b> the client can see what Benjamin decided for their money and why in understandable economic terms. They do not need private model weights, source code, other clients’ portfolios, or raw laboratory internals.</div></>;
}

function Responsibility({ mode }: { mode: ClientViewMode }) {
  const p=clientProjections[mode];
  return <section className="cc-grid two"><article className="cc-card"><div className="cc-card-head"><div><h2>Current Responsibility</h2><p>The authority Benjamin must remain inside.</p></div><span className="cc-status good">VERSION {p.responsibilityVersion}</span></div><div className="cc-detail"><span>Name</span><strong>{p.responsibilityName}</strong></div><div className="cc-detail"><span>Objective</span><strong>{p.primaryObjective}</strong></div><div className="cc-detail"><span>Autonomy</span><strong>{p.autonomy}</strong></div><div className="cc-detail"><span>Max drawdown</span><strong>{p.maxDrawdown}</strong></div><div className="cc-detail"><span>Minimum liquidity</span><strong>{p.minLiquidity}</strong></div></article><article className="cc-card"><div className="cc-card-head"><div><h2>Important authority distinctions</h2></div></div><div className="cc-list"><div className="cc-list-row"><b>1</b><span>Benjamin can understand a market without being permitted to trade it.</span><small>UNDERSTAND ≠ EXECUTE</small></div><div className="cc-list-row"><b>2</b><span>Targets are objectives, not promised returns.</span><small>NO GUARANTEE</small></div><div className="cc-list-row"><b>3</b><span>Changing responsibility is governed and versioned.</span><small>NO SILENT CHANGE</small></div><div className="cc-list-row"><b>4</b><span>Watchman still governs every external-action path.</span><small>SEPARATE AUTHORITY</small></div></div></article></section>;
}

function Protection({ mode }: { mode: ClientViewMode }) {
  const p=clientProjections[mode];
  return <><section className="cc-grid metrics"><Metric label="Watchman status" value={p.watchmanStatus} note="Current preview governance state"/><Metric label="Max drawdown" value={p.maxDrawdown} note="Responsibility boundary"/><Metric label="Liquidity floor" value={p.minLiquidity} note="Responsibility boundary"/><Metric label="Execution authority" value="SEPARATE" note="Benjamin cannot self-authorize"/></section><section className="cc-card"><div className="cc-card-head"><div><h2>How your capital is protected structurally</h2><p>Benjamin proposes capital decisions; Watchman independently authorizes or blocks external action.</p></div><span className="cc-status good">SEPARATION OF DUTIES</span></div><div className="cc-list">{['Responsibility/mandate checked','Risk and concentration checked','Liquidity requirements checked','Allowed market/action checked','Only authorized intent may reach The Hand','The Book records the authority chain'].map((item,index)=><div className="cc-list-row" key={item}><b>{index+1}</b><span>{item}</span><small>Governed</small></div>)}</div></section></>;
}

function Executions() {
  return <section className="cc-card"><div className="cc-card-head"><div><h2>Execution activity</h2><p>Only Hand receipts and reconciled provider outcomes belong on this page.</p></div><span className="cc-status warn">SYNTHETIC</span></div><table className="cc-table"><thead><tr><th>Reference</th><th>State</th><th>Meaning</th></tr></thead><tbody><tr><td><strong>HAND-PREVIEW-021</strong></td><td>RECONCILED</td><td>Authorized spot reduction preview; provider result and internal receipt agree.</td></tr><tr><td><strong>BEN-D-PREVIEW-001</strong></td><td>NOT EXECUTION</td><td>A Benjamin decision remains merely a decision until Watchman authorizes and Hand acts.</td></tr></tbody></table></section>;
}

function Book() {
  return <><section className="cc-card"><div className="cc-card-head"><div><h2>Your evidence trail</h2><p>Account/participant-scoped proof without exposing unrelated institutional secrets.</p></div><span className="cc-status warn">SYNTHETIC</span></div><table className="cc-table"><thead><tr><th>Type</th><th>Reference</th><th>What it proves</th></tr></thead><tbody>{clientEvidence.map(([type,ref,meaning])=><tr key={ref}><td>{type}</td><td><strong>{ref}</strong></td><td>{meaning}</td></tr>)}</tbody></table></section><div className="cc-banner"><b>Book boundary:</b> a client should be able to verify the material story of their money—decision, governance, execution, accounting—without receiving other participants’ PII or proprietary ZLJ research artifacts.</div></>;
}

function Statements({ mode }: { mode: ClientViewMode }) {
  const p=clientProjections[mode];
  return <section className="cc-grid two"><article className="cc-card"><div className="cc-card-head"><div><h2>Statements</h2><p>Formal reporting projections to be derived from authoritative accounting.</p></div><span className="cc-status warn">BACKEND PENDING</span></div>{['Monthly capital statement','Quarterly performance statement','Contribution/redemption statement','Fee statement','Annual/tax package'].map((item,index)=><div className="cc-list-row" key={item}><b>{index+1}</b><span>{item}</span><small>Future Book-backed artifact</small></div>)}</article><article className="cc-card"><div className="cc-card-head"><div><h2>Statement scope</h2></div></div><div className="cc-detail"><span>Client</span><strong>{p.clientDisplayName}</strong></div><div className="cc-detail"><span>Structure</span><strong>{p.structureName}</strong></div><div className="cc-detail"><span>Participant/account scope</span><strong>{p.reportingScope}</strong></div><div className="cc-detail"><span>Other participant private data</span><strong>EXCLUDED</strong></div><div className="cc-detail"><span>Proprietary ZLJ internals</span><strong>EXCLUDED</strong></div></article></section>;
}

export function App() {
  const [page,setPage]=useState<PageKey>('capital');
  const [mode,setMode]=useState<ClientViewMode>('INDIVIDUAL_OWNER');
  const projection=useMemo(()=>clientProjections[mode],[mode]);
  let content;
  if(page==='capital') content=<CapitalHome mode={mode}/>;
  else if(page==='participation') content=<Participation mode={mode}/>;
  else if(page==='performance') content=<Performance mode={mode}/>;
  else if(page==='activity') content=<Activity/>;
  else if(page==='benjamin') content=<BenjaminView/>;
  else if(page==='responsibility') content=<Responsibility mode={mode}/>;
  else if(page==='protection') content=<Protection mode={mode}/>;
  else if(page==='executions') content=<Executions/>;
  else if(page==='book') content=<Book/>;
  else content=<Statements mode={mode}/>;

  return <div className="cc-shell"><Sidebar page={page} setPage={setPage}/><main className="cc-main"><Topbar page={page} mode={mode} setMode={setMode}/><div className="cc-privacy" style={{marginBottom:14}}><strong>{projection.clientDisplayName} · {projection.structureName}</strong><p>{projection.structureType} · {projection.reportingScope} · synthetic frontend-contract preview.</p></div>{content}</main></div>;
}
