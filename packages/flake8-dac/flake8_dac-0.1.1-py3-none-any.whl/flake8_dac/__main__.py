from __future__ import annotations

import os
import sys

from flake8_dac import formatting

is_pipe = not os.isatty(sys.stdin.fileno())
if not is_pipe:
    print("Usage: flake8 [args] | flake8-dac")
    raise SystemExit(1)

groupped = formatting.group(sys.stdin.readlines())
formatting.dac_print(groupped)
raise SystemExit(0)
