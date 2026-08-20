"""Drawing helpers for the constructed quantum circuit and Gaussian input state."""

from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

from utils.regev_result import RegevResult

from .config import MeasRConfig


def draw_gaussian_probabilities(
    result: RegevResult, path: str, cfg: Optional[MeasRConfig]
) -> str:
    """Write three probability plots plus a text data-dump under ``path``.

    Returns a human-readable list of the files written.
    """
    param_R = cfg.param_R if cfg else ""
    measure_output_register = cfg.measure_output_register if cfg else False

    amps = result.amps
    x = np.arange(2 ** result.exp_register_width, dtype=float)
    y = list(amps)

    Path(path).mkdir(parents=True, exist_ok=True)
    written: list[str] = []

    # Point plot with connecting lines
    file = f"{path}/line_points.svg"
    plt.figure(figsize=(8, 4))
    plt.plot(x, y, marker="o")
    plt.xlabel("Input registry value")
    plt.ylabel("Probability amplitude")
    plt.grid(True)
    plt.ticklabel_format(useOffset=False, style="plain")
    plt.savefig(file, format="svg")
    written.append(file)

    # Bar chart
    file = f"{path}/diagram.svg"
    plt.figure(figsize=(8, 4))
    plt.bar(x, y, width=0.8)
    plt.xlabel("Input registry value")
    plt.ylabel("Probability amplitude")
    plt.ticklabel_format(useOffset=False, style="plain")
    plt.savefig(file, format="svg")
    written.append(file)

    # Smooth spline (only defined for len(x) >= 4)
    if len(x) >= 4:
        xs = np.linspace(x.min(), x.max(), 500)
        ys = make_interp_spline(x, y, k=3)(xs)
        file = f"{path}/line_points_cont.svg"
        plt.figure(figsize=(8, 4))
        plt.plot(xs, ys)
        plt.scatter(x, y, color="black", s=20)
        plt.title("Initial qubits probability amplitudes - 1 dimension")
        plt.xlabel("Input registry value")
        plt.ylabel("Probability amplitude")
        plt.grid()
        plt.ticklabel_format(useOffset=False, style="plain")
        plt.savefig(file, format="svg")
        written.append(file)

    data_file = f"{path}/gauss_data"
    data = (
        f"d: {result.number_of_primes}\n"
        f"qd: {result.exp_register_width}\n"
        f"N: {result.N}\n"
        f"n: {result.n}\n\n"
        f"measure_output_register: {measure_output_register}\n"
        f"mu_init: {result.gauss_init_mu}\n"
        f"sigma_init: {result.gauss_init_sigma}\n"
        f"mu: {result.gauss_mu}\n"
        f"param_R: {param_R}\n"
        f"R: {result.gauss_R}\n"
        f"sigma: {result.gauss_sigma}\n"
        f"probabilities sum: {result.probs_sum}\n"
        f"probability amplitudes:\n{y}"
    )
    Path(data_file).write_text(data)
    written.append(data_file)

    return "".join(f" - {f}\n" for f in written)


def save_circuit_image(circuit, filename_no_ext: str, decompose: bool = False) -> str:
    """Render ``circuit`` (optionally decomposed) as SVG and return its path."""
    Path(filename_no_ext).parent.mkdir(parents=True, exist_ok=True)
    target = circuit.decompose() if decompose else circuit
    fig = target.draw(output="mpl", style="iqp-dark", fold=-1)
    file = f"{filename_no_ext}.svg"
    fig.savefig(file, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    return file
