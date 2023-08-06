#!/bin/bash
set -euo pipefail

pega/cli.py -f jpg tests/images/base-1000x1000-m100-0-200-0-transparent.png tests/images/*.jpg -o tests/output/
pega/cli.py -f png tests/images/base-1000x1000-m100-0-200-0-transparent.png tests/images/*.jpg -o tests/output/
pega/cli.py -f webp tests/images/base-1000x1000-m100-0-200-0-transparent.png tests/images/*.jpg -o tests/output/