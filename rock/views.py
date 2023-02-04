from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .forms import FileFieldForm, NormalSerchForm, DetailedSearchForm
from .models import PicInfo, Mine, Region


class NameRepeatError(Exception):
    pass


# 基于类的视图验证superuser权限
class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


def index(request):
    # picinfos = PicInfo.objects.all()[:12]
    # return render(request, 'index.html', {'pics': picinfos})
    picinfos = PicInfo.objects.all()[:12]
    if 'form_type' in request.GET:
        normal_form = NormalSerchForm()
        detailed_form = DetailedSearchForm()
        if request.GET['form_type'] == 'detailed_form':
            messages.info(request, 'detailed_form')
        elif request.GET['form_type'] == 'normal_form':
            messages.info(request, 'normal_form')
    else:
        normal_form = NormalSerchForm()
        detailed_form = DetailedSearchForm()
    return render(request, 'index.html', {'pics': picinfos, 'normal_form': normal_form, 'detailed_form': detailed_form})


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
