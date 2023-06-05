# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2021/6/3 003 0:30
@Remark: 菜单按钮管理
"""
from django.db.models import F, Subquery, OuterRef, Exists
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from dvadmin.system.models import RoleMenuButtonPermission, Menu, MenuButton, Dept, RoleMenuPermission
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class RoleMenuButtonPermissionSerializer(CustomModelSerializer):
    """
    菜单按钮-序列化器
    """

    class Meta:
        model = RoleMenuButtonPermission
        fields = "__all__"
        read_only_fields = ["id"]


class RoleMenuButtonPermissionInitSerializer(CustomModelSerializer):
    """
    初始化菜单按钮-序列化器
    """

    class Meta:
        model = RoleMenuButtonPermission
        fields = "__all__"
        read_only_fields = ["id"]

class RoleMenuButtonPermissionCreateUpdateSerializer(CustomModelSerializer):
    """
    初始化菜单按钮-序列化器
    """

    class Meta:
        model = RoleMenuButtonPermission
        fields = "__all__"
        read_only_fields = ["id"]


class RoleMenuButtonPermissionViewSet(CustomModelViewSet):
    """
    菜单按钮接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = RoleMenuButtonPermission.objects.all()
    serializer_class = RoleMenuButtonPermissionSerializer
    create_serializer_class = RoleMenuButtonPermissionCreateUpdateSerializer
    update_serializer_class = RoleMenuButtonPermissionCreateUpdateSerializer
    extra_filter_class = []

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated])
    def role_get_menu(self, request):
        """根据当前用户的角色返回角色拥有的菜单"""
        data = []
        is_superuser = request.user.is_superuser
        is_admin = request.user.role.values_list('admin', flat=True)
        if is_superuser or True in is_admin:
            queryset = Menu.objects.filter(status=1).values('name','parent','is_catalog',menu_id=F('id'))
            for item in queryset:
                btn_name = MenuButton.objects.filter(menu=item['menu_id']).values_list(
                    'name', flat=True)
                data.append({'menu_id': item['menu_id'], 'name': item['name'], 'parent': item['parent'],
                             'permission': ','.join(btn_name), 'is_catalog': item['is_catalog']})
        else:
            role_id = request.user.role.values_list('id',flat=True)
            queryset = RoleMenuPermission.objects.filter(role__in=role_id).values('menu_id',name=F('menu__name'),parent=F('menu__parent'),is_catalog=F('menu__is_catalog')).distinct()
            for item in queryset:
                btn_name = RoleMenuButtonPermission.objects.filter(menu_button__menu=item['menu_id']).values_list('menu_button__name',flat=True)
                data.append({'menu_id':item['menu_id'], 'name':item['name'], 'parent':item['parent'],'permission':','.join(btn_name),'is_catalog':item['is_catalog']})
        return DetailResponse(data=data)

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated])
    def role_menu_get_button(self,request):
        """
        当前用户角色和菜单获取可下拉选项的按钮:角色授权页面使用
        :param request:
        :return:
        """
        if params := request.query_params:
            if menu_id := params.get('menu', None):
                is_superuser = request.user.is_superuser
                is_admin = request.user.role.values_list('admin', flat=True)
                if is_superuser or True in is_admin:
                    queryset = MenuButton.objects.filter(menu=menu_id).values('id', 'name')
                else:
                    role_list = request.user.role.values_list('id',flat=True)
                    queryset = RoleMenuButtonPermission.objects.filter(role__in=role_list,menu_button__menu=menu_id).values(
                        btn_id=F('menu_button__id'),
                        name=F('menu_button__name')
                    )
                return DetailResponse(data=queryset)
        return ErrorResponse(msg="参数错误")

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated])
    def data_scope(self, request):
        """
        获取数据权限范围:角色授权页面使用
        :param request:
        :return:
        """
        is_superuser = request.user.is_superuser
        if is_superuser:
            data = [
                {
                    "value": 0,
                    "label": '仅本人数据权限'
                },
                {
                    "value": 1,
                    "label": '本部门及以下数据权限'
                },
                {
                    "value": 2,
                    "label": '本部门数据权限'
                },
                {
                    "value": 3,
                    "label": '全部数据权限'
                },
                {
                    "value": 4,
                    "label": '自定义数据权限'
                }
            ]
            return DetailResponse(data=data)
        else:
            data = []
            role_list = request.user.role.values_list('id',flat=True)
            if params := request.query_params:
                if menu_button_id := params.get('menu_button', None):
                    role_queryset = RoleMenuButtonPermission.objects.filter(role__in=role_list,menu_button__id=menu_button_id).values_list('data_range',flat=True)
                    data_range_list = list(set(role_queryset))
                    for item in data_range_list:
                        if item == 0:
                            data = [{
                                "value": 0,
                                "label": '仅本人数据权限'
                            }]
                        elif item == 1:
                            data = [{
                                "value": 0,
                                "label": '仅本人数据权限'
                            }, {
                                "value": 1,
                                "label": '本部门及以下数据权限'
                            },
                                {
                                    "value": 2,
                                    "label": '本部门数据权限'
                                }]
                        elif item == 2:
                            data = [{
                                "value": 0,
                                "label": '仅本人数据权限'
                            },
                                {
                                    "value": 2,
                                    "label": '本部门数据权限'
                                }]
                        elif item == 3:
                            data = [{
                                "value": 0,
                                "label": '仅本人数据权限'
                            },
                                {
                                    "value": 3,
                                    "label": '全部数据权限'
                                }, ]
                        elif item == 4:
                            data = [{
                                "value": 0,
                                "label": '仅本人数据权限'
                            },
                                {
                                    "value": 4,
                                    "label": '自定义数据权限'
                                }]
                        else:
                            data = []
                    return DetailResponse(data=data)
        return ErrorResponse(msg="参数错误")

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    def role_to_dept_all(self, request):
        """
        当前用户角色下所能授权的部门:角色授权页面使用
        :param request:
        :return:
        """
        params = request.query_params
        is_superuser = request.user.is_superuser
        is_admin = request.user.role.values_list('admin', flat=True)
        if is_superuser or True in is_admin:
            queryset = Dept.objects.values('id','name','parent')
        else:
            if not params:
                return ErrorResponse(msg="参数错误")
            menu_button = params.get('menu_button')
            if menu_button is None:
                return ErrorResponse(msg="参数错误")
            role_list = request.user.role.values_list('id', flat=True)
            queryset = RoleMenuButtonPermission.objects.filter(role__in=role_list,menu_button=None).values(
                dept_id=F('dept__id'),
                name=F('dept__name'),
                parent=F('dept__parent')
            )
        return DetailResponse(data=queryset)



    @action(methods=['get'],detail=False,permission_classes=[IsAuthenticated])
    def menu_to_button(self,request):
        """
        根据所选择菜单获取已配置的按钮/接口权限:角色授权页面使用
        :param request:
        :return:
        """
        params = request.query_params
        menu_id = params.get('menu', None)
        if menu_id is None:
            return ErrorResponse(msg="未获取到参数")
        is_superuser = request.user.is_superuser
        is_admin = request.user.role.values_list('admin', flat=True)
        if is_superuser or True in is_admin:
            queryset = RoleMenuButtonPermission.objects.filter(menu_button__menu=menu_id).values(
                'id',
                'data_range',
                'menu_button',
                'menu_button__name',
                'menu_button__value'
            )
            return DetailResponse(data=queryset)
        else:
            if params:

                role_id = params.get('role', None)
                if role_id is None:
                    return ErrorResponse(msg="未获取到参数")
                queryset = RoleMenuButtonPermission.objects.filter(role=role_id,menu_button__menu=menu_id).values(
                    'id',
                    'data_range',
                    'menu_button',
                    'menu_button__name',
                    'menu_button__value'
                )
                return DetailResponse(data=queryset)
        return ErrorResponse(msg="未获取到参数")

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    def role_to_menu(self, request):
        """
        获取角色对应的按钮权限
        :param request:
        :return:
        """
        params = request.query_params
        role_id = params.get('role', None)
        if role_id is None:
            return ErrorResponse(msg="未获取到参数")
        queryset = RoleMenuPermission.objects.filter(role_id=role_id).values_list('menu_id',flat=True).distinct()

        return DetailResponse(data=queryset)

