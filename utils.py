#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Defines various data containers for plotting a transect.
:copyright: 2015 Agile Geoscience
:license: Apache 2.0
"""
import os
import re
from functools import partial

import numpy as np
import pyproj as pp
from shapely.ops import transform


def nearest_point(p, plist):
    """
    Given a shapely Point, finds the nearest Point in a list of Points.

    Args:
        p (Point): A ``shapely`` Point.
        plist (list): A list of Points.

    Returns:
        Point: The nearest Point.
    """
    p = (p.x, p.y)
    plist = [(pt.x, pt.y) for pt in plist]
    d_sq = np.sum((np.asarray(plist) - p)**2, axis=1)
    return plist[np.argmin(d_sq)]


def listdir(directory, match=None):
    """
    Wrapper for `os.listdir()` that returns full paths. A bit like
    `utils.walk()` but not recursive. Case insensitive.

    Args:
        directory (str): The directory to list.

    Yields:
        str: Full path to each file in turn.
    """
    for f in os.listdir(directory):
        if match:
            if not re.search(match, f, flags=re.IGNORECASE):
                continue
        yield os.path.join(directory, f)


def walk(directory, match=None):
    """
    Find files whose names match some regex. Like `fnmatch` but with regex.
    Like `utils.listdir()` but recursive. Case insensitive.

    Args:
        directory (str): The directory to start at.

    Yields:
        str: Full path to each file in turn.
    """
    for path, dirs, files in os.walk(directory):
        for f in files:
            if match:
                if not re.search(match, f, flags=re.IGNORECASE):
                    continue
            yield os.path.join(path, f)


def rolling_median(a, window):
    """
    Apply a moving median filter.
    """
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    rolled = np.lib.stride_tricks.as_strided(a,
                                             shape=shape,
                                             strides=strides)
    rolled = np.median(rolled, -1)
    rolled = np.pad(rolled, window / 2, mode='edge')
    return rolled


def despike(curve, curve_sm, max_clip):
    """
    Remove spikes from a curve.
    """
    spikes = np.where(curve - curve_sm > max_clip)[0]
    spukes = np.where(curve_sm - curve > max_clip)[0]
    out = np.copy(curve)
    out[spikes] = curve_sm[spikes] + max_clip  # Clip at the max allowed diff
    out[spukes] = curve_sm[spukes] - max_clip  # Clip at the min allowed diff
    return out


def utm2lola(data):
    """
    Transform UTMs to lon-lats. Assumes both are NAD83.
    """
    utm_nad83 = pp.Proj("+init=EPSG:26920")
    ll_nad83 = pp.Proj("+proj=longlat +ellps=GRS80 +datum=NAD83 +no_defs")
    utm2lola = partial(pp.transform, utm_nad83, ll_nad83)

    return transform(utm2lola, data)


def get_tops(fname):
    """
    Takes a tops_dictionary for plotting in the logs tracks.

    Args:
        fname (str): The path to a file containing the tops.
    """
    tops = {}
    with open(fname) as f:
        for line in f.readlines():
            if not line.startswith('#'):
                temp = line.strip().split(',')
                tops[temp[0]] = float(temp[1])
    return tops
