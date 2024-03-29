from django.db import models
from django.urls import reverse
import os


class Region(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Mine(models.Model):
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return '%s-%s' % (self.region, self.name)

    @property
    def max_depth(self):
        return LithostratigraphicInfo.objects.filter(mine_num=self).order_by('-lower_border').first().lower_border

    @property
    def pic_num(self):
        return PicInfo.objects.filter(mine_num=self).count()

    @property
    def sample_num(self):
        return RockSample.objects.filter(mine_num=self).count()


def get_upload_to(instance, filename):
    return os.path.join('img/rocks/', str(instance.mine_num.region), instance.mine_num.name, filename)


class PicInfo(models.Model):
    ORTH_MODE = (
        ('o', '正交'),
        ('p', '单偏'),
    )
    LENS_MUL = ((4, '4X'), (10, '10X'))

    FULL_FIELDS = 1
    PARTIAL_FIELDS = 2

    # 井号
    mine_num = models.ForeignKey(Mine, on_delete=models.SET_NULL, null=True)
    # 井深
    depth = models.FloatField()
    # 物镜倍数
    lens_mul = models.SmallIntegerField()
    # 正交/单偏
    orth = models.CharField(
        max_length=1, choices=ORTH_MODE, blank=True, default='o')
    # 图像编号
    pic_num = models.SmallIntegerField()
    # 图像
    image = models.ImageField(upload_to=get_upload_to)
    # 备注
    remarks = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return '.'.join(self.image.name.split('/')[-1].split('.')[:-1])

    def get_clean_name(self, mode):
        if mode == self.FULL_FIELDS:
            return ' '.join([str(self.mine_num.region), self.mine_num.name, "{:g}".format(self.depth) + 'm', str(self.lens_mul) + 'X', dict(self.ORTH_MODE).get(self.orth)])
        else:
            return ' '.join([str(self.mine_num.region), self.mine_num.name])

    @property
    def get_orth(self):
        return dict(self.ORTH_MODE).get(self.orth)

    def get_absolute_url(self):
        return reverse('rock:rock_detail', args=[str(self.id)])


# 界
class Erathem(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


# 系
class System(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


# 统
class Series(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


# 组
class Formation(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


# 段
class Member(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


# 地层信息
class LithostratigraphicInfo(models.Model):
    CATEGORY_NAMES = [('erathem', '界'), ('system', '系'),
                      ('series', '统'), ('formation', '组'), ('member', '段')]
    # 井号
    mine_num = models.ForeignKey(Mine, on_delete=models.CASCADE, null=False)

    erathem = models.ForeignKey(
        Erathem, on_delete=models.SET_NULL, null=True)
    system = models.ForeignKey(
        System, on_delete=models.SET_NULL, null=True)
    series = models.ForeignKey(
        Series, on_delete=models.SET_NULL, null=True)
    formation = models.ForeignKey(
        Formation, on_delete=models.SET_NULL, null=True)
    member = models.ForeignKey(
        Member, on_delete=models.SET_NULL, null=True)

    lower_border = models.FloatField(null=False)
    higher_border = models.FloatField(null=False)
    thickness = models.FloatField(null=False)

    def __str__(self):
        return f'{self.mine_num}-{self.lower_border}'


# 样本镜下定名
class RockSampleName(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# 样本结构
class RockSampleStructure(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# 岩矿样本信息
class RockSample(models.Model):
    METHOD = (
        (0, '碎屑岩'),
        (1, '岩浆岩'),
        (2, '井壁取心')
    )

    method = models.IntegerField(choices=METHOD, null=False, default=0)
    mine_num = models.ForeignKey(Mine, on_delete=models.CASCADE, null=False)
    analysis_number = models.CharField(max_length=10, null=False)
    number = models.CharField(max_length=15, null=False)
    depth = models.FloatField(null=False)
    name = models.ForeignKey(
        RockSampleName, on_delete=models.SET_NULL, null=True)
    structure = models.ForeignKey(
        RockSampleStructure, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=100)
    remarks = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f'{self.mine_num}-{self.analysis_number}'


# 岩石成分
class RockComposition(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# 矿石成分
class MineralComposition(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# 碎屑物成分
class DepositComposition(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# 侵蚀成分
class ErosionComposition(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
