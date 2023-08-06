import cv2
import numpy as np
import scipy.ndimage as ndi
import warnings
from dask import delayed
from scipy.stats import median_abs_deviation

from astropy.modeling import models, fitting


def get_stats(img, nsamples=1000):
    median = []
    mad = []
    for n in range(nsamples):
        i, j = (np.random.uniform(size=2) * img.shape).astype("int")
        cutout = img[i - 50 : i + 50, j - 50 : j + 50]
        if cutout.size < 10000:
            continue
        v1 = np.median(cutout)
        v2 = median_abs_deviation(cutout.ravel(), scale="normal")
        if not np.isnan(v1):
            if v1 > 0:
                median.append(v1)
                mad.append(v2)

    if len(median) > 10:
        z1 = np.percentile(median, 20)
        try:
            z2 = np.percentile([v2 for v1, v2 in zip(median, mad) if v1 < z1], 90)
        except Exception:
            z2 = 0
    else:
        z1 = z2 = 0
    return z1, z2


def compute_background(img, filter_size=256):
    med1 = ndi.median_filter(img, (1, filter_size))
    med2 = ndi.median_filter(img, (filter_size, 1))
    return (med1 + med2) / 2


def compute_mask(img, threshold, background=None):

    if background is not None:
        img = img - background + 10

    z1, z2 = get_stats(img)
    if (z1 == 0) or (z2 == 0):
        return None

    mask = img > z1 + threshold * z2

    mask = ndi.binary_opening(mask, iterations=10)

    mask = (
        ndi.binary_dilation(mask, iterations=3) * 1
        - ndi.binary_erosion(mask, iterations=3) * 1
    )
    mask = ndi.binary_fill_holes(mask)

    mask = mask * 255

    mask = ndi.gaussian_filter(mask, 3)
    if mask.max() > 0:
        mask = mask / mask.max() * 255

    mask = mask.astype("uint8")
    return mask


@delayed
def detect_beads(
    img,
    min_separation=60,
    min_radius=60,
    max_radius=150,
    max_area=100_000,
    high_threshold=40,
    low_threshold=6,
):
    """Detect beads in image using HoughCircles"""
    img = img.astype("float32")
    img = ndi.gaussian_filter(img, 3)

    background = compute_background(img)

    mask0 = compute_mask(img, high_threshold)

    if mask0 is None:
        return

    mask = compute_mask(img, low_threshold, background=background)
    if mask is None:
        return

    mask = np.maximum(mask, mask0)

    analysis = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_16U)
    (totalLabels, label_ids, values, centroid) = analysis

    output = np.zeros(img.shape, dtype="uint8")
    for i in range(1, totalLabels):
        area = values[i, cv2.CC_STAT_AREA]
        if area > max_area:
            continue
        componentMask = (label_ids == i).astype("uint8") * 255

        # Creating the Final output mask
        output = cv2.bitwise_or(output, componentMask)

    circles0 = cv2.HoughCircles(
        output,
        cv2.HOUGH_GRADIENT,
        1,
        min_separation,
        param1=150,
        param2=15,
        minRadius=min_radius,
        maxRadius=max_radius,
    )
    if circles0 is None:
        return None

    circles0 = np.round(circles0[0, :]).astype("int")
    p_init = models.Gaussian2D()
    fit_p = fitting.LevMarLSQFitter()

    circles = []
    buffer = 10
    for c in circles0:
        xc, yc, rad = c
        rad = rad + buffer
        y, x = np.mgrid[: (2 * rad), : (2 * rad)]
        sy = slice(yc - rad, yc + rad)
        sx = slice(xc - rad, xc + rad)
        im = img[sy, sx]
        if im.size < (4 * rad * rad):
            continue
        with warnings.catch_warnings():
            p = fit_p(p_init, x, y, im)
            fwhm = (p.x_fwhm + p.y_fwhm) / 2
            if fwhm < 300:
                c = [
                    xc,
                    yc,
                    rad - buffer,
                    p.amplitude.value,
                    p.x_fwhm,
                    p.y_fwhm,
                    p.theta.value,
                ]
                circles.append(c)
    if len(circles) > 0:
        circles = np.array(circles)
    else:
        circles = None
    return circles
