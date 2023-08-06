from typing import Type, TYPE_CHECKING
import nested_admin

from django.db import models

if TYPE_CHECKING:
    from .registry import AffectRegistry


__all__ = 'AffectConfigSetInline', 'AffectConfigInline', 'make_inline'


class AffectConfigSetInline(
    nested_admin.SortableHiddenMixin,
    nested_admin.NestedStackedPolymorphicInline,
):
    registry: 'AffectRegistry'

    model = None
    sortable_field_name = 'ordering_field'

    def get_registry_child_inlines(self):
        return [x.admin_inline for x in self.registry.values()]

    def get_child_inline_instances(self):
        inlines = list(self.child_inlines) + self.get_registry_child_inlines()

        instances = []
        for ChildInlineType in inlines:
            instances.append(ChildInlineType(parent_inline=self))

        return instances


class AffectConfigInline(
    nested_admin.SortableHiddenMixin,
    nested_admin.NestedStackedPolymorphicInline.Child
):
    model = None
    sortable_field_name = 'ordering_field'


def make_inline(
    model: Type[models.Model],
    /,
    base = AffectConfigInline,
) -> AffectConfigInline:
    return type(model.__name__ + 'Inline', (base,), {'model': model})
