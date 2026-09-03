import type { ComponentType } from 'react';
import { capitalStructures, participants, relationships } from './company-model';

type TopbarProps = { title: string; description: string };

export function ClientReporting({ Topbar }: { Topbar: ComponentType<TopbarProps> }) {
  return <>
    <Topbar title="Client Reporting" description="Control which authoritative capital, performance, activity, fee, mandate, governance, execution, and evidence projections each owner or participant is entitled to receive." />
    <section className="bc-grid metrics">
      <article className="bc-card bc-metric"><label>Relationships</label><strong>{relationships.length}</strong><small>Preview recipients</small></article>
      <article className="bc-card bc-metric"><label>Participants</label><strong>{participants.length}</strong><small>Reporting scopes differ</small></article>
      <article className="bc-card bc-metric"><label>Structures</label><strong>{capitalStructures.length}</strong><small>Individual / joint / entity / pool</small></article>
      <article className="bc-card bc-metric"><label>Formal statements</label><strong>BACKEND</strong><small>Book/accounting-derived later</small></article>
    </section>

    <section className="bc-card">
      <div className="bc-card-head"><div><h2>Reporting matrix</h2><p>What the company must be able to produce without leaking another party’s private information.</p></div><span className="bc-status research">FRONTEND CONTRACT</span></div>
      <table className="bc-authority-table">
        <thead><tr><th>Report / projection</th><th>Individual owner</th><th>Pooled participant</th><th>Authoritative source</th></tr></thead>
        <tbody>
          <tr><td><strong>Current capital / NAV</strong></td><td>Full own structure</td><td>Own economic interest</td><td>Accounting + custody</td></tr>
          <tr><td><strong>Performance</strong></td><td>Own account/structure</td><td>Participant-adjusted economics</td><td>Book + accounting</td></tr>
          <tr><td><strong>Contributions / withdrawals</strong></td><td>Own cash flows</td><td>Own subscriptions/redemptions</td><td>Capital activity ledger</td></tr>
          <tr><td><strong>Fees and costs</strong></td><td>Own allocations</td><td>Own allocations</td><td>Fee ledger</td></tr>
          <tr><td><strong>Benjamin decisions</strong></td><td>Affecting own structure</td><td>Permitted shared-structure decisions</td><td>Decision ledger</td></tr>
          <tr><td><strong>Watchman / Hand / Book</strong></td><td>Own material lineage</td><td>Participant-scoped material lineage</td><td>Institutional receipts</td></tr>
          <tr><td><strong>Other participant PII</strong></td><td>N/A</td><td>EXCLUDED</td><td>Privacy boundary</td></tr>
          <tr><td><strong>Proprietary ZLJ internals</strong></td><td>EXCLUDED</td><td>EXCLUDED</td><td>Company IP boundary</td></tr>
        </tbody>
      </table>
    </section>

    <section className="bc-grid two" style={{marginTop:16}}>
      <article className="bc-card"><div className="bc-card-head"><div><h2>Formal statement set</h2><p>The frontend has now discovered the baseline document family.</p></div></div><div className="bc-priority">{['Monthly/periodic capital statement','Performance statement','Contribution/redemption statement','Fee and cost statement','Annual/tax package','Mandate/responsibility notice','Material activity/evidence export'].map((item,index)=><div className="bc-priority-row" key={item}><b>{index+1}</b><span>{item}</span></div>)}</div></article>
      <article className="bc-card"><div className="bc-card-head"><div><h2>Generation rules</h2><p>Reports must be projections of authoritative records, not dashboard arithmetic.</p></div></div><div className="bc-targets"><div className="bc-target"><span>Source</span><strong>BOOK + ACCOUNTING</strong></div><div className="bc-target"><span>Cutoff</span><strong>EXPLICIT</strong></div><div className="bc-target"><span>Responsibility version</span><strong>BOUND</strong></div><div className="bc-target"><span>Participant scope</span><strong>ENFORCED</strong></div><div className="bc-target"><span>Reproducibility</span><strong>REQUIRED</strong></div></div></article>
    </section>
    <div className="bc-footer-note"><b>Reporting rule:</b> the client console is a projection; the statement/accounting backend must be authoritative. A beautiful number on the screen is never allowed to become the source of financial truth.</div>
  </>;
}

