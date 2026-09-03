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
    <Topbar title="Capital Router" description="Compare feasible economic paths for a capital structure using authoritative Capital State, active Responsibility, qualified intelligence, and hard feasibility gates." />

    <section className="bc-card bc-hero">
      <div className="bc-hero-grid">
        <div>
          <div className="bc-eyebrow">CAPITAL STATE → RESPONSIBILITY → FEASIBLE PATHS → MONEY LOGIC</div>
          <h2>{structure.name}: <em>{bestPermitted?.label ?? 'Hold cash'}</em></h2>
          <p className="bc-hero-copy">The Router may observe a path with a higher economic score and still refuse it because Capital State is degraded, obligations consume deployable capital, or the active Responsibility does not permit the exposure. Hard authority and survival constraints precede return optimization.</p>
          <div className="bc-actions"><select className="bc-button" value={structureId} onChange={(event)=>setStructureId(event.target.value)}>{capitalStructures.map((item)=><option key={item.structureId} value={item.structureId}>{item.name}</option>)}</select><button className="bc-button primary" disabled>Recompute paths — backend pending</button></div>
        </div>
        <div className="bc-constitution">
          <span>Capital State</span><strong>CAPSTATE-7C91… · FULL</strong>
          <span>Current responsibility</span><strong>{responsibility.name}</strong>
          <span>Best observed score</span><strong>{bestObserved.score.toFixed(2)} · {bestObserved.status}</strong>
          <span>Best permitted</span><strong><b>{bestPermitted?.score.toFixed(2)}</b> · {bestPermitted?.label}</strong>
        </div>
      </div>
    </section>

    <section className="bc-grid metrics">
      <article className="bc-card bc-metric"><label>Structure NAV</label><strong>$185,500</strong><small>Authoritative valuation projection</small></article>
      <article className="bc-card bc-metric"><label>Provider-available cash</label><strong>$50,000</strong><small>Not yet deployable</small></article>
      <article className="bc-card bc-metric"><label>Risk capital available</label><strong>$17,000</strong><small>After obligations + risk budget</small></article>
      <article className="bc-card bc-metric"><label>Routing readiness</label><strong>FULL</strong><small>Risk-increasing paths may be evaluated</small></article>
    </section>

    <section className="bc-card">
      <div className="bc-card-head"><div><h2>Candidate economic paths</h2><p>The Router compares transformations of the whole Capital Structure; an evaluated path is not an order.</p></div><span className="bc-status research">SYNTHETIC PREVIEW</span></div>
      <table className="bc-authority-table">
        <thead><tr><th>Path</th><th>Market / relationship</th><th>Score</th><th>Expected benefit</th><th>Expected downside</th><th>Capital</th><th>Status</th></tr></thead>
        <tbody>{[...candidatePaths].sort((a,b)=>b.score-a.score).map((path)=><tr key={path.pathId}><td><strong>{path.label}</strong><br/><span style={{color:'#6f7e97',fontSize:10}}>{path.reason}</span></td><td>{path.market}</td><td>{path.score.toFixed(2)}</td><td>{path.expectedBenefit}</td><td>{path.expectedDownside}</td><td>{path.capitalRequired}</td><td><span className={`bc-status ${path.status==='PERMITTED'?'active':'research'}`}>{path.status.replaceAll('_',' ')}</span></td></tr>)}</tbody>
      </table>
    </section>

    <section className="bc-grid two" style={{marginTop:16}}>
      <article className="bc-card">
        <div className="bc-card-head"><div><h2>Router gate order</h2><p>Hard constraints cannot be traded away for a larger expected return.</p></div></div>
        <div className="bc-priority">
          {['Capital State is routable for this path class','Operationally available','Permitted by active Responsibility','Portfolio survives modeled downside','Required liquidity remains available','Evidence and competence are sufficient','Optimize expected capital outcome'].map((item,index)=><div className="bc-priority-row" key={item}><b>{index+1}</b><span>{item}</span></div>)}
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
      <div className="bc-card-head"><div><h2>Router input contract</h2><p>The eventual decision engine must bind every candidate-path evaluation to these exact inputs.</p></div><span className="bc-status research">BACKEND NEXT</span></div>
      <div className="bc-risk-grid">
        <div className="bc-risk"><span>Capital State</span><strong>Point-in-time + content hash</strong></div>
        <div className="bc-risk"><span>Responsibility</span><strong>Version bound</strong></div>
        <div className="bc-risk"><span>Market intelligence</span><strong>ZLJ · qualified</strong></div>
        <div className="bc-risk"><span>Economic relationships</span><strong>Micro + macro + cross-market</strong></div>
      </div>
    </section>
    <div className="bc-footer-note"><b>Router rule:</b> `FULL` Capital State permits evaluation of new-risk paths; `DEFENSIVE_ONLY` excludes new risk but may still require hold/reduce/exit/protective reasoning; `BLOCKED` means Benjamin lacks enough capital truth to route safely. Watchman still governs any resulting decision.</div>
  </>;
}
