#!/usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2022-present Ramiro Gómez <code@ramiro.org>
# SPDX-License-Identifier: MIT
import argparse
import sys
import timeit

import pega

from pathlib import Path


image_formats = ('jpg', 'png', 'webp')


def main():
    start_time = timeit.default_timer()
    parser = argparse.ArgumentParser(description='Paste images on top of other images.')
    parser.add_argument('base', type=argparse.FileType('rb'), default=sys.stdin,
                        help='Base image file name.')
    parser.add_argument('paste', type=str, nargs='+',
                        help='Image to paste on base image. Use wildcard to process multiple files.')
    parser.add_argument('--margins', '-m', type=int, nargs=4, default=[0, 0, 0, 0], metavar=('TOP', 'RIGHT', 'BOTTOM', 'LEFT'),
                        help='Top, right, bottom, and left (mnemonic: trouble) margins of pasted image relative to base image.')
    parser.add_argument('--output-dir', '-o', type=Path, default='.', help='Write result image to directory.')
    parser.add_argument('--output-format', '-f', type=str, choices=image_formats,
                        help='Output image format. If not specified the format is determined from the pasted image.')
    parser.add_argument('--verbose', '-v', action='store_true', help='Turn on verbose output.')
    argv = parser.parse_args()

    im_base = pega.load(argv.base).convert('RGBA')

    for file_name in argv.paste:
        # Create a base image copy for each image to paste.
        im_new = im_base.copy()

        # Fit pasted image into calculated dimensions, while preserving its aspect ratio.
        dim = pega.dimensions(im_base, argv.margins)
        im_paste = pega.load(file_name)

        # Determine output format before any image manipulations
        format = argv.output_format if argv.output_format else im_paste.format.lower()

        # Resize and fit pasted image
        im_paste.thumbnail(dim)
        im_paste = pega.fit(im_paste, dim)

        argv.output_dir.mkdir(exist_ok=True)

        # Use `alpha_composite` because `paste` would keep transparency in pasted image.
        im_new.alpha_composite(im_paste, dest=(argv.margins[3], argv.margins[0]))

        if format in ('jpg', 'jpeg'):
            im_new = im_new.convert('RGB')
        im_new.save(argv.output_dir.joinpath(f'{Path(file_name).stem}.{format}'))

    argv.verbose and print(f'Script runtime: {timeit.default_timer() - start_time:.3f} sec', )


if __name__ == '__main__':
    main()
