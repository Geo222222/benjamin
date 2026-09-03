import { useMemo, useState, type ComponentType } from 'react';
import { candidatePaths, capitalStructures, responsibilities } from './company-model';

type TopbarProps = { title: string; description: string };

export function CapitalRouter({ Topbar }: { Topbar: ComponentType<TopbarProps> }) {
  const [structureId,setStructureId]=useState('CAP-POOL-001');
  const structure=useMemo(()=>capitalStructures.find((item)=>item.structureId===structureId)??capitalStructures[0],[structureId]);
  const responsibility=responsibilities.find((item)=>item.structureId===structure.structureId)??responsibilities[0];
  const permitted=candidatePaths.filter((path)=>path.status==='PERMITTED');
  const bestPermitted=[...permitted].sort((a,b)=>b.score-a.score)[0];
  const bestObserved=[...candidatePaths].sort((a,b)=>b.score-a.score)[0];

  return <>
    <Topbar title="Capital Router" description="Compare feasible economic paths for a capital structure and select the best justified transformation that survives responsibility, authority, risk, liquidity, and evidence gates." />

    <section className="bc-card bc-hero">
      <div className="bc-hero-grid">
        <div>
          <div className="bc-eyebrow">ACCOUNT TARGETS → FEASIBLE PATHS → MONEY LOGIC</div>
          <h2>{structure.name}: <em>{bestPermitted?.label ?? 'Hold cash'}</em></h2>
          <p className="bc-hero-copy">The router may observe a path with a higher economic score and still refuse it because the active Responsibility does not permit execution. Hard authority and survival constraints are evaluated before return optimization.</p>
          <div className="bc-actions"><select className="bc-button" value={structureId} onChange={(event)=>setStructureId(event.target.value)}>{capitalStructures.map((item)=><option key={item.structureId} value={item.structureId}>{item.name}</option>)}</select><button className="bc-button primary" disabled>Recompute paths — backend pending</button></div>
        </div>
        <div className="bc-constitution">
          <span>Current responsibility</span><strong>{responsibility.name}</strong>
          <span>Best observed score</span><strong>{bestObserved.score.toFixed(2)} · {bestObserved.status}</strong>
          <span>Best permitted</span><strong><b>{bestPermitted?.score.toFixed(2)}</b> · {bestPermitted?.label}</strong>
          <span>Router mode</span><strong>FRONTEND CONTRACT PREVIEW</strong>
        </div>
      </div>
    </section>

    <section className="bc-grid metrics">
      <article className="bc-card bc-metric"><label>Structure NAV</label><strong>{structure.nav}</strong><small>Capital under this responsibility</small></article>
      <article className="bc-card bc-metric"><label>Available cash</label><strong>{structure.cash}</strong><small>Before future reserves/settlement model</small></article>
      <article className="bc-card bc-metric"><label>Candidate paths</label><strong>{candidatePaths.length}</strong><small>{permitted.length} currently permitted</small></article>
      <article className="bc-card bc-metric"><label>Objective</label><strong>{responsibility.primaryObjective.replaceAll('_',' ')}</strong><small>Optimization occurs after hard gates</small></article>
    </section>

    <section className="bc-card">
      <div className="bc-card-head"><div><h2>Candidate economic paths</h2><p>The router compares alternatives; an evaluated path is not an order.</p></div><span className="bc-status research">SYNTHETIC PREVIEW</span></div>
      <table className="bc-authority-table">
        <thead><tr><th>Path</th><th>Market / relationship</th><th>Score</th><th>Expected benefit</th><th>Expected downside</th><th>Capital</th><th>Status</th></tr></thead>
        <tbody>{[...candidatePaths].sort((a,b)=>b.score-a.score).map((path)=><tr key={path.pathId}><td><strong>{path.label}</strong><br/><span style={{color:'#6f7e97',fontSize:10}}>{path.reason}</span></td><td>{path.market}</td><td>{path.score.toFixed(2)}</td><td>{path.expectedBenefit}</td><td>{path.expectedDownside}</td><td>{path.capitalRequired}</td><td><span className={`bc-status ${path.status==='PERMITTED'?'active':'research'}`}>{path.status.replaceAll('_',' ')}</span></td></tr>)}</tbody>
      </table>
    </section>

    <section className="bc-grid two" style={{marginTop:16}}>
      <article className="bc-card">
        <div className="bc-card-head"><div><h2>Router gate order</h2><p>Hard constraints cannot be traded away for a larger expected return.</p></div></div>
        <div className="bc-priority">
          {['Operationally available','Permitted by active Responsibility','Portfolio survives modeled downside','Required liquidity remains available','Evidence and competence are sufficient','Optimize expected capital outcome'].map((item,index)=><div className="bc-priority-row" key={item}><b>{index+1}</b><span>{item}</span></div>)}
        </div>
      </article>
      <article className="bc-card">
        <div className="bc-card-head"><div><h2>Selected permissible path</h2><p>The preview deliberately distinguishes observed attractiveness from usable authority.</p></div><span className="bc-status active">SELECTED</span></div>
        <div className="bc-targets">
          <div className="bc-target"><span>Path</span><strong>{bestPermitted?.label}</strong></div>
          <div className="bc-target"><span>Score</span><strong>{bestPermitted?.score.toFixed(2)}</strong></div>
          <div className="bc-target"><span>Expected benefit</span><strong>{bestPermitted?.expectedBenefit}</strong></div>
          <div className="bc-target"><span>Expected downside</span><strong>{bestPermitted?.expectedDownside}</strong></div>
          <div className="bc-target"><span>Higher-scoring blocked path</span><strong>{bestObserved.status!=='PERMITTED'?bestObserved.label:'NONE'}{bestObserved.status!=='PERMITTED'&&<small>{bestObserved.status}</small>}</strong></div>
        </div>
      </article>
    </section>

    <section className="bc-card" style={{marginTop:16}}>
      <div className="bc-card-head"><div><h2>Backend contract discovered by the Router</h2><p>The eventual decision engine needs these inputs before it may choose a path.</p></div><span className="bc-status research">NOT IMPLEMENTED</span></div>
      <div className="bc-risk-grid">
        <div className="bc-risk"><span>Capital state</span><strong>Portfolio + cash</strong></div>
        <div className="bc-risk"><span>Responsibility</span><strong>Version bound</strong></div>
        <div className="bc-risk"><span>Market intelligence</span><strong>ZLJ</strong></div>
        <div className="bc-risk"><span>Economic relationships</span><strong>Spot / futures / more</strong></div>
      </div>
    </section>
    <div className="bc-footer-note"><b>Router rule:</b> the selected path is a Benjamin decision candidate, not execution authority. Watchman still governs the resulting decision and The Hand remains the only execution organ.</div>
  </>;
}
