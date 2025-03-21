from enum import Enum

from pydantic import BaseModel


class AppStatus(Enum):
    HEALTHY = 0
    BOOT = 1
    SHUTDOWN = 2
    UNHEALTHY = 3


class HealthCheck(BaseModel):
    status: AppStatus = AppStatus.HEALTHY
