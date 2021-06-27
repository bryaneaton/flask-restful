#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

import logging
from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install
import os
install()


def create_logger():
    """Create a logger for use in all cases."""
    loglevel = os.environ.get('LOGLEVEL', 'INFO').upper()
    rich_handler = RichHandler(rich_tracebacks=True, markup=True)
    logging.basicConfig(level=loglevel, format='%(message)s',
                        datefmt="[%Y/%m/%d %H:%M;%S]",
                        handlers=[rich_handler])
    return logging.getLogger('rich')
