from django.contrib import admin

from .models import Cookbook, Step, Material, CookbookTag


class StepInline(admin.TabularInline):
    model = Step
    fk_name = 'cookbook'
    extra = 1


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
