import { useMemo, useState } from 'react';
import {
  capitalStructures,
  companyModelStatus,
  responsibilities,
  type AuthorityState,
} from './company-model';

type PageKey =
  | 'command'
  | 'relationships'
  | 'structures'
  | 'participants'
  | 'accounts'
  | 'responsibility'
  | 'router'
  | 'decisions'
  | 'markets'
  | 'watchman'
  | 'hand'
  | 'book'
  | 'reports'
  | 'operations';

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

const enabledPages = new Set<PageKey>(['command', 'responsibility']);

function AuthorityChip({ value }: { value: AuthorityState }) {
  return <span className={`bc-authority-chip ${value}`}>{value.replace('_', ' ')}</span>;
}

function Sidebar({ page, setPage }: { page: PageKey; setPage: (page: PageKey) => void }) {
  const groups = [...new Set(navItems.map((item) => item.group))];
  return (
    <aside className="bc-sidebar">
      <div className="bc-brand">
        <div className="bc-brand-mark">B</div>
        <div><strong>BENJAMIN</strong><small>Capital Management</small></div>
      </div>
      {groups.map((group) => (
        <div className="bc-nav-group" key={group}>
          <div className="bc-nav-label">{group}</div>
          {navItems.filter((item) => item.group === group).map((item) => {
            const enabled = enabledPages.has(item.key);
            return (
              <button
                key={item.key}
                className={`bc-nav-button ${page === item.key ? 'active' : ''} ${enabled ? '' : 'disabled'}`}
                onClick={() => enabled && setPage(item.key)}
                disabled={!enabled}
                title={enabled ? item.label : `Frontend phase ${item.phase}`}
              >
                <span>{item.glyph}</span><span>{item.label}</span>
              </button>
            );
          })}
        </div>
      ))}
      <div className="bc-side-footer">
        <span>Product mode <b>{companyModelStatus.productMode}</b></span>
        <span>Live execution <b>OFF</b></span>
        <span>Custody authority <b>NONE</b></span>
      </div>
    </aside>
  );
}

function Topbar({ title, description }: { title: string; description: string }) {
  return (
    <header className="bc-topbar">
      <div>
        <div className="bc-eyebrow">Benjamin Capital Management / Manager Console</div>
        <h1>{title}</h1>
        <p>{description}</p>
      </div>
      <div className="bc-top-actions">
        <span className="bc-badge good">FRONTEND CONTRACT</span>
        <span className="bc-badge warn">NO LIVE CAPITAL AUTHORITY</span>
      </div>
    </header>
  );
}

