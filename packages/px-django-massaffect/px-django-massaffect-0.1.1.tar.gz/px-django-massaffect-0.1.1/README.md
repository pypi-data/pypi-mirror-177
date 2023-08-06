# Django configurable affectors

Unified interface to create affector/filters configurations.

## Installation

```sh
pip install px-django-massaffect
```

## Configuration

Library allows to define any amount of filter sets. So to use filtering capabilities you should generate base classes and define adapters to apply filter.

First - create root affector model, that all other affectors will inherit from.

`models/something.py`
```python
from pxd_massaffect.models import make_formula_field


class SomethingThatCanAffect(models.Model):
  # Simple text field, where user may define affectors formula.
  filters_formula = make_formula_field()
```

`models/affector.py`
```python
from pxd_massaffect.models import make_config_base


# Affector model for any other affector to inherit from:
class Affector(make_config_base(
  # Abstract model name prefix.
  'affector',
  # Parent model, that will store configurations inside.
  'yourapp.SomethingThatCanAffect',
  # Related name to find all affectors.
  related_name='affectors',
  # Your app label. Not required.
  app_label='yourapp',
)):
  # Each of your affectors instance fill have a variable name to use in
  # affecting formula.
  # You may change prefix to any simple string. Simpler - better)
  variable_prefix = 'F'
```

Now you may define any particular affector you want. You'll need a configuration model and affector adapter to apply filtering:

`models/affectors.py` - Config
```python
from .affector import Affector


class CategoriesAffectorConfig(Affector):
  categories = models.ManyToManyField(Category)
```

`affector_adapters.py` - Adapters storage:
```python
from django.db import models
from pxd_massaffect.registry import AffectDescriptor, AffectAdapter

from .models import CategoriesAffectorConfig, ModelThatCanBeAffected


class CategoriesAffectAdapter(AffectAdapter):
  # By implementing `affect_Q` or `affect_queryset` we are making affector
  # capable of queryset handling.
  def affect_Q(self, config: CategoriesAffectorConfig, **kw) -> models.Q:
    return models.Q(category__in=config.categories.all())

  # If we want to affect some list of models instances we should
  # implement either `affect_item` or `affect_items`.
  def affect_item(self, config: CategoriesAffectorConfig, item, **kw):
    return item.category_id in {x.pk for x in config.categories.all()}


# Now, to register filter we need to have a filter descriptor instance:
categories_affector = AffectDescriptor(
  CategoriesAffectorConfig,
  CategoriesAffectAdapter({ModelThatCanBeAffected}),
)
```

Then you need to define your affectors registry:

`affectors_registry.py`
```python
from pxd_massaffect.registry import AffectRegistry

from .affector_adapters import categories_affector


registry = AffectRegistry()

# Add affect descriptors to a registry:
registry.multiregister([
  categories_affector,
  # or
  'yourapp.affector_adapters.categories_affector',
])
```

### Admin interface

All your affectors will be presented through 1 inline set:

```python
from pxd_massaffect.admin import AffectConfigSetInline, AffectConfigInline

from .affectors_registry import registry
from .models import Affector


class AffectorSetInline(AffectConfigSetInline):
  registry = registry
  model = Affector
```

And add this inline to a `SomethingThatCanAffect` model admin definition:

```python
from django.contrib import admin

import nested_admin
from .models import SomethingThatCanAffect

from .affectors_admin import AffectorSetInline


@admin.register(SomethingThatCanAffect)
class SomethingThatCanAffectAdmin(nested_admin.NestedPolymorphicModelAdmin):
  inlines = [
    AffectorSetInline,
  ]
```

## Usage

All that configuration above was made for you to be able to:

1. Calculate something during db selection request and add that calculation to annotation field.
2. Calculate something for each element in list and get back result.

For that purpose there are two classes: `Affector` and `ParentsAffector`.

`Affector` is a basic class takes arbitrary configuration instances and runs them for a set of objects/queryset.

When `ParentsAffector` is a little bit more complicated, because it collects affector configurations and resolving formulas from "parent" instances passed inside and then uses `Affector` to get the result.

```python
from pxd_massaffect.affector import (
  Affector, ParentsAffector,
  and_resolver, or_resolver,
  make_formula_resolver,
)
from .affectors_registry import registry


affector = Affector(registry)


class SomethingAffector(ParentsAffector):
  affector = affector

  # Based on formula from 'filters_formula' configurations will be resolved
  # for each passed parent:
  def get_parent_resolver(self, parent: SomethingThatCanAffect):
    return make_formula_resolver(parent.filters_formula)


something = SomethingThatCanAffect.objects.first()
something_affector = SomethingAffector([something])
# QuerySet will have additional annotation fields with result.
# And `fields_map` is the mapping parent->field_name.
# This way you can choose how you want to interpolate/query that data by
# yourself.
queryset, fields_map = something_affector.affect_queryset(
  SomeAffectableModel.objects.all()
)
# > (queryset, {something: 'autogenerated_field_name'})

# Line above with usage of base Affector class could look something like that:
queryset, field_name = affector.affect_queryset(
  # Passing list of affectors
  something.affectors.all(),
  # Queryset to affect
  SomeAffectableModel.objects.all(),
  # Formula resolver. By default it will be a "bitwise and" conjunction:
  resolver=make_formula_resolver(something.filters_formula),
  # Additional kwargs to adapters:
  kwargs={},
)
# > (queryset, 'autogenerated_field_name')
# But `ParentsAffector` is more suitable for multiple parents handling at once.

# After that you may do anything with that field:
queryset.filter(**{field_name: True})
```

Same logic could be used for a lists of objects. You just need to change the method from `affect_queryset` to `affect_items`.
