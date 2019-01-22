import os
import tables as     tb
import numpy  as     np

from   invisible_cities.io      .mcinfo_io import read_mcinfo
from   antea           .io      .mc_io     import read_mcsns_response
from   antea           .sensors            import sensor_functions    as sf


def test_simulate_sipm_response(ANTEADATADIR):

    PATH_IN       = os.path.join(ANTEADATADIR, 'full_ring_test.pet.h5')
    h5in          = tb.open_file(PATH_IN, 'r')
    single_pe_rms = 1.67748
    info_dict     = read_mcinfo(h5in)
    wvf_dict      = read_mcsns_response(PATH_IN)
    sns_dict      = list(wvf_dict.values())[0]
    tot_charges   = np.array(list(map(lambda x: sum(x.charges), list(sns_dict.values()))))
    charge_pes    = sf.simulate_sipm_response(tot_charges, single_pe_rms)

    assert len(charge_pes)  == len(tot_charges)
    assert charge_pes.all() >= 0

