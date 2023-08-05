from re import I
from statistics import mode
from typing import Generator
import numpy as np
import xarray as xr
from pathlib import Path
from datetime import datetime

from gfatpy import DATA_DN
from gfatpy.lidar.utils import LIDAR_INFO
from gfatpy.lidar import file_manager
from gfatpy.lidar.depolarization.io import ghk_output_reader

def backscattering_ratio(
    molecular_backscatter: np.ndarray, particle_backscatter: np.ndarray
) -> np.ndarray:
    """Retrieves the backscattering ratio. Inputs must be in the same units.

    Args:
        molecular_backscatter (np.ndarray): Molecular backscatter coefficient.
        particle_backscatter (np.ndarray):  Particle backscatter coefficient.

    Returns:
        np.ndarray: backscattering ratio
    """

    return molecular_backscatter + particle_backscatter / molecular_backscatter

def linear_volume_depolarization_ratio(
    signal_R: np.ndarray,
    signal_T: np.ndarray,
    channel_R: str,
    channel_T: str,
    range: np.ndarray,
    time: np.ndarray,
    eta: float = 1,
    K: float = 1,
    GT: float = 1,
    HT: float = -1,
    GR: float = 1,
    HR: float = 1,
) -> xr.DataArray:
    """Calculate the linear volume depolarization ratio.

    Args:
        signal_R (np.ndarray): reflected signal in the polarizing beam splitter cube.
        signal_T (np.ndarray): transmitted signal in the polarizing beam splitter cube.
        channel_R (str): reflected channel in the polarizing beam splitter cube.
        channel_T (str): transmitted channel in the polarizing beam splitter cube.
        range (np.ndarray): range series of the signal.
        time (np.ndarray): time vector of the signal.
        eta (float, optional): calibration factor retrieved with Delta90 method. Defaults to 1.
        K (float, optional): K factor value simulated with Volker's algorithm. Defaults to 1.
        GT (float, optional): GT factor value simulated with Volker's algorithm. Defaults to 1.
        HT (float, optional): HT factor value simulated with Volker's algorithm. Defaults to -1.
        GR (float, optional): GR factor value simulated with Volker's algorithm. Defaults to 1.
        HR (float, optional): HR factor value simulated with Volker's algorithm. Defaults to 1.

    Raises:
        ValueError: Wavelength, telescope or mode does not fit raises 'Polarized channels to be merged not appropiated'.
        ValueError: polarization codes do not fit raises 'Polarized channels to be merged not appropiated'.

    Returns:
        xr.DataArray: linear_volume_depolarization_ratio
    """

    wavelengthR, telescopeR, polR, modeR = file_manager.channel2info(channel_R)
    wavelengthT, telescopeT, polT, modeT = file_manager.channel2info(channel_T)

    if wavelengthR != wavelengthT or telescopeR != telescopeT or modeR != modeT:
        raise ValueError("Polarized channels to be merged not appropiated.")

    if polT not in ["p", "c", "s"] or polR not in ["p", "c", "s"] and polR != polT:
        raise ValueError("Polarized channels to be merged not appropiated.")

    eta = eta / K
    ratio = (signal_R / signal_T) / eta
    lvdr_ = (((GT + HT) * ratio - (GR + HR)) / ((GR - HR) - (GT - HT) * ratio)).astype(
        float
    )

    # Create DataArray
    lvdr = xr.DataArray(
        lvdr_,
        coords={"time": time, "range": range},
        dims=["time", "range"],
        attrs={
            "long_name": "Linear Volume Depolarization Ratio",
            "detection_mode": LIDAR_INFO["metadata"]["code_mode_str2number"][modeR],
            "wavelength": wavelengthR,
            "units": "$\\#$",
        },
    )
    
    return lvdr

