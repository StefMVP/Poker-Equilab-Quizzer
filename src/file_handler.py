def open_file(logger, path):
    try:
        f = open(path, "r")
        logger.debug("Opened file from path {}".format(path))
        return f.read()
    except Exception:
        logger.debug("Unable to open file from path {}".format(path))
        return None