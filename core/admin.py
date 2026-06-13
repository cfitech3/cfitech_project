from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import redirect
from .models import ContactMessage
from .models import (
    SiteConfig, Partner, NoorEnergyService, Testimonial,
    FAQ, BlogPost, NewsletterSubscriber, GalleryItem, TeamMember
)


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ('🏢 Identité', {
            'fields': ('site_name', 'slogan', 'logo', 'banderole')
        }),
        ('📞 Coordonnées', {
            'fields': ('phone', 'whatsapp', 'email', 'address', 'google_maps_embed')
        }),
        ('📱 Réseaux sociaux', {
            'fields': ('facebook_url', 'instagram_url', 'linkedin_url',
                       'youtube_url', 'twitter_url', 'tiktok_url'),
            'classes': ('collapse',)
        }),
        ('📊 Statistiques', {
            'fields': ('stat_etudiants', 'stat_reussite',
                       'stat_formations', 'stat_certifications')
        }),
        ('🔍 SEO', {
            'fields': ('meta_description', 'google_analytics_id'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return not SiteConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj, created = SiteConfig.objects.get_or_create(pk=1)
        return redirect(
            f'/cfitech-admin/core/siteconfig/{obj.pk}/change/'
        )


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('logo_preview', 'name', 'partner_type',
                    'is_featured', 'is_noor_energy', 'is_active', 'display_order')
    list_editable = ('is_featured', 'is_active', 'display_order', 'is_noor_energy')
    list_filter = ('partner_type', 'is_featured', 'is_noor_energy', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="height:40px;border-radius:4px;" />',
                obj.logo.url
            )
        return '—'
    logo_preview.short_description = 'Logo'


@admin.register(NoorEnergyService)
class NoorEnergyServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('photo_preview', 'full_name', 'job_title',
                    'rating_stars', 'formation_suivie', 'is_featured', 'is_active')
    list_editable = ('is_featured', 'is_active')
    list_filter = ('rating', 'is_featured', 'is_active')
    search_fields = ('full_name', 'message')

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="height:40px;width:40px;'
                'border-radius:50%;object-fit:cover;" />',
                obj.photo.url
            )
        return '👤'
    photo_preview.short_description = 'Photo'

    def rating_stars(self, obj):
        return '★' * obj.rating + '☆' * (5 - obj.rating)
    rating_stars.short_description = 'Note'


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('question',)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_preview', 'title', 'author_name',
                    'category', 'status', 'is_featured', 'views_count', 'published_at')
    list_editable = ('status', 'is_featured')
    list_filter = ('status', 'is_featured', 'category')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views_count', 'created_at', 'updated_at')

    fieldsets = (
        ('📝 Contenu', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'thumbnail')
        }),
        ('👤 Auteur & Catégorie', {
            'fields': ('author_name', 'category', 'tags')
        }),
        ('⚙️ Publication', {
            'fields': ('status', 'is_featured', 'published_at')
        }),
        ('🔍 SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
        ('📊 Stats', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="height:40px;border-radius:4px;" />',
                obj.thumbnail.url
            )
        return '📷'
    thumbnail_preview.short_description = 'Image'


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'is_active', 'subscribed_at')
    list_editable = ('is_active',)
    search_fields = ('email', 'full_name')
    actions = ['export_emails']

    def export_emails(self, request, queryset):
        emails = ', '.join(
            queryset.filter(is_active=True).values_list('email', flat=True)
        )
        self.message_user(request, f'Emails : {emails}')
    export_emails.short_description = 'Exporter les emails'


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title', 'media_type',
                    'event_name', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    list_filter = ('media_type', 'is_active')

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:50px;border-radius:4px;" />',
                obj.image.url
            )
        return '🎬'
    image_preview.short_description = 'Aperçu'


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('photo_preview', 'full_name', 'job_title',
                    'speciality', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    search_fields = ('full_name', 'job_title')

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="height:40px;width:40px;'
                'border-radius:50%;object-fit:cover;" />',
                obj.photo.url
            )
        return '👤'
    photo_preview.short_description = 'Photo'

   

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'phone', 'subject',
                     'status', 'status_badge', 'created_at')
    list_editable = ('status',)
    list_filter   = ('status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'phone', 'subject',
                       'message', 'ip_address', 'created_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('👤 Expéditeur', {
            'fields': ('name', 'email', 'phone')
        }),
        ('💬 Message', {
            'fields': ('subject', 'message')
        }),
        ('⚙️ Gestion', {
            'fields': ('status', 'notes_admin', 'ip_address', 'created_at')
        }),
    )

    def status_badge(self, obj):
        colors = {
            'new':     ('#E3F2FD', '#1565C0'),
            'read':    ('#FFF9C4', '#F57F17'),
            'replied': ('#E8F5E9', '#2E7D32'),
            'closed':  ('#F5F5F5', '#757575'),
        }
        bg, color = colors.get(obj.status, ('#F5F5F5', '#333'))
        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;'
            'border-radius:100px;font-size:12px;font-weight:600;">{}</span>',
            bg, color, obj.get_status_display()
        )
    status_badge.short_description = 'Aperçu statut'

    def has_add_permission(self, request):
        return False