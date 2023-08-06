# -*- coding: UTF-8 -*-
import os
import pickle
import sys
from datetime import datetime

from django.core.management import BaseCommand
from django.db import transaction
from rest_framework import serializers
from django.db.models import Q
from drf_rbac.settings import User, PERMISSION_PATH, PERMISSION_RELATIVE_PATH
from drf_rbac.models import HttpMethod, Role, Api, ApiMethodMembership, Permission, UserToPermission


def progress_bar(finish_tasks_number, tasks_number):
    percentage = round(finish_tasks_number / tasks_number * 100) if tasks_number else 100
    print(f"\rrate: {percentage}%", "█" * (percentage // 2), end="")
    sys.stdout.flush()


class HttpMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = HttpMethod
        exclude = ["id"]


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        exclude = ["id", "created"]


class SimpleRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ["name"]


class ApiSerializer(serializers.ModelSerializer):

    class Meta:
        model = Api
        exclude = ["id", "method", "created"]


class ApiMethodMembershipSerializer(serializers.ModelSerializer):
    api__url = serializers.SerializerMethodField()
    method__name = serializers.SerializerMethodField()

    def get_api__url(self, obj):
        return obj.api.url

    def get_method__name(self, obj):
        return obj.method.name

    class Meta:
        model = ApiMethodMembership
        fields = ("api__url", "method__name")


class PermissionSerializer(serializers.ModelSerializer):
    api = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    def get_api(self, obj):
        return ApiMethodMembershipSerializer(obj.api.all(), many=True).data

    def get_role(self, obj):
        return SimpleRoleSerializer(obj.role.all(), many=True).data

    class Meta:
        model = Permission
        exclude = ["id", "created"]


class SimplePermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ["name", "type"]


class UserSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)


class UserToPermissionSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    permission = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    def get_permission(self, obj):
        return SimplePermissionSerializer(obj.permission.all(), many=True).data

    class Meta:
        model = UserToPermission
        exclude = ["id", "created"]


class Command(BaseCommand):
    """
        import or export permission
    """
    def export_model(self, file_path, *args):
        for table_name in args:
            model, model_serializer = globals()[table_name], globals()[f"{table_name}Serializer"]
            self.write({"table": table_name,
                        "value": model_serializer(model.objects.all(), many=True).data}, file_path)

    def import_common_model(self, qd):
        if qd.get("table") == "Role" and qd.get("table") in self.__class__.STEP_POOL:
            print(f"step 1.1：import {qd.get('table')} ...")
            for i, j in enumerate(qd.get("value")):
                progress_bar(i, len(qd.get("value")) - 1)
                self.model_create(Role, j, Q(name=j.get("name")), "Role")
        elif qd.get("table") == "HttpMethod" and qd.get("table") in self.__class__.STEP_POOL:
            print(f"\nstep 1.2：import {qd.get('table')} ...")
            for i, j in enumerate(qd.get("value")):
                progress_bar(i, len(qd.get("value")) - 1)
                self.model_create(HttpMethod, j, Q(name=j.get("name")), "HttpMethod")

    def import_api_model(self, qd):
        if qd.get("table") == "Api" and qd.get("table") in self.__class__.STEP_POOL:
            print(f"\nstep 2：import {qd.get('table')} ...")
            for i, j in enumerate(qd.get("value")):
                progress_bar(i, len(qd.get("value")) - 1)
                q_obj = Q(url=j.get("url"))
                self.model_create(Api, j, q_obj, "Api")

    def import_apimethodmembership_model(self, qd):
        if qd.get("table") == "ApiMethodMembership" and qd.get("table") in self.__class__.STEP_POOL:
            print(f"\nstep 3：import {qd.get('table')} ...")
            for i, j in enumerate(qd.get("value")):
                progress_bar(i, len(qd.get("value")) - 1)
                q_obj = Q(api__url=j.get("api__url")) & \
                        Q(method__name=j.get("method__name"))
                self.model_create(ApiMethodMembership, j, q_obj, "ApiMethodMembership")

    def _update_api_ship_for_permission(self, apis, permission_obj):
        for api in apis:
            api_qs = Api.objects.filter(url=api.get("api__url"))
            method_qs = HttpMethod.objects.filter(name=api.get("method__name"))
            if api_qs.exists() and method_qs.exists():
                api_ship_qs = ApiMethodMembership.objects.filter(api=api_qs.first(),
                                                                 method=method_qs.first())
                api_ship_qs.exists() and permission_obj.api.add(api_ship_qs.first())

    def _update_role_for_permission(self, roles, permission_obj):
        for role in roles:
            role_qs = Role.objects.filter(name=role.get("name"))
            role_qs.exists() and permission_obj.role.add(role_qs.first())

    def _update_permission_for_usertopermission(self, permissions, user_to_permission_obj):
        for perm in permissions:
            perm_qs = Permission.objects.filter(name=perm.get("name"), type=perm.get("type"))
            perm_qs.exists() and user_to_permission_obj.permission.add(perm_qs.first())

    def import_permission_model(self, qd):
        if qd.get("table") == "Permission" and qd.get("table") in self.__class__.STEP_POOL:
            print(f"\nstep 4：import {qd.get('table')} ...")
            for i, j in enumerate(qd.get("value")):
                progress_bar(i, len(qd.get("value")) - 1)
                q_obj = Q(name=j.get("name"))
                au_qs = Permission.objects.filter(q_obj)
                apis, roles = j.get("api"), j.get("role")
                if not au_qs.exists():
                    mutating_data = self._data_mutating("Permission", j)
                    permission_obj = Permission.objects.create(**mutating_data)
                else:
                    permission_obj = au_qs.first()
                self._update_api_ship_for_permission(apis, permission_obj)
                self._update_role_for_permission(roles, permission_obj)

    def import_usertopermission_model(self, qd):
        if qd.get("table") == "UserToPermission" and qd.get("table") in self.__class__.STEP_POOL:
            print(f"\nstep 5：import {qd.get('table')} ...")
            for i, j in enumerate(qd.get("value")):
                progress_bar(i, len(qd.get("value")) - 1)
                username = j.get("user")
                user_to_permission_qs = UserToPermission.objects.filter(user__username=username)
                permissions = j.get("permission")
                if not user_to_permission_qs.exists():
                    mutating_data = self._data_mutating("UserToPermission", j)
                    if not isinstance(mutating_data.get("user"), str):
                        user_to_permission_obj = UserToPermission.objects.create(**mutating_data)
                        self._update_permission_for_usertopermission(permissions, user_to_permission_obj)
                else:
                    user_to_permission_obj = user_to_permission_qs.first()
                    self._update_permission_for_usertopermission(permissions, user_to_permission_obj)

    def model_create(self, model, instance_data, q_obj, table):
        if not model.objects.filter(q_obj).exists():
            mutating_data = self._data_mutating(table, instance_data)
            model.objects.create(**mutating_data)

    def _data_mutating(self, table, instance_data):
        if table == "ApiMethodMembership":
            api_qs = Api.objects.filter(url=instance_data.get("api__url"))
            method_qs = HttpMethod.objects.filter(name=instance_data.get("method__name"))
            if api_qs.exists() and method_qs.exists():
                del instance_data["api__url"]
                del instance_data["method__name"]
                instance_data["api"] = api_qs.first()
                instance_data["method"] = method_qs.first()
        elif table == "Permission":
            del instance_data["api"]
            del instance_data["role"]
        elif table == "UserToPermission":
            user_qs = User.objects.filter(username=instance_data.get("user"))
            if user_qs.exists():
                instance_data["user"] = user_qs.first()
            del instance_data["permission"]
        return instance_data

    def write(self, data, file_path):
        with open(file_path, "ab+") as f:
            pickle.dump(data, f)

    def search_permission_file(self, path, file):
        for parent_dir, _, file_names in os.walk(path):
            for walk_file_name in file_names:
                if walk_file_name.startswith(file):
                    file_path = os.path.join(parent_dir, walk_file_name)
                    return file_path
            else:
                raise ValueError("file not exists")

    def assemble_import_file(self, file_path):
        if not file_path:
            raise ValueError("file path not exists")

        elif "/" in file_path:
            if not file_path.startswith("/"):
                raise ValueError("offer abs path")

            if file_path.endswith("/"):
                raise ValueError("offer file name")

            dir_name, file_name = file_path.rsplit("/", 1)

            if not os.path.exists(dir_name):
                raise ValueError("abs path not exists")

            file_path = self.search_permission_file(dir_name, file_name)
        else:
            file_path = self.search_permission_file(os.path.join(PERMISSION_PATH, PERMISSION_RELATIVE_PATH), file_path)
        return file_path

    def read_all(self, file_path=None):
        res = list()
        with open(file_path, "rb") as f:
            while True:
                try:
                    res.append(pickle.load(f))
                except EOFError:
                    break
        return res

    def _check_dir_path(self, path_name):
        commands_dir = os.path.join(PERMISSION_PATH, path_name)
        not os.path.exists(commands_dir) and os.makedirs(commands_dir)
        return commands_dir

    def format_export_file_name(self):
        p_path = self._check_dir_path(PERMISSION_RELATIVE_PATH)
        file_path = os.path.join(p_path, f"permissions-{datetime.now().strftime('%H%M%m%d%Y')}.pickle")
        if os.path.exists(file_path):
            os.remove(file_path)
        return file_path

    def step_trigger(self, options):
        self.__class__.STEP_POOL = list()
        step_map = {"1": ["HttpMethod", "Role"],
                    "2": ["Api"],
                    "3": ["ApiMethodMembership"],
                    "4": ["Permission"],
                    "5": ["UserToPermission"]}
        step = options.get("step")
        if step:
            self.__class__.STEP_POOL.extend(step_map.get(step))
        else:
            for value in step_map.values():
                self.__class__.STEP_POOL.extend(value)

    def add_arguments(self, parser):
        parser.add_argument('--action', help='import/export/test')
        parser.add_argument('--path', help='import必填项: 直接输入文件名则在 pandora-be/data/permission_files 中寻找，'
                                           '找不到抛出错误，输入绝对路径校验成功后导入')
        parser.add_argument('--step', help='1/2/3/4/5')

    @transaction.atomic
    def handle(self, *args, **options):
        start_time = datetime.now()
        print("loading...")
        if options.get("action") == "test":
            print(f"Api\n{ApiSerializer(Api.objects.all()[:2], many=True).data}\n")
            print(f"HttpMethod\n{HttpMethodSerializer(HttpMethod.objects.all(), many=True).data}\n")
            print(f"Role\n{RoleSerializer(Role.objects.all(), many=True).data}\n")
            print(f"ApiMethodMembership\n{ApiMethodMembershipSerializer(ApiMethodMembership.objects.all()[:2], many=True).data}\n")
            print(f"Permission\n{PermissionSerializer(Permission.objects.filter(api__isnull=False, role__isnull=False)[:5], many=True).data}\n")
            print(f"UserToPermission\n{UserToPermissionSerializer(UserToPermission.objects.all(), many=True).data}\n")
        elif options.get("action") == "export":
            file_path = self.format_export_file_name()
            self.export_model(file_path, "Role", "HttpMethod")
            self.export_model(file_path, "Api")
            self.export_model(file_path, "ApiMethodMembership")
            self.export_model(file_path, "Permission")
            self.export_model(file_path, "UserToPermission")
            print(f"action: export\nfile: {file_path}\ntime: {(datetime.now() - start_time).seconds}s")
        elif options.get("action") == "import":
            self.step_trigger(options)
            file_path = self.assemble_import_file(options.get("path"))
            for qd in self.read_all(file_path):
                self.import_common_model(qd)  # step 1
                self.import_api_model(qd)  # step 2
                self.import_apimethodmembership_model(qd)  # step 3
                self.import_permission_model(qd)  # step 4
                self.import_usertopermission_model(qd)  # step 5
            print(f"\naction: import\ntime: {(datetime.now() - start_time).seconds}s\nsource: {file_path}")
