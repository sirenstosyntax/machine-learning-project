"""Create the local-only NEMSIS cardiac-arrest modeling dataset.

The source CSV is the Utstein-enriched analysis file produced outside the Git
repository. The output contains only the broad primary-response cohort, removes
PcrKey, maps NEMSIS codes to readable labels, and adds Utstein subgroup flags.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


DEFAULT_OUTPUT = Path("data/nemsis_cardiac_arrest_modeling.csv")

ETIOLOGY_LABELS = {
    "3002001": "Cardiac (presumed)",
    "3002003": "Drowning/submersion",
    "3002005": "Drug overdose",
    "3002007": "Electrocution",
    "3002009": "Exsanguination (medical)",
    "3002011": "Other",
    "3002013": "Respiratory/asphyxia",
    "3002015": "Traumatic cause",
    "7701001": "Not applicable",
    "7701003": "Not recorded",
}

AED_LABELS = {
    "3007001": "No AED",
    "3007003": "Applied without defibrillation",
    "3007005": "Applied with defibrillation",
    "7701001": "Not applicable",
    "7701003": "Not recorded",
}

RHYTHM_LABELS = {
    "3011001": "Asystole",
    "3011003": "Bradycardia",
    "3011005": "PEA",
    "3011007": "Unknown AED non-shockable rhythm",
    "3011009": "Unknown AED shockable rhythm",
    "3011011": "Ventricular fibrillation",
    "3011013": "Pulseless ventricular tachycardia",
    "7701001": "Not applicable",
    "7701003": "Not recorded",
}

WITNESS_LABELS = {
    "3004001": "Not witnessed",
    "3004003": "Family member",
    "3004005": "Healthcare provider",
    "3004007": "Bystander",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Path to nemsis_cardiac_arrest_analysis_utstein.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output CSV path (default: {DEFAULT_OUTPUT})",
    )
    return parser.parse_args()


def contains_any(series: pd.Series, codes: str) -> pd.Series:
    return series.fillna("").str.contains(codes, regex=True)


def label_witness(value: object) -> str:
    if pd.isna(value) or str(value).strip() in {"", "."}:
        return "Missing"

    codes = {part for part in str(value).split("|") if part}
    witnessed_codes = {"3004003", "3004005", "3004007"}
    if "3004001" in codes and codes.intersection(witnessed_codes):
        return "Contradictory"
    if "7701003" in codes:
        return "Not recorded"
    if "7701001" in codes:
        return "Not applicable"

    labels = [
        label for code, label in WITNESS_LABELS.items() if code in codes
    ]
    return " + ".join(labels) if labels else "Missing"


def mapped_labels(series: pd.Series, mapping: dict[str, str]) -> pd.Series:
    return series.map(mapping).fillna("Missing")


def build_modeling_dataset(raw: pd.DataFrame) -> pd.DataFrame:
    required_columns = {
        "eArrest_02",
        "eArrest_03",
        "eArrest_04",
        "eArrest_07",
        "eArrest_11",
        "eArrest_12",
        "eScene_01",
        "eResponse_05",
        "EMSSystemResponseTimeMin",
        "ageinyear",
        "Urbanicity",
        "USCensusRegion",
    }
    missing = sorted(required_columns.difference(raw.columns))
    if missing:
        raise ValueError("Input is missing column(s): " + ", ".join(missing))

    attempted = contains_any(raw["eArrest_03"], r"3003001|3003003|3003005")
    positive = contains_any(raw["eArrest_12"], r"3012003|3012005|3012007")
    negative = contains_any(raw["eArrest_12"], r"3012001")
    response = pd.to_numeric(
        raw["EMSSystemResponseTimeMin"], errors="coerce"
    )

    broad = (
        attempted
        & (positive ^ negative)
        & raw["eScene_01"].eq("9923003")
        & raw["eResponse_05"].eq("2205001")
        & response.notna()
    )

    witness_text = raw["eArrest_04"].fillna("")
    has_bystander_witness = witness_text.str.contains(
        r"3004003|3004005|3004007", regex=True
    )
    has_not_witnessed = witness_text.str.contains(r"3004001", regex=True)
    clean_bystander_witnessed = has_bystander_witness & ~has_not_witnessed
    shockable = contains_any(raw["eArrest_11"], r"3011009|3011011|3011013")
    utstein_style = broad & clean_bystander_witnessed & shockable
    classic_utstein = utstein_style & raw["eArrest_02"].eq("3002001")

    selected = raw.loc[broad].copy()
    output = pd.DataFrame(index=selected.index)
    output["rosc"] = positive.loc[broad].astype(int)
    output["response_time_minutes"] = response.loc[broad]
    output["age_years"] = pd.to_numeric(selected["ageinyear"], errors="coerce")
    output["urbanicity"] = selected["Urbanicity"].fillna("Missing")
    output["census_region"] = selected["USCensusRegion"].fillna("Missing")
    output["arrest_etiology"] = mapped_labels(
        selected["eArrest_02"], ETIOLOGY_LABELS
    )
    output["witness_category"] = selected["eArrest_04"].apply(label_witness)
    output["aed_use_prior_ems"] = mapped_labels(
        selected["eArrest_07"], AED_LABELS
    )
    output["initial_rhythm"] = mapped_labels(
        selected["eArrest_11"], RHYTHM_LABELS
    )
    output["bystander_witnessed"] = clean_bystander_witnessed.loc[broad].astype(int)
    output["shockable_rhythm"] = shockable.loc[broad].astype(int)
    output["utstein_style"] = utstein_style.loc[broad].astype(int)
    output["classic_utstein"] = classic_utstein.loc[broad].astype(int)

    return output.reset_index(drop=True)


def main() -> None:
    args = parse_args()
    if not args.input.is_file():
        raise FileNotFoundError(f"Input dataset not found: {args.input}")

    raw = pd.read_csv(args.input, dtype=str)
    output = build_modeling_dataset(raw)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(args.output, index=False)

    print(f"Created: {args.output}")
    print(f"Rows: {len(output):,}")
    print(f"ROSC positive: {int(output['rosc'].sum()):,}")
    print(f"Utstein-style rows: {int(output['utstein_style'].sum()):,}")
    print(f"Classic Utstein rows: {int(output['classic_utstein'].sum()):,}")
    print("PcrKey included: No")


if __name__ == "__main__":
    main()
