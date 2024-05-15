import logging


def setup_logger(name, is_ch=True):
    """
    功能：设置logger记录器
    参数1：log名
    """
    formatter = logging.Formatter('%(asctime).19s [%(levelname)s] %(message)s')
    logger = logging.getLogger(str(name))
    logger.setLevel(logging.INFO)
    if is_ch:
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    fh = logging.FileHandler(f"{name}_log.log")
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger
