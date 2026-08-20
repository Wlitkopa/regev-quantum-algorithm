"""Build the output/image directory paths used by the Regev pipeline.

Path layout mirrors what the original monolithic ``regev.py`` produced, so
existing analysis scripts keep working. The layout depends on:

* ``main_path_dir``  — user-chosen root under ``output_data/`` / ``images/``
* ``d_mode`` / ``qd_mode``  — ``"ceil"`` or ``"floor"``
* ``gauss_init``  — whether qubits were initialised with a Gaussian
* ``cfg`` (MeasRConfig) — measure-output-register + R-variant flags
"""

from pathlib import Path
from typing import Optional

from .config import MeasRConfig


def _ensure(dir_str: str) -> str:
    Path(dir_str).mkdir(parents=True, exist_ok=True)
    return dir_str


def _gauss_variant_dir(cfg: MeasRConfig) -> str:
    return (
        f"quantum_part_{cfg.measuring_output_register}_output_register_measuring_"
        f"{cfg.param_R}_R"
    )


def quantum_part_dir(
    main_path_dir: str,
    d_mode: str,
    qd_mode: str,
    n: int,
    R: float,
    cfg: Optional[MeasRConfig],
    gauss_init,
) -> str:
    """Directory that holds the raw quantum-part outputs for one N."""
    if gauss_init and cfg is not None:
        path = (
            f"output_data/{main_path_dir}/quantum_part/{_gauss_variant_dir(cfg)}/"
            f"{d_mode}_{qd_mode}/n_{n}_R_{R}"
        )
    else:
        path = f"output_data/{main_path_dir}/quantum_part/{d_mode}_{qd_mode}"
    return _ensure(path)


def all_parts_dir(
    main_path_dir: str,
    d_mode: str,
    qd_mode: str,
    n: int,
    R: float,
    cfg: Optional[MeasRConfig],
    gauss_init,
) -> str:
    """Directory for the ``run_all_algorithm`` (quantum + classical) writeup."""
    if gauss_init and cfg is not None:
        path = (
            f"output_data/{main_path_dir}/all_parts/quantum_part/"
            f"{cfg.measuring_output_register}_output_register_measuring_"
            f"{cfg.param_R}_R/{d_mode}_{qd_mode}/n_{n}_R_{R}"
        )
    else:
        path = f"output_data/{main_path_dir}/all_parts/quantum_part/{d_mode}_{qd_mode}"
    return _ensure(path)


def classical_analysis_dir(
    main_path_dir: str,
    type_dir: str,
    d_mode: str,
    qd_mode: str,
    cfg: Optional[MeasRConfig],
    gauss_params_dir: Optional[str],
) -> str:
    """Directory into which ``run_file_data_analyzer`` writes per-N results."""
    if cfg is None:
        path = (
            f"output_data/{main_path_dir}/classical_part/"
            f"file_analysis_all_types/{type_dir}/{d_mode}_{qd_mode}"
        )
    else:
        path = (
            f"output_data/{main_path_dir}/classical_part/"
            f"file_analysis_all_types_{cfg.measuring_output_register}_"
            f"output_register_measuring_{cfg.param_R}_R/{type_dir}/"
            f"{d_mode}_{qd_mode}/{gauss_params_dir}"
        )
    return _ensure(path)


def circuit_image_dirs(
    main_path_dir: str,
    d_mode: str,
    qd_mode: str,
    n: int,
    R: float,
    cfg: Optional[MeasRConfig],
    gauss_init,
) -> tuple[str, str]:
    """(general, decomposed) directories used when saving circuit images."""
    if gauss_init and cfg is not None:
        base = (
            f"images/{main_path_dir}/quantum_part/{_gauss_variant_dir(cfg)}/"
            f"{d_mode}_{qd_mode}/n_{n}_R_{R}/N_"
        )
        return base, base
    general = f"images/publikacja/general/{d_mode}_{qd_mode}"
    decomposed = f"images/publikacja/decomposed/{d_mode}_{qd_mode}"
    return general, decomposed


def find_gauss_quantum_file(
    main_path_dir: str, d_mode: str, qd_mode: str, N: int, cfg: MeasRConfig
) -> tuple[Optional[str], Optional[str]]:
    """Locate an existing quantum-part file (``N_<N>``) for a Gaussian run.

    Returns ``(file_name, gauss_params_dir)`` if found, otherwise ``(None, None)``.
    The gauss-params dir name (e.g. ``n_5_R_2866.001…``) is inferred from the
    matched path, because the on-disk name depends on values only known after
    running the quantum part.
    """
    base = (
        f"output_data/{main_path_dir}/quantum_part/"
        f"{_gauss_variant_dir(cfg)}/{d_mode}_{qd_mode}"
    )
    target = f"N_{N}"
    for p in Path(base).rglob(target):
        gauss_params_dir = p.parent.name
        return str(p), gauss_params_dir
    return None, None
