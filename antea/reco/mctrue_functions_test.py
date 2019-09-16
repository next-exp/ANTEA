import os
import math
import numpy  as np
import pandas as pd

from .           import reco_functions   as rf
from .           import mctrue_functions as mcf
from .. database import load_db          as db


def test_find_hits_of_given_particles(ANTEADATADIR):
    """
    This test checks that the sum of the energy of the hits is always lower
    than the initial kinetic energy of the event.
    """
    PATH_IN    = os.path.join(ANTEADATADIR, 'ring_test_new_tbs.h5')
    particles  = pd.read_hdf(PATH_IN, 'MC/particles')
    hits       = pd.read_hdf(PATH_IN, 'MC/hits')

    primaries  = particles[particles.primary == True]
    evt_energy = primaries.groupby(['event_id'])['kin_energy'].sum()

    part_id    = particles.particle_id.values
    sel_hits   = mcf.find_hits_of_given_particles(part_id, hits)
    sum_e_hits = sel_hits.groupby(['event_id'])[['energy']].sum()
    for e_hit, e_evt in zip(sum_e_hits.values, evt_energy.values):
        assert e_hit <= e_evt


def test_select_photoelectric(ANTEADATADIR):
    """
    This test checks that the function select_photoelectric takes the events
    in which at least one of the initial gammas interacts via photoelectric
    effect depositing its 511 keV and stores the weighted average position
    of its/their hits.
    """
    PATH_IN      = os.path.join(ANTEADATADIR, 'ring_test_new_tbs.h5')
    DataSiPM     = db.DataSiPM('petalo', 0)
    DataSiPM_idx = DataSiPM.set_index('SensorID')
    sns_response = pd.read_hdf(PATH_IN, 'MC/waveforms')
    threshold    = 2
    sel_df       = rf.find_SiPMs_over_threshold(sns_response, threshold)

    particles = pd.read_hdf(PATH_IN, 'MC/particles')
    hits      = pd.read_hdf(PATH_IN, 'MC/hits')
    events    = particles.event_id.unique()

    for evt in events[:]:
        evt_parts = particles[particles.event_id == evt]
        evt_hits  = hits     [hits     .event_id == evt]

        select, true_pos = mcf.select_photoelectric(evt_parts, evt_hits)

        if select:
            assert rf.greater_or_equal(evt_hits.energy.sum(), 0.476443, 1.e-3)
        else:
            assert len(true_pos) == 0

        if len(true_pos) == 1:
            assert rf.lower_or_equal(evt_hits.energy.sum(), 0.511, 1.e-3)
        elif len(true_pos) == 2:
            assert evt_hits.energy.sum() > 0.511

