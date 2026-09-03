import asyncio
import logging
from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum

from media_record.infrastructure.consumer.consumer import MediaRecordConsumer
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

PROBE_TIMEOUT_SECONDS = 2.0


class ComponentStatus(StrEnum):
    UP = "up"
    DOWN = "down"


@dataclass(frozen=True, slots=True)
class ComponentHealth:
    name: str
    status: ComponentStatus
    error: str | None = None


class HealthCheck(ABC):
    """Readiness probe for a single downstream component."""

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    async def _probe(self) -> None:
        """Return normally when the component is reachable, raise otherwise."""
        raise NotImplementedError

    async def check(self) -> ComponentHealth:
        try:
            async with asyncio.timeout(PROBE_TIMEOUT_SECONDS):
                await self._probe()
        except Exception as exc:
            logger.warning("Health probe %s failed", self.name, exc_info=exc)
            # Only the exception type is reported: the probe is unauthenticated
            # and driver messages can carry hosts, users and other internals.
            return ComponentHealth(
                name=self.name,
                status=ComponentStatus.DOWN,
                error=type(exc).__name__,
            )
        return ComponentHealth(name=self.name, status=ComponentStatus.UP)


class DatabaseHealthCheck(HealthCheck):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @property
    def name(self) -> str:
        return "database"

    async def _probe(self) -> None:
        await self._session.execute(text("SELECT 1"))


class BrokerHealthCheck(HealthCheck):
    def __init__(self, consumer: MediaRecordConsumer) -> None:
        self._consumer = consumer

    @property
    def name(self) -> str:
        return "broker"

    async def _probe(self) -> None:
        await self._consumer.ping_broker()


class ResultBackendHealthCheck(HealthCheck):
    def __init__(self, consumer: MediaRecordConsumer) -> None:
        self._consumer = consumer

    @property
    def name(self) -> str:
        return "result_backend"

    async def _probe(self) -> None:
        await self._consumer.ping_result_backend()


async def check_all(checks: Sequence[HealthCheck]) -> list[ComponentHealth]:
    """Run every probe concurrently. `check` never raises, so neither does this."""
    return list(await asyncio.gather(*(check.check() for check in checks)))