export function Operations({ Topbar }: { Topbar: ComponentType<TopbarProps> }) {
  const lifecycle = [
    ['Relationship onboarding','Identity / legal relationship / communications established'],
    ['Capital-structure setup','Ownership/participants/base currency/economic container established'],
    ['Account & custody connection','External account authority and reconciliation source established'],
    ['Responsibility activation','Objectives, targets, market/action authority and risk envelope versioned'],
    ['Funding / subscription','Capital accepted into the correct owner/participant economic ledger'],
    ['Managed operation','Router → Decision → Watchman → Hand → Book lifecycle'],
    ['Accounting & reconciliation','Positions, cash, fills, fees, P&L, participant economics reconciled'],
    ['Reporting','Statements, disclosures, activity and participant/client projections produced'],
    ['Restriction / exception','Freeze/restrict without corrupting ownership or prior history'],
    ['Closure / redemption','Final economics settled, records preserved, authority terminated'],
  ];
  return <>
    <Topbar title="Operations" description="Manage the non-trading lifecycle required to operate capital relationships cleanly from onboarding through funding, reconciliation, reporting, restrictions, redemptions, and closure." />
    <section className="bc-card bc-hero"><div className="bc-hero-grid"><div><div className="bc-eyebrow">CAPITAL RELATIONSHIP LIFECYCLE</div><h2>Managing money includes everything <em>around the decision engine.</em></h2><p className="bc-hero-copy">Benjamin’s Router can be excellent and the company can still fail if ownership, funding, reconciliation, fees, restrictions, statements, or closure are undefined. This surface makes those responsibilities explicit before backend implementation.</p></div><div className="bc-constitution"><span>Trading engine</span><strong>ONE SUBSYSTEM</strong><span>Accounting truth</span><strong><b>REQUIRED</b></strong><span>Client lifecycle</span><strong>END TO END</strong><span>Silent deletion</span><strong>NEVER</strong></div></div></section>

    <section className="bc-card">
      <div className="bc-card-head"><div><h2>Capital-management lifecycle</h2><p>Each state transition will eventually need validation, authority, durable evidence, and recovery semantics.</p></div><span className="bc-status research">BACKEND INVENTORY INPUT</span></div>
      <div className="bc-priority">{lifecycle.map(([name,detail],index)=><div className="bc-priority-row" key={name}><b>{index+1}</b><span><strong>{name}</strong> — {detail}</span></div>)}</div>
    </section>

    <section className="bc-grid three" style={{marginTop:16}}>
      <article className="bc-card"><div className="bc-card-head"><div><h2>Money movement</h2></div></div><div className="bc-targets"><div className="bc-target"><span>Contributions / deposits</span><strong>TRACK</strong></div><div className="bc-target"><span>Redemptions / withdrawals</span><strong>GOVERN</strong></div><div className="bc-target"><span>Distributions</span><strong>ACCOUNT</strong></div><div className="bc-target"><span>Internal same-owner transfer</span><strong>SEPARATE AUTHORITY</strong></div></div></article>
      <article className="bc-card"><div className="bc-card-head"><div><h2>Accounting</h2></div></div><div className="bc-targets"><div className="bc-target"><span>Cash / positions</span><strong>RECONCILE</strong></div><div className="bc-target"><span>Realized / unrealized P&L</span><strong>SEPARATE</strong></div><div className="bc-target"><span>Fees / expenses</span><strong>ALLOCATE</strong></div><div className="bc-target"><span>Pool units / capital accounts</span><strong>REQUIRED</strong></div></div></article>
      <article className="bc-card"><div className="bc-card-head"><div><h2>Exceptions</h2></div></div><div className="bc-targets"><div className="bc-target"><span>Stale/disconnected custodian</span><strong>FAIL CLOSED</strong></div><div className="bc-target"><span>Reconciliation break</span><strong>VISIBLE</strong></div><div className="bc-target"><span>Restricted relationship</span><strong>NO NEW RISK</strong></div><div className="bc-target"><span>Closure</span><strong>PRESERVE HISTORY</strong></div></div></article>
    </section>
    <div className="bc-footer-note"><b>Operations rule:</b> no lifecycle transition should rewrite prior economic truth. Corrections, restrictions, closures, and reconciliations must remain reconstructable through The Book.</div>
  </>;
}
