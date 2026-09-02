# Benjamin Future Cognitive Architecture

> **Status: ARCHITECTURAL TARGET / NON-LIVE**
>
> This document defines Benjamin's intended cognitive structure and v1 qualification direction. It does not activate live capital, promote a model, weaken Watchman, grant The Hand execution authority, or change The Book's evidence/privacy rules.

## Constitutional position

> **ZLJ sees. Benjamin decides. Watchman governs. The Hand executes. The Book remembers and proves.**

Benjamin is Epinnox's **decision intelligence**, not a monolithic trading model and not an execution system.

The architecture must let Benjamin consume heterogeneous evidence, reason over it according to context and measured competence, create bounded capital decisions, learn from outcomes, and remain subordinate to governance.

## V1 cognitive mandate

Benjamin's first capability benchmark is intentionally narrow:

1. **scalping / micro trades** — milliseconds/seconds to minutes where infrastructure allows;
2. **intraday trading** — minutes to hours;
3. **short swing trading** — hours to several days.

Long-horizon investment planning, strategic portfolio allocation, multi-year fundamental underwriting, and broader treasury/capital-allocation intelligence are later capability families.

V1 therefore prioritizes reasoning about:

- spread, depth, liquidity, volume, and order flow;
- microstructure and imbalance;
- price action, momentum, mean reversion, and volatility;
- market state and regime;
- forecast distributions across explicit short horizons;
- fees, slippage, latency, and expected executable edge;
- position and exposure state;
- entry, target, stop/invalidation, hold/reduce/exit;
- confidence and measured competence;
- trade versus abstention.

`NO TRADE` is a first-class output.

## Z Look Jamaican boundary

Z Look Jamaican (ZLJ) is the producer of market-perception and model-intelligence objects Benjamin consumes.

ZLJ may provide, subject to contract and qualification:

- raw market observation references;
- source/freshness/sequence quality;
- deterministic measurements and features;
- market-structure and microstructure objects;
- market-state and transition objects;
- regime classifications;
- statistical/ML model objects;
- prediction distributions and expected-move objects;
- calibration, drift, and contextual competence records;
- opportunity evidence;
- prediction-versus-outcome evaluation records.

ZLJ does **not** gain capital authority by producing a strong forecast.

Conceptually:

```text
RAW MARKET
    |
    v
ZLJ observations
    |
    v
features / market state / regimes
    |
    v
models / predictions / competence
    |
    v
qualified intelligence objects
    |
    v
BENJAMIN
```

Only Benjamin converts that evidence into a capital decision.

## Benjamin is not one model

Benjamin may use many computational systems internally:

```text
Benjamin
  |- deterministic context compiler
  |- EvidenceQualifier
  |- ContradictionDetector
  |- RegimeInterpreter
  |- ForecastComparator
  |- CostAndEdgeReasoner
  |- ThesisBuilder
  |- Scenario / counterfactual reasoner
  |- Position / portfolio reasoner
  |- DecisionReasoner
  |- ConfidenceCalibrator
  |- SelfModel / metacognition
  `- OutcomeLearner
```

Some may be deterministic algorithms, some statistical models, some ML models, some language/reasoning models, and some retrieval systems.

Models are **cognitive operators**. Benjamin is the governed system that composes them.

No single model is sovereign.

## Three cognitive speeds

A scalp-oriented decision system should not force every computation through one large slow reasoner.

### Reflex layer

Fast deterministic/canonical truth and immediate validity conditions:

- current spread;
- position state;
- available buying/capital state supplied by authoritative services;
- fee schedule;
- slippage bounds/estimates supplied by qualified services;
- data freshness;
- authorization-independent order constraints;
- market/venue health;
- hard invalidation conditions that can be deterministically evaluated.

The reflex layer does not invent strategy. It keeps generated reasoning from replacing known machine truth.

### Tactical layer

The heart of Benjamin v1:

- Is the setup actually valid?
- Which evidence is relevant to this exact horizon?
- Which models are qualified here?
- Are the signals independent or derivatives of the same evidence?
- Where do qualified sources disagree?
- What is the expected move and downside distribution?
- Does expected edge survive fees, spread, slippage, latency, and uncertainty?
- What thesis explains the trade?
- What invalidates the thesis?
- What size is justified by current capital/position context?
- Should Benjamin enter, hold, reduce, exit, or abstain?

### Reflective layer

Slower self-evaluation and learning:

- Why is Benjamin losing in a particular regime?
- Which ZLJ models have degraded?
- Is a model's stated confidence miscalibrated?
- Is Benjamin systematically entering too late?
- Are fees/slippage destroying theoretical edge?
- Are repeated errors coming from ZLJ, Benjamin reasoning, Watchman constraints, or Hand execution quality?
- Should a model, feature, procedure, or confidence threshold be demoted or replaced?

This layer may operate after cases, periodically, or after sessions rather than on every market event.

## Object graph instead of one giant prompt

Benjamin should reason over a graph of typed, provenance-bearing objects rather than one giant JSON dump or unrestricted database context.

```text
ZLJ Observation Objects
        |
        v
