import logger_main
import global_config
import json_utils
#from GuiApp import QtApp
import sys
import range_quiz_main

if __name__ == "__main__":
    try:
        logger = logger_main.MainLogger().logger
        const = global_config.Const()
        configJson = json_utils.get_json_dict(logger, const.GlobalConfigPath)
        config = global_config.Config(**configJson)
        logger.setLevel(config.LogLevel)
        #ui = QtApp.QtApp(logger, const, config)
        range_quiz_main.main(logger, const, config)

    except Exception as e:
        logger.exception(e)
    finally:
        logger.debug("Finally kill")
        sys.exit(1)