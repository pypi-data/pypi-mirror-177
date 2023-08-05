import warnings
import pkg_resources

from .config import get_system_and_data_dn, set_logger_level

set_logger_level("WARNING")

SYSTEM_DN, DATA_DN = get_system_and_data_dn()

if DATA_DN is None:
    if SYSTEM_DN is None:
        warnings.warn(
            f"No {SYSTEM_DN} directory on this system. NAS not available",
            ResourceWarning,
        )
    else:
        warnings.warn(
            f"No {DATA_DN} directory on this system. NAS data not available",
            ResourceWarning,
        )


from . import lidar, utils, cloudnet, atmo, constants, aeronet

__all__ = ["lidar", "utils", "cloudnet", "atmo", "constants", "aeronet"]
__version__ = pkg_resources.get_distribution("gfatpy")

__doc__ = """
# What is gfatpy?
A python package for GFAT utilities

# Installation
You can use gfatpy either you could use the API (functions) only or maybe prefer to modify the source code. The second option requires aditional configuration.
The following are common requirements

- Python>=3.10 (Run `python3 --version` to verify)
- [Brew](https://brew.sh/) and [netCDF4](https://formulae.brew.sh/formula/netcdf#default) installed (MacOS)

## Downloading the repository
You must have access to the gfatpy [repository](https://gitlab.com/gfat1/gfatpy). Stable releases are at the `main` brach while other experimental features or work in progress is at `develop`.

## User installation
User installation is limited and could not be isolated for other system dependencies. Not recommended if you need to make changes to the code, run tests
Once the source code is downloaded, go to the directory where pyproject.toml is in shell (linux, macOS) or Powershell (Windows) and execute the following line:
```
python3 -m pip install .
```
Then, gfatpy will be available to import from your global python (or local in case you use virtualenvs)
## Development installation
This is the recommended way if changing code is needed, running the included notebooks, run the test and contribute.
You will need as aditional dependencies:
- [Poetry](https://python-poetry.org/docs/#installation)

After downloading or clonning the repository into your local machine execute `poetry install` to create the virtual environment and then `poetry shell` to activate it in the current shell.

Aditional commands:
- `gfatpy` will be available
- `pytest` will execute all the tests. Also it can recieve an argument especifying the route or file. For instance, `pytest tests/test_ecmwf.py` will execute only ECMWF related tests.

Contribution considerations:
- Merge requests or commits to develop branch on Gitlab.
- Run [pre-commit] on local by installing the git hook with `pre-commit install`

## Troubleshooting

#
"""
