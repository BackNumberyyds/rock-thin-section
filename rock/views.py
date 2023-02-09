from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .forms import FileFieldForm, NormalSerchForm, DetailedSearchForm
from .models import PicInfo, Mine, Region
from fuzzywuzzy import fuzz, process

minimum_match_ratio = 50
depth_query_tolerance = 5
lens_query_tolerance = 1

pics_per_page = 12


class NameRepeatError(Exception):
    pass


# 基于类的视图验证superuser权限
class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


def index(request):
    pic_list = []
    form_type = 'detailed_form'
    query_url_preffix = request.path

    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1

    if 'form_type' in request.GET:
        query_url_preffix = request.META['QUERY_STRING'].split('&page=')[0]
        form_type = request.GET['form_type']
        pics_all = PicInfo.objects.all()

        if form_type == 'normal_form':
            # normal_form = NormalSerchForm(request.GET)
            # detailed_form = DetailedSearchForm()
            # if normal_form.is_valid():
            #     search = normal_form.cleaned_data['search_field']
            #     picinfos = process.extract(
            #         search, pics_dic, scorer=fuzz.token_set_ratio)
            #     for pic in picinfos:
            #         id = pic[2]
            #         pic_inst = PicInfo.objects.get(pk=id)
            #         pic_list.append(pic_inst)
            pass

        elif form_type == 'detailed_form':
            normal_form = NormalSerchForm()
            detailed_form = DetailedSearchForm(request.GET)

            if detailed_form.is_valid():
                pics_queryset = pics_all

                if pics_queryset.exists() and (depth := detailed_form.cleaned_data['depth_field']):
                    if pics_queryset.filter(depth=depth).exists():
                        pics_queryset = pics_queryset.filter(depth=depth)
                    else:
                        pics_queryset = pics_queryset.filter(depth__range=(
                            depth-depth_query_tolerance, depth+depth_query_tolerance))

                if pics_queryset.exists() and (lens := detailed_form.cleaned_data['lens_field']):
                    if pics_queryset.filter(lens_mul=lens).exists():
                        pics_queryset = pics_queryset.filter(lens_mul=lens)
                    else:
                        pics_queryset = pics_queryset.filter(lens_mul__range=(
                            lens-lens_query_tolerance, lens+lens_query_tolerance))

                if pics_queryset.exists() and (orth := detailed_form.cleaned_data['orth_field']):
                    pics_queryset = pics_queryset.filter(orth=orth)

                # messages.info(request, str(pics_queryset))

                # 对地区和井号字段进行模糊搜索
                if pics_queryset.exists():
                    abstract_list = []
                    if region_name := detailed_form.cleaned_data['region_field']:
                        abstract_list.append(region_name)

                    if mine_name := detailed_form.cleaned_data['mine_field']:
                        abstract_list.append(mine_name)

                    # if depth := detailed_form.cleaned_data['depth_field']:
                    #     abstract_list.append('{:g}'.format(depth) + 'm')

                    # if lens := detailed_form.cleaned_data['lens_field']:
                    #     abstract_list.append(str(lens) + 'X')

                    # if orth := detailed_form.cleaned_data['orth_field']:
                    #     abstract_list.append(dict(PicInfo.ORTH_MODE).get(orth))

                    if abstract_list:
                        abstract_str = ' '.join(abstract_list)

                        pics_dic = {}
                        for pic in pics_queryset:
                            pics_dic[pic.id] = pic.get_clean_name(
                                PicInfo.PARTIAL_FIELDS)

                        all_ratios = process.extract(
                            abstract_str, pics_dic, scorer=fuzz.token_set_ratio, limit=10000)
                        highest_ratio = all_ratios[0][1]
                        # messages.info(request, 'highest ratio:' +
                        #               str(highest_ratio))

                        if highest_ratio >= minimum_match_ratio:
                            picinfos = [
                                ratio for ratio in all_ratios if ratio[1] == highest_ratio]
                            pics_queryset = pics_queryset.filter(
                                pk__in=[pic[2] for pic in picinfos])
                        else:
                            pics_queryset = []

                pics_pages_obj = Paginator(pics_queryset, pics_per_page)
                pics_page_obj = pics_pages_obj.get_page(page_num)

        return render(request, 'index.html', {'pics': pics_page_obj, 'normal_form': normal_form, 'detailed_form': detailed_form, 'form_type': form_type, 'query_url_preffix': query_url_preffix})

    else:
        normal_form = NormalSerchForm()
        detailed_form = DetailedSearchForm()
        pic_list = PicInfo.objects.all()
        pics_pages_obj = Paginator(pic_list, pics_per_page)
        pics_page_obj = pics_pages_obj.get_page(page_num)

        return render(request, 'index.html', {'pics': pics_page_obj, 'normal_form': normal_form, 'detailed_form': detailed_form, 'form_type': form_type})


class FileFieldFormView(SuperUserRequiredMixin, FormView):
    form_class = FileFieldForm
    template_name = 'upload_images.html'
    success_url = reverse_lazy('rock:upload_images')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')

        error_files_num = 0
        successful_files_num = 0
        if form.is_valid():
            for f in files:
                try:
                    img_infos = f.name.split('-')
                    region = Region.objects.get(name=img_infos[0])
                    mine = Mine.objects.get(name=img_infos[1])
                    lens = int(img_infos[-3][:-1])
                    if img_infos[-2] == '正交':
                        orth = 'o'
                    elif img_infos[-2] == '单偏':
                        orth = 'p'
                    else:
                        raise ValueError
                    pic_num = int(img_infos[-1].split('.')[0])
                    if len(img_infos) == 6:
                        depth = float(img_infos[2][:-1])
                        if PicInfo.objects.filter(mine_num=mine, depth=depth, lens_mul=lens, orth=orth, pic_num=pic_num, remarks__isnull=True).exists():
                            raise NameRepeatError
                        picInfo_instance = PicInfo(
                            mine_num=mine, depth=depth, lens_mul=lens, orth=orth, pic_num=pic_num, image=f)
                    elif len(img_infos) == 7:
                        depth = float(img_infos[2])
                        remarks = int(img_infos[3][:-1])
                        if PicInfo.objects.filter(mine_num=mine, depth=depth, lens_mul=lens, orth=orth, pic_num=pic_num, remarks=remarks).exists():
                            raise NameRepeatError
                        picInfo_instance = PicInfo(
                            mine_num=mine, depth=depth, lens_mul=lens, orth=orth, pic_num=pic_num, image=f, remarks=remarks)
                    else:
                        raise ValueError
                    picInfo_instance.save()
                    successful_files_num = successful_files_num + 1
                except NameRepeatError:
                    messages.error(request, f'\'%s\'文件重复，无法导入。' % f.name)
                    error_files_num = error_files_num + 1
                except BaseException:
                    messages.error(request, f'\'%s\'文件命名不正确，无法导入。' % f.name)
                    error_files_num = error_files_num + 1
            messages.info(request, f'共选择%d个文件，成功导入%d个，失败%d个。' %
                          (len(files), successful_files_num, error_files_num))
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def search_rocks(request):
    if request.method == 'POST':
        pass
    else:
        normal_form = NormalSerchForm()
        detailed_form = DetailedSearchForm()
    return render(request, )
