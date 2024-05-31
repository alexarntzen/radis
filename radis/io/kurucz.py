""""

Summary
-----------------------

Kurucz database parser

-----------------------

Defines :py:func:`~radis.io.fetch_kurucz` based on :py:class:`~AdBKurucz`

"""

import os

from radis.api.hdf5 import DataFileManager
from radis.api.kuruczapi import AdBKurucz,get_atomic_number,get_ionization_state


def fetch_kurucz(species):
    kurucz = AdBKurucz(species)
    data_manager = DataFileManager(engine="pytables")
    atomic_number = f"{get_atomic_number(species):02}"
    ionization_state_str = f"{get_ionization_state(species):02}"
    hdf5_file = f"gf{atomic_number}{ionization_state_str}.hdf5"
    kurucz.url = kurucz.get_url(atomic_number, ionization_state_str)
    kurucz.hdf5_file = hdf5_file  # Set kurucz.hdf5_file to hdf5_file

    # If hdf5 file exists, read data from it
    if os.path.exists(hdf5_file):
        print("HDF5 file already exists, reading data from it.")
        df = data_manager.read(fname=hdf5_file, key="df")
        kurucz.add_airbrd(df)
    else:
        kuruczf = kurucz.download_file()
        df = kurucz.read_kurucz(kuruczf)
        data_manager.write(
            file=hdf5_file,
            df=df,
            append=False,
            key="df",
            format="table",
            data_columns=df.columns,
        )
        df = data_manager.read(fname=hdf5_file, key="df")
        kurucz.add_airbrd(df)

    return hdf5_file, df
