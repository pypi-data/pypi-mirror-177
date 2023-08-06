import itertools

import dask
import dask.array as da
import numpy as np
import xarray as xr
import pandas as pd
from owl_dev.logging import logger

from ..settings import Settings
from ..utils import trim_memory_workers
from .detect import detect_beads


def beads(output_path, overwrite=False):
    """Detect beads in a given image."""
    (output_path / "bead").mkdir(exist_ok=True)

    ds = xr.open_zarr(output_path / "mos")
    sections = list(ds)
    if Settings.sections:
        sections = [sections[i - 1] for i in Settings.sections]

    logger.info(f"{len(sections)} section(s) to proceed with")

    for sect in sections:
        output_bead = output_path / "bead" / f"{sect}.parquet"
        if output_bead.exists() and not overwrite:
            logger.info(f"Skipping section {sect}")
            continue

        all_df = []
        for zval in ds[sect].z.values:
            logger.debug(f"Processing section {sect}:Z{zval}")
            im = ds[sect].sel(z=zval).data.mean(axis=0)

            fut = []
            im_o = da.overlap.overlap(im, 200, {0: 1, 1: 1})
            for indx in itertools.product(*map(range, im_o.blocks.shape)):
                fut.append(
                    detect_beads(
                        im_o.blocks[indx],
                        min_radius=Settings.beads["min_radius"],
                        max_radius=Settings.beads["max_radius"],
                        min_separation=Settings.beads["min_separation"],
                        high_threshold=Settings.beads["high_threshold"],
                        low_threshold=Settings.beads["low_threshold"],
                    )
                )

            circles = dask.compute(fut)[0]
            circles_full = []
            dy, dx = im.chunksize
            for j, indx in enumerate(itertools.product(*map(range, im_o.blocks.shape))):
                c = circles[j]
                if c is None:
                    continue
                c[:, 0] = c[:, 0] - 200 + dx * indx[1]
                c[:, 1] = c[:, 1] - 200 + dy * indx[0]
                circles_full.append(c)

            try:
                beads = np.concatenate(circles_full)
            except ValueError:
                logger.warning("No beads detected in section %s", sect)
                continue

            df = pd.DataFrame(
                beads,
                columns=["x", "y", "radius", "amplitude", "x_fwhm", "y_fwhm", "theta"],
            )

            df["z"] = zval
            df["section"] = str(sect)
            logger.info(
                "Bead detection done for section %s:Z%d (%d)", sect, zval, len(df)
            )
            all_df.append(df)

        df = pd.concat(all_df, ignore_index=True)
        df.to_parquet(output_bead)

        trim_memory_workers()
