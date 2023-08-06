""" This modules contains utility to create offresonance related parameters"""
__all__ = ["generate_inhomogeneity_map"]

import numpy as np
from pint import Quantity


def generate_inhomogeneity_map(labels, B0: Quantity, sus_maps: dict, padsize):
    """ Calculates inhomogeneity maps on discrete 3D maps of suseptibility values

    :param labels: 3D volume oof labels
    :param B0: Field strength in
    :param sus_maps: dictionary that maps a suszeptibility for all values in labels
    :param padsize:
    :return:
    """
    labels_pad = np.pad(labels, padsize, constant_values=0)

    phantom = np.ones_like(labels_pad).astype(np.float64) * -7e-7
    for key, val in sus_maps.items():
        phantom[np.where(labels_pad == key)] = val
    # phantom = Quantity(phantom, "")

    mu0 = Quantity(4. * np.pi * 1e-7, "H/m")

    # Equation 5
    center = np.ceil((np.array(phantom.shape) + 1) / 2)
    x, z, y = np.meshgrid(*[np.arange(phantom.shape[i]) - center[i] for i in range(3)], indexing="ij")
    corterm = 3 * z ** 2 / (x ** 2 + y ** 2 + z ** 2) - 1

    # Equation 4
    Mz = B0.to("T") * phantom / mu0
    Mk = np.fft.fftshift(np.fft.fftn(Mz.m))
    Bk = (-mu0 * Mk / 3. * corterm).m
    Bk[int(center[0]), int(center[1]), int(center[2])] = -B0.m_as("T") * 2.9e-8 / 3

    result = np.fft.ifftn(np.fft.ifftshift(Bk))
    inhomogeneity = np.real(result[padsize:-padsize, padsize:-padsize, padsize:-padsize])
    background_mean = np.mean(inhomogeneity[np.where(labels == 0)])
    inhomogeneity -= background_mean

    pmax = np.percentile(np.abs(inhomogeneity[np.where(labels != 0)]), 95)
    inhomogeneity /= pmax
    return inhomogeneity
