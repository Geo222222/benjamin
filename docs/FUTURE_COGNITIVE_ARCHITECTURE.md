# Benjamin Future Cognitive Architecture

> **Status: FUTURE PLAN / NON-OPERATIVE**
>
> This document defines intended cognitive architecture. It does not grant execution authority, change current production behavior, promote any model, or weaken the Covenant, Watchman, Governor, evidence, privacy, or authorization boundaries.

## Purpose

Benjamin should become an evidence-driven decision intelligence, not a monolithic trading model.

The long-term design is to let Benjamin reason over a graph of typed, provenance-bearing objects produced by deterministic systems, research systems, machine-learning systems, market-perception systems, portfolio systems, and historical memory. Benjamin may synthesize those objects into a decision proposal, but no model may convert a proposal into capital-moving authority by itself.

The central architectural rule is:

> **Objects may inform Benjamin. Only governed authority may authorize action.**

## Z Look Jamaican boundary

Z Look Jamaican (ZLJ) may evolve into a producer of structured market-intelligence objects that Benjamin can consume later.

ZLJ may provide, subject to contract and qualification:

- raw market observation references;
- deterministic measurements and classifications;
- statistical and technical measurements;
- market-structure objects;
- microstructure objects;
- visual/chart-perception objects;
- market-state and transition objects;
- market-story hypotheses;
- strategy-applicability objects;
- machine-learning model objects and prediction objects;
- opportunity-candidate objects;
- prediction/outcome evaluation records;
- model qualification, calibration, drift, and competence records.

ZLJ does **not** gain Benjamin decision authority by producing these objects. ZLJ output is evidence and intelligence input. Benjamin retains responsibility for capital intent, portfolio context, decision synthesis, and governed authorization. The Watchman/Governor remains downstream and cannot be bypassed.

## Object graph instead of one giant state

Benjamin should not consume one giant JSON state blob. The intended design is a composable object graph in which each object class owns one kind of truth or inference.

```text
Raw Evidence Objects
        ↓
Measurement Objects
        ↓
Structure / Context / Perception Objects
        ↓
State + Transition Objects
        ↓
Market Story Objects
        ↓
ML Model + Prediction Objects
        ↓
Strategy Applicability Objects
        ↓
Opportunity Objects
        ↓
Portfolio / Risk / Cost Objects
        ↓
Decision Context Object
        ↓
Benjamin Investment Reasoner
        ↓
Decision Proposal Object
        ↓
Watchman / Governor
        ↓
Bounded Authorization
```

Each object should carry enough lineage to answer:

- what produced it;
- which source evidence it depends on;
- when the underlying information became knowable;
- which software/model/rule version produced it;
- whether it is a fact, deterministic derivation, inference, hypothesis, prediction, or policy decision;
- what qualification status applies;
- what invalidates or expires it;
- which later objects consumed it.

## Evidence classes are not equal

The reasoner must see heterogeneous evidence without treating all inputs as peers.

A future evidence-qualification layer should distinguish at minimum:

1. canonical observations;
2. deterministic derived measurements;
3. deterministic state classifications;
4. qualified statistical or ML estimates;
5. structured market-story inferences;
6. visual/perception interpretations;
7. language-model hypotheses or explanations.

This is not a universal fixed ranking. Applicability depends on the question, horizon, instrument, data quality, and model competence. However, lower-authority inference must never silently overwrite higher-authority observations.

## Model objects

Machine-learning systems are first-class objects, not invisible implementation details.

A model object should identify at minimum:

- model ID and version;
- model family and purpose;
- owner/provider;
- training dataset references;
- feature definitions and versions;
- label definitions;
- training and evaluation windows;
- leakage/look-ahead controls;
- validation method;
- supported instruments, horizons, and regimes;
- known failure modes;
- calibration state;
- drift state;
- qualification/graduation status;
- artifact hash;
- deployment status.

A single model may emit a multi-outcome prediction object. For example, one qualified model may estimate return distributions, drawdown risk, breakout-failure probability, volatility, liquidity deterioration, or execution quality across multiple horizons.

The prediction object must remain separate from the model object and from realized outcome labels.

## Evidence Reliability / Model Competence Router

The future Benjamin Investment Reasoner should not simply average model outputs.

A dedicated qualification and competence layer should estimate how much trust a given expert deserves for the current question and context.

Conceptually:

```text
Effective trust
    = hard qualification
    × empirical competence
    × current applicability
    × calibration quality
```

The exact combination need not be literal multiplication, but the decomposition should remain explicit.

### Hard qualification

Deterministic and fail-closed. Examples:

- model is allowed for this decision class;
- feature provenance is valid;
- data freshness passes;
- schema is compatible;
- current instrument/horizon is in scope;
- artifact/version is known;
- no quarantine or suspension applies.

A hard qualification failure can force effective trust to zero regardless of model confidence.

### Empirical competence

Learned from prediction versus realized outcome, conditioned on relevant contexts such as:

