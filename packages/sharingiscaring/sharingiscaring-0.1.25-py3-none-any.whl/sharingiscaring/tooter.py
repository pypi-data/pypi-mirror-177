from apprise import Apprise
from enum import Enum

class TooterType(Enum):
    INFO = "info"
    GRAPHQL_ERROR = "graphql error"
    REQUESTS_ERROR = "requests error"
    BOT_MAIN_LOOP_ERROR = "bot_main_loop_error"
    


class Tooter:
    def __init__(self, appriser: Apprise , environment: str, branch: str) -> None:
        self.appriser     = appriser
        self.environment  = environment
        self.branch        = branch

    def send(self, message: str, notifier_type: TooterType, value=None, error=None):
        title   = f"t: {notifier_type.value} | e: {self.environment} | b: {self.branch}"
        body    = message
        if value:
            body += '| value: {value} '
        if error:
            body += '| error: {error}.' 

        self.appriser.notify(title=title, body=body)