import dask.array as da
import numpy as np
import xarray as xr
from dask import delayed
from owl_dev.logging import logger
import sep

from ..settings import Settings
from ..utils import trim_memory_workers
from .bead_detector import bead_detect_worker, create_mask, plot_beads


def bead_detect(output_path, overwrite=False, fig=False):
    """Detect beads in a given image."""
    mod_input_path = output_path / "mos"
    (output_path / "bead").mkdir(exist_ok=True)

    ds = xr.open_zarr(mod_input_path)
    ds16 = xr.open_zarr(mod_input_path, group="l.16")
    sections = list(ds)
    if Settings.sections:
        sections = [sections[i - 1] for i in Settings.sections]

    logger.info(f"{len(sections)} section(s) to proceed with")

    for sect in sections:
        output_bead = output_path / "bead" / f"{sect}.parquet"
        if output_bead.exists() and not overwrite:
            logger.info(f"Skipping section {sect}")
            continue
        logger.debug(f"Processing section {sect}")

        # loop over all available z planes
        for z_sect in list(ds[sect]["z"].data):
            mean_data_org = ds[sect].sel(z=z_sect).data.mean(axis=0)
            mean_data_l16 = ds16[sect].sel(z=z_sect).data.mean(axis=0)

            # create a mask from the scaled image
            # A- mask with similar l16 dimensions
            mask_image_l16 = create_mask(
                mean_data_l16,
                cl_morph_parm=10,
                c_min_area=0.01,
                c_count_max=15,
                output_size=None,
            )

            # B- mask with similar original data dimensions
            mask_image_d = delayed(create_mask)(
                mean_data_l16,
                cl_morph_parm=10,
                c_min_area=0.01,
                c_count_max=15,
                output_size=mean_data_org.shape[::-1],
            )

            mask_image = da.from_delayed(
                mask_image_d, shape=mean_data_org.shape, dtype="uint8"
            ).rechunk(mean_data_org.chunksize)

            # Evaluate standard deviation of background extracted from l16
            # In case the original background failed, we deploy this value

            try:
                l16_bkg = sep.Background(
                    np.array(mean_data_l16), mask=mask_image_l16, bw=128, bh=128
                )
                std_l16 = np.std(l16_bkg.back())
            except Exception:
                std_l16 = np.nanmax(np.array(mean_data_l16))

            beads_df = bead_detect_worker(
                mean_data_org, mask_image, overlap_size=200, std_l16=std_l16
            )
            beads_df["section"] = str(sect)
            beads_df["z"] = z_sect

            beads_df.to_parquet(output_bead)

            if fig:
                plot_beads(
                    mean_data_org,
                    mask_image,
                    beads_df,
                    fig_fname=output_path / "bead" / f"{sect}_bead.png",
                )
            del mask_image
            del mean_data_org
            del mean_data_l16
            trim_memory_workers()


# TODO: write as script
# if __name__ == "__main__":
