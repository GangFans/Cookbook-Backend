from rest_framework import serializers

from utils.mixins import EagerLoaderMixin

from .models import (
    CookbookTag,
    Cookbook,
    Step,
    Material,
    MaterialStepRelationship
)


class CookbookTagSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='tag-detail',
        lookup_field='pk'
    )

    class Meta:
        model = CookbookTag
        fields = (
            'id',
            'url',
            'name',
            'cookbook_sum',
        )


class MaterialStepRelationshipSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='material.id')
    name = serializers.ReadOnlyField(source='material.name')

    class Meta:
        model = MaterialStepRelationship
        fields = (
            'id',
            'name',
            'amount',
        )


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = (
            'id',
            'name',
        )


class StepSerializer(serializers.ModelSerializer, EagerLoaderMixin):
    material_set = serializers.SerializerMethodField()

    class Meta:
        model = Step
        fields = (
            'id',
            # 'url',
            'name',
            'detail',
            'img_url',
            'duration',
            'material_set',
        )

    def get_material_set(self, obj):
        qset = MaterialStepRelationship.objects.filter(step=obj)
        return [MaterialStepRelationshipSerializer(m).data for m in qset]


class CookbookSerializer(serializers.HyperlinkedModelSerializer, EagerLoaderMixin):
    """
    菜谱序列化器
    """
    tag_set = CookbookTagSerializer(many=True, read_only=True)

    SELECT_RELATED_FIELDS = []
    PREFETCH_RELATED_FIELDS = [
        'tag_set',
    ]

    class Meta:
        model = Cookbook
        fields = (
            'id',
            'url',
            'name',
            'url_video',
            'url_cover_image',
            'description',
            'tag_set',
        )


class CookbookDetailSerializer(CookbookSerializer):
    step_set = StepSerializer(many=True, read_only=True)

    class Meta:
        model = Cookbook
        fields = (
            'id',
            'url',
            'name',
            'url_video',
            'url_cover_image',
            'description',
            'step_set',
            'tag_set',
        )