def lvdr_from_dataset(dataset: xr.Dataset, ghk_filepath: Path | None = None, calibration: dict | None = None) -> xr.Dataset:
    """Retrieve linear volume depolarization ratio for the polarizing channels and include it in the dataset.

    Args:
        dataset (xr.Dataset): lidar dataset.
        ghk_filepath (Path | None, optional): GHK filepath. Defaults to None. If None, it is searched in the GFAT server.
        calibration (dict | None, optional): eta star calibration dictionary with `ghk_output_reader` output shape. Defaults to None. If None, it is searched in the GFAT server.

    Raises:
        ValueError: 'dataset must have dimension `time`.'
        FileNotFoundError: 'ghk_filepath not found.'
        KeyError: 'eta_star_mean must be key in calibration dictionary.'
        ValueError: "DATA_DN is None."
        ValueError: 'No GHK file found.'
        ValueError: 'No GHK file found.'

    Returns:
        xr.Dataset: lidar dataset including linear volue depolarization ratio for every polarizing channel.
    """    
    #Take date
    if 'time' not in list(dataset.variables.keys()):
        raise ValueError('dataset must have dimension `time`.')                
    date = dataset.time.values[0]

    #check ghk_filepath
    if ghk_filepath is not None:
        if not ghk_filepath.exists():
            raise FileNotFoundError('ghk_filepath not found.')

    #check calibration
    if calibration is not None: 
        if 'eta_star_mean' not in calibration.keys():
            raise KeyError('eta_star_mean must be key in calibration dictionary.')

    #Get lidar name
    lidar_name: str = dataset.attrs['system'].upper()

    #Get polarization channels to be processed
    polarized_channels = LIDAR_INFO['lidars'][lidar_name]['polarized_channels']
    ghk_channels = LIDAR_INFO['lidars'][lidar_name]['GHK_channels']
    
    for channel_ in ghk_channels.keys():
        wavelength_, telescope_ = channel_[0:2], channel_[-1]
        for mode_ in polarized_channels[telescope_][wavelength_].keys():
            
            #Search GHK file according to date
            if ghk_filepath is None:
                if DATA_DN is None:
                    raise ValueError("DATA_DN is None.")                
                year = datetime.strftime(date,'%Y')
                month = datetime.strftime(date,'%m')
                day = datetime.strftime(date,'%d')
                lidar_nick = LIDAR_INFO['metadata']['name2nick'][lidar_name]
                root_dir = Path(DATA_DN / lidar_name / 'QA' / 'GHK')
                if root_dir.exists():
                    ghk_files = root_dir.rglob(f'output_optic_input_{lidar_nick}*{channel_}*.dat')
                    if isinstance(ghk_files, Generator):
                        ghk_files = [*ghk_files]
                        #Select the previous closest ghk_filepath to target_time.
                        ghk_filepath = search_ghk(ghk_files, date)            
                    else:
                        raise ValueError('No GHK file found.')
                else:
                    raise ValueError('No GHK-file found.')

            #read data from GHK file
            ghk_dict = ghk_output_reader(ghk_filepath)

            #Data
            channel_R = polarized_channels[telescope_][wavelength_][mode_]['R']
            channel_T = polarized_channels[telescope_][wavelength_][mode_]['T']
            signal_R = dataset[f"signal_{channel_R}"].values
            signal_T = dataset[f"signal_{channel_T}"].values
            range = dataset.range.values
            time = dataset.time.values
            eta, K, GT, HT, GR, HR, = ghk_dict['eta'], ghk_dict['K'], ghk_dict['GT'], ghk_dict['HT'], ghk_dict['GR'], ghk_dict['HR']

            #Retrieve LVDR
            lvdr = linear_volume_depolarization_ratio(
                signal_R,
                signal_T,
                channel_R,
                channel_T,
                range,
                time,
                eta,
                K,
                GT,
                HT,
                GR,
                HR,
            )     
            #Save lvdr in dataset           
            key_channel = channel_R.replace('p','').replace('a','')
            dataset[f'linear_volume_depolarization_ratio_{key_channel}'] = lvdr

    return dataset

def search_ghk(file_list: list, date: datetime)->Path:
    #FIXME: to be done.
    ghk_filepath = Path()
    return ghk_filepath


def particle_depolarization(
    linear_volume_depolarization_ratio: np.ndarray,
    backscattering_ratio: np.ndarray,
    molecular_depolarization: float,
    time: np.ndarray,
    range: np.ndarray,
) -> xr.DataArray: #FIXME: this function may realy direction to the lvdr xr.DataArray inside the lidar dataset once executed lvdr_from_dataset.
    """Calculate the linear particle depolarization ratio.

    Args:
        linear_volume_depolarization_ratio (np.ndarray): linear volume depolarization ratio
        backscattering_ratio (np.ndarray): _description_
        molecular_depolarization (float): molecular linear volume depolarization ratio
        time (np.ndarray): time vector of the signal.
        range (np.ndarray): range series of the signal.

    Returns:
        np.ndarray: linear particle depolarization ratio.

    Notes:
    The linear particle depolarization ratio is calculated by the formula:

    .. math::
       \delta^p = \frac{(1 + \delta^m)\delta^V \mathbf{R} - (1 + \delta^V)\delta^m}
       {(1 + \delta^m)\mathbf{R} - (1 + \delta^V)}


    References:
    Freudenthaler, V. et al. Depolarization ratio profiling at several wavelengths in pure
    Saharan dust during SAMUM 2006. Tellus, 61B, 165-179 (2008)
    """

    delta_p = (
        (1 + molecular_depolarization)
        * linear_volume_depolarization_ratio
        * backscattering_ratio
        - (1 + linear_volume_depolarization_ratio) * molecular_depolarization
    ) / (
        (1 + molecular_depolarization) * backscattering_ratio
        - (1 + linear_volume_depolarization_ratio)
    )

    # Create DataArray
    delta_p_xarray = xr.DataArray(
        delta_p,
        coords={"time": time, "range": range},
        dims=["time", "range"],
        attrs={
            "long_name": "Linear Volume Depolarization Ratio",
            "units": "$\\#$",
        },  # TODO: decide where the attributes should be included.
    )
    return delta_p_xarray