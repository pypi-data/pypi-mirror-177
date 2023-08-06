#!/usr/bin/env python3

""" Command Line Interface for DataSafe """

import sys
import logging
import argparse
from timeit import default_timer as timer
from ._utils import _encrypt_cli, _decrypt_cli
from ._version import __version__


def parseArgs() -> argparse.Namespace:
    epilog = 'Stephen Richer, (stephen.richer@proton.me)'
    baseParser = getBaseParser(__version__)
    parser = argparse.ArgumentParser(
        epilog=epilog, description=__doc__, parents=[baseParser])
    subparser = parser.add_subparsers(
        title='required commands',
        description='',
        dest='command',
        metavar='Commands',
        help='Description:')

    sp1 = subparser.add_parser(
        'encrypt',
        description=_encrypt_cli.__doc__,
        help='Encrypt a file with password.',
        parents=[baseParser],
        epilog=parser.epilog)
    sp1.add_argument('file', nargs='?', help='File to encrypt.')
    sp1.set_defaults(function=_encrypt_cli)

    sp2 = subparser.add_parser(
        'decrypt',
        description=_decrypt_cli.__doc__,
        help='Decrypt a file with password.',
        parents=[baseParser],
        epilog=parser.epilog)
    sp2.add_argument('file', help='File to decrypt.')
    sp2.set_defaults(function=_decrypt_cli)

    args = parser.parse_args()
    if 'function' not in args:
        parser.print_help()
        sys.exit()

    rc = executeCommand(args)
    return rc


def executeCommand(args):
    # Initialise logging
    logFormat = '%(asctime)s - %(levelname)s - %(funcName)s - %(message)s'
    logging.basicConfig(level=args.verbose, format=logFormat)
    del args.verbose, args.command
    # Pop main function and excute script
    function = args.__dict__.pop('function')
    start = timer()
    rc = function(**vars(args))
    end = timer()
    logging.info(f'Total execution time: {end - start:.3f} seconds.')
    logging.shutdown()
    return rc


def getBaseParser(version: str) -> argparse.Namespace:
    """ Create base parser of verbose/version. """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        '--version', action='version', version='%(prog)s {}'.format(version))
    parser.add_argument(
        '--verbose', action='store_const', const=logging.DEBUG,
        default=logging.ERROR, help='verbose logging for debugging')
    return parser
