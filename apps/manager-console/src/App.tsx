import { useState } from 'react';
import { companyModelStatus } from './company-model';
import { CompanyCommand } from './CompanyCommand';
import { Relationships } from './Relationships';
import { CapitalStructures } from './CapitalStructures';
import { Accounts } from './Accounts';
import { CapitalStateSurface } from './CapitalState';
import { ResponsibilityCenter } from './ResponsibilityCenter';
import { Participants } from './Participants';
import { CapitalRouter } from './CapitalRouter';
import { MarketRelationships } from './MarketRelationships';
import { DecisionDesk } from './DecisionDesk';
import { InstitutionalBridge } from './InstitutionalBridge';
import { ClientReporting, Operations } from './CompanyOperations';

type PageKey = 'command' | 'relationships' | 'structures' | 'participants' | 'accounts' | 'capital-state' | 'responsibility' | 'router' | 'decisions' | 'markets' | 'watchman' | 'hand' | 'book' | 'reports' | 'operations';
type NavItem = { key: PageKey; label: string; glyph: string; group: string };

const navItems: NavItem[] = [
  { key: 'command', label: 'Company Command', glyph: '⌂', group: 'Benjamin Capital Management' },
  { key: 'relationships', label: 'Relationships', glyph: '◎', group: 'Company' },
  { key: 'structures', label: 'Capital Structures', glyph: '◈', group: 'Company' },
  { key: 'participants', label: 'Participants', glyph: '♙', group: 'Company' },
  { key: 'accounts', label: 'Accounts', glyph: '▤', group: 'Company' },
  { key: 'capital-state', label: 'Capital State', glyph: '◫', group: 'Capital Truth' },
  { key: 'responsibility', label: 'Responsibility Center', glyph: '◇', group: 'Benjamin Authority' },
  { key: 'router', label: 'Capital Router', glyph: '⌁', group: 'Benjamin Authority' },
  { key: 'decisions', label: 'Decision Desk', glyph: '◉', group: 'Benjamin Authority' },
  { key: 'markets', label: 'Market Relationships', glyph: '⌗', group: 'Intelligence' },
  { key: 'watchman', label: 'Watchman Bridge', glyph: '⬡', group: 'Institution' },
  { key: 'hand', label: 'The Hand Bridge', glyph: '▣', group: 'Institution' },
  { key: 'book', label: 'The Book Bridge', glyph: '▧', group: 'Institution' },
  { key: 'reports', label: 'Client Reporting', glyph: '▥', group: 'Operations' },
  { key: 'operations', label: 'Operations', glyph: '⚙', group: 'Operations' },
];

export function Topbar({ title, description }: { title: string; description: string }) {
  return <header className="bc-topbar"><div><div className="bc-eyebrow">Benjamin Capital Management / Manager Console</div><h1>{title}</h1><p>{description}</p></div><div className="bc-top-actions"><span className="bc-badge good">FRONTEND CONTRACT</span><span className="bc-badge warn">NO LIVE CAPITAL AUTHORITY</span></div></header>;
}

function Sidebar({ page, setPage }: { page: PageKey; setPage: (page: PageKey) => void }) {
  const groups=[...new Set(navItems.map((item)=>item.group))];
  return <aside className="bc-sidebar"><div className="bc-brand"><div className="bc-brand-mark">B</div><div><strong>BENJAMIN</strong><small>Capital Management</small></div></div>{groups.map((group)=><div className="bc-nav-group" key={group}><div className="bc-nav-label">{group}</div>{navItems.filter((item)=>item.group===group).map((item)=><button key={item.key} className={`bc-nav-button ${page===item.key?'active':''}`} onClick={()=>setPage(item.key)}><span>{item.glyph}</span><span>{item.label}</span></button>)}</div>)}<div className="bc-side-footer"><span>Product mode <b>{companyModelStatus.productMode}</b></span><span>Live execution <b>OFF</b></span><span>Custody authority <b>NONE</b></span></div></aside>;
}

export function App() {
  const [page,setPage]=useState<PageKey>('command');
  const [responsibilityStructure,setResponsibilityStructure]=useState<string|undefined>();
  const openResponsibility=(id:string)=>{setResponsibilityStructure(id);setPage('responsibility');};
  const navigate=(next:PageKey)=>{setResponsibilityStructure(undefined);setPage(next);};

  let content;
  if(page==='command') content=<CompanyCommand Topbar={Topbar}/>;
  else if(page==='relationships') content=<Relationships Topbar={Topbar}/>;
  else if(page==='structures') content=<CapitalStructures Topbar={Topbar} openResponsibility={openResponsibility}/>;
  else if(page==='participants') content=<Participants Topbar={Topbar}/>;
  else if(page==='accounts') content=<Accounts Topbar={Topbar}/>;
  else if(page==='capital-state') content=<CapitalStateSurface Topbar={Topbar}/>;
  else if(page==='responsibility') content=<ResponsibilityCenter Topbar={Topbar} initialStructureId={responsibilityStructure}/>;
  else if(page==='router') content=<CapitalRouter Topbar={Topbar}/>;
  else if(page==='decisions') content=<DecisionDesk Topbar={Topbar}/>;
  else if(page==='markets') content=<MarketRelationships Topbar={Topbar}/>;
  else if(page==='watchman') content=<InstitutionalBridge kind="watchman" Topbar={Topbar}/>;
  else if(page==='hand') content=<InstitutionalBridge kind="hand" Topbar={Topbar}/>;
  else if(page==='book') content=<InstitutionalBridge kind="book" Topbar={Topbar}/>;
  else if(page==='reports') content=<ClientReporting Topbar={Topbar}/>;
  else content=<Operations Topbar={Topbar}/>;

  return <div className="bc-shell"><Sidebar page={page} setPage={navigate}/><main className="bc-main">{content}</main></div>;
}
