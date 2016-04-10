"""
Logging
=======
"""
import logging

import colorlog

# Default logger conf
BOUSSOLE_LOGGER_CONF = (
    ('DEBUG', 'cyan'),
    ('INFO', 'green'),
    ('WARNING', 'yellow'),
    ('ERROR', 'red'),
)


def init_logger(level, printout=True):
    """
    Initialize app logger to configure its level/handler/formatter/etc..

    Todo:
        * Colors using "python-colorlog";
        * We need a "notice" level higher than ERROR (so it's allways
          displayed);
        * A mean to raise click.Abort when ERROR is used;

    Args:
        level (str): Level name (``debug``, ``info``, etc..).

    Keyword Arguments:
        printout (bool): If False, logs will never be outputed.

    Returns:
        logging.Logger: Application logger.
    """
    root_logger = logging.getLogger("boussole")
    root_logger.setLevel(level)

    # Redirect outputs to the void space, mostly for usage within unittests
    if not printout:
        from StringIO import StringIO
        dummystream = StringIO()
        handler = logging.StreamHandler(dummystream)
    # Standard output with colored messages
    else:
        handler = logging.StreamHandler()
        handler.setFormatter(
            colorlog.ColoredFormatter(
                '%(asctime)s - %(log_color)s%(message)s',
                datefmt="%H:%M:%S"
            )
        )

    root_logger.addHandler(handler)

    return root_logger
