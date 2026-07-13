# NEMSIS Cardiac-Arrest ROSC Prediction

This machine-learning capstone evaluates whether EMS system response time adds predictive value for return of spontaneous circulation (ROSC) after out-of-hospital cardiac arrest. It uses a 50,000-record cardiac-arrest sample linked from the 2025 NEMSIS Public-Release Research Dataset.

The analysis compares logistic regression and random forest models in two cohorts:

- A broad primary-response cohort for general model development (`n = 17,198`).
- A classic Utstein-style subgroup with bystander-witnessed, initially shockable, presumed-cardiac arrests (`n = 1,777`).

The outcome is any documented ROSC during EMS care. It is not survival to hospital discharge or neurologically favorable survival.

## Research question

Does EMS system response time add predictive value for ROSC beyond age, geography, arrest etiology, witness category, pre-arrival AED use, and initial rhythm?

## Main findings

- Broad-cohort ROSC rate: **29.64%**.
- Classic Utstein-style ROSC rate: **53.91%**.
- In the classic subgroup, ROSC declined from **62.92%** in the fastest response-time decile to **43.68%** in the slowest decile.
- Adding response time improved cross-validated ROC AUC for both algorithms in both cohorts.
- The enhanced random forest had the highest threshold-independent performance: ROC AUC **0.7321** in the broad cohort and **0.6095** in the classic subgroup.
- The improvements were consistent but modest. Results demonstrate prediction and association, not causation.

## Model comparison

| Cohort | Algorithm | Response time | ROC AUC | Average precision | Balanced accuracy | F1 |
|---|---|---:|---:|---:|---:|---:|
| Broad | Logistic regression | No | 0.7215 | 0.4946 | 0.5891 | 0.3624 |
| Broad | Logistic regression | Yes | 0.7241 | 0.4979 | 0.5959 | 0.3793 |
| Broad | Random forest | No | 0.7289 | 0.5088 | 0.6787 | 0.5587 |
| Broad | Random forest | Yes | **0.7321** | **0.5160** | **0.6805** | **0.5604** |
| Classic Utstein | Logistic regression | No | 0.5947 | 0.6129 | 0.5682 | 0.6363 |
| Classic Utstein | Logistic regression | Yes | 0.6049 | 0.6154 | 0.5758 | **0.6441** |
| Classic Utstein | Random forest | No | 0.5933 | 0.6199 | 0.5691 | 0.5864 |
| Classic Utstein | Random forest | Yes | **0.6095** | **0.6328** | **0.5921** | 0.6192 |

Metrics are out-of-fold estimates from five-fold stratified cross-validation. Threshold-dependent metrics use a fixed probability threshold of 0.50.

## Repository contents

```text
machine-learning-project/
|-- modeling.ipynb
|-- prepare_modeling_dataset.py
|-- requirements.txt
|-- Machine_Learning_Analysis_Report.pdf
|-- figures/
|   |-- model_metric_comparison.png
|   |-- random_forest_feature_importance.png
|   |-- rosc_by_initial_rhythm.png
|   `-- rosc_by_response_decile.png
|-- results/
|   `-- model_comparison.csv
`-- data/
    `-- README.md
```

The row-level modeling CSV is intentionally excluded by `.gitignore`.

## Environment setup

The project was developed with Python 3.13. From PowerShell in the repository root:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Preparing the local modeling data

The preparation script expects the locally generated, Utstein-enriched cardiac-arrest analysis file. It filters the broad cohort, maps NEMSIS codes to readable categories, creates subgroup indicators, and omits `PcrKey`.

```powershell
py -3.13 .\prepare_modeling_dataset.py `
  --input "C:\Users\rirgmc\capstone-data\nemsis_2025\working\nemsis_cardiac_arrest_analysis_utstein.csv"
```

Expected local output:

```text
data/nemsis_cardiac_arrest_modeling.csv
```

Expected validation counts:

```text
Rows: 17,198
ROSC positive: 5,097
Utstein-style rows: 2,054
Classic Utstein rows: 1,777
PcrKey included: No
```

## Running the analysis

Execute the notebook in place:

```powershell
py -3.13 -m jupyter nbconvert `
  --to notebook `
  --execute .\modeling.ipynb `
  --inplace `
  --ExecutePreprocessor.timeout=1800
```

The notebook regenerates the aggregate model results and figures in `results/` and `figures/`.

## Cohort definitions

The broad cohort requires:

- attempted resuscitation;
- an unambiguous positive or negative ROSC outcome;
- a recorded EMS system response time;
- the reporting agency identified as the first EMS unit on scene; and
- a primary-area emergency response.

The classic Utstein-style subgroup additionally requires:

- a clean bystander-witnessed category;
- an initially shockable rhythm; and
- presumed cardiac etiology.

The term *Utstein-style* is used deliberately. The available target is ROSC during EMS care, so this analysis does not measure the Utstein survival outcome of survival to hospital discharge.

## Data governance

The source archive and row-level derived CSV are not included in this repository. The NEMSIS research-data terms restrict redistribution and require responsible handling of the dataset. Only code, aggregate results, figures, the executed notebook, and the final report are included.

- [NEMSIS request-research-data page](https://nemsis.org/using-ems-data/request-research-data/)
- [NEMSIS 2025 public-release dataset overview](https://nemsis.org/2025-nemsis-public-release-research-dataset-now-available/)

## Limitations

- NEMSIS is a convenience sample rather than a nationally population-based sample.
- Records represent EMS activations, not necessarily unique patients or incidents.
- Missing and not-recorded values may reflect documentation practices.
- The 50,000-record source sample is a subset of the complete 2025 cardiac-arrest population.
- ROSC is an intermediate outcome and should not be interpreted as survival to discharge.
- Unmeasured factors such as CPR quality, exact collapse-to-CPR time, comorbidities, and agency practices may confound associations.
- Cross-validation estimates internal predictive performance; external validation was not performed.
- Random-forest feature importance is descriptive and can favor continuous or high-cardinality predictors.

## Author

Grant Collings
Machine Learning Capstone, July 2026
