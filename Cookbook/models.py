import datetime
from typing import List

from django.db import models
from model_utils.models import TimeStampedModel

from .defines import MaterialType


class CookbookTag(TimeStampedModel):
    name = models.CharField("菜谱标签", max_length=255)
    priority = models.SmallIntegerField("优先级", default=0)

    cookbook_sum = models.IntegerField("菜谱数量", default=0)

    class Meta:
        verbose_name = "菜谱标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'<CookbookTag>{str(self)}'

    def update_cookbook_sum(self):
        self.cookbook_sum = self.cookbook_set.count()
        self.save()


class Material(TimeStampedModel):
    name = models.CharField("原料名称", max_length=255)
    amount = models.CharField("原料数量", max_length=255, default='')
    detail = models.TextField("原料详情", default='')
    type = models.SmallIntegerField("原料类型", choices=(
        (MaterialType.FOOD, '食材'),
        (MaterialType.CONDIMENT, '调料'),
        (MaterialType.TOOL, '工具'),
    ))
    priority = models.SmallIntegerField("优先级", default=0)

    img_url = models.URLField("原料图片", default='')

    step = models.ForeignKey(
        "Step",
        on_delete=models.CASCADE,
        related_name="material_set"
    )

    class Meta:
        verbose_name = "菜谱原料"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name} - {self.step}'


class Step(TimeStampedModel):
    name = models.CharField("步骤名称", max_length=255)
    detail = models.TextField("步骤详情", default='')
    priority = models.SmallIntegerField("优先级", default=0)

    img_url = models.URLField("步骤图片", default='')
    duration = models.DurationField("步骤持续时间", default=datetime.timedelta(minutes=0))

    cookbook = models.ForeignKey(
        "Cookbook",
        on_delete=models.CASCADE,
        related_name="step_set"
    )

    class Meta:
        verbose_name = "菜谱步骤"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'<CookbookStep>{str(self)}'

    @property
    def duration_describe(self) -> str:
        return str(self.duration)

    def get_material_set(self) -> List[Material]:
        return self.material_set.order_by("priority", "id").all()


class Cookbook(TimeStampedModel):
    name = models.CharField("菜谱名称", max_length=255)
    url_video = models.URLField("菜谱视频", default='')
    url_cover_image = models.URLField("封面图", default='')

    tag_set = models.ManyToManyField(
        "CookbookTag",
        related_name="cookbook_set",
        blank=True,
        through='TagCookbookRelationship'
    )

    @property
    def materials(self) -> List[Material]:
        return Material.objects.filter(step__cookbook=self).all()

    def add_tag(self, tag: CookbookTag):
        if TagCookbookRelationship.objects.filter(cookbook=self, tag=tag).exists():
            return
        TagCookbookRelationship.objects.create(
            tag=tag, cookbook=self
        )

    class Meta:
        verbose_name = "菜谱"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'<Cookbook>{self.name}'


class TagCookbookRelationship(models.Model):
    cookbook = models.ForeignKey(Cookbook, on_delete=models.CASCADE)
    tag = models.ForeignKey(CookbookTag, on_delete=models.CASCADE)
    like = models.IntegerField('点赞数量', default=0)
    unlike = models.IntegerField('踩数量', default=0)
