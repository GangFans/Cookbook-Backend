from django.contrib import admin

from .models import Cookbook, Step, Material, CookbookTag


class StepInline(admin.TabularInline):
    model = Step
    fk_name = 'cookbook'
    extra = 1
    fields = ('name', 'duration', 'admin_material_set_list', 'admin_change_page_link')
    readonly_fields = ('admin_material_set_list', 'admin_change_page_link')


@admin.register(Cookbook)
class CookBookAdmin(admin.ModelAdmin):
    inlines = (StepInline, )
    list_display = ('name', )
    pass


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    pass


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    pass


@admin.register(CookbookTag)
class CookbookTagAdmin(admin.ModelAdmin):
    pass
