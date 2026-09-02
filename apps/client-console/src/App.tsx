import { useMemo, useState } from 'react';

type NavItem = { key: string; label: string; glyph: string };
type ClientSurfaceSpec = {
  title: string;
  question: string;
  sources: string[];
  actions: string[];
  metrics: Array<[string, string, string?]>;
  items: Array<[string, string, string]>;
};

const navItems: NavItem[] = [
  { key: 'home', label: 'Home', glyph: '⌂' },
  { key: 'account', label: 'My Account', glyph: '♙' },
  { key: 'performance', label: 'Performance', glyph: '⌁' },
  { key: 'activity', label: 'Activity', glyph: '◇' },
  { key: 'benjamin', label: 'Benjamin', glyph: '◉' },
  { key: 'mandate', label: 'Mandate', glyph: '▣' },
  { key: 'risk', label: 'Risk & Protection', glyph: '⬡' },
  { key: 'book', label: 'The Book', glyph: '▤' },
  { key: 'money', label: 'Money', glyph: '$' },
  { key: 'documents', label: 'Documents', glyph: '▧' },
  { key: 'messages', label: 'Messages & Alerts', glyph: '✉' },
  { key: 'support', label: 'Support', glyph: '?' },
  { key: 'tax', label: 'Tax Center', glyph: 'T' },
  { key: 'notifications', label: 'Notification Preferences', glyph: '◌' },
  { key: 'settings', label: 'Settings & Security', glyph: '⚙' },
];

