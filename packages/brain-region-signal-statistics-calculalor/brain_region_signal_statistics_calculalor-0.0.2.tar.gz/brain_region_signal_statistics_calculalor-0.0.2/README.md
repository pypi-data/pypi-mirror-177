# Welcome!
This is a repository for computing region signal statistics for 3D brain volume.


# Instructions
To use the brain-region-signal-statistics-calculalor library, either clone this repository and install the requirements listed in setup.py or install directly with pip.

Install package

```
pip install brain-region-signal-statistics-calculalor
```

The script should take four inputs:

- an image volume to summarize (e.g. data/signal.npz)
- an image volume that maps voxels to brain region IDs (e.g. data/annotation.npz)
- a CSV describing brain regions (e.g. data/structures.csv)
- an output CSV file name (e.g. data/statistics.csv)

# Testing 

To compute the statistics for the given signal image, run:

```
./run.py --annotation_volume_path data/annotation.npz --signal_volume_path data/signal.npz --structures_df_path data/structures.csv --statistics_df_path data/statistics.csv
```

# Contact
Di Wang (di-wang@uiowa.edu)