import json
import datetime


def get_json_dict(logger, path):
    try:
        with open(path) as f:
            data = json.load(f)
            logger.debug("Done loading json dict path:{}, data:{}".format(data, path))
            return data
    except Exception:
        logger.exception("Unable to load json dict {}".format(path))
        return None


def converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def write_to_json(data, path):
    try:
        with open(path, "w") as f:
            json.dump(data, f, default=converter)
            # TODO logger currently not working
            # logger.debug("Agent saved in path:{}, data:{}".format(path,data))
    except Exception as e:
        pass
        # logger.debug("Unable to save agent to json dict {}".format(path))