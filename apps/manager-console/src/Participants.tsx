import type { ComponentType } from 'react';
import { capitalStructures, participants } from './company-model';

type TopbarProps = { title: string; description: string };
type Props = { Topbar: ComponentType<TopbarProps> };

export function Participants({ Topbar }: Props) {
  const pool = capitalStructures.find((item) => item.type === 'POOLED_PORTFOLIO') ?? capitalStructures[0];
  const poolParticipants = participants.filter((participant) => pool.participantIds.includes(participant.participantId));
  const economicTotal = poolParticipants.reduce((sum, participant) => sum + (participant.economicInterestPct ?? 0), 0);

  return <>
    <Topbar title="Participants" description="Track economic interest, beneficial participation, permissions, and reporting rights without confusing a participant with the capital structure Benjamin manages." />
    <section className="bc-grid metrics">
      <article className="bc-card bc-metric"><label>Participants</label><strong>{participants.length}</strong><small>Across preview structures</small></article>
      <article className="bc-card bc-metric"><label>{pool.name}</label><strong>{poolParticipants.length}</strong><small>Pooled participants</small></article>
      <article className="bc-card bc-metric"><label>Pool interest accounted</label><strong>{economicTotal}%</strong><small>Preview ownership check</small></article>
      <article className="bc-card bc-metric"><label>Shared mandate</label><strong>1</strong><small>Participants do not issue separate trades</small></article>
    </section>

    <section className="bc-card bc-hero">
      <div className="bc-hero-grid">
        <div>
          <div className="bc-eyebrow">POOLED CAPITAL / ECONOMIC INTEREST</div>
          <h2>{pool.name} <em>{pool.nav}</em></h2>
          <p className="bc-hero-copy">Benjamin manages the pool under one governed Responsibility. Participants own economic interests and receive scoped reporting, but they do not each inject separate market instructions into the shared decision engine.</p>
        </div>
        <div className="bc-constitution">
          <span>Pool mandate</span><strong>SHARED</strong>
          <span>Participant privacy</span><strong>SEGREGATED</strong>
          <span>Economic interest</span><strong>{economicTotal}% ACCOUNTED</strong>
          <span>Live unit accounting</span><strong><b>BACKEND PENDING</b></strong>
        </div>
      </div>
    </section>

    <section className="bc-card">
      <div className="bc-card-head"><div><h2>Participant ledger</h2><p>Economic interest and reporting rights are distinct from decision authority.</p></div><span className="bc-status active">FRONTEND CONTRACT</span></div>
      <table className="bc-authority-table">
        <thead><tr><th>Participant</th><th>Role</th><th>Economic interest</th><th>Reporting rights</th><th>Structure</th></tr></thead>
        <tbody>{participants.map((participant) => {
          const structure = capitalStructures.find((item) => item.participantIds.includes(participant.participantId));
          return <tr key={participant.participantId}>
            <td><strong>{participant.displayName}</strong><br/><span style={{color:'#6f7e97',fontSize:10}}>{participant.participantId}</span></td>
            <td>{participant.role.replaceAll('_', ' ')}</td>
            <td>{participant.economicInterestPct == null ? '—' : `${participant.economicInterestPct}%`}</td>
            <td>{participant.reportingRights.replaceAll('_', ' ')}</td>
            <td>{structure?.name ?? 'Multiple / unresolved preview'}</td>
          </tr>;
        })}</tbody>
      </table>
    </section>

    <section className="bc-grid two" style={{marginTop:16}}>
      <article className="bc-card">
        <div className="bc-card-head"><div><h2>Participant rights</h2><p>Rights that belong to the participant relationship.</p></div></div>
        <div className="bc-priority">
          {['View own economic interest','View permitted portfolio activity','Receive statements and tax records','Request permitted contribution/redemption','View mandate and decisions affecting their money'].map((item,index)=><div className="bc-priority-row" key={item}><b>{index+1}</b><span>{item}</span></div>)}
        </div>
      </article>
      <article className="bc-card">
        <div className="bc-card-head"><div><h2>Not participant authority</h2><p>Shared structures need one coherent governed responsibility.</p></div></div>
        <div className="bc-targets">
          <div className="bc-target"><span>Issue individual trade instruction into pool</span><strong>NO<small>NOT IMPLIED</small></strong></div>
          <div className="bc-target"><span>View another participant's private records</span><strong>NO<small>PRIVACY BOUNDARY</small></strong></div>
          <div className="bc-target"><span>Change shared risk envelope unilaterally</span><strong>NO<small>GOVERNED CHANGE</small></strong></div>
          <div className="bc-target"><span>Withdraw another participant's capital</span><strong>NO<small>ECONOMIC OWNERSHIP</small></strong></div>
        </div>
      </article>
    </section>
    <div className="bc-footer-note"><b>Accounting requirement discovered:</b> the future backend needs unit/NAV or equivalent participant capital-account accounting so subscriptions, redemptions, gains, losses, fees, and distributions are allocated without transferring one participant's economics to another.</div>
  </>;
}
