"""CFI-TECH — Admin formations"""

from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse
import csv
from .models import Domain, Trainer, Formation, Inscription


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'color_preview', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}

    def color_preview(self, obj):
        return format_html(
            '<span style="background:{};padding:4px 12px;border-radius:4px;color:white;font-size:11px;">{}</span>',
            obj.color, obj.color
        )
    color_preview.short_description = 'Couleur'


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('photo_preview', 'full_name', 'title', 'years_experience', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('full_name', 'title', 'certifications')

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height:40px;width:40px;border-radius:50%;object-fit:cover;" />', obj.photo.url)
        return '👤'
    photo_preview.short_description = 'Photo'


@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ('affiche_preview', 'title', 'domain', 'status', 'level', 'price_display',
                    'spots_display', 'start_date', 'is_featured', 'is_active')
    list_editable = ('status', 'is_featured', 'is_active')
    list_filter = ('domain', 'status', 'level', 'mode', 'is_featured', 'is_active')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_date'
    readonly_fields = ('views_count', 'created_at', 'updated_at', 'occupancy_bar')

    fieldsets = (
        ('📋 Informations générales', {
            'fields': ('domain', 'title', 'slug', 'subtitle', 'excerpt', 'affiche')
        }),
        ('📚 Détails pédagogiques', {
            'fields': ('description', 'level', 'mode', 'duration', 'schedule', 'trainer')
        }),
        ('📅 Planification', {
            'fields': ('status', 'start_date', 'end_date', 'registration_deadline', 'total_spots', 'registered_count', 'occupancy_bar')
        }),
        ('💰 Tarification', {
            'fields': ('is_free', 'price', 'price_note')
        }),
        ('📖 Programme', {
            'fields': ('objectives', 'program', 'prerequisites', 'certification'),
            'classes': ('collapse',)
        }),
        ('🔍 SEO & Affichage', {
            'fields': ('meta_description', 'is_featured', 'is_active', 'views_count'),
            'classes': ('collapse',)
        }),
    )

    def affiche_preview(self, obj):
        if obj.affiche:
            return format_html('<img src="{}" style="height:50px;border-radius:4px;" />', obj.affiche.url)
        return '🖼️'
    affiche_preview.short_description = 'Affiche'

    def price_display(self, obj):
        return obj.get_price_display()
    price_display.short_description = 'Prix'

    def spots_display(self, obj):
        pct = obj.occupancy_percent
        color = '#28a745' if pct < 70 else '#ffc107' if pct < 90 else '#dc3545'
        return format_html(
            '<span style="color:{};">{}/{} ({} restantes)</span>',
            color, obj.registered_count, obj.total_spots, obj.available_spots
        )
    spots_display.short_description = 'Places'

    def occupancy_bar(self, obj):
        pct = obj.occupancy_percent
        color = '#28a745' if pct < 70 else '#ffc107' if pct < 90 else '#dc3545'
        return format_html(
            '<div style="background:#eee;border-radius:4px;width:200px;">'
            '<div style="background:{};width:{}%;height:16px;border-radius:4px;"></div></div>'
            '<span style="font-size:11px;">{}/{} places occupées ({}%)</span>',
            color, pct, obj.registered_count, obj.total_spots, pct
        )
    occupancy_bar.short_description = 'Taux de remplissage'


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('reference', 'full_name', 'phone', 'email', 'formation', 'level',
                    'status', 'synced_to_sheets', 'created_at')
    list_editable = ('status',)
    list_filter = ('status', 'formation', 'level', 'synced_to_sheets')
    search_fields = ('last_name', 'first_name', 'email', 'phone', 'reference')
    date_hierarchy = 'created_at'
    readonly_fields = ('reference', 'created_at', 'updated_at')
    actions = ['export_csv', 'mark_confirmed', 'mark_cancelled']

    fieldsets = (
        ('👤 Candidat', {
            'fields': ('last_name', 'first_name', 'phone', 'email', 'address', 'level')
        }),
        ('📚 Formation', {
            'fields': ('formation', 'message')
        }),
        ('⚙️ Gestion', {
            'fields': ('status', 'reference', 'notes_admin', 'synced_to_sheets', 'created_at', 'updated_at')
        }),
    )

    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="inscriptions_cfitech.csv"'
        response.write('\ufeff')  # BOM pour Excel
        writer = csv.writer(response)
        writer.writerow(['Référence', 'Nom', 'Prénom', 'Téléphone', 'Email',
                        'Formation', 'Niveau', 'Statut', 'Date d\'inscription'])
        for obj in queryset:
            writer.writerow([
                obj.reference, obj.last_name, obj.first_name, obj.phone,
                obj.email, obj.formation, obj.get_level_display(),
                obj.get_status_display(), obj.created_at.strftime('%d/%m/%Y %H:%M')
            ])
        return response
    export_csv.short_description = 'Exporter en CSV'

    def mark_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
        self.message_user(request, f'{queryset.count()} inscription(s) confirmée(s).')
    mark_confirmed.short_description = 'Marquer comme confirmées'

    def mark_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, f'{queryset.count()} inscription(s) annulée(s).')
    mark_cancelled.short_description = 'Marquer comme annulées'