function CompanyCommand() {
  const totalStructures = capitalStructures.length;
  const active = capitalStructures.filter((item) => item.status === 'ACTIVE').length;
  const pooled = capitalStructures.filter((item) => item.type === 'POOLED_PORTFOLIO').length;
  const responsibility = responsibilities[0];
  return (
    <>
      <Topbar title="Company Command" description="Operate Benjamin as a capital-management company while keeping the Benjamin decision engine inside explicit account and portfolio responsibilities." />
      <section className="bc-card bc-hero">
        <div className="bc-hero-grid">
          <div>
            <div className="bc-eyebrow">THE MONEY MAN + THE MONEY LOGIC</div>
            <h2>Define the responsibility. <em>Benjamin chooses the path.</em></h2>
            <p className="bc-hero-copy">The company manages relationships, capital structures, participants, accounts, mandates, and reporting. The decision engine receives those governed structures and qualified market intelligence, evaluates permissible economic paths, and records the best justified capital decision for Watchman.</p>
          </div>
          <div className="bc-constitution">
            <span>Institutional chain</span>
            <strong>ZLJ <b>sees</b></strong>
            <strong>Benjamin <b>decides</b></strong>
            <strong>Watchman <b>governs</b></strong>
            <strong>Hand <b>executes</b></strong>
            <strong>Book <b>proves</b></strong>
          </div>
        </div>
      </section>
      <section className="bc-grid metrics">
        <article className="bc-card bc-metric"><label>Capital structures</label><strong>{totalStructures}</strong><small>Individual, joint, entity, pool</small></article>
        <article className="bc-card bc-metric"><label>Active structures</label><strong>{active}</strong><small>Preview domain state</small></article>
        <article className="bc-card bc-metric"><label>Pooled structures</label><strong>{pooled}</strong><small>End-state model represented</small></article>
        <article className="bc-card bc-metric"><label>Active responsibility</label><strong>{responsibility.name}</strong><small>Version {responsibility.version}</small></article>
      </section>
      <section className="bc-grid two">
        <article className="bc-card">
          <div className="bc-card-head"><div><h2>Company model</h2><p>What Benjamin Capital Management owns operationally.</p></div><span className="bc-status active">DEFINED</span></div>
          <div className="bc-priority">
            {[
              ['Relationship', 'Who Benjamin has a governed capital-management relationship with.'],
              ['Capital Structure', 'The economic container whose money Benjamin is responsible for.'],
              ['Participant', 'Who has economic interest, beneficial ownership, permission, or reporting rights.'],
              ['Account', 'The externally authoritative custody/broker/exchange connection.'],
              ['Responsibility', 'What Benjamin must accomplish and which paths are permitted.'],
              ['Decision', 'The selected economic path after comparing permissible alternatives.'],
            ].map(([name, detail], index) => <div className="bc-priority-row" key={name}><b>{index + 1}</b><span><strong>{name}</strong> — {detail}</span></div>)}
          </div>
        </article>
        <article className="bc-card">
          <div className="bc-card-head"><div><h2>Current build boundary</h2><p>Capabilities are modeled before they are activated.</p></div><span className="bc-status research">PREVIEW</span></div>
          <div className="bc-targets">
            <div className="bc-target"><span>Capital custody</span><strong>NONE<small>NOT ACTIVATED</small></strong></div>
            <div className="bc-target"><span>Live execution</span><strong>OFF<small>NOT ACTIVATED</small></strong></div>
            <div className="bc-target"><span>Crypto futures understanding</span><strong>MODELED</strong></div>
            <div className="bc-target"><span>Crypto futures execution</span><strong>DISABLED<small>RESPONSIBILITY GATE</small></strong></div>
            <div className="bc-target"><span>Responsibility versioning</span><strong>DEFINED</strong></div>
          </div>
        </article>
      </section>
      <div className="bc-footer-note"><b>Product rule:</b> the owner defines Benjamin's responsibility and authority. Benjamin is not configured by manually forcing daily trades or hidden model weights through this console.</div>
    </>
  );
}

