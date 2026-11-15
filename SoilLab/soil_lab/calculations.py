import numpy as np
import pandas as pd
from scipy.stats import norm


REQUIRED_COLUMNS = {"sieve_mm", "retained_g"}


def clean_sieve_data(data: pd.DataFrame) -> pd.DataFrame:
    """Validate and standardize sieve size and retained-mass columns."""
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")

    missing = REQUIRED_COLUMNS - set(data.columns)
    if missing:
        raise ValueError(
            "Missing required column(s): " + ", ".join(sorted(missing))
        )

    df = data[["sieve_mm", "retained_g"]].copy()
    df["sieve_mm"] = pd.to_numeric(df["sieve_mm"], errors="coerce")
    df["retained_g"] = pd.to_numeric(df["retained_g"], errors="coerce")
    df = df.dropna(subset=["sieve_mm", "retained_g"])

    if df.empty:
        raise ValueError("No valid sieve data were provided.")
    if (df["sieve_mm"] < 0).any():
        raise ValueError("Sieve size cannot be negative.")
    if (df["retained_g"] < 0).any():
        raise ValueError("Retained mass cannot be negative.")
    if (df["sieve_mm"] == 0).sum() > 1:
        raise ValueError("Only one pan row (sieve_mm = 0) is allowed.")
    if df["sieve_mm"].duplicated().any():
        raise ValueError("Duplicate sieve openings were found.")
    if df["retained_g"].sum() <= 0:
        raise ValueError("Total retained mass must be greater than zero.")

    return df.sort_values("sieve_mm", ascending=False).reset_index(drop=True)


def calculate_sieve_results(data: pd.DataFrame, total_dry_mass_g: float) -> pd.DataFrame:
    """Calculate retained, cumulative retained and passing percentages."""
    try:
        total_dry_mass_g = float(total_dry_mass_g)
    except (TypeError, ValueError):
        raise ValueError("Enter a valid total dry sample mass.")
    if not np.isfinite(total_dry_mass_g) or total_dry_mass_g <= 0:
        raise ValueError("Total dry sample mass must be a positive number.")

    df = clean_sieve_data(data)
    recovered_mass = float(df["retained_g"].sum())
    recovery = recovered_mass / total_dry_mass_g * 100.0
    if recovery > 100.5:
        raise ValueError(
            f"Recovered mass is {recovery:.2f}% of the stated sample mass. "
            "The retained mass cannot exceed the original dry sample mass; "
            "check the entered masses and total sample mass."
        )

    df["percent_retained"] = df["retained_g"] / total_dry_mass_g * 100.0
    df["cumulative_retained_pct"] = df["percent_retained"].cumsum()
    df["percent_passing"] = 100.0 - df["cumulative_retained_pct"]

    # Tiny floating-point negatives can occur if the retained mass is marginally high.
    df["percent_passing"] = df["percent_passing"].clip(lower=0.0, upper=100.0)

    df.attrs["mass_recovery_pct"] = recovery
    df.attrs["total_dry_mass_g"] = total_dry_mass_g
    return df


def characteristic_size(results: pd.DataFrame, passing_percent: float):
    """
    Return D_x using interpolation on log10(particle size).
    Returns None if the requested percentage is not bracketed by the data.
    """
    if not 0 <= passing_percent <= 100:
        raise ValueError("Passing percentage must be between 0 and 100.")

    curve = results.loc[
        (results["sieve_mm"] > 0)
        & results["percent_passing"].between(0, 100),
        ["sieve_mm", "percent_passing"],
    ].copy()

    # Interpolation needs a monotonic percentage axis. Duplicate passing values
    # are collapsed by retaining the largest particle size for that percentage.
    curve = curve.groupby("percent_passing", as_index=False)["sieve_mm"].max()
    curve = curve.sort_values("percent_passing")

    x = curve["percent_passing"].to_numpy(dtype=float)
    sizes = curve["sieve_mm"].to_numpy(dtype=float)

    if len(x) < 2 or passing_percent < x.min() or passing_percent > x.max():
        return None

    log_d = np.interp(passing_percent, x, np.log10(sizes))
    return float(10 ** log_d)


def soil_parameters(results: pd.DataFrame) -> dict:
    """Calculate D10, D30, D40, D60, D70, Cu and Cc."""
    d = {
        f"D{p}": characteristic_size(results, p)
        for p in [10, 30, 40, 60, 70]
    }
    d10, d30, d60 = d["D10"], d["D30"], d["D60"]
    d["Cu"] = d60 / d10 if d10 and d60 else None
    d["Cc"] = (d30 ** 2) / (d10 * d60) if d10 and d30 and d60 else None
    return d


def design_filter_pack(aquifer_d30: float, factor: int = 5, target_cu: float = 2.0):
    """
    Generate a theoretical lognormal filter-pack grading curve.

    The curve passes exactly through the selected D30 target and has the
    requested lognormal Cu. It is a preliminary mathematical grading target,
    not a substitute for laboratory testing of actual filter-pack material.
    """
    if aquifer_d30 is None or not np.isfinite(aquifer_d30) or aquifer_d30 <= 0:
        raise ValueError("A valid positive aquifer D30 is required.")
    if factor not in (4, 5, 6):
        raise ValueError("Select a filter-pack ratio of 4, 5 or 6.")
    if not (1.0 < target_cu <= 2.5):
        raise ValueError("Target filter-pack Cu must be greater than 1 and no more than 2.5.")

    d30_pack = factor * aquifer_d30
    z10, z30, z60 = norm.ppf([0.10, 0.30, 0.60])

    # For a lognormal distribution, Cu = D60/D10.
    sigma = np.log(target_cu) / (z60 - z10)
    mu = np.log(d30_pack) - z30 * sigma

    sizes = np.logspace(mu - 3.5 * sigma, mu + 3.5 * sigma, 300)
    passing = norm.cdf((np.log(sizes) - mu) / sigma) * 100.0

    curve = pd.DataFrame({
        "particle_size_mm": sizes,
        "percent_passing": passing,
    })

    d10 = float(np.exp(mu + z10 * sigma))
    d30 = float(np.exp(mu + z30 * sigma))
    d60 = float(np.exp(mu + z60 * sigma))

    properties = {
        "D10": d10,
        "D30": d30,
        "D60": d60,
        "Cu": d60 / d10,
        "target_Cu": target_cu,
        "factor": factor,
    }
    return curve, properties
