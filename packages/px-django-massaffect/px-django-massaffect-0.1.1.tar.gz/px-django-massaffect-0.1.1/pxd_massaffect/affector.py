from functools import cached_property, reduce
from collections import OrderedDict
import operator
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, TypeVar, Union
from django.db import models

from px_formula import Formula

from .models import GenericConfig
from .registry import AffectRegistry, FieldGeneratorMixin


__all__ = (
    'and_resolver', 'or_resolver', 'make_formula_resolver',
    'Affector', 'ParentsAffector',
)

Q = TypeVar('Q', bound=models.QuerySet)
T = TypeVar('T')
M = TypeVar('M', bound=models.Model)
Variables = Dict[str, Union[models.F, Any]]


def and_resolver(variables: Variables):
    return reduce(operator.and_, variables.values()) if variables else None


def or_resolver(variables: Variables):
    return reduce(operator.or_, variables.values()) if variables else None


def make_formula_resolver(
    formula: Formula,
    expression: str,
    fallback: Callable[[Variables], Any] = and_resolver,
    merge: Callable = operator.and_,
):
    if not expression:
        return fallback

    parsed = formula.parse(expression)
    searchable = set(parsed)

    def resolver(variables: Variables):
        diff = variables.keys() - searchable
        result = formula.evaluate(parsed, variables)

        if len(diff) == 0:
            return result

        return merge(result, fallback({k: variables[k] for k in diff}))

    return resolver


class Affector(FieldGeneratorMixin):
    registry: AffectRegistry

    def __init__(self, registry: AffectRegistry):
        self.registry = registry

    def affect_queryset(
        self,
        configs: Sequence[GenericConfig],
        queryset: Q,
        resolver: Callable[[Variables], Any] = and_resolver,
        kwargs = {},
    ) -> Tuple[Q, str]:
        result: Variables = {}
        registry = self.registry
        field_name = self.make_unique_name()
        model = queryset.model

        for config in configs:
            config_model = config.__class__
            descriptor = registry.get_for_model(config_model)

            if (
                descriptor is not None
                and
                descriptor.adapter.can_affect(model)
            ):
                queryset, field = descriptor.adapter.affect_queryset(
                    config, queryset, kwargs=kwargs
                )
                result[config.variable_name] = models.ExpressionWrapper(
                    models.F(field), output_field=models.BooleanField(),
                )

        return (
            queryset.annotate(**{
                field_name: resolver(result) if result else models.Value(False),
            }),
            field_name,
        )

    def affect_items(
        self,
        configs: Sequence[GenericConfig],
        items: Sequence[T],
        resolver: Callable[[Variables], Any] = and_resolver,
        kwargs = {},
    ) -> List[Tuple[T, Any]]:
        registry = self.registry
        result: Dict[int, Variables] = {x: {} for x in range(len(items))}
        items = list(items)

        for config in configs:
            config_model = config.__class__
            descriptor = registry.get_for_model(config_model)

            if descriptor is None:
                continue

            affectable = OrderedDict(
                (i, item) for i, item in enumerate(items)
                if descriptor.adapter.can_affect(item.__class__)
            )

            if len(affectable) == 0:
                continue

            indexes = list(affectable.keys())
            temp = descriptor.adapter.affect_items(
                config, affectable.values(), kwargs=kwargs,
            )
            variable_name = config.variable_name

            for i, (item, value) in enumerate(temp):
                index = indexes[i]
                result[index][variable_name] = value
                items[index] = item

        return [(item, resolver(result[i])) for i, item in enumerate(items)]


class ParentsAffector:
    parents: Sequence[M]
    config_queryset: models.QuerySet = None
    related_name: str = 'affect_configs'
    affector: Affector = None

    def __init__(
        self,
        parents: Sequence[M],
        config_queryset: models.QuerySet = None,
        related_name: Optional[str] = None,
        affector: Optional[Affector] = None,
        get_parent_resolver: Optional[Callable[[M], Callable[[Variables], Any]]] = None,
    ):
        assert len(parents) > 0, 'There must be at leas one parent passed'

        self.affector = self.affector if affector is None else affector
        self.config_queryset = self.config_queryset if config_queryset is None else config_queryset
        self.related_name = self.related_name if related_name is None else related_name

        for value, name in (
            (self.affector, 'Affector'),
            (self.related_name, 'Related name'),
        ):
            assert value is not None, (
                f'{name} must be either declared as class property or passed on '
                'initialization.'
            )

        self.parents = parents

        if self.config_queryset is None:
            field = getattr(parents[0].__class__, self.related_name)
            self.config_queryset = field.rel.related_model.objects.all()

        if get_parent_resolver is not None:
            self.get_parent_resolver = get_parent_resolver

    def get_parent_resolver(self, parent: M) -> Callable[[Variables], Any]:
        return and_resolver

    @cached_property
    def parent_configs(self) -> Dict[M, List[GenericConfig]]:
        queryset = self.config_queryset

        if callable(queryset):
            queryset = queryset()

        configs = queryset.filter(parent__in=self.parents)
        result = OrderedDict((parent, []) for parent in self.parents)
        parents_map = {x.pk: x for x in self.parents}

        for config in configs:
            parent = parents_map[config.parent_id]
            result[parent].append(config)

        return result

    def affect_queryset(
        self,
        queryset: Q,
        get_parent_resolver: Optional[Callable[[M], Callable[[Variables], Any]]] = None,
        kwargs = {},
    ) -> Tuple[Q, Dict[M, str]]:
        parent_configs = self.parent_configs
        affector = self.affector
        results = {}
        get_parent_resolver = (
            self.get_parent_resolver
            if get_parent_resolver is None else
            get_parent_resolver
        )

        for parent, configs in parent_configs.items():
            queryset, field_name = affector.affect_queryset(
                configs, queryset, resolver=get_parent_resolver(parent),
                kwargs=kwargs,
            )
            results[parent] = field_name

        return queryset, results

    def affect_items(
        self,
        items: Sequence[T],
        get_parent_resolver: Optional[Callable[[M], Callable[[Variables], Any]]] = None,
        kwargs = {},
    ) -> List[Tuple[T, Dict[M, Any]]]:
        parent_configs = self.parent_configs
        affector = self.affector
        results = [[x, {}] for x in items]
        get_parent_resolver = (
            self.get_parent_resolver
            if get_parent_resolver is None else
            get_parent_resolver
        )

        for parent, configs in parent_configs.items():
            temp = affector.affect_items(
                configs, items, resolver=get_parent_resolver(parent),
                kwargs=kwargs,
            )
            for i, (item, value) in enumerate(temp):
                results[i][0] = item
                results[i][1][parent] = value

        return results
