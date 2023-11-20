# -*- coding: utf-8 -*-
from django.apps import apps
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from dvadmin.system.models import  Role, MenuField
from dvadmin.utils.models import get_custom_app_models
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.json_response import DetailResponse, ErrorResponse, SuccessResponse


class ColumnSerializer(CustomModelSerializer):
    """
    列权限序列化器
    """

    class Meta:
        model = MenuField
        fields = '__all__'
        read_only_fields = ['id']


class ColumnViewSet(CustomModelViewSet):
    """
    列权限视图集
    """
    queryset = MenuField.objects.all()
    serializer_class = ColumnSerializer

    def list(self, request, *args, **kwargs):
        app_name = request.query_params.get('app')
        model_name = request.query_params.get('model')
        menu = request.query_params.get('menu')
        if  not menu:
            return SuccessResponse([])
        queryset = self.filter_queryset(self.get_queryset().filter(menu=menu))
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True, request=request)
        #     return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, request=request)
        return SuccessResponse(data=serializer.data, msg="获取成功")

    def create(self, request, *args, **kwargs):
        payload = request.data
        print(11,get_custom_app_models())
        for model in apps.get_models():
            print(model.__name__)
            if payload.get('model') == model.__name__:
                break
        else:
            return ErrorResponse(msg='模型表不存在')

        if MenuField.objects.filter(menu=payload.get('menu'),model=model.__name__, field_name=payload.get('field_name')).exists():
            return ErrorResponse(msg='‘%s’ 字段权限已有，不可重复创建' % payload.get('title'))

        return super().create(request, *args, **kwargs)

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated])
    def get_models(self, request):
        """获取所有项目app下的model"""
        res = []
        for app in get_custom_app_models():
            for model in app:
                res.append({
                    'app': model['app'],
                    'title': model['verbose'],
                    'key': model['model']
                })
        return DetailResponse(res)

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated])
    def auto_match_fields(self, request):
        """自动匹配已有的字段"""
        menu_id = request.data.get('menu')
        app_name = request.data.get('app')
        model_name = request.data.get('model')
        if not menu_id or not model_name or not app_name:
            return ErrorResponse( msg='参数错误')
        for model in get_custom_app_models(app_name):
            if model['model'] != model_name:
                continue
            for field in model['fields']:
                if MenuField.objects.filter(
                        menu_id=menu_id, app=app_name, model=model_name, field_name=field['name']
                ).exists():
                    continue
                data = {
                    'menu': menu_id,
                    'app': app_name,
                    'model': model_name,
                    'field_name': field['name'],
                    'title': str(field['title']),
                }
                serializer = self.get_serializer(data=data, request=request)
                serializer.is_valid(raise_exception=True)
                serializer.save()
        return SuccessResponse(msg='匹配成功')
