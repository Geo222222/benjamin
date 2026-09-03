import { useState, type ComponentType } from 'react';
import { capitalStructures, type CapitalStructure } from './company-model';

type TopbarProps = { title: string; description: string };

function Card({ structure, onOpen }: { structure: CapitalStructure; onOpen: () => void }) {
  return <article className="bc-card"><div className="bc-card-head"><div><div className="bc-eyebrow">{structure.type.replaceAll('_',' ')}</div><h2 style={{marginTop:7}}>{structure.name}</h2><p>{structure.structureId}</p></div><span className={`bc-status ${structure.status==='ACTIVE'?'active':'research'}`}>{structure.status}</span></div><div className="bc-grid two" style={{gridTemplateColumns:'1fr 1fr',gap:10}}><div className="bc-risk"><span>Net asset value</span><strong>{structure.nav}</strong></div><div className="bc-risk"><span>Participants</span><strong>{structure.participantCount}</strong></div><div className="bc-risk"><span>Cash</span><strong>{structure.cash}</strong></div><div className="bc-risk"><span>Deployed</span><strong>{structure.deployed}</strong></div></div><div className="bc-actions" style={{marginTop:14}}><button className="bc-button" onClick={onOpen}>View responsibility</button><button className="bc-button" disabled>Edit structure</button></div></article>;
}

export function CapitalStructures({ Topbar, openResponsibility }: { Topbar: ComponentType<TopbarProps>; openResponsibility: (id: string) => void }) {
  const [filter,setFilter]=useState<'ALL'|'ACTIVE'|'ONBOARDING'>('ALL');
  const visible=capitalStructures.filter((item)=>filter==='ALL'||item.status===filter);
  return <><Topbar title="Capital Structures" description="The economic containers Benjamin is responsible for managing: individually owned accounts, household/joint portfolios, entities/treasuries, and pooled portfolios."/><div className="bc-actions" style={{marginBottom:16}}><button className="bc-button primary" disabled>+ Create capital structure — backend pending</button>{(['ALL','ACTIVE','ONBOARDING'] as const).map((item)=><button key={item} className={`bc-button ${filter===item?'gold':''}`} onClick={()=>setFilter(item)}>{item}</button>)}</div><section className="bc-grid two">{visible.map((structure)=><Card key={structure.structureId} structure={structure} onOpen={()=>openResponsibility(structure.structureId)}/>)}</section><div className="bc-footer-note"><b>Container rule:</b> each Capital Structure owns one active Responsibility version even when it spans several accounts or participants. The router decides for the economic structure, not whichever provider happens to execute the action.</div></>;
}