- instrument;
- asset class;
- horizon;
- volatility regime;
- liquidity regime;
- market story;
- session;
- strategy family;
- distribution-shift state.

The question for the competence model is not "which way will price move?" It is:

> **How reliable is expert X for question Y under context Z?**

### Current applicability

The system should estimate whether the current observation resembles the model's qualified experience. Out-of-distribution conditions should reduce trust and may fail closed where policy requires.

## Three required forms of memory

Benjamin's long-term cognitive architecture requires three distinct memory systems. They must not be collapsed into one generic vector store or one mutable prompt.

### 1. Semantic memory — what Benjamin knows

Semantic memory contains durable, versioned knowledge and beliefs, for example:

- strategy definitions and operator doctrine;
- indicator and measurement definitions;
- market-state ontology;
- known economic mechanisms;
- research findings and replication evidence;
- portfolio and risk concepts;
- policy and governance knowledge;
- model capability and limitation knowledge;
- validated lessons that have graduated beyond a single case.

Semantic memory should distinguish externally published research, internal historical evidence, shadow evidence, and live evidence. Published research is evidence of a proposition, not proof that Benjamin can execute the edge economically.

### 2. Episodic memory — what happened

Episodic memory contains time-bounded cases and reasoning trajectories.

A market case may preserve:

- the world/decision snapshot available at the time;
- facts and deterministic measurements;
- state and transition objects;
- market-story hypotheses;
- competing interpretations;
- model predictions and effective trust weights;
- portfolio context;
- the reasoner's thesis;
- expected next states;
- decision proposal;
- actual later observations and outcomes;
- prediction errors;
- discovered contradictions;
- post-case lessons.

This enables retrieval of structurally similar prior situations without pretending that the past is identical to the present.

### 3. Procedural memory — how Benjamin reasons

Procedural memory contains governed decision methods rather than facts about one market case.

Examples:

- how to evaluate a breakout candidate;
- how to resolve conflicting model evidence;
- how to downgrade stale or out-of-distribution evidence;
- how to distinguish fact, inference, and hypothesis;
- how to assemble a Decision Context Object;
- how to request missing evidence;
- how to compare strategy candidates;
- how to handle uncertainty and abstain;
- how to prepare a bounded Decision Proposal Object;
- how to escalate to Watchman/Governor without bypassing them.

Procedural memory is versioned policy/skill knowledge. A model may recommend a procedural change, but it must not silently rewrite governing procedure while operating.

## Self model / metacognition

Benjamin should maintain an empirical self-model rather than claim generalized intelligence.

A future `SelfModelObject` may contain:

- current reasoner/model versions;
- measured competence by decision family;
- measured competence by market regime and horizon;
- calibration curves;
- known weaknesses;
- recent recurring error patterns;
- distribution-shift indicators;
- abstention thresholds;
- unresolved qualification gaps.

The purpose is practical metacognition:

> **Benjamin should know where evidence says Benjamin is reliable, where it is weak, and when it should reduce confidence or abstain.**

The self model must be empirical and versioned. It is not a claim of consciousness or authority.

## Decision Context Object

The reasoner should receive a bounded `DecisionContextObject`, not unrestricted database access or an unstructured prompt dump.

A future context may reference:

- market/world snapshot;
- deterministic measurements;
- structure, state, and transition objects;
- market stories and competing hypotheses;
- research evidence;
- strategy applicability;
- ML predictions;
- model qualification/competence/calibration;
- similar episodic cases;
- semantic knowledge;
- procedural rule version;
- portfolio state;
- liquidity and cash state;
- risk state;
- costs and execution feasibility;
- contradictions and missing evidence;
- explicit decision question.

The compiler that builds this context should itself be versioned and auditable.

## Benjamin Investment Reasoner

The future reasoner is a synthesis component, not a source-of-truth calculator.

Its responsibilities may include:

- compare competing hypotheses;
- reconcile heterogeneous evidence;
- explicitly surface disagreement;
- use qualification and competence weights;
- retrieve analogous historical cases;
- evaluate strategy fit;
- incorporate portfolio and risk context;
- identify missing evidence;
- define invalidation conditions;
- estimate uncertainty;
- recommend action, watch, research, or abstention;
- produce a typed `DecisionProposalObject`.

It should not be trusted to calculate canonical RSI, prices, P&L, accounting, limits, or execution state when deterministic services can provide those values.

## Decision proposal, not execution

A reasoner output should preserve at least:

- recommendation;
- decision class;
- confidence and confidence decomposition;
- primary hypothesis;
- competing hypotheses;
- supporting evidence references;
- contradicting evidence references;
- missing evidence;
- relevant model predictions and effective trust;
- analogous cases retrieved;
- strategy candidates;
- portfolio implications;
- economic/cost assessment;
- expected outcomes;
- invalidation conditions;
- requested authority, if any;
- reasoner, context-compiler, and procedure versions.

The proposal remains non-authoritative until the existing governance path permits action.