const surfaceSpecs: Record<string, ClientSurfaceSpec> = {
  activity: {
    title: 'Activity', question: 'What has happened in my account?',
    sources: ['The Hand · account orders & fills', 'The Book · account transactions'],
    actions: ['Filter activity', 'View detail', 'Download activity', 'Dispute / request support'],
    metrics: [['Trades this month', '1,442'], ['Deposits', '$2,000.00'], ['Withdrawals', '$0.00'], ['Fees & costs', '-$1,521.70']],
    items: [['10:42 AM', 'Sold NVDA 120 sh', '+$156.72'], ['10:38 AM', 'Bought AMD 250 sh', 'Trade opened'], ['10:31 AM', 'Watchman blocked order', 'Position limit'], ['10:26 AM', 'Sold AAPL 80 sh', '+$96.32'], ['May 10', 'Monthly advisory fee', '-$84.00']],
  },
  benjamin: {
    title: 'Benjamin', question: 'What is Benjamin thinking and doing for my account right now?',
    sources: ['Benjamin · account decisions', 'ZLJ · qualified market evidence', 'The Book · account decision history'],
    actions: ['Ask Benjamin', 'View case detail', 'View decision detail', 'View strategy detail'],
    metrics: [['Current posture', 'SELECTIVE'], ['Active strategies', '2'], ['Decisions today', '27'], ['Latest confidence', '0.81']],
    items: [['AMD', 'BUY · EPX-SCALP-003', 'Qualified evidence · confidence 0.81'], ['NVDA', 'NO TRADE', 'Edge after costs insufficient'], ['AAPL', 'REDUCE', 'Short-horizon thesis decayed'], ['Cash', 'HOLD', 'No alternative edge meets threshold']],
  },
  mandate: {
    title: 'Mandate', question: 'What authority have I granted Benjamin?',
    sources: ['The Book · mandate', 'Watchman · constraints'],
    actions: ['View full mandate', 'Request mandate change', 'View history', 'Download mandate'],
    metrics: [['Mandate', 'BM-SCALP-01'], ['Managed capital', '$25,000'], ['Max deployed', '40%'], ['Daily loss limit', '1.00%']],
    items: [['Allowed horizon', 'Scalp → intraday', 'Short swing requires separate authority'], ['Maximum position', '5% of equity', 'Watchman enforced'], ['Leverage', 'Not permitted', 'Hard mandate rule'], ['Overnight holding', 'Not permitted', 'Current mandate'], ['Withdrawal authority', 'Not granted', 'Client / custodian controlled']],
  },
  risk: {
    title: 'Risk & Protection', question: 'What risk is being taken and what is Watchman preventing?',
    sources: ['Watchman · account decisions', 'Benjamin · risk metrics', 'The Book · risk history'],
    actions: ['View Watchman log', 'View limit details', 'View scenario results', 'Download risk report'],
    metrics: [['Risk utilization', '31%'], ['Daily loss utilization', '14%'], ['Drawdown utilization', '22%'], ['Watchman status', 'NORMAL']],
    items: [['Position concentration', '22.47%', 'Inside current limit'], ['Current drawdown', '-4.72%', 'Inside mandate'], ['Blocked today', '1 action', 'Position limit protected account'], ['Emergency halt', 'Available', 'Watchman governed control']],
  },
  book: {
    title: 'The Book', question: 'Can I verify the historical record of my account?',
    sources: ['The Book · account-scoped records'],
    actions: ['Search my Book', 'Filter by type', 'Export records', 'View receipt'],
    metrics: [['Account records', '18,442'], ['Verified', '100%'], ['Reconciled', '99.98%'], ['Open exceptions', '1']],
    items: [['BEN-D-084921', 'Benjamin decision', 'BUY AMD · confidence 0.81'], ['WATCH-11822', 'Watchman authorization', 'Mandate satisfied'], ['HAND-A-91221', 'Execution receipt', 'Broker fill reconciled'], ['OUT-40219', 'Outcome record', 'Net result +$18.42']],
  },
  money: {
    title: 'Money', question: 'Where is my money, and how do I move it?',
    sources: ['Custodian · balances', 'The Book · cash records', 'The Hand · governed transfers'],
    actions: ['Deposit funds', 'Withdraw funds', 'View transfer history', 'Manage funding sources'],
    metrics: [['Cash', '$5,847.32'], ['Buying power', '$7,412.65'], ['Invested', '$20,232.40'], ['Pending transfers', '$0.00']],
    items: [['Custodian', 'Interactive Brokers LLC', 'External custody'], ['Account type', 'Individual', 'Client-owned account'], ['Last deposit', '+$2,000.00', 'Apr 23, 2027'], ['Withdrawal authority', 'Client controlled', 'Benjamin cannot withdraw freely']],
  },
  documents: {
    title: 'Documents', question: 'What agreements and documents govern the relationship?',
    sources: ['The Book · document records'],
    actions: ['View document', 'Download', 'Sign / acknowledge', 'Request document'],
    metrics: [['Current agreements', '4'], ['Statements', '12'], ['Disclosures', '6'], ['Action required', '1']],
    items: [['Managed Account Agreement', 'Current', 'Signed Jan 18, 2027'], ['BM-SCALP-01 Mandate', 'Current', 'Version 3'], ['Account Statement', 'May 2027', 'Available'], ['Risk Disclosure', 'Current', 'Acknowledged']],
  },
  messages: {
    title: 'Messages & Alerts', question: 'What important messages and alerts do I have?',
    sources: ['Watchman · alerts', 'System · messages', 'The Book · communications'],
    actions: ['Mark read', 'View details', 'Configure alerts', 'Archive'],
    metrics: [['Unread', '3'], ['Risk alerts', '1'], ['Benjamin updates', '2'], ['Action required', '0']],
    items: [['Risk protection', 'Watchman blocked one position-limit breach', 'Today 10:31 AM'], ['Benjamin update', 'AMD trade completed and reconciled', 'Today 10:34 AM'], ['Account notice', 'Monthly statement available', 'May 31'], ['System', 'Custodian connection healthy', '8 sec ago']],
  },
  support: {
    title: 'Support', question: 'How do I get help?',
    sources: ['Support system', 'The Book · support records'],
    actions: ['Contact support', 'View tickets', 'Escalate', 'View responses'],
    metrics: [['Open tickets', '0'], ['Avg response', '18 min'], ['Account specialist', 'Assigned'], ['System status', 'Healthy']],
    items: [['Account question', 'Start secure conversation', 'General account support'], ['Trade review', 'Request decision explanation', 'Evidence-bound response'], ['Money movement', 'Custody / transfer support', 'Governed process'], ['Security', 'Report account concern', 'Priority routing']],
  },
  tax: {
    title: 'Tax Center', question: 'What tax information is available?',
    sources: ['The Book · tax records', 'Custodian · tax forms'],
    actions: ['Download tax forms', 'Export data', 'Generate tax report'],
    metrics: [['Realized gain', '$4,182.13'], ['Realized loss', '-$2,068.71'], ['Net realized', '$2,113.42'], ['Available forms', '2']],
    items: [['1099 package', '2027', 'Pending year-end'], ['Realized gain/loss report', 'YTD', 'Available'], ['Tax-lot activity', 'Current', 'View detail'], ['Cost-basis source', 'Custodian', 'Authoritative']],
  },
  notifications: {
    title: 'Notification Preferences', question: 'What notifications do I want and how?',
    sources: ['The Book · preferences', 'System · notifications'],
    actions: ['Update preferences', 'Test notifications', 'Save'],
    metrics: [['Email', 'ON'], ['Push', 'ON'], ['SMS', 'OFF'], ['Critical risk', 'ALWAYS ON']],
    items: [['Benjamin trade updates', 'Push + email', 'Enabled'], ['Watchman risk alerts', 'Push + email', 'Required critical alerts'], ['Statements', 'Email', 'Enabled'], ['Market commentary', 'Push', 'Disabled']],
  },
  settings: {
    title: 'Settings & Security', question: 'How do I manage my account settings and security?',
    sources: ['The Book · preferences', 'Identity / auth service'],
    actions: ['Update profile', 'Change recovery settings', 'Manage MFA', 'Manage authorized devices'],
    metrics: [['MFA', 'ENABLED'], ['Trusted devices', '2'], ['Last sign-in', '10:39 AM'], ['Security status', 'HEALTHY']],
    items: [['Profile & contact', 'Robert M.', 'Verified'], ['Multi-factor authentication', 'Authenticator app', 'Enabled'], ['Login notifications', 'Enabled', 'All new devices'], ['Authorized devices', '2 devices', 'Review']],
  },
};

