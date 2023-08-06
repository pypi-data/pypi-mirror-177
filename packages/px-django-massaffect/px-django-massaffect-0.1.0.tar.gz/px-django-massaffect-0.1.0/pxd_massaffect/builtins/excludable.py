from django.utils.translation import pgettext_lazy
from django.db import models


class ExcludableConfig(models.Model):
    class Meta:
        abstract = True

    exclude = models.BooleanField(
        verbose_name=pgettext_lazy('pxd_massaffect', 'Exclude'),
        default=False, null=False,
    )


class ExcludableAdapterMixin:
    def exclude_Q(self, config: ExcludableConfig, q: models.Q) -> models.Q:
        return ~q if config.exclude else q
