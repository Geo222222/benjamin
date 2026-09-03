import { useState } from 'react';
import { companyModelStatus } from './company-model';
import { CompanyCommand } from './CompanyCommand';
import { Relationships } from './Relationships';
import { CapitalStructures } from './CapitalStructures';
import { Accounts } from './Accounts';
import { ResponsibilityCenter } from './ResponsibilityCenter';
import { Participants } from './Participants';

type PageKey = 'command' | 'relationships' | 'structures' | 'participants' | 'accounts' | 'responsibility' | 'router' | 'decisions' | 'markets' | 'watchman' | 'hand' | 'book' | 'reports' | 'operations';
type NavItem = { key: PageKey; label: string; glyph: string; phase: number; group: string };

const navItems: NavItem[] = [
  { key: 'command', label: 'Company Command', glyph: '⌂', phase: 2, group: 'Benjamin Capital Management' },
  { key: 'relationships', label: 'Relationships', glyph: '◎', phase: 3, group: 'Company' },
  { key: 'structures', label: 'Capital Structures', glyph: '◈', phase: 3, group: 'Company' },
  { key: 'participants', label: 'Participants', glyph: '♙', phase: 4, group: 'Company' },
  { key: 'accounts', label: 'Accounts', glyph: '▤', phase: 3, group: 'Company' },
  { key: 'responsibility', label: 'Responsibility Center', glyph: '◇', phase: 2, group: 'Benjamin Authority' },
  { key: 'router', label: 'Capital Router', glyph: '⌁', phase: 5, group: 'Benjamin Authority' },
  { key: 'decisions', label: 'Decision Desk', glyph: '◉', phase: 7, group: 'Benjamin Authority' },
  { key: 'markets', label: 'Market Relationships', glyph: '⌗', phase: 6, group: 'Intelligence' },
  { key: 'watchman', label: 'Watchman', glyph: '⬡', phase: 9, group: 'Institution' },
  { key: 'hand', label: 'The Hand', glyph: '▣', phase: 9, group: 'Institution' },
  { key: 'book', label: 'The Book', glyph: '▧', phase: 9, group: 'Institution' },
  { key: 'reports', label: 'Client Reporting', glyph: '▥', phase: 8, group: 'Operations' },
  { key: 'operations', label: 'Operations', glyph: '⚙', phase: 9, group: 'Operations' },
];

const enabledPages = new Set<PageKey>(['command','relationships','structures','participants','accounts','responsibility']);

export function Topbar({ title, description }: { title: string; description: string }) {
  return <header className="bc-topbar"><div><div className="bc-eyebrow">Benjamin Capital Management / Manager Console</div><h1>{title}</h1><p>{description}</p></div><div className="bc-top-actions"><span className="bc-badge good">FRONTEND CONTRACT</span><span className="bc-badge warn">NO LIVE CAPITAL AUTHORITY</span></div></header>;
}

function Sidebar({ page, setPage }: { page: PageKey; setPage: (page: PageKey) => void }) {
  const groups=[...new Set(navItems.map((item)=>item.group))];
  return <aside className="bc-sidebar"><div className="bc-brand"><div className="bc-brand-mark">B</div><div><strong>BENJAMIN</strong><small>Capital Management</small></div></div>{groups.map((group)=><div className="bc-nav-group" key={group}><div className="bc-nav-label">{group}</div>{navItems.filter((item)=>item.group===group).map((item)=>{const enabled=enabledPages.has(item.key);return <button key={item.key} className={`bc-nav-button ${page===item.key?'active':''} ${enabled?'':'disabled'}`} onClick={()=>enabled&&setPage(item.key)} disabled={!enabled} title={enabled?item.label:`Frontend phase ${item.phase}`}><span>{item.glyph}</span><span>{item.label}</span></button>;})}</div>)}<div className="bc-side-footer"><span>Product mode <b>{companyModelStatus.productMode}</b></span><span>Live execution <b>OFF</b></span><span>Custody authority <b>NONE</b></span></div></aside>;
}

function Placeholder({ page }: { page: PageKey }) {
  const item=navItems.find((candidate)=>candidate.key===page)!;
  return <><Topbar title={item.label} description="This area is represented in the company information architecture but remains intentionally unavailable until its dedicated frontend phase is defined and verified."/><section className="bc-card bc-placeholder"><div><span className="bc-status research">PHASE {item.phase}</span><strong>{item.label} is next in the governed build sequence.</strong><p>The UI will not imply capability before its data model, controls, authority, evidence, and client impact are defined.</p></div></section></>;
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
  else if(page==='responsibility') content=<ResponsibilityCenter Topbar={Topbar} initialStructureId={responsibilityStructure}/>;
  else content=<Placeholder page={page}/>;

  return <div className="bc-shell"><Sidebar page={page} setPage={navigate}/><main className="bc-main">{content}</main></div>;
}
