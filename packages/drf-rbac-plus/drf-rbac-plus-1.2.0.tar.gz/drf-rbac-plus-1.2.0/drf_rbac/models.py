from django.db import models
from .settings import User
from django.utils.translation import ugettext_lazy as _


class PermissionTypes(models.TextChoices):
    common = "common", u"Page and Api"
    api = "api", u"Api"
    page = "page", u"Page"


class Role(models.Model):
    name = models.CharField(max_length=64, unique=True)
    comment = models.TextField(_("Comment"), null=True, blank=True)
    user = models.ManyToManyField(User, blank=True, through="UserRoleMembership",
                                  verbose_name=u"Related User-Role")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = verbose_name
        ordering = ('-created',)


class UserRoleMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return '{} has {}'.format(self.user.username, self.role.name)

    class Meta:
        verbose_name = _("User Role")
        verbose_name_plural = verbose_name
        unique_together = (
            ('user', 'role'),
        )


class HttpMethod(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Http Methods")
        verbose_name_plural = verbose_name


class Api(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    alias_name = models.CharField(_("Alias Name"), max_length=64, null=True, blank=True)
    url = models.CharField(_("URL"), unique=True, max_length=1024)
    comment = models.TextField(_("Comment"), null=True, blank=True)
    method = models.ManyToManyField(HttpMethod, through='ApiMethodMembership')
    username = models.CharField(_("Operation User"), max_length=64, null=True, blank=True)

    def __str__(self):
        return "{}({})".format(self.url, self.alias_name)

    class Meta:
        ordering = ('-created',)
        verbose_name = _("Api")
        verbose_name_plural = verbose_name


class ApiMethodMembership(models.Model):
    api = models.ForeignKey(Api, on_delete=models.CASCADE)
    method = models.ForeignKey(HttpMethod, on_delete=models.CASCADE)

    def __str__(self):
        return '{}-{}'.format(self.api.url, self.method.name)

    class Meta:
        verbose_name = _("api method")
        verbose_name_plural = verbose_name
        unique_together = (
            ('api', 'method'),
        )


class Permission(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(_("Permission Name"), max_length=64, unique=True)
    alias_name = models.CharField(_("Alias Name"), max_length=128, null=True, blank=True)
    type = models.CharField(_("Permission Type"), max_length=64, db_index=True,
                            default=PermissionTypes.common, choices=PermissionTypes.choices)
    role = models.ManyToManyField(Role, related_name='role_permission')
    status = models.BooleanField(_("effective"), default=True)
    api = models.ManyToManyField(ApiMethodMembership, blank=True, verbose_name=u"Related Api-Method")
    username = models.CharField(_("Operation User"), max_length=128, null=True, blank=True)
    comment = models.TextField(_("Comment"), null=True, blank=True)

    def __str__(self):
        return '{}({})'.format(self.name, self.alias_name)

    class Meta:
        ordering = ('-created',)
        verbose_name = _("Role Permission")
        verbose_name_plural = verbose_name
        unique_together = (
            ('name', 'type',),
        )


class UserToPermission(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='user_permission')
    permission = models.ManyToManyField(Permission)

    class Meta:
        ordering = ('-created',)
        verbose_name = _("User Permission")
        verbose_name_plural = verbose_name
