# Django-Rest-Framework RBAC plus

**Based on the django USER model, a permission system based on RBAC mode is implemented, 
which provides a background admin entry mechanism for permission, 
and implements permission control with drf middleware.**

---


# Requirements

- Python (3.5, 3.6, 3.7, 3.8)
- Django (2.1, 2.2, 3.0)

I **highly recommend** and only officially support the latest patch release of each Python and Django series.
# Installation
Install using pip...

```
pip install drf-rbac-plus
```

Add 'drf_rbac' to your INSTALLED_APPS setting.

```
INSTALLED_APPS = [
    ...
    'drf_rbac',
]
```

Add path to your URL setting.

```
urlpatterns = [
    ...
    path('drf_rbac/', include('drf_rbac.urls')),
]
```

## Example

### RegexValidator

These validators can be used to customized regex, the value must be match the 'word'(r"^[a-zA-Z\u4e00-\u9fa5]+$")

```
    aa
```