const equityPoints = [12,15,14,17,19,18,22,21,24,23,28,31,29,35,34,39,37,43,47,45,51,49,55,58,56,61,65,63,69,72,68,74,76,81,79,86,84,89,93,90,96,92];

function EquityChart({ compact = false }: { compact?: boolean }) {
  const width = compact ? 420 : 720;
  const height = compact ? 120 : 250;
  const max = Math.max(...equityPoints);
  const min = Math.min(...equityPoints);
  const points = equityPoints.map((value, index) => `${(index / (equityPoints.length - 1)) * width},${height - ((value - min) / (max - min || 1)) * (height - 24) - 12}`).join(' ');
  const area = `0,${height} ${points} ${width},${height}`;
  return <svg className={compact ? 'equity-chart compact' : 'equity-chart'} viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Synthetic account equity curve"><defs><linearGradient id="areaBlue" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#2f70e8" stopOpacity=".22"/><stop offset="100%" stopColor="#2f70e8" stopOpacity="0"/></linearGradient></defs><line x1="0" y1={height*.25} x2={width} y2={height*.25}/><line x1="0" y1={height*.5} x2={width} y2={height*.5}/><line x1="0" y1={height*.75} x2={width} y2={height*.75}/><polygon points={area} fill="url(#areaBlue)"/><polyline points={points} fill="none" /></svg>;
}

function Pill({ children, tone = 'good' }: { children: string; tone?: 'good' | 'warn' | 'bad' | 'neutral' }) {
  return <span className={`client-pill ${tone}`}><i />{children}</span>;
}

function Metric({ label, value, sub, tone = 'normal' }: { label: string; value: string; sub?: string; tone?: 'normal' | 'good' | 'bad' }) {
  return <div className="client-metric"><span>{label}</span><strong className={tone === 'good' ? 'positive' : tone === 'bad' ? 'negative' : ''}>{value}</strong>{sub && <small className={tone === 'bad' ? 'negative' : 'positive'}>{sub}</small>}</div>;
}

