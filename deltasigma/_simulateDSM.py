# -*- coding: utf-8 -*-
# _simulateDSM.py
# Module providing the simulateDSM function,
#
#
# python-deltasigma is a 1:1 Python replacement of Richard Schreier's
# MATLAB delta sigma toolbox (aka "delsigma"), upon which it is heavily based.
# The delta sigma toolbox is (c) 2009, Richard Schreier.
#
# python-deltasigma is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# LICENSE file for the licensing terms.
#
# This file was originally from `pydsm`, then modified quite a bit.
# Many thanks to the original author.
#
# The original file is
# Copyright (c) 2012, Sergio Callegari
# All rights reserved.
#
# The modifications are mine.
# Copyright (c) 2014, G. Venturini and the python-deltasigma contributors
#

from __future__ import print_function


from ._simulateDSM_python import simulateDSM as _simulateDSM_python

warned = False

# Code to compile the Cython extensions
# Extensions tested on Linux and Mac OS X, but not on Windows
# please report any bug (or patches!) on
# https://github.com/ggventurini/python-deltasigma/issues


def simulateDSM(u, arg2, nlev=2, x0=0.0):
    """Simulate a delta-sigma modulator.

    Compute the output of a general delta-sigma modulator with input ``u``,
    a structure described by ``ABCD``, an initial state ``x0`` (default zero) and
    a quantizer with a number of levels specified by ``nlev``.

    **Syntax:**

     * ``[v, xn, xmax, y] = simulateDSM(u, ABCD, nlev=2, x0=0)``
     * ``[v, xn, xmax, y] = simulateDSM(u, ntf, nlev=2, x0=0)``

    **Parameters:**

    u : ndarray or sequence
        The input vector to be used in the simulation. Multiple inputs
        are implied by the number of rows in ``u``.
    arg2 : 2D ndarray or a supported LTI description
        The second argument may be either the ABCD matrix describing the
        modulator or its NTF. In the latter case, the NTF is converted to
        a ZPK description and the structure that is simulated is the
        block-diagonal structure used by scipy's ``zpk2ss()``.
        The STF is assumed to be 1.
    nlev : int or sequence or ndarray
        Number of levels in the quantizers. Set ``nlev`` to a scalar for a
        single quantizer modulator. Multiple quantizers are implied by
        making ``nlev`` an array.
    x0 : float or sequence or ndarray
        The initial status of the modulator. If ``x0`` is set to float, its
        value will be used for all the states. If it is set to a sequence of
        floats, each of its values will be assigned to a state variable.

    **Returns:**

    v : ndarray
        The quantizer output.
    xn : ndarray
        The modulator states.
    xmax : ndarray
        The maximum value that each state reached during simulation.
    y : ndarray
        The quantizer input (ie the modulator output).

    **Notes:**

    Three implementations of this function are (potentially) available to the
    user, in order of ascending execution speed:

    * A CPython implementation, always available.
    * A Cython-based implementation requiring the BLAS headers and a compatible
      compiler.
    * A Cython-based implementation accessing the BLAS library pre-compiled
      through scipy, requiring only a compatible compiler.

    The difference in execution time from the first implementation -- dynamically
    interpreted -- to the latter two -- statically compiled automatically before
    execution -- is a factor 20.

    The fastest available implementation is automatically selected.

    To assess which implementations are available in your installation, check
    the ``simulation_backends`` variable, for example::

       from __future__ import print_function
       import deltasigma as ds
       print(ds.simulation_backends)

    Example output::

        {'Scipy_BLAS': True, 'CBLAS': True, 'CPython': True}


    **Example:**

    Simulate a 5th-order binary modulator with a half-scale sine-wave input and
    plot its output in the time and frequency domains.::

        import numpy as np
        from deltasigma import *
        OSR = 32
        H = synthesizeNTF(5, OSR, 1)
        N = 8192
        fB = np.ceil(N/(2*OSR))
        f = 85
        u = 0.5*np.sin(2*np.pi*f/N*np.arange(N))
        v = simulateDSM(u, H)[0]

    Graphical display of the results:

    .. plot::

        import numpy as np
        import pylab as plt
        from numpy.fft import fft
        from deltasigma import *
        OSR = 32
        H = synthesizeNTF(5, OSR, 1)
        N = 8192
        fB = np.ceil(N/(2*OSR))
        f = 85
        u = 0.5*np.sin(2*np.pi*f/N*np.arange(N))
        v = simulateDSM(u, H)[0]
        plt.figure(figsize=(10, 7))
        plt.subplot(2, 1, 1)
        t = np.arange(85)
        # the equivalent of MATLAB 'stairs' is step in matplotlib
        plt.step(t, u[t], 'g', label='u(n)')
        plt.hold(True)
        plt.step(t, v[t], 'b', label='v(n)')
        plt.axis([0, 85, -1.2, 1.2]);
        plt.ylabel('u, v');
        plt.xlabel('sample')
        plt.legend()
        plt.subplot(2, 1, 2)
        spec = fft(v*ds_hann(N))/(N/4)
        plt.plot(np.linspace(0, 0.5, N/2 + 1), dbv(spec[:N/2 + 1]))
        plt.axis([0, 0.5, -120, 0])
        plt.grid(True)
        plt.ylabel('dBFS/NBW')
        snr = calculateSNR(spec[:fB], f)
        s = 'SNR = %4.1fdB' % snr
        plt.text(0.25, -90, s)
        s =  'NBW = %7.5f' % (1.5/N)
        plt.text(0.25, -110, s)
        plt.xlabel("frequency $1 \\\\rightarrow f_s$")

    Click on "Source" above to see the source code.
    """
    return _simulateDSM_python(u, arg2, nlev, x0)
