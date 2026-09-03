import { accounts } from './company-model';
import type { ComponentType } from 'react';

type TopbarProps = { title: string; description: string };

export function Accounts({ Topbar }: { Topbar: ComponentType<TopbarProps> }) {
  return <><Topbar title="Accounts" description="Inspect the externally authoritative brokerage, exchange, custodian, and future on-chain account connections attached to Benjamin capital structures."/><div className="bc-actions" style={{marginBottom:16}}><button className="bc-button primary" disabled>+ Connect account — backend pending</button><button className="bc-button" disabled>Reconcile all — backend pending</button></div><section className="bc-card"><div className="bc-card-head"><div><h2>Account connections</h2><p>Connections are execution/custody surfaces; they do not define the economic responsibility by themselves.</p></div></div><table className="bc-authority-table"><thead><tr><th>Account</th><th>Provider</th><th>Type</th><th>Custody</th><th>Status</th></tr></thead><tbody>{accounts.map((account)=><tr key={account.accountId}><td><strong>{account.accountId}</strong></td><td>{account.provider}</td><td>{account.accountType}</td><td>{account.custody.replaceAll('_',' ')}</td><td><span className={`bc-status ${account.status==='CONNECTED'?'active':'research'}`}>{account.status}</span></td></tr>)}</tbody></table></section><div className="bc-footer-note"><b>Custody rule:</b> Benjamin's decision authority must not silently imply unrestricted withdrawal authority or beneficial ownership of client assets.</div></>;
}
