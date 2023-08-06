from __future__ import unicode_literals
from django.contrib import admin
from django.db import transaction
from .models import Role, Api, HttpMethod, ApiMethodMembership, Permission, UserToPermission, UserRoleMembership
from django import forms
from django.utils.html import format_html


def role_validate(value):
    if value not in [role.name for role in Role.objects.all()]:
        raise forms.ValidationError(u'name error')


class RoleForm(forms.ModelForm):
    clone = forms.BooleanField(required=False, widget=forms.NullBooleanSelect, initial=False)
    clone_role_field = forms.CharField(required=False,
                                       widget=forms.TextInput(attrs={'placeholder': u'role name'}),
                                       validators=[role_validate])


class UsersInline(admin.TabularInline):
    model = UserRoleMembership


class RoleAdmin(admin.ModelAdmin):
    form = RoleForm
    list_display = ('name', 'show_permission_num',)
    search_fields = ('name', 'comment')
    inlines = [
        UsersInline,
    ]

    def show_permission_num(self, obj):
        count = obj.role_permission.count()
        text = "<a href='/drf_rbac/role_perm/{}/'>{}</a>".format(obj.id, count)
        return format_html(text)

    show_permission_num.short_description = "permission count"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            clone_role = form.cleaned_data.get("clone_role_field")
            if form.cleaned_data.get("clone") and clone_role:
                for i in Permission.objects.filter(role=Role.objects.filter(name=clone_role).first()):
                    i.role.add(obj)


class HttpMethodAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class MethodInline(admin.TabularInline):
    model = ApiMethodMembership


class ApiAdmin(admin.ModelAdmin):
    list_display = ('url', 'alias_name', 'show_method', 'show_permission', 'username', 'updated', 'created',)
    list_editable = ('alias_name',)
    search_fields = ('id', 'alias_name', 'url', 'username',)
    list_display_links = ('url',)
    filter_horizontal = ('method',)
    list_filter = ('username',)
    actions = ['copy']
    list_per_page = 10
    ordering = ('-pk',)
    fieldsets = [
        (None, {'fields': ('url', 'alias_name',)}),
    ]
    inlines = [
        MethodInline,
    ]

    @transaction.atomic
    def copy(self, request, queryset):
        for instance in queryset:

            obj = Api.objects.create(alias_name="{}-copy?".format(instance.alias_name),
                                     url="?{}".format(instance.url),
                                     username=instance.username)
            ship_list = []
            for method in instance.method.all():
                ship_list.append(ApiMethodMembership.objects.create(api=obj, method=method))

            for ship_obj in ApiMethodMembership.objects.filter(api=instance):
                for perm in ship_obj.permission_set.all():
                    perm.api.add(*ship_list)

        self.message_user(request, "copy completed!")

    copy.short_description = "copy"

    def show_permission(self, obj):
        apimethodmembership = obj.apimethodmembership_set.all()
        results = []
        for mem in apimethodmembership:
            for permission in mem.permission_set.all():
                results.append("{},{}".format(permission.id, permission.name))
        res = ""
        for i in set(results):
            _, name = i.split(",")
            res += "<a href='/admin/drf_rbac/permission/?q={name}'>{name}</a> </br>".format(name=name)
        text = """<div>
                    <div style="margin-left:20px;margin-bottom:5px;margin-top:5px">
                    <a style="border-style:outset;padding:2px" onclick="
                         var parent= window.event.target.parentNode;
                         if(parent.nextElementSibling){{
                            console.log(parent.nextElementSibling.style.display)
                            if(parent.nextElementSibling.style.display=='block'){{
                                parent.nextElementSibling.style.display='none';
                            }}else{{
                                parent.nextElementSibling.style.display='block';
                            }}
                        }}else {{
                            parent.nextElementSibling.style.display='none';
                        }}">click</a></div>
                    <div style="display:none">""" + res + "</div></div>"
        return format_html(text)

    show_permission.short_description = "permission"

    def show_method(self, obj):
        method = obj.method.all()
        results = []
        for m in method:
            results.append(m.name)
        return " ".join(results)

    show_method.short_description = "http methods"

    def save_model(self, request, obj, form, change):
        obj.username = request.user.username
        super(__class__, self).save_model(request, obj, form, change)


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'alias_name', 'type', 'status', 'username', 'updated', 'created')
    search_fields = ('name', 'alias_name', 'comment')
    list_editable = ('alias_name', 'status')
    ordering = ('-pk',)
    date_hierarchy = 'created'
    # empty_value_display = "---"
    list_display_links = ('name',)
    list_per_page = 20
    radio_fields = {"type": admin.HORIZONTAL}
    actions = ["copy"]
    fieldsets = [
        ('common info', {'fields': ('type', ('name', 'alias_name',), 'status', 'comment')}),
        ('role info', {'fields': ('role',)}),
        ('api info', {'fields': ('api',),
                      'classes': ['wide'],
                      'description': 'Attached API information'}),
    ]
    filter_horizontal = ('role', 'api',)
    list_filter = ('type', 'username')
    save_as = True
    save_on_top = True

    @transaction.atomic
    def copy(self, request, queryset):
        for instance in queryset:
            obj = Permission.objects.create(alias_name="{}-copy?".format(instance.alias_name),
                                            name="?{}".format(instance.name),
                                            type=instance.type,
                                            status=instance.status,
                                            username=instance.username,
                                            comment=instance.comment)

            obj.role.add(*instance.role.all())
            obj.api.add(*instance.api.all())

        self.message_user(request, "copy completed!")

    copy.short_description = "copy"

    def save_model(self, request, obj, form, change):
        obj.username = request.user.username
        super(__class__, self).save_model(request, obj, form, change)


class UserToPermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'created', 'updated')
    filter_horizontal = ('permission',)


admin.site.register(Role, RoleAdmin)
admin.site.register(HttpMethod, HttpMethodAdmin)
admin.site.register(Api, ApiAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(UserToPermission, UserToPermissionAdmin)