Measurement / Feature Objects
        |
        v
Market State / Regime Objects
        |
        v
Model / Prediction / Competence Objects
        |
        v
Opportunity Evidence
        |
        +-----------------------+
        |                       |
        v                       v
Portfolio/Capital State    Book Memory/Evidence
        |                       |
        +-----------+-----------+
                    |
                    v
          DecisionContextObject
                    |
                    v
             Benjamin Reasoner
                    |
                    v
           TradeDecisionObject
                    |
                    v
                Watchman
```

Each object should preserve enough lineage to answer:

- what produced it;
- which evidence it depends on;
- when the information became knowable;
- which software/model/rule version produced it;
- whether it is fact, deterministic derivation, inference, hypothesis, prediction, decision, or outcome;
- what qualification applies;
- what horizon it applies to;
- what invalidates or expires it;
- which later objects consumed it.

## Evidence classes are not equal

Benjamin must see heterogeneous evidence without treating all inputs as peers.

A useful distinction is:

1. canonical observations;
2. deterministic derived measurements;
3. deterministic state classifications;
4. qualified statistical/ML estimates;
5. structured hypotheses/inferences;
6. visual/perception interpretations;
7. generated explanations.

This is not a universal fixed ranking. Relevance depends on the exact decision question, horizon, instrument, data quality, and contextual competence.

However, a lower-authority inference must never silently overwrite a higher-authority observation.

## Model objects

Machine-learning systems are first-class objects, not invisible implementation details.

A model object should identify where relevant:

- model ID/version/family/purpose;
- owner/provider;
- training dataset references;
- feature definitions/versions;
- label definitions;
- training and evaluation windows;
- leakage/look-ahead controls;
- validation method;
- supported instruments/horizons/regimes;
- known failure modes;
- calibration state;
- drift state;
- qualification status;
- artifact hash;
- deployment state.

A prediction object remains separate from the model object and from the later realized outcome.

A model may emit multiple outcomes or a distribution rather than one direction bit.

## Evidence reliability and model competence

Benjamin should not simply average model outputs.

A qualification/competence layer should determine how much trust an expert deserves for the current question.

Conceptually:

```text
Effective trust
  = hard qualification
  x empirical competence
  x current applicability
  x calibration quality
```

The exact implementation need not literally multiply these values, but the decomposition should remain inspectable.

### Hard qualification

Examples:

- model allowed for this decision family;
- feature provenance valid;
- data fresh enough;
- schema compatible;
- instrument/horizon in scope;
- artifact/version known;
- no quarantine/suspension.

A hard failure can force effective trust to zero regardless of model confidence.

### Empirical competence

Learned from prediction versus outcome under relevant contexts such as:

- instrument;
- asset class;
- horizon;
- volatility regime;
- liquidity regime;
- session;
- market state;
- strategy family;
- distribution-shift state.

The competence question is:

> **How reliable is expert X for question Y under context Z?**

### Current applicability

Out-of-distribution or unfamiliar conditions should reduce trust and may force abstention where policy requires.

## Three required forms of memory

Benjamin requires three distinct memory systems. They must not be collapsed into one generic vector store or mutable prompt.

### Semantic memory — what Benjamin knows

Examples:

- strategy definitions and doctrine;
- market-state ontology;
- validated research findings;
- model capability and limitation knowledge;
- market mechanisms;
- portfolio/risk concepts;
- validated lessons that have graduated beyond one case.

### Episodic memory — what happened

A short-horizon market case may preserve:

- market snapshot available at the time;
- features/state/regime;
- competing hypotheses;
- model predictions/effective trust;
- capital/position context;
- Benjamin's thesis and invalidation;
- expected outcomes;
- decision;
- later price path/outcome;
- prediction errors;
- MFE/MAE and other case measurements where relevant;
- execution quality references;
- discovered contradictions;
- post-case lessons.

### Procedural memory — how Benjamin reasons

Examples:

- how to evaluate a scalp candidate;
- how to compare conflicting model evidence;
- how to downgrade stale/OOD evidence;
- how to calculate which deterministic facts must be fetched rather than generated;
- how to construct a bounded decision context;
- how to abstain;
- how to build a TradeDecisionObject;
- how to route a decision to Watchman without bypassing governance.

Procedural memory is governed/versioned skill knowledge. A model may recommend a procedural change; it does not silently rewrite procedure while operating.

## Relationship with The Book

Benjamin owns the **meaning and use** of its cognitive memory. The Book owns authoritative cross-organ evidence/proof lineage.

The Big Book should preserve or reference the minimum material evidence needed to reconstruct decisions and outcomes without becoming a dump of every feature vector, token, prompt, private research artifact, or ephemeral thought.

A useful trading learning chain is:

```text
MARKET MEMORY
what the market looked like
       +
