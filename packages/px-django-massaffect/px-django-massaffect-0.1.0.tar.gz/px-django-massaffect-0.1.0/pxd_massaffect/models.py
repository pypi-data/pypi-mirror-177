from typing import Union, Optional, Type, TypeVar
from django.db import models
from django.utils.translation import pgettext_lazy
from polymorphic.models import PolymorphicModel


__all__ = (
    'GenericConfig',
    'make_formula_field',
    'make_config_base',
)

T = TypeVar('T')


class GenericConfig(PolymorphicModel):
    variable_prefix = 'affect'

    class Meta:
        abstract = True
        verbose_name = pgettext_lazy('pxd_massaffect', 'Config')
        verbose_name_plural = pgettext_lazy('pxd_massaffect', 'Configs')
        ordering = ('-ordering_field', '-pk',)

    parent = models.ForeignKey(
        'content_type.ContentType', on_delete=models.CASCADE
    )
    ordering_field = models.BigIntegerField(
        verbose_name=pgettext_lazy('pxd_massaffect', 'Ordering value'),
        db_index=True, default=0,
    )

    @property
    def variable_name(self):
        return self.variable_prefix + str(self.pk)

    def __str__(self):
        return self.variable_name


def make_formula_field(**kwargs) -> models.TextField:
    return models.TextField(
        verbose_name=pgettext_lazy('pxd_massaffect', 'Formula'),
        blank=True, null=False, **kwargs,
    )


def make_config_base(
    name: str,
    parent: Union[str, Type[models.Model]],
    /,
    base: T = GenericConfig,
    related_name: str = 'affect_configs',
    app_label: Optional[str] = None,
    **kwargs
) -> T:
    return type(name.title() + base.__name__, (base,), {
        '__module__': __name__, '__doc__': base.__doc__,
        'Meta': type('Meta', (base.Meta,), {
            'abstract': True,
            'app_label': app_label,
            'verbose_name': base._meta.verbose_name,
            'verbose_name_plural': base._meta.verbose_name_plural,
        }),
        'parent': models.ForeignKey(
            parent,
            verbose_name=pgettext_lazy('pxd_massaffect', 'Parent'),
            related_name=related_name,
            on_delete=models.CASCADE, null=False, blank=False,
            **kwargs,
        )
    })
