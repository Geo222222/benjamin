import type { ComponentType } from 'react';

type TopbarProps = { title: string; description: string };

type StateRow = { label: string; value: string; note?: string };

const accounting: StateRow[] = [
  { label: 'Net asset value', value: '$185,500', note: 'Authoritative valuation projection' },
  { label: 'Gross assets', value: '$198,000' },
  { label: 'Gross liabilities', value: '$12,500' },
  { label: 'Cash balance', value: '$100,000' },
  { label: 'Provider-available cash', value: '$50,000', note: 'Before Benjamin internal obligations' },
  { label: 'Spot asset value', value: '$80,000' },
  { label: 'Derivative mark value', value: '-$2,000', note: 'Signed marked economic value, not notional' },
];

const obligations: StateRow[] = [
  { label: 'Operational reserve', value: '$5,000' },
  { label: 'Minimum liquidity', value: '$15,000' },
  { label: 'Pending redemptions', value: '$10,000' },
  { label: 'Pending withdrawals', value: '$2,000' },
  { label: 'Pending distributions', value: '$1,000' },
  { label: 'Pending inflows', value: '$25,000', note: 'Does not increase deployable capital until settled' },
];

const exposure: StateRow[] = [
  { label: 'Spot gross exposure', value: '$80,000' },
  { label: 'Derivative gross notional', value: '$40,000' },
  { label: 'Gross market exposure', value: '$120,000' },
  { label: 'Net market exposure', value: '$60,000' },
  { label: 'Collateral committed', value: '$12,000' },
  { label: 'Current drawdown', value: '4.20%' },
  { label: 'Risk budget remaining', value: '$25,000' },
];

function Rows({ rows }: { rows: StateRow[] }) {
  return <div className="bc-targets">{rows.map((row)=><div className="bc-target" key={row.label}><span>{row.label}</span><strong>{row.value}{row.note&&<small>{row.note}</small>}</strong></div>)}</div>;
}

export function CapitalStateSurface({ Topbar }: { Topbar: ComponentType<TopbarProps> }) {
  return <>
    <Topbar title="Capital State" description="The authoritative point-in-time economic state Benjamin must use before evaluating what this capital should do next." />

    <section className="bc-card bc-hero">
      <div className="bc-hero-grid">
        <div>
          <div className="bc-eyebrow">ACCOUNTING TRUTH → OBLIGATIONS → DEPLOYABILITY → ROUTER READINESS</div>
          <h2>Family Growth I: <em>FULL</em></h2>
          <p className="bc-hero-copy">Capital State is the money-side equivalent of ZLJ market state. It tells Benjamin what exists, what is committed, what is owed, what is stale or disputed, and how much capital is genuinely available for new risk.</p>
        </div>
        <div className="bc-constitution">
          <span>Capital State</span><strong>CAPSTATE-7C91…</strong>
          <span>As of</span><strong>2026-09-03 20:00:00Z</strong>
          <span>Reconciliation</span><strong><b>RECONCILED</b></strong>
          <span>Routing readiness</span><strong><b>FULL</b></strong>
        </div>
      </div>
    </section>

    <section className="bc-grid metrics">
      <article className="bc-card bc-metric"><label>Net asset value</label><strong>$185,500</strong><small>Valuation policy bound</small></article>
      <article className="bc-card bc-metric"><label>Liquidity available</label><strong>$17,000</strong><small>After reserves + pending outflows</small></article>
      <article className="bc-card bc-metric"><label>Risk capital available</label><strong>$17,000</strong><small>Min(liquidity, remaining risk budget)</small></article>
      <article className="bc-card bc-metric"><label>Pending obligations</label><strong>$13,000</strong><small>Redemptions + withdrawals + distributions</small></article>
    </section>

    <section className="bc-grid two" style={{marginTop:16}}>
      <article className="bc-card"><div className="bc-card-head"><div><h2>Accounting truth</h2><p>Booked and marked economic value. Forecast return never appears here.</p></div><span className="bc-status research">SYNTHETIC PREVIEW</span></div><Rows rows={accounting}/></article>
      <article className="bc-card"><div className="bc-card-head"><div><h2>Liquidity & obligations</h2><p>Money already promised is not free capital.</p></div></div><Rows rows={obligations}/></article>
    </section>

    <section className="bc-grid two" style={{marginTop:16}}>
      <article className="bc-card"><div className="bc-card-head"><div><h2>Economic exposure</h2><p>Cash paid, marked value, gross notional, collateral, and net exposure remain distinct concepts.</p></div></div><Rows rows={exposure}/></article>
      <article className="bc-card">
        <div className="bc-card-head"><div><h2>Routing readiness</h2><p>State quality constrains what classes of paths Benjamin may even consider.</p></div><span className="bc-status active">FULL</span></div>
        <div className="bc-priority">
          <div className="bc-priority-row"><b>F</b><span><strong>FULL</strong><br/>Capital truth is reconciled and fresh enough to evaluate risk-increasing and defensive paths.</span></div>
          <div className="bc-priority-row"><b>D</b><span><strong>DEFENSIVE ONLY</strong><br/>No new risk. Benjamin may still need to consider hold, reduce, exit, or a separately qualified protective hedge.</span></div>
          <div className="bc-priority-row"><b>B</b><span><strong>BLOCKED</strong><br/>Capital truth is too incomplete to route an economic transformation safely.</span></div>
        </div>
        <div className="bc-footer-note"><b>Important:</b> routing readiness is not Watchman authorization. It is an upstream statement about whether Benjamin has enough capital truth to reason safely.</div>
      </article>
    </section>

    <section className="bc-card" style={{marginTop:16}}>
      <div className="bc-card-head"><div><h2>Point-in-time lineage</h2><p>Every Capital State must be reproducible from the exact valuation policy and source evidence knowable at the cutoff.</p></div><span className="bc-status active">NO LOOKAHEAD</span></div>
      <table className="bc-authority-table">
        <thead><tr><th>Source</th><th>Account</th><th>Observed</th><th>Known</th><th>Quality</th><th>Digest</th></tr></thead>
        <tbody>
          <tr><td>Custodian account snapshot</td><td>ACC-001</td><td>20:00:00Z</td><td>20:00:00Z</td><td><span className="bc-status active">VALID</span></td><td>aaaa…aaaa</td></tr>
          <tr><td>Valuation policy</td><td>Family Growth I</td><td>v1.0.0</td><td>effective before cutoff</td><td><span className="bc-status active">VALID</span></td><td>bbbb…bbbb</td></tr>
          <tr><td>Reconciliation</td><td>ACC-001</td><td>20:00:01Z</td><td>20:00:01Z</td><td><span className="bc-status active">RECONCILED</span></td><td>receipt pending backend</td></tr>
        </tbody>
      </table>
    </section>

    <section className="bc-card" style={{marginTop:16}}>
      <div className="bc-card-head"><div><h2>Capital-state cognition rule</h2><p>Accounting is part of Benjamin's cognition loop, not a report produced after the fact.</p></div></div>
      <div className="bc-priority">
        {['Capital State T0','Benjamin evaluates candidate economic paths','Watchman governs the selected decision','The Hand executes an authorized action','Accounting events + reconciliation','Capital State T1 becomes the next decision input'].map((item,index)=><div className="bc-priority-row" key={item}><b>{index+1}</b><span>{item}</span></div>)}
      </div>
    </section>
  </>;
}
