import re

from django import http
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from pymysql import DatabaseError

from apps.health.models import Health


class HealthView(View):

    def get(self, request):
        return HttpResponse('OK')

    def post(self, request):
        name = request.POST.get('name')
        age = request.POST.get('age')
        body = request.POST.get('body')
        location = request.POST.get('location')
        time = request.POST.get('time')

        if not all([name, age, body, location, time]):
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^[1-9]\d*$', age):
            return http.HttpResponseForbidden('请输入正确的年龄')
        if not re.match(r'^3[5-9]\.\d$|^4[0-1]\.\d$', body):
            return http.HttpResponseForbidden('请输入正确的体温')

        # 保存注册数据
        try:
            Health.objects.create(name=name, age=age, body=body, location=location, time=time)
        except DatabaseError:
            return render(request, {'errmsg': '上传失败'})

        return http.HttpResponse('上传成功')
