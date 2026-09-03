import type { ComponentType } from 'react';

type TopbarProps = { title: string; description: string };

const weights = [
  ['Predictive information', 'Spot 0.37', 'Futures 0.63', 'Futures currently carries more short-horizon directional information in this synthetic state.'],
  ['Regime information', 'Spot 0.46', 'Futures 0.54', 'Both markets contribute to the leverage/liquidity regime interpretation.'],
  ['Fragility / risk', 'Spot 0.18', 'Futures 0.82', 'Leverage, funding, open interest, and liquidation pressure dominate fragility assessment.'],
  ['Capital confidence', 'Spot 0.68', 'Futures 0.32', 'Futures supports direction but leverage expansion reduces confidence in adding capital.'],
  ['Execution suitability', 'Spot 0.78', 'Futures 0.22', 'The current responsibility permits spot execution and blocks futures execution.'],
];

export function MarketRelationships({ Topbar }: { Topbar: ComponentType<TopbarProps> }) {
  return <>
    <Topbar title="Market Relationships" description="Understand the economic relationships among spot, futures, perpetuals, term structure, leverage, liquidity, and cross-market price discovery before Benjamin routes capital." />

    <section className="bc-card bc-hero">
      <div className="bc-hero-grid">
        <div>
          <div className="bc-eyebrow">BTC ECONOMIC COMPLEX / SYNTHETIC FRONTEND PREVIEW</div>
          <h2>Direction can be bullish while <em>capital confidence falls.</em></h2>
          <p className="bc-hero-copy">This surface demonstrates the end-state reasoning contract. Futures evidence is not hard-coded as fake or dominant; its importance adapts by information family, market state, evidence quality, leverage, liquidity, basis, and current authority.</p>
        </div>
        <div className="bc-constitution">
          <span>Price discovery</span><strong>FUTURES LEADING · PREVIEW</strong>
          <span>Leverage state</span><strong><b>EXPANDING</b></strong>
          <span>Spot liquidity</span><strong>HEALTHY · PREVIEW</strong>
          <span>Capital posture</span><strong>REDUCED SIZE / WAIT</strong>
        </div>
      </div>
    </section>

    <section className="bc-grid two">
      <article className="bc-card">
        <div className="bc-card-head"><div><h2>Spot market</h2><p>Underlying-market evidence family.</p></div><span className="bc-status active">UNDERSTAND</span></div>
        <div className="bc-targets">
          <div className="bc-target"><span>Illustrative price</span><strong>$62,481</strong></div>
          <div className="bc-target"><span>Liquidity</span><strong>HEALTHY</strong></div>
          <div className="bc-target"><span>Cross-venue agreement</span><strong>HIGH</strong></div>
          <div className="bc-target"><span>Aggressive flow</span><strong>POSITIVE</strong></div>
          <div className="bc-target"><span>Realized volatility</span><strong>ELEVATED</strong></div>
        </div>
      </article>
      <article className="bc-card">
        <div className="bc-card-head"><div><h2>Futures / derivative market</h2><p>Leverage, positioning, financing, and forward-price evidence family.</p></div><span className="bc-status research">UNDERSTAND / EXECUTION BLOCKED</span></div>
        <div className="bc-targets">
          <div className="bc-target"><span>Illustrative future</span><strong>$62,792</strong></div>
          <div className="bc-target"><span>Basis</span><strong>+49.8 bps</strong></div>
          <div className="bc-target"><span>Funding / financing pressure</span><strong>POSITIVE</strong></div>
          <div className="bc-target"><span>Open interest</span><strong>EXPANDING</strong></div>
          <div className="bc-target"><span>Liquidation pressure</span><strong>ELEVATED</strong></div>
        </div>
      </article>
    </section>

    <section className="bc-card" style={{marginTop:16}}>
      <div className="bc-card-head"><div><h2>Adaptive relationship weights</h2><p>These illustrative values show why Benjamin needs multiple weight families instead of one static spot/futures split.</p></div><span className="bc-status research">SYNTHETIC</span></div>
      <table className="bc-authority-table">
        <thead><tr><th>Interpretation</th><th>Spot</th><th>Futures</th><th>Why it differs</th></tr></thead>
        <tbody>{weights.map(([kind,spot,futures,why])=><tr key={kind}><td><strong>{kind}</strong></td><td>{spot}</td><td>{futures}</td><td>{why}</td></tr>)}</tbody>
      </table>
    </section>

    <section className="bc-grid three" style={{marginTop:16}}>
      <article className="bc-card"><div className="bc-card-head"><div><h2>Relationship state</h2></div></div><div className="bc-priority">{['Basis expanding','Futures leading short-horizon move','Open interest rising with price','Spot confirms direction','Leverage fragility elevated'].map((item,index)=><div className="bc-priority-row" key={item}><b>{index+1}</b><span>{item}</span></div>)}</div></article>
      <article className="bc-card"><div className="bc-card-head"><div><h2>Benjamin interpretation</h2></div></div><div className="bc-targets"><div className="bc-target"><span>Directional evidence</span><strong>BULLISH</strong></div><div className="bc-target"><span>Fragility</span><strong>HIGH</strong></div><div className="bc-target"><span>Capital confidence</span><strong>MODERATE</strong></div><div className="bc-target"><span>Hedging value</span><strong>RISING</strong></div><div className="bc-target"><span>Execution preference</span><strong>SPOT</strong></div></div></article>
      <article className="bc-card"><div className="bc-card-head"><div><h2>Economic structures to learn</h2></div></div><div className="bc-priority">{['Directional exposure','Cash-and-carry / reverse carry','Funding and basis convergence','Cross-market hedge','Relative-value / spread','Roll and term structure'].map((item,index)=><div className="bc-priority-row" key={item}><b>{index+1}</b><span>{item}</span></div>)}</div></article>
    </section>

    <section className="bc-card" style={{marginTop:16}}>
      <div className="bc-card-head"><div><h2>Backend contract discovered by this surface</h2><p>ZLJ/Benjamin eventually need point-in-time relationship objects, not hard-coded labels.</p></div><span className="bc-status research">NOT IMPLEMENTED</span></div>
      <div className="bc-risk-grid"><div className="bc-risk"><span>Spot state</span><strong>Liquidity + flow</strong></div><div className="bc-risk"><span>Derivative state</span><strong>Basis + OI + funding</strong></div><div className="bc-risk"><span>Relationship state</span><strong>Lead/lag + divergence</strong></div><div className="bc-risk"><span>Weight families</span><strong>Adaptive + evidenced</strong></div></div>
    </section>
    <div className="bc-footer-note"><b>Interpretation rule:</b> “futures leads” does not mean “use futures.” Information authority, capital confidence, and execution authority are separate dimensions.</div>
  </>;
}
