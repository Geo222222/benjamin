export type CapitalStructureType =
  | 'INDIVIDUAL_MANAGED_ACCOUNT'
  | 'HOUSEHOLD_OR_JOINT_PORTFOLIO'
  | 'ENTITY_OR_TREASURY_ACCOUNT'
  | 'POOLED_PORTFOLIO';

export type RelationshipType = 'PERSON' | 'HOUSEHOLD' | 'TRUST' | 'ENTITY';
export type ParticipantRole = 'OWNER' | 'BENEFICIAL_OWNER' | 'PARTICIPANT' | 'AUTHORIZED_VIEWER';
export type AuthorityState = 'ENABLED' | 'DISABLED' | 'RESEARCH_ONLY';
export type AutonomyLevel = 'ADVISORY' | 'CONFIRM_EACH_DECISION' | 'FULL_WITHIN_MANDATE';

export type Relationship = {
  relationshipId: string;
  displayName: string;
  relationshipType: RelationshipType;
  status: 'ACTIVE' | 'ONBOARDING' | 'RESTRICTED';
  structureIds: string[];
};

export type Participant = {
  participantId: string;
  relationshipId: string;
  displayName: string;
  role: ParticipantRole;
  economicInterestPct: number | null;
  reportingRights: 'FULL_STRUCTURE' | 'OWN_INTEREST_ONLY' | 'ACCOUNT_OWNER';
};

export type AccountConnection = {
  accountId: string;
  provider: string;
  accountType: string;
  custody: 'EXTERNAL' | 'CLIENT_CONTROLLED' | 'FUTURE_ONCHAIN';
  status: 'CONNECTED' | 'PENDING' | 'RESTRICTED';
};

export type Target = {
  targetId: string;
  label: string;
  value: string;
  priority: number;
  hardBoundary: boolean;
};

export type MarketAuthority = {
  market: string;
  understand: AuthorityState;
  execute: AuthorityState;
};

export type ActionAuthority = {
  action: string;
  state: AuthorityState;
  note?: string;
};

export type Responsibility = {
  responsibilityId: string;
  version: number;
  structureId: string;
  name: string;
  mission: string;
  primaryObjective: string;
  objectivePrecedence: string[];
  targets: Target[];
  autonomy: AutonomyLevel;
  horizons: string[];
  marketAuthority: MarketAuthority[];
  actionAuthority: ActionAuthority[];
  maxDrawdownPct: number;
  minLiquidityPct: number;
  maxInstrumentExposurePct: number;
  maxCorrelatedExposurePct: number;
  effectiveAt: string;
  status: 'ACTIVE' | 'SUPERSEDED' | 'DRAFT';
};

export type CandidateEconomicPath = {
  pathId: string;
  label: string;
  market: string;
  expectedBenefit: string;
  expectedDownside: string;
  capitalRequired: string;
  score: number;
  status: 'PERMITTED' | 'BLOCKED' | 'RESEARCH_ONLY';
  reason: string;
};

export type CapitalStructure = {
  structureId: string;
  name: string;
  type: CapitalStructureType;
  status: 'ACTIVE' | 'ONBOARDING' | 'RESTRICTED';
  baseCurrency: string;
  nav: string;
  cash: string;
  deployed: string;
  participantIds: string[];
  accountIds: string[];
  activeResponsibilityId: string;
  participantCount: number;
};

export const relationships: Relationship[] = [
  { relationshipId: 'REL-001', displayName: 'Robert M.', relationshipType: 'PERSON', status: 'ACTIVE', structureIds: ['CAP-IMA-001'] },
  { relationshipId: 'REL-002', displayName: 'Martin Family', relationshipType: 'HOUSEHOLD', status: 'ACTIVE', structureIds: ['CAP-POOL-001', 'CAP-JOINT-001'] },
  { relationshipId: 'REL-003', displayName: 'Northstar Holdings LLC', relationshipType: 'ENTITY', status: 'ACTIVE', structureIds: ['CAP-ENTITY-001'] },
];

