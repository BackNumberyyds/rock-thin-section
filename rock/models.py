from django.db import models
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


ORTH_MODE = (
    ('o', '正交'),
    ('p', '单偏'),
)


class PicInfo(models.Model):

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
