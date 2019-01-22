import numpy  as np
import pandas as pd

from invisible_cities.reco import wfm_functions    as wfm
from invisible_cities.reco import sensor_functions as sf


def simulate_sipm_response(tot_charges, pe_resolution):
    """ Return total signal in adc counts with the fluctuation of the pe.

    Parameters
    ----------
    tot_charges     : np.array
    Number of photoelectrons detected by each sipm.
    sipm_adc_to_pes : np.array or float
    Gain value of each sipm, or the same value for all of them.
    pe_resolution   : float
    Single photoelectron rms for sipms.

    Returns
    -------
    charges_adc     : np.array
    Total charges in adc counts.
    """

    ## Fluctuate according to charge resolution
    sipm_fl    = sf.charge_fluctuation(tot_charges, pe_resolution)
    return sipm_fl