DECISION MEMORY
what Benjamin believed/decided
       +
OUTCOME MEMORY
what actually happened
       |
       v
EVALUATION / LEARNING
```

The Book can preserve the authoritative lineage connecting those records while Benjamin's memory services optimize retrieval and cognition.

## Self model / metacognition

Benjamin should maintain an empirical self-model rather than claiming generalized intelligence.

A `SelfModelObject` may include:

- current reasoner/operator/model versions;
- measured competence by decision family;
- competence by instrument/regime/horizon;
- calibration curves;
- known weaknesses;
- recurring error patterns;
- distribution-shift indicators;
- abstention thresholds;
- unresolved qualification gaps.

The operational purpose is:

> **Benjamin should know where evidence says Benjamin is reliable, where it is weak, and when it should reduce confidence or abstain.**

## Decision Context Object

The reasoner should receive a bounded context containing only decision-relevant authoritative or qualified material.

A future context may reference:

- market/world snapshot;
- deterministic measurements;
- microstructure/state/regime;
- ZLJ predictions;
- model qualification/competence/calibration;
- similar episodic cases;
- semantic knowledge;
- procedural rule version;
- current position/capital/liquidity state;
- fees/slippage/latency estimates;
- contradictions;
- missing evidence;
- explicit horizon;
- explicit decision question.

The context compiler itself should be versioned and auditable.

## TradeDecisionObject

Benjamin's v1 output should remain a **decision**, not an external execution instruction that bypasses Watchman.

A decision may preserve:

- decision ID;
- instrument/market;
- decision class: `ENTER | HOLD | REDUCE | EXIT | NO_TRADE`;
- side/direction where applicable;
- intended size or bounded sizing request;
- horizon;
- entry conditions;
- target/expected outcome;
- stop/invalidation conditions;
- confidence and confidence decomposition;
- primary thesis;
- competing hypotheses;
- supporting/contradicting evidence;
- relevant model predictions/effective trust;
- estimated fees/spread/slippage/latency;
- expected edge after costs;
- capital/position context reference;
- reasoner/context/procedure versions;
- expiration or decision-validity window.

It then goes to Watchman.

## Watchman boundary

Watchman owns the final policy/governance decision required before an external financial action.

Watchman may consider:

- mandate;
- maximum risk/exposure;
- available capital;
- concentration;
- leverage;
- jurisdiction/compliance;
- venue/account permissions;
- kill switches;
- evidence completeness;
- decision expiry;
- other deterministic or governed constraints.

Watchman may `AUTHORIZE` or `BLOCK`. It does not need to become the investment reasoner.

Benjamin may revise and resubmit a new decision when a block reveals a correctable constraint. It may not route around Watchman.

## The Hand boundary

The Hand receives a Watchman-authorized action envelope plus only the information required to perform the approved capability.

The Hand may own many integrations:

- exchanges;
- brokers;
- wallet/custody providers;
- banks;
- payment processors;
- treasury/settlement rails;
- other future external financial systems.

The Hand is therefore best understood as Epinnox's **authorized tool/capability plane**.

It may choose a technically equivalent adapter only when the authorization permits that routing. It cannot change side, size, destination, economic purpose, or other material intent on its own.

## Continuous learning without uncontrolled self-modification

Benjamin should learn continuously, but the production reasoner's neural weights should not mutate invisibly while making capital decisions.

### Fast — memory and evidence updates

Continuously update:

- case outcomes;
- prediction errors;
- model competence;
- calibration observations;
- episodic memory;
- unresolved contradictions;
- self-model observations.

### Medium — online calibration / competence

Controlled, reproducible algorithms may update contextual reliability estimates and calibration state.

### Slow — model succession

Actual weight changes create a new candidate model version:

```text
Production Model N
      |
