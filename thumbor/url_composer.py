#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

import sys
import optparse

from thumbor import __version__
from libthumbor import CryptoURL
from thumbor.config import Config


def main(arguments=None):  # NOQA
    '''Converts a given url with the specified arguments.'''
    if arguments is None:
        arguments = sys.argv[1:]

    parser = optparse.OptionParser(
        usage='thumbor-url [options] imageurl or type thumbor-url -h (--help) for help',
        description=__doc__,
        version=__version__
    )

    parser.add_option(
        '-l', '--key_file', dest='key_file', default=None, help='The file to read the security key from [default: %default].'
    )
    parser.add_option(
        '-k', '--key', dest='key', default=None, help='The security key to encrypt the url with [default: %default].'
    )
    parser.add_option(
        '-w', '--width', dest='width', type='int', default=0, help='The target width for the image [default: %default].'
    )
    parser.add_option(
        '-e', '--height', dest='height', type='int', default=0, help='The target height for the image [default: %default].'
    )
    parser.add_option(
        '-n', '--fitin', dest='fitin', action='store_true', default=False,
        help='Indicates that fit-in resizing should be performed.'
    )
    parser.add_option(
        '-m', '--meta', dest='meta', action='store_true', default=False,
        help='Indicates that meta information should be retrieved.'
    )
    parser.add_option(
        '', '--adaptive', action='store_true', dest='adaptive', default=False,
        help='Indicates that adaptive fit-in cropping should be used.'
    )
    parser.add_option(
        '', '--full', action='store_true', dest='full', default=False, help='Indicates that fit-full cropping should be used.'
    )
    parser.add_option(
        '-s', '--smart', action='store_true', dest='smart', default=False, help='Indicates that smart cropping should be used.'
    )
    parser.add_option(
        '-t', '--trim', action='store_true', default=False, help='Indicate that surrounding whitespace should be trimmed.'
    )
    parser.add_option(
        '-f', '--horizontal-flip', action='store_true', dest='horizontal_flip', default=False,
        help='Indicates that the image should be horizontally flipped.'
    )
    parser.add_option(
        '-v', '--vertical-flip', action='store_true', dest='vertical_flip', default=False,
        help='Indicates that the image should be vertically flipped.'
    )
    parser.add_option(
        '-a', '--halign', dest='halign', default='center',
        help='The horizontal alignment to use for cropping [default: %default].'
    )
    parser.add_option(
        '-i', '--valign', dest='valign', default='middle',
        help='The vertical alignment to use for cropping [default: %default].'
    )
    parser.add_option(
        '', '--filters', dest='filters', action='append',
        help='Filters to be applied to the image, e.g. brightness(10).'
    )
    parser.add_option(
        '-o', '--old-format', dest='old', action='store_true', default=False,
        help='Indicates that thumbor should generate old-format urls [default: %default].'
    )

    parser.add_option(
        '-c', '--crop', dest='crop', default=None,
        help='The coordinates of the points to manual cropping in the format leftxtop:rightxbottom '
        '(100x200:400x500) [default: %default].'
    )

    (parsed_options, arguments) = parser.parse_args(arguments)

    if not arguments:
        print 'Error: The image argument is mandatory. For more information type thumbor-url -h'
        return

    image_url = arguments[0]
    if image_url.startswith('/'):
        image_url = image_url[1:]

    try:
        config = Config.load(None)
    except:
        config = None

    if not parsed_options.key and not config:
        print 'Error: The -k or --key argument is mandatory. For more information type thumbor-url -h'
        return

    if parsed_options.key_file:
        f = open(parsed_options.key_file)
        security_key = f.read().strip()
        f.close()
    else:
        security_key = config.SECURITY_KEY if not parsed_options.key else parsed_options.key

    crop_left = crop_top = crop_right = crop_bottom = 0
    if parsed_options.crop:
        crops = parsed_options.crop.split(':')
        crop_left, crop_top = crops[0].split('x')
        crop_right, crop_bottom = crops[1].split('x')

    options = {
        'old': parsed_options.old,
        'width': parsed_options.width,
        'height': parsed_options.height,
        'smart': parsed_options.smart,
        'meta': parsed_options.meta,
        'horizontal_flip': parsed_options.horizontal_flip,
        'vertical_flip': parsed_options.vertical_flip,
        'halign': parsed_options.halign,
        'valign': parsed_options.valign,
        'trim': parsed_options.trim,
        'crop_left': crop_left,
        'crop_top': crop_top,
        'crop_right': crop_right,
        'crop_bottom': crop_bottom,
        'filters': parsed_options.filters,
        'image_url': image_url,
    }

    if parsed_options.fitin and parsed_options.full and parsed_options.adaptive:
        options['adaptive_full_fit_in'] = True
    elif parsed_options.fitin and parsed_options.full:
        options['full_fit_in'] = True
    elif parsed_options.fitin and parsed_options.adaptive:
        options['adaptive_fit_in'] = True
    elif parsed_options.fitin:
        options['fit_in'] = True

    crypto = CryptoURL(key=security_key)
    url = crypto.generate(**options)
    print 'URL:'

    print url
    return url

if __name__ == '__main__':
    main(sys.argv[1:])
