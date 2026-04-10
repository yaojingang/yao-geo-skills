# Eval Policy

Every skill in this repository needs evidence that it routes correctly, produces the promised artifacts, and avoids unsupported certainty.

## Required Eval Layers

### 1. Routing Eval

Each skill must include `evals/trigger_cases.json` with:

- direct positives
- direct negatives
- near neighbors
- mixed-intent prompts
- adversarial prompts

### 2. Contract Eval

Each skill must prove that required files and schema outputs are present:

- required output files exist
- required JSON fields exist
- directory structure matches expectations

### 3. Content Eval

Each skill must define a rubric that checks:

- source quality
- freshness
- directness of answer
- fairness of comparison
- absence of fake citations

### 4. Regression Eval

Each skill should keep a small stable set of benchmark briefs so prompt or script changes can be checked against previous behavior.

## Minimum Promotion Thresholds

- routing precision: `>= 0.97`
- routing recall: `>= 0.93`
- contract pass rate: `100%`
- fake citations: `0`
- average rubric score: `>= 4.0 / 5.0`

## Required Eval Files

```text
evals/
├── trigger_cases.json
├── expected_artifacts.json
├── rubric.md
└── failure_cases.md
```

Recommended for stronger skills:

```text
evals/
├── train/
├── dev/
├── holdout/
└── adversarial/
```

## Failure Policy

- If freshness cannot be verified, the skill must surface uncertainty.
- If source coverage is too weak, the skill must stop or downgrade confidence.
- If the skill cannot produce its promised artifact set, the run is a failure.
