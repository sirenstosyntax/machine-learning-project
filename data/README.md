# Local modeling data

This directory is the expected location of the local modeling dataset:

```text
data/nemsis_cardiac_arrest_modeling.csv
```

The CSV is intentionally excluded from Git. Do not commit or redistribute it. The repository contains code and aggregate outputs only.

## Data source

The modeling file is derived from a 50,000-record cardiac-arrest sample linked from the 2025 NEMSIS Public-Release Research Dataset. The source archive and intermediate row-level files remain outside the repository.

NEMSIS describes its research dataset as a de-identified convenience sample and places conditions on access, use, and redistribution. Review the current terms before sharing row-level data or submitting it to another system.

- [NEMSIS request-research-data page](https://nemsis.org/using-ems-data/request-research-data/)
- [NEMSIS 2025 public-release dataset overview](https://nemsis.org/2025-nemsis-public-release-research-dataset-now-available/)

## Creating the file

From the repository root, run:

```powershell
py -3.13 .\prepare_modeling_dataset.py `
  --input "C:\Users\rirgmc\capstone-data\nemsis_2025\working\nemsis_cardiac_arrest_analysis_utstein.csv"
```

The default output is `data/nemsis_cardiac_arrest_modeling.csv`.

The script:

- selects the broad first-unit, primary-response cohort;
- requires attempted resuscitation, known ROSC, and recorded response time;
- converts NEMSIS codes into readable categories;
- adds Utstein-style subgroup flags;
- keeps only analysis variables; and
- omits `PcrKey`.

## Expected validation output

```text
Created: data\nemsis_cardiac_arrest_modeling.csv
Rows: 17,198
ROSC positive: 5,097
Utstein-style rows: 2,054
Classic Utstein rows: 1,777
PcrKey included: No
```

If these counts differ, stop before running the notebook and verify that the intended enriched source file was supplied.

## Schema

| Column | Type | Description |
|---|---|---|
| `rosc` | Integer, 0/1 | Target. Any positive ROSC code documented during EMS care. |
| `response_time_minutes` | Numeric | EMS system response time from unit notification by dispatch to unit arrival on scene. |
| `age_years` | Numeric | Patient age in years. Missing values are imputed inside each model pipeline. |
| `urbanicity` | Categorical | Urban, suburban, rural, frontier, or missing/not recorded. |
| `census_region` | Categorical | U.S. Census region supplied by the NEMSIS computed-elements file. |
| `arrest_etiology` | Categorical | Readable mapping of `eArrest.02`, including presumed cardiac, respiratory/asphyxia, trauma, overdose, and other categories. |
| `witness_category` | Categorical | Readable mapping of `eArrest.04`; conflicting witnessed/not-witnessed records are labeled contradictory. |
| `aed_use_prior_ems` | Categorical | Readable mapping of `eArrest.07` for AED use before EMS arrival. |
| `initial_rhythm` | Categorical | Readable mapping of `eArrest.11`, including asystole, PEA, VF, and pulseless VT. |
| `bystander_witnessed` | Integer, 0/1 | Clean witnessed-category indicator used to construct Utstein-style cohorts. |
| `shockable_rhythm` | Integer, 0/1 | Initial-shockable-rhythm indicator used to construct Utstein-style cohorts. |
| `utstein_style` | Integer, 0/1 | Broad cohort plus clean bystander witness and initially shockable rhythm. |
| `classic_utstein` | Integer, 0/1 | Utstein-style subgroup additionally restricted to presumed cardiac etiology. |

The four cohort flags are used for cohort selection and validation, not as model predictors.

## Outcome note

`rosc` is an intermediate clinical outcome. It is not equivalent to survival to hospital discharge or neurologically favorable survival. Accordingly, this project describes a classic Utstein-style **ROSC** subgroup analysis, not an Utstein survival analysis.

## Quality checks

Before modeling, confirm that:

- the file has 17,198 rows and 13 columns;
- `PcrKey` is absent;
- `rosc` contains only 0 and 1;
- response time is present for every row;
- the ROSC-positive count is 5,097;
- `utstein_style` sums to 2,054; and
- `classic_utstein` sums to 1,777.

The notebook repeats the principal cohort and data-quality checks before fitting any models.