function Onboarding({ onContinue }: { onContinue: () => void }) {
  const steps = ['Welcome', 'Your Profile', 'Mandate', 'Agreements', 'Brokerage', 'Funding', 'Activation'];
  return <section className="onboarding-screen"><header className="screen-title"><h1>1. Onboarding — Join Benjamin</h1><Pill tone="neutral">DESIGN PREVIEW</Pill></header><div className="stepper">{steps.map((step,index)=><div key={step} className={index===0?'step active':'step'}><b>{index+1}</b><span>{step}</span></div>)}</div><div className="onboarding-content"><div className="welcome-copy"><h2>Welcome to Benjamin<br/><span>Intelligent Capital Management<br/>With You in Control</span></h2><p>Benjamin is Epinnox’s capital decision intelligence for an individually managed account. It seeks short-duration opportunities in liquid markets using qualified market intelligence, strict account-specific controls, and reconstructable evidence.</p><div className="benefit-list"><div><b>◇</b><span><strong>Individually managed account</strong><small>Your money. Your mandate. Your externally custodied account.</small></span></div><div><b>◎</b><span><strong>Autonomous decision-making</strong><small>Benjamin analyzes and decides inside the authority you grant.</small></span></div><div><b>⬡</b><span><strong>Built-in risk governance</strong><small>Watchman enforces account limits before external action.</small></span></div><div><b>▤</b><span><strong>Reconstructable history</strong><small>Material decisions, governance, execution, and outcomes connect through The Book.</small></span></div></div></div><aside className="expect-card"><h3>What to Expect</h3><div><b>♙</b><span><strong>We learn about you and your goals</strong><small>Complete your financial profile.</small></span></div><div><b>⌁</b><span><strong>You set your mandate and risk limits</strong><small>You stay in control of the authority boundary.</small></span></div><div><b>▣</b><span><strong>We connect to a trusted broker or custodian</strong><small>You remain the account owner.</small></span></div><div><b>B</b><span><strong>Benjamin starts managing</strong><small>You monitor. Benjamin works inside the mandate.</small></span></div><div className="estimate"><b>◷</b><span><strong>Estimated time to complete</strong><small>15–20 minutes</small></span></div></aside></div><footer className="onboarding-footer"><button className="secondary">Cancel</button><button className="primary" onClick={onContinue}>Get Started →</button></footer></section>;
}

function Home() {
  return <div className="client-screen-stack"><section className="home-grid top-home"><article className="white-card value-card"><span>Current Account Value</span><strong>$28,491.72</strong><small className="positive">+$156.72 (0.55%) Today</small><div className="value-breakdown"><div><span>Starting Capital</span><b>$25,000.00</b></div><div><span>Withdrawals</span><b>$0.00</b></div><div><span>Investment Result</span><b className="positive">+$3,491.72</b></div></div></article><article className="white-card benjamin-card"><span>Benjamin Status</span><strong className="positive small-strong">ACTIVE</strong><div className="brain-mark">B</div><div className="benjamin-facts"><div><span>Current Posture</span><b>SELECTIVE</b></div><div><span>Market Regime</span><b>HIGH VOLATILITY</b></div><div><span>Capital Deployed</span><b>31%</b></div></div></article><article className="white-card health-card"><span>Account Health</span>{[['Account','Healthy'],['Brokerage','Connected'],['Watchman','Active'],['The Book','Reconciled'],['Last Sync','8 sec ago']].map(([a,b])=><div key={a}><span>✓ {a}</span><b>{b}</b></div>)}</article></section><section className="home-grid middle-home"><article className="white-card equity-card"><div className="card-head"><span>Account Equity (All Time)</span><div className="ranges"><b>1D</b><b>1W</b><b>1M</b><b>3M</b><b>6M</b><b>YTD</b><b>1Y</b><b className="active">ALL</b></div></div><EquityChart compact/><div className="axis"><span>Jan 27</span><span>Mar 27</span><span>May 27</span></div></article><article className="white-card today-card"><span>Today</span><strong className="positive">+$156.72</strong><small className="positive">0.55%</small><div className="today-grid"><div><span>Trades</span><b>27</b></div><div><span>Wins / Losses</span><b>18 / 9</b></div><div><span>Capital Deployed</span><b>31%</b></div><div><span>Gross P&L</span><b className="positive">+$212.91</b></div><div><span>Net P&L</span><b className="positive">+$156.72</b></div></div></article><article className="white-card positions-card"><div className="card-head"><span>Current Positions (3)</span><button>View All →</button></div><table><thead><tr><th>Symbol</th><th>Shares</th><th>Market</th><th>Market Value</th><th>P&L</th></tr></thead><tbody><tr><td>NVDA</td><td>120</td><td>$119.03</td><td>$14,283.60</td><td className="positive">+$312.48</td></tr><tr><td>AMD</td><td>250</td><td>$26.57</td><td>$6,827.50</td><td className="positive">+$185.25</td></tr><tr><td>AAPL</td><td>80</td><td>$66.81</td><td>$5,345.60</td><td className="positive">+$96.32</td></tr></tbody><tfoot><tr><td colSpan={3}>Total</td><td>$26,491.10</td><td className="positive">+$593.05</td></tr></tfoot></table></article></section><section className="home-grid bottom-home"><article className="white-card activity-card"><div className="card-head"><span>Recent Benjamin Activity</span></div><div className="feed"><div><time>10:42 AM</time><span>Exited NVDA position for <b className="positive">+$156.72</b></span><Pill>Trade Closed</Pill></div><div><time>10:38 AM</time><span>Watchman blocked additional AMD size</span><Pill tone="warn">Risk Protected</Pill></div><div><time>10:31 AM</time><span>Entered AMD based on EPX-SCALP-003</span><Pill>Trade Opened</Pill></div><div><time>10:26 AM</time><span>Identified opportunities — preserving capital</span><Pill tone="neutral">Decision</Pill></div><div><time>10:12 AM</time><span>Reduced AAPL exposure by 20%</span><Pill>Trade Closed</Pill></div></div><button className="text-link">View All Activity →</button></article><article className="white-card strategies-card"><div className="card-head"><span>Strategies in Use</span><button>View All →</button></div><div className="strategy-donut"><strong>2</strong><span>ACTIVE</span></div><div className="strategy-list"><div><i className="blue"/><span>EPX-SCALP-003</span><b>68%</b><small>$156.82</small></div><div><i className="cyan"/><span>EPX-SCALP-001</span><b>22%</b><small>$6.045</small></div><div><i className="navy"/><span>EPX-MOM-01</span><b>10%</b><small>$18.04</small></div></div></article><article className="white-card risk-card"><span>Risk Overview</span><div className="risk-circle"><strong>31%</strong><small>Risk Utilization</small></div><div className="risk-lines"><div><span>Daily Loss Utilization</span><b>14%</b></div><div><span>Drawdown Utilization</span><b>22%</b></div><div><span>Concentration</span><b>18%</b></div><div><span>Status</span><b className="positive">Normal</b></div></div></article></section></div>;
}

