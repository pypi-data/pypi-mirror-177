from typing import Any, List, Optional, Sequence, Tuple, Type, TypeVar
from django.db import models

from .admin import AffectConfigInline, make_inline
from .utils.registry import Adapter, Descriptor, DescriptorRegistry
from .utils import make_unique_label, get_model_content_type_key


Q = TypeVar('Q')
T = TypeVar('T')


class FieldGeneratorMixin:
    field_prefix: str = 'affected_'

    def make_unique_name(self, prefix: Optional[str] = None):
        prefix = prefix if prefix is not None else self.field_prefix

        return prefix + make_unique_label(8)


class AffectAdapter(FieldGeneratorMixin, Adapter):
    affected_models: Sequence[Type[models.Model]]

    def __init__(self, affected_models: Sequence[Type[models.Model]]):
        self.affected_models = affected_models

    def can_affect(self, model: Type[models.Model]):
        return model in self.affected_models

    def affect_Q(self, config: models.Model, **kwargs) -> models.Q:
        raise NotImplementedError()

    def affect_queryset(
        self,
        config: models.Model,
        queryset: Q,
        kwargs = {},
    ) -> Tuple[Q, str]:
        field_name = self.make_unique_name()
        q = self.affect_Q(config, **kwargs)
        sub_q = models.Exists(queryset.filter(q).filter(pk=models.OuterRef('pk')))

        return queryset.annotate(**{field_name: q}), field_name

    def affect_item(self, config: models.Model, item: T, kwargs = {}) -> Any:
        raise NotImplementedError()

    def affect_items(
        self,
        config: models.Model,
        items: Sequence[T],
        kwargs = {},
    ) -> List[Tuple[T, Any]]:
        return [
            (item, self.affect_item(config, item, kwargs=kwargs))
            for item in items
        ]


class AffectDescriptor(Descriptor):
    model: Type[models.Model]
    adapter: AffectAdapter
    admin_inline: Type[AffectConfigInline]

    _make_inline = staticmethod(make_inline)

    def __init__(
        self,
        model: Type[models.Model],
        adapter: AffectAdapter,
        verbose_name: Optional[str] = None,
        admin_inline: Optional[Type[AffectConfigInline]] = None,
    ):
        self.model = model
        self.admin_inline = (
            admin_inline if admin_inline is not None else self._make_inline(model)
        )
        opts = model._meta

        super().__init__(
            get_model_content_type_key(model),
            adapter=adapter,
            verbose_name=(
                verbose_name if verbose_name is not None else
                opts.verbose_name
            )
        )


class AffectRegistry(DescriptorRegistry):
    def get_for_model(self, model: models.Model, dflt=None) -> Optional[AffectDescriptor]:
        return self.get(get_model_content_type_key(model), dflt)
