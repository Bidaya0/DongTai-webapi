#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh

# software: PyCharm
# project: lingzhi-webapi
import logging, time
from dongtai.endpoint import R
from django.db.models import Q
from dongtai.endpoint import UserEndPoint
from dongtai.models.project_version import IastProjectVersion
from dongtai.models.agent import IastAgent
from django.utils.translation import gettext_lazy as _
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from rest_framework import serializers

logger = logging.getLogger("django")

class _ProjectVersionCurrentSerializer(serializers.Serializer):
    version_id = serializers.CharField(
        help_text=_("The version id of the project"))
    project_id = serializers.IntegerField(help_text=_("The id of the project"))


_ResponseSerializer = get_response_serializer(status_msg_keypair=(
    ((202, _('Version does not exist')), ''),
    ((202, _('Version setting failed')), ''),
    ((201, _('Version setting success')), ''),
))


class ProjectVersionCurrent(UserEndPoint):
    name = "api-v1-project-version-current"
    description = _("Set to the current application version")

    @extend_schema_with_envcheck(
        request=_ProjectVersionCurrentSerializer,
        tags=[_('Project')],
        summary=_('Projects Version Current'),
        description=
        _("Specify the selected version as the current version of the project according to the given conditions."
          ),
        response_schema=_ResponseSerializer,
    )
    def post(self, request):
        try:
            project_id = request.data.get("project_id", 0)
            version_id = request.data.get("version_id", 0)
            if not version_id or not project_id:
                return R.failure(status=202, msg=_('Parameter error'))

            users = self.get_auth_users(request.user)
            users_id = [user.id for user in users]
            version = IastProjectVersion.objects.filter(project_id=project_id, id=version_id, user_id__in=users_id).first()
            if version:
                version.current_version = 1
                version.update_time = int(time.time())
                version.save(update_fields=["current_version", "update_time"])
                IastAgent.objects.filter(user=version.user, bind_project_id=project_id, project_version_id=version.id).update(online=1)

                IastAgent.objects.filter(~Q(project_version_id=version.id), user=version.user, bind_project_id=project_id).update(online=0)
                IastProjectVersion.objects.filter(
                    ~Q(id=version_id),
                    project_id=project_id,
                    user=version.user,
                    current_version=1,
                    status=1
                ).update(current_version=0, update_time=int(time.time()))

                return R.success(msg=_('Version setting success'))
            else:
                return R.failure(status=202, msg=_('Version does not exist'))

        except Exception as e:
            logger.error(e)
            return R.failure(status=202, msg=_("Version setting failed"))
