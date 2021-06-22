#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# datetime:2021/06/09 上午10:52
# software: PyCharm
# project: lingzhi-webapi
import logging, time
from base import R
from iast.base.user import UserEndPoint
from dongtai_models.models.project_version import IastProjectVersion
from dongtai_models.models.project import IastProject
from dongtai_models.models.agent import IastAgent

logger = logging.getLogger("django")


class UpdateProjectVersion(UserEndPoint):
    name = "api-v1-project-version-check"
    description = "检测并关联项目版本信息"

    def get(self, request):
        try:
            all_project = IastProject.objects.all()
            data = []
            for one in all_project:
                result = IastProjectVersion.objects.filter(project_id=one.id, user_id=one.user_id, status=1).first()
                if not result:
                    result = IastProjectVersion.objects.create(
                        version_name="V1.0",
                        project_id=one.id,
                        user_id=one.user_id,
                        current_version=1,
                        status=1
                    )
                    data.append(result.id)
                IastAgent.objects.filter(
                    bind_project_id=one.id,
                    user_id=one.user_id,
                    project_version_id=0
                ).update(
                    project_version_id=result.id,
                    latest_time=int(time.time())
                )
            return R.success(msg='检测完成', data=data)
        except Exception as e:
            return R.failure(status=202, msg=e)