# License: BSD 3 clause

# Copyright (c) 2021, Stefan Güttel, Xinye Chen
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
cimport cython
import numpy as np
cimport numpy as np 
np.import_array()

# @cython.boundscheck(False)
# @cython.wraparound(False)
# @cython.binding(True)

def compress(np.ndarray[np.float64_t, ndim=1] ts, double tol=0.5, int max_len=-1):
    """
    Approximate a time series using a continuous piecewise linear function.

    Parameters
    ----------
    ts - numpy ndarray
        Time series as input of numpy array

    Returns
    -------
    pieces - numpy array
        Numpy ndarray with three columns, each row contains length, increment, error for the segment.
    """
    if max_len < 0:
        max_len = len(ts)
        
    cdef int start = 0
    cdef int end = 1
    cdef int i, len_t = len(ts)
    cdef list pieces = list() # np.empty([0, 3])
    cdef np.ndarray[np.float64_t, ndim=1] x = np.arange(0, len_t, dtype=float)
    cdef double epsilon =  np.finfo(float).eps
    
    cdef double t_st, t_ed
    cdef double inc, lastinc, err, lasterr
    
    while end < len_t:

        t_st = ts[start]
        t_ed = ts[end]
        inc = t_ed - t_st
        err = 0.0
        
        for i in range(end-start+1):
            err = err + (t_st + (inc/(end-start))*x[0:end-start+1][i] - ts[start:end+1][i])**2
        
        if (err <= tol*(end-start-1) + epsilon) and (end-start-1 < max_len):
            (lastinc, lasterr) = (inc, err) 
            end = end + 1
        else:
            # pieces = np.vstack([pieces, np.array([end-start-1, lastinc, lasterr])])
            pieces.append([end-start-1, lastinc, lasterr])
            start = end - 1

    # pieces = np.vstack([pieces, np.array([end-start-1, lastinc, lasterr])])
    pieces.append([end-start-1, lastinc, lasterr])

    return pieces
