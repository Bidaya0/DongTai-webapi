from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from webapi.settings import config
from dongtai.models.profile import IastProfile


class ProfileEndpoint(UserEndPoint):
    def get(self, request, key):
        """
        获取profile配置
        """
        profile = IastProfile.objects.filter(key=key).values_list(
            'value', flat=True).first()
        if profile is None:
            return R.failure(msg=''.join(["获取", key, "配置失败"]))
        return R.success(data={key: profile})

    def put(self, request, key):
        """
        更新profile配置
        """
        fields = get_model_field(IastProfile, exclude=['id'])
        data = {k: v for k, v in request.data.items() if k in fields}
        profile = IastProfile.objects.filter(key=key).first()
        try:
            profile.__dict__.update(**data)
            profile.save()
        except Exception as e:
            print(e)
            return R.failure(msg="".join(["更新", key, "失败"]))
        return R.success(data={'key': profile.key})

def get_model_field(model, exclude=[], include=[]):
    fields = [field.name for field in model._meta.fields]
    if include:
        return [
            include for field in list(set(fields) - set(exclude))
            if field in include
        ]
    return list(set(fields) - set(exclude))