new evidence
      v
Candidate N+1
      |
historical replay / leakage controls
      v
out-of-sample / walk-forward evaluation
      v
shadow comparison
      v
qualification
      v
explicit promotion
```

A candidate may be rejected, quarantined, rolled back, or promoted. Past decisions must remain reproducible from the model/version that actually produced them.

## Prediction, outcome, and learning lineage

```text
ZLJ WorldSnapshot
      |
      v
ZLJ Feature/State/Prediction Objects
      |
      v
Benjamin DecisionContext
      |
      v
Benjamin TradeDecision
      |
      v
Watchman Authorization / Block
      |
      v
Hand Execution if authorized
      |
      v
Later Outcome
      |
      v
Prediction Evaluation
      |
      +------> ZLJ calibration/competence
      |
      +------> Benjamin decision/self-model learning
      |
      v
The Book authoritative lineage
```

Labels become available only after the relevant outcome window closes. Timing semantics are mandatory.

## Disagreement is first-class evidence

Where material experts disagree, preserve an explicit conflict record containing:

- experts/models/hypotheses in conflict;
- their predictions;
- qualification/effective trust;
- evidence each relied upon;
- plausible reasons for disagreement;
- what future observation would discriminate between them.

Minority evidence should not disappear merely because a majority agrees.

## Confidence decomposition

Reasoner confidence should be explainable across factors such as:

- data quality/freshness;
- market-state certainty;
- model qualification;
- calibration;
- model agreement/disagreement;
- regime applicability;
- historical-case similarity;
- position/capital-state certainty;
- cost/slippage certainty;
- Benjamin's measured competence.

A single unexplained confidence scalar is insufficient for material capital decisions.

## V1 qualification benchmark

The primary benchmark is not simply positive P&L.

> **Does Benjamin demonstrate repeatable positive decision quality after realistic costs under controlled/shadow conditions?**

Measure where relevant:

- opportunities considered;
- decisions accepted/rejected/abstained;
- expected edge at decision time;
- realized edge;
- gross and net P&L;
- fees/slippage;
- win rate and win/loss distribution;
- profit factor;
- maximum drawdown;
- MFE/MAE;
- holding period;
- confidence calibration;
- performance by instrument;
- performance by horizon;
- performance by market/volatility/liquidity regime;
- performance by ZLJ model;
- performance by Benjamin procedure/strategy family.

A key calibration check is:

`predicted probability -> observed frequency`

If Benjamin repeatedly calls a comparable class of decisions 70% likely, the observed outcome frequency must support that meaning over sufficient samples.

## Attribution across organs

Performance evaluation must separate:

- **ZLJ prediction/perception quality**;
- **Benjamin decision quality**;
- **Watchman governance effects**;
- **Hand execution/slippage quality**.

Otherwise Epinnox will learn the wrong lesson from wins and losses.

## Privacy

Semantic, episodic, procedural, self-model, model-performance, strategy, portfolio, and internal reasoning records are private by default.

The Big Book preserves minimum-necessary material evidence. The Little Book receives no automatic export from cognitive memory.

## Non-negotiable invariants

1. No model is sovereign.
2. ZLJ intelligence is input, not decision authority.
3. Benjamin decides but does not authorize itself.
4. Watchman governance is downstream and cannot be bypassed.
5. The Hand executes authorized capabilities but does not originate economic intent.
6. The Book preserves lineage but does not invent domain truth.
7. Raw observations and deterministic accounting outrank generated explanation.
8. Fact, inference, prediction, decision, authorization, execution, and outcome remain distinct types.
9. Memory does not create authority.
10. Learning does not bypass qualification.
11. Production models are versioned and reproducible.
12. Continuous learning does not mean uncontrolled in-place weight mutation.
13. Every material prediction can eventually be compared with an outcome when the label becomes knowable.
14. Material disagreement is preserved, not hidden.
15. Benjamin may abstain when competence or evidence is insufficient.
16. V1 success in scalping/intraday/swing does not automatically qualify long-horizon investment intelligence.

## Intended end state

Benjamin should eventually be able to answer:

> "What is happening, which evidence actually matters for this horizon, which experts are competent here, where do they disagree, what does this opportunity mean given our current capital state, what would invalidate the thesis, is the edge positive after real costs, how confident should I be based on my own measured history, and should Epinnox act at all?"

That is the target: **a provable, self-evaluating capital decision intelligence whose knowledge can grow while authority remains separated and governed.**
