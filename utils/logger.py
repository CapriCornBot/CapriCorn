def register_logger(log_file_name, bot_name):
    """
    This function registers a logger to the program.
    :param log_file_name: The name of the log file.
    :return: The logger.
    """
    import logging
    import os
    import sys
    from colorama import init, Fore

    init(autoreset=True)
    cw = Fore.WHITE
    cc = Fore.BLUE

    logger = logging.getLogger(bot_name)
    logger.setLevel(logging.DEBUG)

    # Create a file handler
    log_file_path = os.path.join(os.path.dirname(sys.argv[0]), log_file_name)
    handler = logging.FileHandler(log_file_path, encoding="utf-8", mode="w")
    handler.setLevel(logging.DEBUG)

    # Create a logging format
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")

    handler.setFormatter(formatter)

    # add stream logger
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(
        logging.Formatter(
            f"{cw}[{cc}%(asctime)s{cw}] [{cc}%(levelname)s{cw}] %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )
    )

    # Add the handlers to the logger
    logger.addHandler(stream_handler)
    logger.addHandler(handler)
    return logger