function MyAccount() {
  return <div className="client-screen-stack"><section className="metric-strip client-five"><Metric label="Net Liquidation Value" value="$28,491.72" sub="+$156.72 (0.55%) Today" tone="good"/><Metric label="Cash" value="$5,847.32"/><Metric label="Buying Power" value="$7,412.65"/><Metric label="Capital Deployed" value="$20,232.40" sub="31%" tone="good"/><Metric label="Daily P&L" value="+$156.72" sub="0.55%" tone="good"/></section><section className="account-grid"><article className="white-card positions-large"><div className="card-head"><span>Positions</span><button>View All →</button></div><table><thead><tr><th>Symbol</th><th>Shares</th><th>Avg. Cost</th><th>Market Price</th><th>Market Value</th><th>P&L (Unreal.)</th><th>P&L %</th></tr></thead><tbody><tr><td>NVDA</td><td>120</td><td>$118.32</td><td>$119.65</td><td>$14,238.00</td><td className="positive">+$312.48</td><td className="positive">2.24%</td></tr><tr><td>AMD</td><td>250</td><td>$26.57</td><td>$27.31</td><td>$6,827.50</td><td className="positive">+$185.25</td><td className="positive">2.78%</td></tr><tr><td>AAPL</td><td>80</td><td>$66.61</td><td>$67.82</td><td>$5,425.60</td><td className="positive">+$96.32</td><td className="positive">1.81%</td></tr><tr><td>MSFT</td><td>40</td><td>$409.21</td><td>$408.63</td><td>$16,345.20</td><td className="negative">-$23.20</td><td className="negative">-0.14%</td></tr></tbody><tfoot><tr><td colSpan={4}>Total</td><td>$42,836.30</td><td className="positive">+$570.85</td><td className="positive">1.35%</td></tr></tfoot></table></article><article className="white-card allocation-card"><span>Account Allocation</span><div className="allocation-donut"><strong>$38,491.72</strong><small>Total</small></div><div className="alloc-list"><div><i className="blue"/><span>Cash</span><b>20.5%</b><small>$5,847</small></div><div><i className="cyan"/><span>Equity Exposure</span><b>71.0%</b><small>$20,232</small></div><div><i className="gray"/><span>Risk Reserve</span><b>8.5%</b><small>$2,412</small></div></div></article></section><section className="account-bottom-grid"><article className="white-card"><div className="card-head"><span>Account Timeline</span><button>View All →</button></div><div className="timeline-list"><div><time>Jan 18, 2027</time><span>Account opened</span></div><div><time>Jan 18, 2027</time><span>Initial funding: $25,000.00</span></div><div><time>Jan 18, 2027</time><span>Mandate BM-SCALP-01 activated</span></div><div><time>Jan 23, 2027</time><span>Additional deposit: $2,000.00</span></div><div><time>Apr 12, 2027</time><span>Strategy EPX-MOM-01 added</span></div></div></article><article className="white-card"><span>Balance Breakdown</span><div className="summary-list">{[['Starting Capital','$25,000.00'],['Net Deposits','+$3,000.00'],['Withdrawals','$0.00'],['Gross Trading P&L','+$2,113.42'],['Fees (Advisory)','-$321.70'],['Trading Costs (Est.)','-$1,300.00'],['Net Investment Result','+$1,491.72'],['Current Equity','$28,491.72']].map(([a,b],index)=><div className={index===7?'total':''} key={a}><span>{a}</span><b className={b.startsWith('+')?'positive':b.startsWith('-')?'negative':''}>{b}</b></div>)}</div></article><article className="white-card brokerage-card"><span>Brokerage Connection</span><div className="broker-brand">IBKR <small>Interactive Brokers LLC</small></div><div className="summary-list"><div><span>Account Type</span><b>Individual</b></div><div><span>Account Number</span><b>U12345678</b></div><div><span>Status</span><b className="positive">● Connected</b></div><div><span>Last Sync</span><b>8 sec ago</b></div></div><button className="text-link">View in Money →</button></article></section></div>;
}

