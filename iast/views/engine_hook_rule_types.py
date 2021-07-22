#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/2/19 下午3:59
# software: PyCharm
# project: lingzhi-webapi
import logging

from dongtai.endpoint import UserEndPoint, R
from dongtai.models.hook_type import HookType
from dongtai.utils import const

from iast.serializers.hook_type_strategy import HookTypeSerialize

logger = logging.getLogger('dongtai-webapi')


class EngineHookRuleTypesEndPoint(UserEndPoint):
    def parse_args(self, request):
        try:
            rule_type = request.query_params.get('type', const.RULE_PROPAGATOR)
            rule_type = int(rule_type)
            if rule_type not in (
                    const.RULE_SOURCE, const.RULE_ENTRY_POINT, const.RULE_PROPAGATOR, const.RULE_FILTER,
                    const.RULE_SINK):
                rule_type = None

            page = request.query_params.get('page', 1)
            page = int(page)

            page_size = request.query_params.get('pageSize', 20)
            page_size = int(page_size)
            if page_size > const.MAX_PAGE_SIZE:
                page_size = const.MAX_PAGE_SIZE

            return rule_type, page, page_size
        except Exception as e:
            logger.error(f"参数解析出错，错误原因：{e}")
            return None, None, None

    def get(self, request):
        rule_type, page, page_size = self.parse_args(request)
        if rule_type is None:
            return R.failure(msg='策略类型不存在')

        queryset = HookType.objects.filter(created_by__in=[request.user.id, const.SYSTEM_USER_ID], type=rule_type)
        data = HookTypeSerialize(queryset, many=True).data
        return R.success(data=data)
