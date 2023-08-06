from django.apps import AppConfig
from django.utils.translation import pgettext_lazy

from .const import APP_LABEL


__all__ = ('MassAffectConfig',)


class MassAffectConfig(AppConfig):
    name = 'pxd_massaffect'
    label = APP_LABEL
    verbose_name = pgettext_lazy('pxd_massaffect', 'MassAffect')
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self) -> None:
        super().ready()

        self.module.autodiscover()
