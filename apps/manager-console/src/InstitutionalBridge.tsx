import type { ComponentType } from 'react';

type TopbarProps = { title: string; description: string };
type BridgeKind = 'watchman' | 'hand' | 'book';

const bridgeCopy = {
  watchman: {
    title: 'Watchman Bridge',
    description: 'See how Benjamin decisions are governed without turning Benjamin into the policy authority.',
    eyebrow: 'BENJAMIN.DECISION → WATCHMAN.AUTHORIZATION / BLOCK',
    headline: 'Benjamin proposes. Watchman decides whether the path may proceed.',
    status: 'PENDING / READ-ONLY PREVIEW',
  },
  hand: {
    title: 'The Hand Bridge',
    description: 'See authorized external-action status and receipts without giving Benjamin execution authority.',
    eyebrow: 'WATCHMAN.AUTHORIZATION → HAND.EXECUTION',
    headline: 'The Hand receives authorized intent; it never receives raw market opinions as economic authority.',
    status: 'NO LIVE EXECUTION',
  },
  book: {
    title: 'The Book Bridge',
    description: 'Trace Benjamin decisions to evidence and receipts without duplicating The Book’s forensic administration frontend.',
    eyebrow: 'ZLJ → BENJAMIN → WATCHMAN → HAND → BOOK',
    headline: 'Every material capital story should be reconstructable from signed, causally linked evidence.',
    status: 'FRONTEND CONTRACT',
  },
} as const;

export function InstitutionalBridge({ kind, Topbar }: { kind: BridgeKind; Topbar: ComponentType<TopbarProps> }) {
  const copy = bridgeCopy[kind];
  return <>
    <Topbar title={copy.title} description={copy.description} />
    <section className="bc-card bc-hero">
      <div className="bc-hero-grid">
        <div><div className="bc-eyebrow">{copy.eyebrow}</div><h2>{copy.headline}</h2><p className="bc-hero-copy">This is a Benjamin-side projection of another institutional organ. Operational controls for that organ remain in its own frontend and authority plane.</p></div>
        <div className="bc-constitution"><span>Bridge mode</span><strong>READ ONLY</strong><span>Current status</span><strong><b>{copy.status}</b></strong><span>Capital authority inherited</span><strong>NONE</strong><span>Deep administration</span><strong>OTHER ORGAN</strong></div>
      </div>
    </section>
    {kind === 'watchman' && <WatchmanPreview />}
    {kind === 'hand' && <HandPreview />}
    {kind === 'book' && <BookPreview />}
  </>;
}

function WatchmanPreview() {
  return <><section className="bc-grid metrics"><article className="bc-card bc-metric"><label>Awaiting governance</label><strong>1</strong><small>Synthetic decision preview</small></article><article className="bc-card bc-metric"><label>Authorized</label><strong>0</strong><small>No live authorization asserted</small></article><article className="bc-card bc-metric"><label>Blocked</label><strong>1</strong><small>Historical synthetic example</small></article><article className="bc-card bc-metric"><label>Policy authority</label><strong>WATCHMAN</strong><small>Not Benjamin</small></article></section><section className="bc-card"><div className="bc-card-head"><div><h2>Governance queue projection</h2><p>What Benjamin needs to know about the disposition of its decisions.</p></div><span className="bc-status research">SYNTHETIC</span></div><table className="bc-authority-table"><thead><tr><th>Decision</th><th>Structure</th><th>Requested path</th><th>Watchman state</th><th>Reason</th></tr></thead><tbody><tr><td><strong>BEN-D-PREVIEW-001</strong></td><td>Family Growth I</td><td>Increase BTC spot exposure</td><td>PENDING</td><td>Await independent mandate/risk authorization</td></tr><tr><td><strong>BEN-D-PREVIEW-000</strong></td><td>Family Growth I</td><td>Increase derivative exposure</td><td>BLOCKED</td><td>Current Responsibility does not permit derivatives execution</td></tr></tbody></table></section><div className="bc-footer-note"><b>Watchman boundary:</b> Benjamin may read authorization/block results and reasons. It may not edit Watchman policy from this bridge.</div></>;
}

function HandPreview() {
  return <><section className="bc-grid metrics"><article className="bc-card bc-metric"><label>Authorized queue</label><strong>0</strong><small>No live action asserted</small></article><article className="bc-card bc-metric"><label>In progress</label><strong>0</strong><small>Frontend contract only</small></article><article className="bc-card bc-metric"><label>Reconciled receipts</label><strong>1</strong><small>Synthetic example</small></article><article className="bc-card bc-metric"><label>Execution authority</label><strong>HAND</strong><small>Not Benjamin</small></article></section><section className="bc-card"><div className="bc-card-head"><div><h2>Execution projection</h2><p>Benjamin sees execution outcomes after Watchman authorization; it does not operate provider credentials here.</p></div><span className="bc-status research">SYNTHETIC</span></div><table className="bc-authority-table"><thead><tr><th>Receipt</th><th>Authorization</th><th>Capability</th><th>Result</th><th>Reconciliation</th></tr></thead><tbody><tr><td><strong>HAND-PREVIEW-021</strong></td><td>WATCH-PREVIEW-013</td><td>SPOT.REDUCE</td><td>COMPLETED</td><td>RECONCILED</td></tr></tbody></table></section><div className="bc-footer-note"><b>Hand boundary:</b> exchange/broker credentials, signing authorities, adapters, provider permissions, and live execution controls belong to The Hand frontend—not Benjamin.</div></>;
}

function BookPreview() {
  const chain = [
    ['ZLJ.INTELLIGENCE','Qualified market/intelligence evidence'],
    ['BENJAMIN.DECISION','Responsibility-bound capital judgment'],
    ['WATCHMAN.AUTHORIZATION','Independent authority result'],
    ['HAND.EXECUTION','External-action receipt'],
    ['ACCOUNTING.OUTCOME','Reconciled economic outcome'],
  ];
  return <><section className="bc-grid two"><article className="bc-card"><div className="bc-card-head"><div><h2>Causal evidence chain</h2><p>The manager can inspect the story; The Book owns durable proof and forensic verification.</p></div><span className="bc-status research">SYNTHETIC</span></div><div className="bc-priority">{chain.map(([event,meaning],index)=><div className="bc-priority-row" key={event}><b>{index+1}</b><span><strong>{event}</strong> — {meaning}</span></div>)}</div></article><article className="bc-card"><div className="bc-card-head"><div><h2>What Benjamin may query</h2></div></div><div className="bc-targets"><div className="bc-target"><span>Decision evidence</span><strong>READ</strong></div><div className="bc-target"><span>Authorization evidence</span><strong>READ</strong></div><div className="bc-target"><span>Execution receipts</span><strong>READ</strong></div><div className="bc-target"><span>Accounting outcomes</span><strong>READ</strong></div><div className="bc-target"><span>Rewrite/delete evidence</span><strong>NO<small>BOOK AUTHORITY</small></strong></div></div></article></section><div className="bc-footer-note"><b>Book boundary:</b> Benjamin should be able to navigate evidence relevant to its managed capital, but hash verification, evidence ingestion policy, forensic replay, audit exports, and Little Book disclosure administration belong in The Book’s own frontend.</div></>;
}