function Performance() {
  return <div className="client-screen-stack"><section className="metric-strip client-six"><Metric label="Net Return (All Time)" value="5.97%" sub="+$1,491.72" tone="good"/><Metric label="Gross Return" value="8.63%" sub="+$2,113.42" tone="good"/><Metric label="Realized P&L" value="+$1,842.13" tone="good"/><Metric label="Unrealized P&L" value="+$270.59" tone="good"/><Metric label="Max Drawdown" value="-4.72%" tone="bad"/><Metric label="Profit Factor" value="1.84"/></section><section className="performance-grid"><article className="white-card performance-chart"><div className="card-head"><span>Equity Curve</span><div className="ranges"><b>1D</b><b>1W</b><b>1M</b><b>3M</b><b>6M</b><b>YTD</b><b>1Y</b><b className="active">ALL</b></div></div><EquityChart/><div className="axis"><span>Jan 27</span><span>Feb 27</span><span>Mar 27</span><span>Apr 27</span><span>May 27</span></div></article><article className="white-card return-card"><span>Return Decomposition (All Time)</span><div className="summary-list">{[['Starting Capital','$25,000.00'],['Net Deposits','+$2,000.00'],['Withdrawals','$0.00'],['Gross Trading P&L','+$2,113.42'],['Advisory Fees','-$321.70'],['Trading Costs (Est.)','-$1,300.00'],['Net Investment Result','+$1,491.72'],['Current Equity','$28,491.72']].map(([a,b],i)=><div className={i>5?'total':''} key={a}><span>{a}</span><b className={b.startsWith('+')?'positive':b.startsWith('-')?'negative':''}>{b}</b></div>)}</div></article></section><section className="performance-bottom"><article className="white-card metrics-card"><span>Performance Metrics</span><div className="perf-metrics">{[['Winning Days','62.1%'],['Losing Days','37.9%'],['Avg Gain','+$24.38'],['Avg Loss','-$16.22'],['Profit Factor','1.84'],['Expected P/Trade','+$0.21'],['Total Trades','1,442'],['Winning Trades','1,073'],['Losing Trades','769'],['Max Drawdown','-4.72%']].map(([a,b])=><div key={a}><span>{a}</span><b className={b.startsWith('+')?'positive':b.startsWith('-')?'negative':''}>{b}</b></div>)}</div></article><article className="white-card"><span>Performance by Strategy</span><div className="strategy-donut large"><strong>+$1,491.72</strong><span>Total Return</span></div><div className="strategy-list"><div><i className="blue"/><span>EPX-SCALP-003</span><b className="positive">+$1,056.24</b><small>70.5%</small></div><div><i className="cyan"/><span>EPX-SCALP-001</span><b className="positive">+$382.21</b><small>24.2%</small></div><div><i className="navy"/><span>EPX-MOM-01</span><b className="positive">+$77.17</b><small>5.2%</small></div></div></article><article className="white-card monthly-card"><div className="card-head"><span>Monthly Performance</span><button>View Table →</button></div><div className="month-bars">{[['Dec ’26','+1.22%',30],['Jan ’27','+2.87%',62],['Feb ’27','+3.92%',82],['Mar ’27','-1.18%',-30],['Apr ’27','+4.21%',90],['May ’27','+2.11%',50]].map(([m,v,h])=><div key={m}><span>{v}</span><i className={Number(h)<0?'down':''} style={{height:`${Math.abs(Number(h))}%`}}/><small>{m}</small></div>)}</div></article></section></div>;
}

