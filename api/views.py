from django.shortcuts import render
from django.contrib import sessions
from rest_framework.decorators import api_view
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rock.models import PicInfo, Region, Mine, LithostratigraphicInfo, RockSample
from collections import Counter
from django.core.cache import cache
import jieba
import os


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

        # 存在查询值，则传入前端
        if ('form_data' in request.session):
            ret['form_data'] = request.session['form_data']

        return Response(ret)


class MineDetailData(APIView):
    def get(self, request, pk):
        mine_inst = Mine.objects.get(pk=pk)

        if cache.get(f'mine_detail_{mine_inst.pk}') is not None:
            print(f'[mine_detail_{mine_inst.pk}]缓存存在')
            return Response(cache.get(f'mine_detail_{mine_inst.pk}'))
        else:
            print(f'[mine_detail_{mine_inst.pk}]缓存不存在')
            ret = {
                'layer_data': [],
                'sample_name_data':
                {
                    'data': [],
                    'categories': []
                }
            }

            # 地质分层数据
            layer_qs = LithostratigraphicInfo.objects.filter(
                mine_num=mine_inst).order_by('higher_border')
            for category in LithostratigraphicInfo.CATEGORY_NAMES:
                layer_cache = []
                for layer in layer_qs:
                    layer_value = getattr(layer, category[0])
                    if layer_value:
                        layer_cache.append(
                            (layer_value.name, layer.higher_border, layer.lower_border))
                if layer_cache:
                    merger = []
                    name = layer_cache[0][0]
                    low = layer_cache[0][1]
                    high = layer_cache[0][2]
                    l = len(layer_cache)
                    for i in range(1, l):
                        if layer_cache[i][0] == layer_cache[i-1][0]:
                            high = layer_cache[i][2]
                        else:
                            merger.append((name, low, high))
                            name = layer_cache[i][0]
                            low = layer_cache[i][1]
                            high = layer_cache[i][2]
                    merger.append((name, low, high))

                    for layer in merger:
                        mark = False
                        for dic in ret['layer_data']:
                            if dic['name'] == layer[0]:
                                mark = True
                                dic['data'].append({
                                    'x': category[1],
                                    'y': [layer[1], layer[2]]
                                })
                                break
                        if not mark:
                            ret['layer_data'].append({
                                'name': layer[0],
                                'data': [{
                                    'x': category[1],
                                    'y': [layer[1], layer[2]]
                                }]
                            })

            # 镜下命名数据
            sample_qs = RockSample.objects.filter(
                mine_num=mine_inst).order_by("depth")
            sample_name_hash = []
            for sample in sample_qs:
                sample_name = str(sample.name)
                if not sample_name in sample_name_hash:
                    sample_name_hash.append(sample_name)
                ret['sample_name_data']['data'].append(
                    {
                        'x': sample_name,
                        'y': sample.depth
                    }
                )
            ret['sample_name_data']['categories'] = sample_name_hash

            # 样本成份数据
            corpus_dir = os.path.join(settings.BASE_DIR, 'resource', 'corpus')
            jieba.load_userdict(os.path.join(corpus_dir, 'rock.txt'))
            jieba.load_userdict(os.path.join(corpus_dir, 'deposit.txt'))
            jieba.load_userdict(os.path.join(corpus_dir, 'erosion.txt'))
            jieba.load_userdict(os.path.join(corpus_dir, 'mineral.txt'))
            composition_dic = {
                'data': [],
                'categories': []
            }

            for sample in sample_qs:
                corpus_path = os.path.join(corpus_dir, 'rock.txt')
                word_freq = Counter()

                with open(corpus_path, 'r', encoding='utf-8') as f:
                    corpus_list = [line.split(' ')[0]
                                   for line in f.readlines()]
                words = jieba.lcut(sample.description, cut_all=False)

                for word in words:
                    if word in word_freq.keys():
                        word_freq[word] += 1
                    else:
                        word_freq[word] = 1

                filtered_word_freq = {k: v for k,
                                      v in word_freq.items() if k in corpus_list}

                for key in filtered_word_freq:
                    if key in composition_dic['categories']:
                        index = composition_dic['categories'].index(key)
                        composition_dic['data'][index]['data'].append(
                            [sample.depth, filtered_word_freq[key]])
                    else:
                        composition_dic['categories'].append(key)
                        composition_dic['data'].append({
                            'name': key,
                            'data': [[sample.depth, filtered_word_freq[key]]]
                        })

            for sample in sample_qs:
                for rock in composition_dic['data']:
                    for item in rock['data']:
                        if item[0] == sample.depth:
                            break
                    else:
                        rock['data'].append([sample.depth, 0])

            for rock in composition_dic['data']:
                rock['data'] = sorted(rock['data'], key=lambda x: x[0])

            ret['sample_composition_data'] = composition_dic

            cache.set(f'mine_detail_{mine_inst.pk}', ret)

            return Response(ret)
