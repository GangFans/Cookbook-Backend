from django.http import JsonResponse
from django.test import TestCase, Client
from django.urls import reverse
import json

from Cookbook.defines import MaterialType
from Cookbook.models import (
    CookbookTag,
    Cookbook,
    Material,
    MaterialStepRelationship,
)


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.tag = CookbookTag.objects.create(name='测试标签1')
        CookbookTag.objects.create(name='测试标签2')
        CookbookTag.objects.create(name='测试标签3')

        self.cookbook_checked = Cookbook.objects.create(
            name='红油白斩鸡', checked=True
        )
        self.cookbook_checked.add_tag(self.tag)
        self.the_step = self.cookbook_checked.step_set.create(
            name='白斩鸡切块',
        )

        self.the_material = Material.objects.create(
            name='白斩鸡',
            type=MaterialType.FOOD.value
        )
        MaterialStepRelationship.objects.create(
            step=self.the_step,
            material=self.the_material,
            amount='1000克'
        )

        self.cookbook_unchecked = Cookbook.objects.create(
            name='蒜蓉辣椒'
        )

    def test_version(self):
        response: JsonResponse = self.client.get(reverse('Book:version'))
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertIn('data', content)
        self.assertEqual(content['data'], 'v0.0.1')

    def test_tag_list(self):
        response: JsonResponse = self.client.get(reverse('tag-list'))
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        # response content should be a Array with 3 node
        self.assertEqual(len(content), 3)
        self.assertEqual(content[0]['id'], 1)
        self.assertEqual(content[0]['name'], '测试标签1')
        self.assertEqual(content[0]['cookbook_sum'], 0)  # default cookbook_sum is 0

        self.tag.update_cookbook_sum()

        response: JsonResponse = self.client.get(reverse('tag-list'))
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        # response content should be a Array with 3 node
        self.assertEqual(len(content), 3)
        self.assertEqual(content[0]['id'], 1)
        self.assertEqual(content[0]['name'], '测试标签1')
        self.assertEqual(content[0]['cookbook_sum'], 1)  # updated

    def test_cookbook_list(self):
        # test cookbook list api only show public Cookbook
        response: JsonResponse = self.client.get(reverse('cookbook-list'))
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['count'], 1)
        self.assertEqual(content['data'][0]['name'], '红油白斩鸡')

        self.cookbook_unchecked.checked = True
        self.cookbook_unchecked.save()

        response: JsonResponse = self.client.get(reverse('cookbook-list'))
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['count'], 2)

        # test tag filter
        response: JsonResponse = self.client.get(
            reverse('cookbook-list'), data={'tag_set': self.tag.id}
        )
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['count'], 1)
        self.assertEqual(content['data'][0]['name'], '红油白斩鸡')

    def test_cookbook_detail(self):
        response: JsonResponse = self.client.get(
            reverse('cookbook-detail', args=(self.cookbook_checked.id,))
        )
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        print(content)
        self.assertEqual(content['name'], '红油白斩鸡')
        # check tag
        self.assertEqual(content['tag_set'][0]['name'], self.tag.name)
        # check step
        self.assertEqual(content['step_set'][0]['name'], self.the_step.name)
        # check step's material
        self.assertEqual(
            content['step_set'][0]['material_set'][0]['name'],
            self.the_material.name
        )
        self.assertEqual(
            content['step_set'][0]['material_set'][0]['amount'],
            '1000克'
        )