function ClientOperationalSurface({ spec }: { spec: ClientSurfaceSpec }) {
  return <section className="operational-client"><header className="screen-title"><div><h1>{spec.title}</h1><p>{spec.question}</p></div><Pill tone="neutral">ACCOUNT-SCOPED</Pill></header><div className="metric-strip client-four">{spec.metrics.map(([label,value,sub])=><Metric key={label} label={label} value={value} sub={sub}/>)}</div><div className="client-surface-grid"><article className="white-card"><div className="card-head"><span>Current account view</span><button>Refresh</button></div><div className="surface-items">{spec.items.map(([a,b,c])=><div key={`${a}-${b}`}><strong>{a}</strong><span>{b}</span><small>{c}</small></div>)}</div></article><article className="white-card scope-card"><span>Authoritative sources</span><ul>{spec.sources.map(source=><li key={source}>{source}</li>)}</ul><span className="subhead">Available actions</span><div className="surface-actions">{spec.actions.map(action=><button key={action}>{action}</button>)}</div><div className="privacy-note"><strong>Account boundary</strong><p>This surface is constructed from Robert M.’s authorized account read model. Another client’s account state is not part of this payload.</p></div></article></div></section>;
}

export function App() {
  const [active, setActive] = useState('home');
  const activeItem = useMemo(() => navItems.find(item => item.key === active), [active]);

  const renderScreen = () => {
    if (active === 'onboarding') return <Onboarding onContinue={() => setActive('home')} />;
    if (active === 'home') return <Home />;
    if (active === 'account') return <MyAccount />;
    if (active === 'performance') return <Performance />;
    const spec = surfaceSpecs[active];
    return spec ? <ClientOperationalSurface spec={spec} /> : null;
  };

  return <div className="client-app-shell"><aside className="client-sidebar"><div className="client-brand"><div className="crest">B</div><div><strong>BENJAMIN</strong><span>AN EPINNOX SYSTEM</span></div></div><nav><button className={active==='onboarding'?'active onboarding-link':'onboarding-link'} onClick={()=>setActive('onboarding')}><span>01</span><b>Join Benjamin</b></button>{navItems.map(item=><button key={item.key} className={active===item.key?'active':''} onClick={()=>setActive(item.key)}><span>{item.glyph}</span><b>{item.label}</b></button>)}</nav><div className="support-box"><span>Need help?</span><strong>Chat with Support</strong></div><div className="system-health"><span>System Status</span><strong><i/>Design systems healthy</strong></div></aside><main className="client-workspace"><header className="client-topbar"><div className="topbar-context">{active==='onboarding'?'RELATIONSHIP SETUP':activeItem?.label.toUpperCase()}</div><div className="account-select"><span>Account</span><strong>BEN-000184</strong><b>⌄</b></div><button className="bell">♢</button><div className="client-user"><div>RM</div><span>Robert M.</span></div></header><div className="prototype-banner">DESIGN / SHADOW DATA — NOT LIVE PERFORMANCE OR LIVE CLIENT CAPITAL</div><div className="client-page">{renderScreen()}</div></main></div>;
}
