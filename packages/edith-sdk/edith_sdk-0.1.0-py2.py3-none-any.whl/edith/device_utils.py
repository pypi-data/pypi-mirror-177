from typing import Dict, Any
import pkg_resources
import multiprocessing
import psutil
import sys
import platform

allowed_packages = (
    'tensorflow',
    'tensorflow-hub',
    'tensorflow-estimator',
    'tensorboard',
    'numpy',
    'huggingface-hub',
    'datasets'
    'transformers',
    'torch',
    'keras',
    'tokenizers',
    'optuna',
    'pandas',
    'protobuf',
    'scikit-learn',
    'scipy',
    'sklearn',
    'edith'
)


def fetch_host_details() -> Dict[str, Any]:
    os_name = platform.system() + " v" + platform.release()
    vcpu = multiprocessing.cpu_count()
    ram_in_GIB = round(psutil.virtual_memory().total / (1024 * 1024 * 1024), 2)
    python_version = sys.version_info
    python_version = f"{python_version.major}.{python_version.minor}"
    return {
        "Operating System": "Unable to determine",
        "vcpu": vcpu,
        "RAM": f"{ram_in_GIB} GiB",
        "Executable": f"Python {python_version}",
        "GPU": "Unable to determine",
        # "TPU": "Unable to determine",
    }


def fetch_env_details() -> Dict[str, Any]:
    details = {}
    packages = list(pkg_resources.working_set)
    for package in packages:
        if package.key in allowed_packages:
            details[package.key] = package.version
    return details
