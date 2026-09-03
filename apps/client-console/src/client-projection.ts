export type ClientViewMode = 'INDIVIDUAL_OWNER' | 'POOLED_PARTICIPANT';

export type ClientProjection = {
  mode: ClientViewMode;
  clientDisplayName: string;
  relationshipId: string;
  structureId: string;
  structureName: string;
  structureType: string;
  participantId: string;
  reportingScope: string;
  currentValue: string;
  economicInterestPct: number;
  contributedCapital: string;
  distributedCapital: string;
  netGainLoss: string;
  fees: string;
  cashShare: string;
  investedShare: string;
  responsibilityName: string;
  responsibilityVersion: number;
  primaryObjective: string;
  maxDrawdown: string;
  minLiquidity: string;
  autonomy: string;
  watchmanStatus: string;
  custodyLabel: string;
};

export const clientProjections: Record<ClientViewMode, ClientProjection> = {
  INDIVIDUAL_OWNER: {
    mode: 'INDIVIDUAL_OWNER',
    clientDisplayName: 'Robert M.',
    relationshipId: 'REL-001',
    structureId: 'CAP-IMA-001',
    structureName: 'Robert Individual Growth',
    structureType: 'INDIVIDUAL MANAGED ACCOUNT',
    participantId: 'PART-001',
    reportingScope: 'ACCOUNT OWNER',
    currentValue: '$28,491.72',
    economicInterestPct: 100,
    contributedCapital: '$25,000.00',
    distributedCapital: '$0.00',
    netGainLoss: '+$3,491.72',
    fees: '-$312.44',
    cashShare: '$22,108.49',
    investedShare: '$6,383.23',
    responsibilityName: 'Individual Growth',
    responsibilityVersion: 1,
    primaryObjective: 'CAPITAL GROWTH',
    maxDrawdown: '8%',
    minLiquidity: '20%',
    autonomy: 'FULL WITHIN MANDATE',
    watchmanStatus: 'NORMAL',
    custodyLabel: 'External client-owned brokerage',
  },
  POOLED_PARTICIPANT: {
    mode: 'POOLED_PARTICIPANT',
    clientDisplayName: 'Participant C',
    relationshipId: 'REL-002',
    structureId: 'CAP-POOL-001',
    structureName: 'Family Growth I',
    structureType: 'POOLED PORTFOLIO',
    participantId: 'PART-103',
    reportingScope: 'OWN INTEREST + PERMITTED STRUCTURE ACTIVITY',
    currentValue: '$36,488.24',
    economicInterestPct: 20,
    contributedCapital: '$30,000.00',
    distributedCapital: '$0.00',
    netGainLoss: '+$6,488.24',
    fees: '-$428.13',
    cashShare: '$15,310.42',
    investedShare: '$21,177.82',
    responsibilityName: 'Aggressive Multiplication',
    responsibilityVersion: 1,
    primaryObjective: 'CAPITAL GROWTH',
    maxDrawdown: '12%',
    minLiquidity: '15%',
    autonomy: 'FULL WITHIN MANDATE',
    watchmanStatus: 'NORMAL',
    custodyLabel: 'Pooled structure / external custody preview',
  },
};

export const clientActivity = [
  ['BEN-D-PREVIEW-001', 'Benjamin decision', 'Increase BTC spot exposure', 'Decision only · Watchman pending'],
  ['WATCH-PREVIEW-014', 'Watchman protection', 'Prior exposure increase blocked', 'Risk envelope protected'],
  ['HAND-PREVIEW-021', 'Execution receipt', 'Spot reduction completed', 'Reconciled preview'],
  ['CAP-PREVIEW-007', 'Capital activity', 'Contribution credited', '+$2,000.00'],
  ['FEE-PREVIEW-004', 'Fee allocation', 'Management/advisory fee preview', '-$84.00'],
];

export const clientDecisions = [
  ['BTC spot exposure', 'SELECTED PATH', 'Permitted by current Responsibility; futures execution remains disabled.'],
  ['BTC futures long', 'BLOCKED / NOT USED', 'Benjamin may understand futures evidence, but this Responsibility does not permit futures execution.'],
  ['Hold cash', 'ALTERNATIVE', 'Preserves optionality and remains a valid path when evidence is insufficient.'],
];

export const clientEvidence = [
  ['Benjamin decision', 'BEN-D-PREVIEW-001', 'Responsibility-bound capital judgment'],
  ['Watchman status', 'WATCH-PREVIEW-014', 'Mandate/risk governance evidence'],
  ['Hand receipt', 'HAND-PREVIEW-021', 'Execution/reconciliation evidence'],
  ['Capital statement', 'STMT-PREVIEW-001', 'Participant/account-scoped accounting projection'],
];

export const clientProjectionStatus = {
  schemaVersion: '1.0',
  productMode: 'FRONTEND_CONTRACT_PREVIEW',
  syntheticData: true,
  otherParticipantPrivateDataVisible: false,
  proprietaryZljInternalsVisible: false,
  liveMoneyMovementEnabled: false,
};