## Continuous learning without uncontrolled self-modification

Benjamin should learn continuously, but the production reasoner's neural weights should not mutate invisibly while making capital decisions.

Learning should occur at different speeds.

### Fast: memory and belief updates

Continuously update evidence such as:

- case outcomes;
- prediction errors;
- story confidence;
- model competence records;
- calibration observations;
- distribution-shift indicators;
- episodic memory;
- unresolved contradictions.

This changes what Benjamin knows without silently replacing the production model.

### Medium: online calibration and competence estimation

Model confidence may be recalibrated from live/shadow prediction performance. The competence router may update contextual reliability estimates under controlled, reproducible algorithms.

These updates must be versioned and replayable.

### Slow: candidate model succession

Actual model-weight updates should create a new candidate model version rather than mutate the qualified production model in place.

```text
Production Model N
      |
new evidence
      v
Candidate Model N+1
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

A candidate may be rejected, quarantined, rolled back, or promoted. Model succession must preserve reproducibility and permit reconstruction of any past decision.

## Prediction, outcome, and learning lineage

The intended learning chain is:

```text
WorldSnapshot
      ↓
Feature Objects
      ↓
Model Prediction Object
      ↓
Decision Context
      ↓
Decision Proposal
      ↓
Later Outcome Object
      ↓
Prediction Evaluation
      ↓
Competence / Calibration Update
      ↓
Episodic Memory
      ↓
Candidate Semantic or Procedural Lesson
      ↓
Qualification before promotion
```

Labels must become available only after the relevant outcome window closes. `known_at` / `available_after` semantics are mandatory to prevent outcome leakage.

## Disagreement is first-class evidence

Benjamin should not hide disagreement by averaging everything into one score.

Where material experts disagree, create an explicit conflict record that captures:

- which experts disagree;
- their predictions;
- their qualification and effective trust;
- which evidence each expert relied on;
- plausible reasons for disagreement;
- what observation would discriminate between the hypotheses.

The reasoner should examine minority evidence rather than treat majority vote as truth.

## Confidence decomposition

Reasoner confidence should be decomposable, for example across:

- data quality;
- freshness;
- state certainty;
- story certainty;
- strategy evidence;
- ML consensus;
- model calibration;
- historical-case similarity;
- portfolio certainty;
- execution/cost certainty;
- reasoner measured competence.

A single unexplained confidence scalar is insufficient for material capital decisions.

## Research and ML relationship

Known research should enter as versioned evidence objects, not as unquestioned doctrine.

The system must distinguish:

- published/external evidence;
- internal replication evidence;
- historical backtest evidence;
- out-of-sample evidence;
- shadow evidence;
- live evidence.

Machine learning may classify, forecast, rank, calibrate, detect anomalies, discover recurring statistical states, evaluate strategy candidates, or estimate model competence. Unsupervised discovery may propose new clusters or regimes, but it does not automatically promote them into canonical market knowledge.

## Privacy and the books

Semantic, episodic, procedural, self-model, model-performance, strategy, portfolio, and internal reasoning records are private by default.

The Big Book may preserve minimum necessary immutable evidence of material decisions, model versions, qualification, and governance events. It should not become a dump of all model features, prompts, private research, positions, or internal cognition.

The Little Book receives no automatic export from cognitive memory.

Existing privacy and minimum-necessary evidence rules continue to govern disclosure.

## Future object families

Potential repository contracts include:

```text
cognition/
  context/
  reasoner/
  self_model/
  conflicts/
  confidence/

memory/
  semantic/
  episodic/
  procedural/

models/
  registry/
  predictions/
  qualification/
  calibration/
  competence/
  drift/
  evaluations/

intelligence/
  market_objects/
  stories/
  strategies/
  opportunities/
  research/
```

These directories are conceptual future boundaries, not a requirement to create empty code structure before contracts are ready.

## Non-negotiable invariants

1. No model is sovereign.
2. Raw observations and deterministic accounting outrank generated explanation.
3. Fact, inference, hypothesis, prediction, and decision remain distinct types.
4. Memory does not create authority.
5. Learning does not bypass qualification.
6. Production models are versioned and reproducible.
7. Continuous learning does not mean uncontrolled in-place weight mutation.
8. Every material prediction can eventually be compared with an outcome.
9. Model disagreement is preserved, not hidden.
10. Benjamin may abstain when competence or evidence is insufficient.
11. ZLJ intelligence is input, not authorization.
12. Watchman/Governor and existing evidence-required authorization remain downstream.

## Intended end state

Benjamin should eventually be able to answer not only:

> "What do the current indicators say?"

but:

> "What do I know, what happened in analogous cases, which reasoning procedure applies, which experts are competent here, where do they disagree, what changed since my previous belief, how well calibrated am I in this situation, what would prove the thesis wrong, how does this affect the portfolio, and am I qualified to recommend action at all?"

That is the target: a provable, self-evaluating investment decision system whose intelligence can grow while authority remains governed.