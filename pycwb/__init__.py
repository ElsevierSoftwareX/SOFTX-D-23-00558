from ._version import version, __version__, version_tuple, __version_tuple__

import ROOT
from pycwb.utils.check_ROOT import check_and_load_wavelet

# load wavelet library if not loaded
check_and_load_wavelet(ROOT)
