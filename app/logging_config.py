import json
import logging
from datetime import datetime, UTC

from app.logging_context import get_request_id


class JsonFormatter(logging.Formatter):

    def format(
        self,
        record: logging.LogRecord,
    ) -> str:

        log = {
            "timestamp": datetime.now(
                UTC
            ).isoformat(),

            "level": record.levelname,

            "logger": record.name,

            "message": record.getMessage(),

            "request_id": get_request_id(),
        }

        if record.exc_info:
            log["exception"] = self.formatException(
                record.exc_info
            )

        return json.dumps(log)


def configure_logging():

    handler = logging.StreamHandler()

    handler.setFormatter(
        JsonFormatter()
    )

    root = logging.getLogger()

    root.handlers.clear()

    root.addHandler(handler)

    root.setLevel(logging.INFO)