export const participants: Participant[] = [
  { participantId: 'PART-001', relationshipId: 'REL-001', displayName: 'Robert M.', role: 'OWNER', economicInterestPct: 100, reportingRights: 'ACCOUNT_OWNER' },
  { participantId: 'PART-101', relationshipId: 'REL-002', displayName: 'Participant A', role: 'PARTICIPANT', economicInterestPct: 40, reportingRights: 'OWN_INTEREST_ONLY' },
  { participantId: 'PART-102', relationshipId: 'REL-002', displayName: 'Participant B', role: 'PARTICIPANT', economicInterestPct: 30, reportingRights: 'OWN_INTEREST_ONLY' },
  { participantId: 'PART-103', relationshipId: 'REL-002', displayName: 'Participant C', role: 'PARTICIPANT', economicInterestPct: 20, reportingRights: 'OWN_INTEREST_ONLY' },
  { participantId: 'PART-104', relationshipId: 'REL-002', displayName: 'Participant D', role: 'PARTICIPANT', economicInterestPct: 10, reportingRights: 'OWN_INTEREST_ONLY' },
  { participantId: 'PART-201', relationshipId: 'REL-003', displayName: 'Northstar Holdings LLC', role: 'OWNER', economicInterestPct: 100, reportingRights: 'ACCOUNT_OWNER' },
];

export const accounts: AccountConnection[] = [
  { accountId: 'ACC-IMA-001', provider: 'IBKR', accountType: 'Individual brokerage', custody: 'EXTERNAL', status: 'CONNECTED' },
  { accountId: 'ACC-POOL-001', provider: 'Preview Custodian', accountType: 'Pooled structure preview', custody: 'EXTERNAL', status: 'PENDING' },
  { accountId: 'ACC-JOINT-001', provider: 'Fidelity', accountType: 'Joint brokerage', custody: 'EXTERNAL', status: 'CONNECTED' },
  { accountId: 'ACC-ENTITY-001', provider: 'Coinbase', accountType: 'Entity spot account', custody: 'EXTERNAL', status: 'CONNECTED' },
];

export const responsibilities: Responsibility[] = [
  {
    responsibilityId: 'RESP-AGG-001',
    version: 1,
    structureId: 'CAP-POOL-001',
    name: 'Aggressive Multiplication',
    mission: 'Compound capital aggressively while remaining solvent, liquid, and inside the governed mandate.',
    primaryObjective: 'CAPITAL_GROWTH',
    objectivePrecedence: ['SOLVENCY', 'MANDATE_COMPLIANCE', 'DOWNSIDE_CONTROL', 'LIQUIDITY', 'CAPITAL_GROWTH'],
    targets: [
      { targetId: 'T-RETURN', label: 'Return objective', value: '15–25% annualized target', priority: 5, hardBoundary: false },
      { targetId: 'T-DD', label: 'Maximum drawdown', value: '12%', priority: 2, hardBoundary: true },
      { targetId: 'T-LIQ', label: 'Minimum liquidity reserve', value: '15%', priority: 4, hardBoundary: true },
    ],
    autonomy: 'FULL_WITHIN_MANDATE',
    horizons: ['SCALP', 'INTRADAY', 'SHORT_SWING'],
    marketAuthority: [
      { market: 'Crypto spot', understand: 'ENABLED', execute: 'ENABLED' },
      { market: 'Crypto futures', understand: 'ENABLED', execute: 'DISABLED' },
      { market: 'Equities', understand: 'ENABLED', execute: 'RESEARCH_ONLY' },
      { market: 'Options', understand: 'RESEARCH_ONLY', execute: 'DISABLED' },
    ],
    actionAuthority: [
      { action: 'Hold cash', state: 'ENABLED' },
      { action: 'Increase spot exposure', state: 'ENABLED' },
      { action: 'Reduce / exit', state: 'ENABLED' },
      { action: 'Rebalance', state: 'ENABLED' },
      { action: 'Hedge', state: 'RESEARCH_ONLY' },
      { action: 'Short', state: 'DISABLED' },
      { action: 'Use leverage', state: 'DISABLED' },
      { action: 'Execute futures', state: 'DISABLED' },
      { action: 'Basis / relative value', state: 'RESEARCH_ONLY' },
    ],
    maxDrawdownPct: 12,
    minLiquidityPct: 15,
    maxInstrumentExposurePct: 8,
    maxCorrelatedExposurePct: 25,
    effectiveAt: '2026-09-03T00:00:00Z',
    status: 'ACTIVE',
  },
];

