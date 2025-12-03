+++
date = '2025-12-02T19:55:58-07:00'
draft = false
title = 'Increase django-polymorphic per model query limit'
+++

[`django-polymorphic`](https://github.com/jazzband/django-polymorphic), to quote the docs:

>...builds on top of the standard Django model inheritance. It makes using inherited models easier. When a query is made at the base model, the inherited model classes are returned.

This has downstream effects to polymorphic viewsets such as requiring the top-level query to get the base model then N downstream queries for each child model type.

For example, with the following set of models:
```Python
# app/models.py

from polymorphic.models import PolymorphicModel

class BaseModel(PolymorphicModel):
    pass

class FooModel(BaseModel):
    pass

class BarModel(BaseModel):
    pass
```

And with the following viewset:
```Python
# app/views.py

from rest_framework import mixins, viewsets

import app.models

class ModelViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = app.models.BaseModel.objects.all()
```

The list request to `ModelViewSet` would run a query for on the `BaseModel` table (`app_basemodel`) first then (assuming the queryset returns both subclasses) a query on the `FooModel` table (`app_foomodel`) and on the `BarModel` table (`app_barmodel`) to populate the child specific properties. This is easy to use but has an internal limitation of 100 items per queryset iteration when using the built in `django-rest-framework` serializers ([jazzband/django-polymorphic#465](https://github.com/jazzband/django-polymorphic/issues/465)).

In the case where, for example, the `FooModel` count in the original `BaseModel` query is greater than 100 items then this can result in N queries (batched by 100) to populate all the `FooModel` models.

This limitation is controlled via [this line in `django-polymorphic`](https://github.com/jazzband/django-polymorphic/blob/600acb89c1478193195ffe0545dc419e123cd8f1/src/polymorphic/query.py#L20-L22):
```Python
# chunk-size: maximum number of objects requested per db-request
# by the polymorphic queryset.iterator() implementation
Polymorphic_QuerySet_objects_per_request = 100
```

In some cases, it's helpful to raise this limit by simplistically including the following line in your Django app:
```Python
polymorphic.query.Polymorphic_QuerySet_objects_per_request = 1000
```

This doesn't fix the issue but helps, in some cases, to avoid unnecessary N+1 queries as the queryset grows.
