from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Cookbook, Step, Material, CookbookTag


class StepInline(admin.TabularInline):
    model = Step
    fk_name = 'cookbook'
    extra = 1
    fields = ('name', 'duration', 'admin_material_set_list', 'admin_change_page_link')
    readonly_fields = ('admin_material_set_list', 'admin_change_page_link')


class TagInline(admin.TabularInline):
    model = Cookbook.tag_set.through
    extra = 1


class MaterialInline(admin.TabularInline):
    model = Material.step.through
    extra = 1


class CookbookTagFilter(admin.SimpleListFilter):
    title = _('标签筛选')
    parameter_name = 'tag'

    def lookups(self, request, model_admin):
        return (
            (tag.id, tag.name)
            for tag in CookbookTag.objects.all()
        )

    def queryset(self, request, queryset):
        return queryset.filter(tag_set__id=self.value())


@admin.register(Cookbook)
class CookBookAdmin(admin.ModelAdmin):
    inlines = (StepInline, TagInline)
    list_display = ('name',)
    list_filter = (CookbookTagFilter,)


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin_cookbook_url')
    inlines = (MaterialInline,)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_filter = ('type',)


@admin.register(CookbookTag)
class CookbookTagAdmin(admin.ModelAdmin):
    pass