export const capitalStructures: CapitalStructure[] = [
  { structureId: 'CAP-IMA-001', name: 'Robert Individual Growth', type: 'INDIVIDUAL_MANAGED_ACCOUNT', status: 'ACTIVE', baseCurrency: 'USD', nav: '$28,491.72', cash: '$22,108.49', deployed: '$6,383.23', participantIds: ['PART-001'], accountIds: ['ACC-IMA-001'], activeResponsibilityId: 'RESP-IMA-001', participantCount: 1 },
  { structureId: 'CAP-POOL-001', name: 'Family Growth I', type: 'POOLED_PORTFOLIO', status: 'ONBOARDING', baseCurrency: 'USD', nav: '$182,441.21', cash: '$76,552.08', deployed: '$105,889.13', participantIds: ['PART-101', 'PART-102', 'PART-103', 'PART-104'], accountIds: ['ACC-POOL-001'], activeResponsibilityId: 'RESP-AGG-001', participantCount: 4 },
  { structureId: 'CAP-JOINT-001', name: 'Household Opportunity', type: 'HOUSEHOLD_OR_JOINT_PORTFOLIO', status: 'ACTIVE', baseCurrency: 'USD', nav: '$64,330.40', cash: '$39,210.80', deployed: '$25,119.60', participantIds: ['PART-101', 'PART-102'], accountIds: ['ACC-JOINT-001'], activeResponsibilityId: 'RESP-JOINT-001', participantCount: 2 },
  { structureId: 'CAP-ENTITY-001', name: 'Northstar Treasury', type: 'ENTITY_OR_TREASURY_ACCOUNT', status: 'ACTIVE', baseCurrency: 'USD', nav: '$310,884.17', cash: '$181,440.17', deployed: '$129,444.00', participantIds: ['PART-201'], accountIds: ['ACC-ENTITY-001'], activeResponsibilityId: 'RESP-ENTITY-001', participantCount: 1 },
];

export const candidatePaths: CandidateEconomicPath[] = [
  { pathId: 'PATH-CASH', label: 'Hold cash', market: 'USD', expectedBenefit: 'Preserve optionality', expectedDownside: 'Opportunity cost', capitalRequired: '$0', score: 0.61, status: 'PERMITTED', reason: 'Always available while liquidity and mandate remain satisfied.' },
  { pathId: 'PATH-BTC-SPOT', label: 'Increase BTC spot exposure', market: 'BTC-USD spot', expectedBenefit: '+2.4% scenario', expectedDownside: '-0.9% scenario', capitalRequired: '$8,000', score: 0.72, status: 'PERMITTED', reason: 'Spot execution is permitted and current exposure fits the preview risk envelope.' },
  { pathId: 'PATH-BTC-FUT', label: 'BTC futures long', market: 'BTC futures', expectedBenefit: '+3.3% scenario', expectedDownside: '-2.8% scenario', capitalRequired: '$3,000 margin', score: 0.81, status: 'BLOCKED', reason: 'Benjamin may understand futures but this responsibility does not grant futures execution authority.' },
  { pathId: 'PATH-BTC-HEDGE', label: 'BTC spot with hedge', market: 'BTC spot + derivative hedge', expectedBenefit: '+2.0% scenario', expectedDownside: '-0.5% scenario', capitalRequired: '$9,500', score: 0.84, status: 'RESEARCH_ONLY', reason: 'Researchable end-state path; hedge execution authority has not been activated.' },
];

export const companyModelStatus = {
  schemaVersion: '1.0',
  productMode: 'FRONTEND_CONTRACT_PREVIEW',
  liveExecution: false,
  capitalCustody: false,
  regulatoryActivation: false,
};
