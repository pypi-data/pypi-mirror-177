import logging
from typing import Any, TypedDict

from powerflex_monitoring.server_base import ServerBase

logger = logging.getLogger(__name__)


class ReadyCheckResponse(TypedDict):
    ready: bool
    cause: str


class ReadyCheck(ServerBase):
    def __init__(
        self,
        initial_state: bool = False,
        initial_cause: str = "Service is initializing",
    ) -> None:
        self._is_ready = initial_state
        self._cause = initial_cause
        self.supervisor_ready_check: dict[str, dict[str, Any]] = {}

    @property
    def _status(self) -> int:
        return 200 if self._is_ready else 503

    @property
    def _response(self) -> ReadyCheckResponse:
        return {"ready": self._is_ready, "cause": self._cause}

    @property
    def is_ready(self) -> bool:
        return self._is_ready

    def set_ready(
        self, ready: bool, readiness_identifier: str = "default", cause: str = "Unknown"
    ) -> None:
        if (
            self.supervisor_ready_check.get(readiness_identifier) is not None
            and self.supervisor_ready_check[readiness_identifier]["ready"] == ready
        ):
            return

        self.supervisor_ready_check[readiness_identifier] = {
            "ready": ready,
            "cause": cause,
        }
        log_level = logging.INFO if ready else logging.WARNING
        logger.log(
            log_level,
            "Readiness Identifier %s notifies the service as %s due to %s",
            readiness_identifier,
            "ready" if ready else "not ready",
            cause,
            stack_info=True,
        )
        self._cause = ""
        causes: dict[str, Any] = {"not ready": {}, "ready": {}}
        for key, value in self.supervisor_ready_check.items():
            if not value["ready"]:
                causes["not ready"][key] = value["cause"]
                self._is_ready = False
                if self._cause == "":
                    self._cause = value["cause"]
                    continue
                self._cause = self._cause + " - " + value["cause"]
                continue
            causes["ready"][key] = value["cause"]
        if len(causes["not ready"]) > 0:
            logger.log(
                logging.WARNING,
                "Service has been marked as not ready.",
                stack_info=True,
                extra=causes["not ready"],
            )
            return
        self._is_ready = True
        # Only the last reason that made the service complete "ready" is reported.
        self._cause = cause
        logger.log(
            logging.INFO,
            "Service has been marked as ready.",
            stack_info=True,
            extra=causes["ready"],
        )
