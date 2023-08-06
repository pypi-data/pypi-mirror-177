from django.shortcuts import render
from .models import Role


def detail_auth(request, role_id):
    role = Role.objects.get(pk=role_id)
    auth = role.role_permission.all()
    res = []
    header = ['permission name', 'permission alias', 'permission type']
    for i in set(auth):
        name = "<a style='display:block' href='/admin/drf_rbac/permission/?q={name}'>{name}&nbsp</a>".format(
            name=i.name)
        res.append([name, i.alias_name, i.get_type_display()])
    return render(request, 'detail_auth.html', {"permission": res, "role_name": role.name, "header": header})
