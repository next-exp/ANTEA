import tables as tb
import numpy  as np

from invisible_cities.io  .table_io    import make_table
from invisible_cities.io  .  dst_io    import load_dst
from invisible_cities.reco.corrections import Correction


class ZRfactors(tb.IsDescription):
    z            = tb.Float32Col(pos=0)
    r            = tb.Float32Col(pos=1)
    factor       = tb.Float32Col(pos=2)
    uncertainty  = tb.Float32Col(pos=3)
    nevt         = tb. UInt32Col(pos=4)


def zr_writer(hdf5_file, **kwargs):
    zr_table = make_table(hdf5_file,
                          fformat = ZRfactors,
                          **kwargs)

    def write_zr(zs, rs, fs, us, ns):
        row = zr_table.row
        for i, z in enumerate(zs):
            for j, r in enumerate(rs):
                row["z"]           = z
                row["r"]           = r
                row["factor"]      = fs[i,j]
                row["uncertainty"] = us[i,j]
                row["nevt"]        = ns[i,j]
                row.append()
    return write_zr


def zr_correction_writer(hdf5_file, * ,
                         group       = "Corrections",
                         table_name  = "ZRcorrections",
                         compression = 'ZLIB4'):
    return zr_writer(hdf5_file,
                     group        = group,
                     name         = table_name,
                     description  = "ZR corrections",
                     compression  = compression)


def load_zr_corrections(filename, *,
                        group = "Corrections",
                        node  = "ZRcorrections",
                        **kwargs):
    dst  = load_dst(filename, group, node)
    z, r = np.unique(dst.z.values), np.unique(dst.r.values)
    f, u = dst.factor.values, dst.uncertainty.values

    return Correction((z, r),
                      f.reshape(z.size, r.size),
                      u.reshape(z.size, r.size),
                      **kwargs)
