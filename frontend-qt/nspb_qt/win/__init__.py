"""The Windows build path: everything the Qt front end needs to produce an IPA on a PC.

This package is imported **only on Windows** (see `nspb_qt.model`). On macOS it is never
touched, so a Mac build behaves exactly as before; importing it here is still safe, because
no module in it runs a subprocess or reads a Windows-only path at import time.

The upstream pipeline (`scripts/build_ipa_from_nsp.py`) is not modified: `driver.py` loads it
as a module and replaces the functions that assume a Mac. `shim/` covers the calls that cross
process boundaries, where a function replacement cannot reach.
"""
from __future__ import annotations

import os

#: DM_IOS_M3 opts into iOS 18 and classic Metal. The default remains iOS 26 / Metal 4.
IOS_DEPLOYMENT = '18.0' if os.environ.get('DM_IOS_M3') == '1' else '26.0'

#: The classic path uses the reference's A14 baseline, including the iPhone 13's A15.
IOS_CPU = 'apple-a14' if os.environ.get('DM_IOS_M3') == '1' else 'apple-a16'

#: Environment variable names this package sets for the build. They all carry the `NSPB_`
#: prefix so they cannot collide with the upstream script's own vocabulary.
ENV_TOOLCHAIN = 'NSPB_TOOLCHAIN_JSON'
ENV_LLVM = 'NSPB_LLVM_DIR'
ENV_SDK = 'NSPB_IOS_SDK'
ENV_METAL = 'NSPB_METAL_DIR'
ENV_PREFIX = 'NSPB_PREFIX'