function ResponsibilityCenter() {
  const [structureId, setStructureId] = useState('CAP-POOL-001');
  const structure = useMemo(() => capitalStructures.find((item) => item.structureId === structureId) ?? capitalStructures[0], [structureId]);
  const responsibility = responsibilities.find((item) => item.structureId === structure.structureId) ?? responsibilities[0];
  return (
    <>
      <Topbar title="Responsibility Center" description="Set what Benjamin is responsible for achieving, what it may understand, what it may execute, and how much risk or liquidity authority exists for each capital structure." />
      <section className="bc-card bc-hero">
        <div className="bc-hero-grid">
          <div>
            <div className="bc-eyebrow">OWNER DEFINED / VERSIONED AUTHORITY</div>
            <h2>{responsibility.name} <em>v{responsibility.version}</em></h2>
            <p className="bc-hero-copy">{responsibility.mission}</p>
            <div className="bc-actions">
              <select className="bc-button" value={structure.structureId} onChange={(event) => setStructureId(event.target.value)}>
                {capitalStructures.map((item) => <option value={item.structureId} key={item.structureId}>{item.name}</option>)}
              </select>
              <button className="bc-button gold" disabled>Edit responsibility — backend pending</button>
              <button className="bc-button" disabled>Version history — backend pending</button>
            </div>
          </div>
          <div className="bc-constitution">
            <span>Capital structure</span><strong>{structure.name}</strong>
            <span>Structure type</span><strong>{structure.type.replaceAll('_', ' ')}</strong>
            <span>Autonomy</span><strong>{responsibility.autonomy.replaceAll('_', ' ')}</strong>
            <span>Effective</span><strong>{responsibility.effectiveAt.slice(0, 10)}</strong>
          </div>
        </div>
      </section>

      <section className="bc-grid metrics">
        <article className="bc-card bc-metric"><label>Primary objective</label><strong>{responsibility.primaryObjective.replaceAll('_', ' ')}</strong><small>Targets do not imply guarantees</small></article>
        <article className="bc-card bc-metric"><label>Max drawdown</label><strong>{responsibility.maxDrawdownPct}%</strong><small>Hard risk boundary</small></article>
        <article className="bc-card bc-metric"><label>Minimum liquidity</label><strong>{responsibility.minLiquidityPct}%</strong><small>Reserve requirement</small></article>
        <article className="bc-card bc-metric"><label>Max instrument exposure</label><strong>{responsibility.maxInstrumentExposurePct}%</strong><small>Per economic instrument</small></article>
      </section>

      <section className="bc-grid two">
        <article className="bc-card">
          <div className="bc-card-head"><div><h2>Objective precedence</h2><p>Hard priorities are evaluated before return optimization.</p></div><span className="bc-status active">ACTIVE</span></div>
          <div className="bc-priority">
            {responsibility.objectivePrecedence.map((item, index) => <div className="bc-priority-row" key={item}><b>{index + 1}</b><span>{item.replaceAll('_', ' ')}</span></div>)}
          </div>
        </article>
        <article className="bc-card">
          <div className="bc-card-head"><div><h2>Targets</h2><p>Desired outcomes and hard boundaries attached to this responsibility.</p></div></div>
          <div className="bc-targets">
            {responsibility.targets.map((target) => <div className="bc-target" key={target.targetId}><span>{target.label}</span><strong>{target.value}{target.hardBoundary && <small>HARD BOUNDARY</small>}</strong></div>)}
          </div>
        </article>
      </section>

      <section className="bc-grid two" style={{ marginTop: 16 }}>
        <article className="bc-card">
          <div className="bc-card-head"><div><h2>Market authority</h2><p>Benjamin may understand a market without being permitted to express exposure in it.</p></div></div>
          <table className="bc-authority-table">
            <thead><tr><th>Market</th><th>Understand</th><th>Execute</th></tr></thead>
            <tbody>{responsibility.marketAuthority.map((item) => <tr key={item.market}><td>{item.market}</td><td><AuthorityChip value={item.understand} /></td><td><AuthorityChip value={item.execute} /></td></tr>)}</tbody>
          </table>
        </article>
        <article className="bc-card">
          <div className="bc-card-head"><div><h2>Economic action authority</h2><p>What transformations the router may consider for this capital structure.</p></div></div>
          <table className="bc-authority-table">
            <thead><tr><th>Action</th><th>Authority</th></tr></thead>
            <tbody>{responsibility.actionAuthority.map((item) => <tr key={item.action}><td>{item.action}</td><td><AuthorityChip value={item.state} /></td></tr>)}</tbody>
          </table>
        </article>
      </section>

      <section className="bc-card" style={{ marginTop: 16 }}>
        <div className="bc-card-head"><div><h2>Risk & capital envelope</h2><p>The router must reason inside this feasible set before comparing expected economic outcomes.</p></div><span className="bc-status active">OWNER CONTROLLED</span></div>
        <div className="bc-risk-grid">
          <div className="bc-risk"><span>Max drawdown</span><strong>{responsibility.maxDrawdownPct}%</strong></div>
          <div className="bc-risk"><span>Min liquidity</span><strong>{responsibility.minLiquidityPct}%</strong></div>
          <div className="bc-risk"><span>Max instrument</span><strong>{responsibility.maxInstrumentExposurePct}%</strong></div>
          <div className="bc-risk"><span>Max correlated</span><strong>{responsibility.maxCorrelatedExposurePct}%</strong></div>
        </div>
      </section>
      <div className="bc-footer-note"><b>Authority rule:</b> changing a Responsibility creates a new effective version for future decisions. Prior decisions remain bound to the version that existed when they were made.</div>
    </>
  );
}

function Placeholder({ page }: { page: PageKey }) {
  const item = navItems.find((nav) => nav.key === page)!;
  return <><Topbar title={item.label} description="This area is represented in the company information architecture but remains intentionally unimplemented until its dedicated frontend phase is defined and verified." /><section className="bc-card bc-placeholder"><div><span className="bc-status research">PHASE {item.phase}</span><strong>{item.label} is next in the governed build sequence.</strong><p>Keeping the surface explicit but unavailable prevents the frontend from implying capability before its data model, controls, authority, and evidence expectations are defined.</p></div></section></>;
}

export function App() {
  const [page, setPage] = useState<PageKey>('command');
  return (
    <div className="bc-shell">
      <Sidebar page={page} setPage={setPage} />
      <main className="bc-main">
        {page === 'command' ? <CompanyCommand /> : page === 'responsibility' ? <ResponsibilityCenter /> : <Placeholder page={page} />}
      </main>
    </div>
  );
}
