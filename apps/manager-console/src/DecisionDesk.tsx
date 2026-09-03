import type { ComponentType } from 'react';
import { candidatePaths, capitalStructures, responsibilities } from './company-model';

type TopbarProps = { title: string; description: string };

export function DecisionDesk({ Topbar }: { Topbar: ComponentType<TopbarProps> }) {
  const structure=capitalStructures.find((item)=>item.structureId==='CAP-POOL-001')??capitalStructures[0];
  const responsibility=responsibilities.find((item)=>item.structureId===structure.structureId)??responsibilities[0];
  const permitted=[...candidatePaths].filter((item)=>item.status==='PERMITTED').sort((a,b)=>b.score-a.score);
  const selected=permitted[0];
  const rejected=[...candidatePaths].filter((item)=>item.pathId!==selected.pathId).sort((a,b)=>b.score-a.score);

  return <>
    <Topbar title="Decision Desk" description="Inspect Benjamin decisions as durable capital judgments: selected path, alternatives, responsibility version, expected portfolio effect, invalidation, evidence lineage, and Watchman status." />

    <section className="bc-card bc-hero">
      <div className="bc-hero-grid">
        <div>
          <div className="bc-eyebrow">BENJAMIN.DECISION / SYNTHETIC FRONTEND PREVIEW</div>
          <h2>{selected.label} <em>for {structure.name}</em></h2>
          <p className="bc-hero-copy">Benjamin selected the highest-scoring currently permitted path in the Router preview. A higher-scoring research-only or blocked path remains visible as an alternative rather than being silently discarded.</p>
        </div>
        <div className="bc-constitution">
          <span>Decision id</span><strong>BEN-D-PREVIEW-001</strong>
          <span>Responsibility</span><strong>{responsibility.responsibilityId}@{responsibility.version}</strong>
          <span>Watchman</span><strong><b>PENDING</b></strong>
          <span>Execution authority</span><strong>NONE</strong>
        </div>
      </div>
    </section>

    <section className="bc-grid metrics">
      <article className="bc-card bc-metric"><label>Selected score</label><strong>{selected.score.toFixed(2)}</strong><small>Illustrative path-evaluation score</small></article>
      <article className="bc-card bc-metric"><label>Capital required</label><strong>{selected.capitalRequired}</strong><small>Before future reserve/settlement model</small></article>
      <article className="bc-card bc-metric"><label>Expected benefit</label><strong>{selected.expectedBenefit}</strong><small>Scenario, not guarantee</small></article>
      <article className="bc-card bc-metric"><label>Expected downside</label><strong>{selected.expectedDownside}</strong><small>Scenario estimate</small></article>
    </section>

    <section className="bc-grid two">
      <article className="bc-card">
        <div className="bc-card-head"><div><h2>Decision rationale</h2><p>What the durable decision should explain.</p></div><span className="bc-status active">SELECTED</span></div>
        <div className="bc-targets">
          <div className="bc-target"><span>Capital structure</span><strong>{structure.name}</strong></div>
          <div className="bc-target"><span>Objective</span><strong>{responsibility.primaryObjective.replaceAll('_',' ')}</strong></div>
          <div className="bc-target"><span>Selected path</span><strong>{selected.label}</strong></div>
          <div className="bc-target"><span>Why permitted</span><strong>Fits current market + action authority</strong></div>
          <div className="bc-target"><span>Why not maximum raw score</span><strong>Hard mandate gates precede return optimization</strong></div>
        </div>
      </article>
      <article className="bc-card">
        <div className="bc-card-head"><div><h2>Invalidation conditions</h2><p>The decision must say when it stops being justified.</p></div><span className="bc-status research">PREVIEW CONTRACT</span></div>
        <div className="bc-priority">
          {['Qualified intelligence becomes stale or contradicted','Spot/futures relationship materially changes','Expected downside exceeds remaining risk budget','Liquidity falls below required reserve','Watchman blocks or responsibility authority changes'].map((item,index)=><div className="bc-priority-row" key={item}><b>{index+1}</b><span>{item}</span></div>)}
        </div>
      </article>
    </section>

    <section className="bc-card" style={{marginTop:16}}>
      <div className="bc-card-head"><div><h2>Alternatives considered</h2><p>Rejected and blocked paths remain part of the explanation.</p></div></div>
      <table className="bc-authority-table">
        <thead><tr><th>Alternative</th><th>Score</th><th>Status</th><th>Reason not selected</th></tr></thead>
        <tbody>{rejected.map((path)=><tr key={path.pathId}><td><strong>{path.label}</strong></td><td>{path.score.toFixed(2)}</td><td><span className={`bc-status ${path.status==='PERMITTED'?'active':'research'}`}>{path.status.replaceAll('_',' ')}</span></td><td>{path.reason}</td></tr>)}</tbody>
      </table>
    </section>

    <section className="bc-grid two" style={{marginTop:16}}>
      <article className="bc-card">
        <div className="bc-card-head"><div><h2>Evidence lineage expected</h2><p>The Book should eventually let an operator reconstruct this decision.</p></div></div>
        <div className="bc-priority">
          {['ZLJ intelligence object','Spot/futures relationship state','Portfolio + cash state','Responsibility version','Router path evaluations','Benjamin decision receipt'].map((item,index)=><div className="bc-priority-row" key={item}><b>{index+1}</b><span>{item}</span></div>)}
        </div>
      </article>
      <article className="bc-card">
        <div className="bc-card-head"><div><h2>Institutional handoff</h2><p>A decision is still not an authorized external action.</p></div></div>
        <div className="bc-targets">
          <div className="bc-target"><span>Benjamin</span><strong>DECISION RECORDED</strong></div>
          <div className="bc-target"><span>Watchman</span><strong>PENDING<small>MUST AUTHORIZE OR BLOCK</small></strong></div>
          <div className="bc-target"><span>The Hand</span><strong>NO REQUEST YET</strong></div>
          <div className="bc-target"><span>The Book</span><strong>DECISION EVIDENCE EXPECTED</strong></div>
        </div>
      </article>
    </section>
    <div className="bc-footer-note"><b>Decision rule:</b> Benjamin may explain and record the best permissible capital path. It cannot turn its own decision into external financial action without Watchman authorization and Hand execution.</div>
  </>;
}
