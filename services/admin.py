from django.contrib import admin
from django.utils.html import format_html
from .models import Service, Logiciel


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display  = ('title', 'icon', 'display_order', 'is_featured', 'is_active')
    list_editable = ('display_order', 'is_featured', 'is_active')
    search_fields = ('title', 'short_description')


@admin.register(Logiciel)
class LogicielAdmin(admin.ModelAdmin):
    list_display  = ('logo_preview', 'name', 'editor', 'category',
                     'version', 'is_free', 'is_formation',
                     'is_sale', 'is_featured', 'is_active', 'display_order')
    list_editable = ('is_featured', 'is_active', 'display_order',
                     'is_formation', 'is_sale')
    list_filter   = ('category', 'is_free', 'is_formation',
                     'is_sale', 'is_featured', 'is_active')
    search_fields = ('name', 'editor', 'description')
    ordering      = ('display_order', 'name')

    fieldsets = (
        ('🖥️ Informations', {
            'fields': ('name', 'logo', 'category', 'editor',
                       'version', 'description', 'website_url')
        }),
        ('💰 Tarification', {
            'fields': ('is_free', 'price_info')
        }),
        ('⚙️ Affichage', {
            'fields': ('is_formation', 'is_sale', 'is_featured',
                       'is_active', 'display_order')
        }),
    )

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="height:36px;width:36px;'
                'object-fit:contain;border-radius:6px;" />',
                obj.logo.url
            )
        return format_html(
            '<div style="width:36px;height:36px;background:#E3F2FD;'
            'border-radius:6px;display:flex;align-items:center;'
            'justify-content:center;font-size:16px;">🖥️</div>'
        )
    logo_preview.short_description = 'Logo'