from dataclasses import dataclass
from px_settings.contrib.django import settings as s


__all__ = 'Settings', 'settings',


@s('pxd_massaffect')
@dataclass
class Settings:
    pass


settings = Settings()
