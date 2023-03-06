from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rock.models import PicInfo, Region, Mine


class AllPhotoFormData(APIView):
    def get(self, request):
        # 序列化所有矿井以符合react-checkbox-tree渲染所需的格式
        region_ary = []
        region_all = Region.objects.all()
        for region in region_all:
            mine_ary = []
            mines = Mine.objects.filter(region=region)

            for mine in mines:
                mine_ary.append(
                    {
                        'value': str(mine.pk) + '-mine',
                        'label': mine.name
                    }
                )

            region_ary.append(
                {
                    'value': str(region.pk) + '-region',
                    'label': region.name,
                    'expand': True,
                    'children': mine_ary
                }
            )

        lens_ary = []
        for len in PicInfo.LENS_MUL:
            lens_ary.append(
                {
                    'value': len[0],
                    'label': len[1]
                }
            )

        orth_ary = []
        for orth in PicInfo.ORTH_MODE:
            orth_ary.append(
                {
                    'value': orth[0],
                    'label': orth[1]
                }
            )

        ret = {
            'regions': [{
                'value': 'region',
                'label': '地区',
                'children': region_ary
            }],
            'lens': [{
                'value': 'wujingbeishu',
                'label': '物镜倍数',
                'children': lens_ary
            }],
            'orths': [{
                'value': 'zhengjiaopianguang',
                'label': '正交偏光',
                'children': orth_ary

            }]
        }

        return Response(ret)
