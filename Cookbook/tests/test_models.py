import datetime
from django.test import TestCase

from Cookbook.models import Cookbook, Step, Material, CookbookTag
from Cookbook.defines import MaterialType


class CookbookModelTests(TestCase):
    def setUp(self):
        self.tag_oil = CookbookTag.objects.create(name='宽油警告')
        self.tag_hot = CookbookTag.objects.create(name='🌶️')
        self.tag_too_hot = CookbookTag.objects.create(name='🌶️🌶️🌶️')

    def test_cookbook_step_material(self):
        step_str_1 = '准备一个锅，要能放下大鹅。倒入半锅清水。'
        material_str_1 = '直径36CM以上的大锅'

        cookbook = Cookbook.objects.create(
            name='铁锅炖大鹅'
        )
        cookbook.step_set.create(
            name=step_str_1,
            duration=datetime.timedelta(hours=10),
        )

        step1 = Step.objects.filter(name=step_str_1).first()
        step1.material_set.create(
            name=material_str_1,
            type=MaterialType.TOOL
        )

        material_1 = Material.objects.filter(name=material_str_1).first()
        self.assertIn(
            step1,
            cookbook.step_set.all()
        )

        self.assertIn(
            material_1,
            step1.material_set.all()
        )

        self.assertIn(
            material_1,
            cookbook.materials
        )

    def test_cookbook_tag(self):
        cookbook = Cookbook.objects.create(
            name='红油白斩鸡'
        )
        cookbook.add_tag(self.tag_hot)
        self.assertIn(
            cookbook,
            self.tag_hot.cookbook_set.all()
        )
        cookbook2 = Cookbook.objects.create(name='辣子雪糕')
        cookbook2.add_tag(self.tag_hot)

        self.assertEqual(2, self.tag_hot.cookbook_set.count())
        self.assertEqual(0, self.tag_too_hot.cookbook_set.count())

        # tag update cookbook_sum
        for tag in [self.tag_hot, self.tag_too_hot]:
            tag.update_cookbook_sum()

        self.assertEqual(2, self.tag_hot.cookbook_sum)
        self.assertEqual(0, self.tag_too_hot.cookbook_sum)
