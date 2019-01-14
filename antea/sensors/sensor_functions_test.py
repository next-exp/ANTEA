import os
import tables as     tb
import numpy  as     np

from   invisible_cities.database           import load_db             as DB
from   invisible_cities.io      .mcinfo_io import read_mcinfo
from   antea           .io      .mc_io     import read_mcsns_response
from   antea           .sensors            import sensor_functions    as sf


def test_simulate_sipm_response(ANTEADATADIR):
    run_number         = 100000
    single_pe_rms      = DB.DataSiPM(run_number).Sigma.values
    single_pe_rms_mean = np.mean(single_pe_rms)
    adc_to_pes         = DB.DataSiPM(run_number).adc_to_pes.values
    adc_to_pes_mean    = np.mean(adc_to_pes)

    PATH_IN     = os.path.join(ANTEADATADIR, 'full_ring_test.pet.h5')
    h5in        = tb.open_file(PATH_IN, 'r')

    info_dict   = read_mcinfo(h5in)
    wvf_dict    = read_mcsns_response(PATH_IN)
    sns_dict    = list(wvf_dict.values())[0]
    tot_charges = np.array(list(map(lambda x: sum(x.charges), list(sns_dict.values()))))
    charge_adc  = sf.simulate_sipm_response(tot_charges, adc_to_pes_mean, single_pe_rms_mean)

    assert len(charge_adc)  == len(tot_charges)
    assert charge_adc.all() >= 0

