import pyautogui as pag


def sleep(logger, seconds):
    try:
        pag.sleep(seconds)
    except Exception:
        logger.exception("Failed to sleep for {} seconds".format(seconds))


def advanced_sleep(logger, seconds):
    while seconds > 0:
        pag.sleep(1)
        seconds -= 1