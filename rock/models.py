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
