"""
CFI-TECH — Modèles de l'application core
Gestion : Configuration site, Partenaires, Témoignages, FAQ, Blog, Newsletter
"""

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit


class SiteConfig(models.Model):
    """Configuration globale du site — singleton"""
    site_name = models.CharField('Nom du site', max_length=100, default='CFI-TECH')
    slogan = models.CharField('Slogan', max_length=200, default='Apprenez, Innovez, Réussissez avec CFI-TECH')
    logo = models.ImageField('Logo', upload_to='branding/', null=True, blank=True)
    banderole = models.ImageField('Banderole hero', upload_to='branding/', null=True, blank=True)
    phone = models.CharField('Téléphone', max_length=30, default='+223 78 78 73 39')
    whatsapp = models.CharField('WhatsApp', max_length=30, default='+22378787339')
    email = models.EmailField('Email', default='cfitech3@gmail.com')
    address = models.TextField('Adresse', default='Moussabougou, près du marché, descente du 3e pont, Bamako, Mali')
    google_maps_embed = models.TextField('Google Maps Embed URL', blank=True)
    facebook_url = models.URLField('Facebook', blank=True)
    instagram_url = models.URLField('Instagram', blank=True)
    linkedin_url = models.URLField('LinkedIn', blank=True)
    youtube_url = models.URLField('YouTube', blank=True)
    twitter_url = models.URLField('Twitter/X', blank=True)
    tiktok_url = models.URLField('TikTok', blank=True)
    meta_description = models.TextField('Meta description SEO', max_length=160, blank=True,
        default='CFI-TECH - Centre de Formation et d\'Innovation Technologique à Bamako, Mali. Formations en informatique, programmation, cybersécurité, IA, énergie solaire.')
    google_analytics_id = models.CharField('Google Analytics ID', max_length=50, blank=True)
    # Statistiques hero
    stat_etudiants = models.IntegerField('Étudiants formés', default=500)
    stat_reussite = models.IntegerField('Taux de réussite (%)', default=95)
    stat_formations = models.IntegerField('Formations', default=20)
    stat_certifications = models.IntegerField('Certifications délivrées', default=300)

    class Meta:
        verbose_name = 'Configuration du site'
        verbose_name_plural = 'Configuration du site'

    def __str__(self):
        return 'Configuration CFI-TECH'

    def save(self, *args, **kwargs):
        self.pk = 1  # Singleton
        super().save(*args, **kwargs)

    @classmethod
    def get_config(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Partner(models.Model):
    """Partenaires de CFI-TECH"""
    PARTNER_TYPES = [
        ('strategique', 'Partenaire Stratégique'),
        ('technique', 'Partenaire Technique'),
        ('academique', 'Partenaire Académique'),
        ('commercial', 'Partenaire Commercial'),
        ('institutionnel', 'Partenaire Institutionnel'),
    ]
    name = models.CharField('Nom du partenaire', max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    logo = ProcessedImageField(
        upload_to='partners/',
        processors=[ResizeToFit(300, 150)],
        format='PNG',
        options={'quality': 90},
        null=True, blank=True
    )
    partner_type = models.CharField('Type', max_length=20, choices=PARTNER_TYPES, default='strategique')
    description = RichTextField('Description', blank=True)
    services = models.TextField('Services offerts', blank=True)
    website_url = models.URLField('Site web', blank=True)
    facebook_url = models.URLField('Facebook', blank=True)
    linkedin_url = models.URLField('LinkedIn', blank=True)
    is_featured = models.BooleanField('Mise en avant', default=False)
    is_noor_energy = models.BooleanField('Noor Energy', default=False)
    display_order = models.IntegerField('Ordre d\'affichage', default=0)
    is_active = models.BooleanField('Actif', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Partenaire'
        verbose_name_plural = 'Partenaires'
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class NoorEnergyService(models.Model):
    """Services Noor Energy - partenariat énergétique"""
    ICONS = [
        ('solar-panel', '☀️ Énergie Solaire'),
        ('zap', '⚡ Électricité'),
        ('home', '🏠 Bâtiment'),
        ('wind', '💨 Climatisation'),
        ('activity', '📊 Audit'),
        ('tool', '🔧 Maintenance'),
    ]
    title = models.CharField('Titre', max_length=150)
    icon = models.CharField('Icône', max_length=30, choices=ICONS, default='zap')
    description = models.TextField('Description')
    image = models.ImageField('Image', upload_to='noor_energy/', null=True, blank=True)
    display_order = models.IntegerField('Ordre', default=0)
    is_active = models.BooleanField('Actif', default=True)

    class Meta:
        verbose_name = 'Service Noor Energy'
        verbose_name_plural = 'Services Noor Energy'
        ordering = ['display_order']

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    """Témoignages des diplômés / clients"""
    RATING_CHOICES = [(i, f'{i} étoile(s)') for i in range(1, 6)]
    full_name = models.CharField('Nom complet', max_length=100)
    job_title = models.CharField('Titre / Poste', max_length=100, blank=True)
    photo = ProcessedImageField(
        upload_to='testimonials/',
        processors=[ResizeToFill(120, 120)],
        format='JPEG',
        options={'quality': 85},
        null=True, blank=True
    )
    message = models.TextField('Témoignage')
    rating = models.IntegerField('Note', choices=RATING_CHOICES, default=5)
    formation_suivie = models.CharField('Formation suivie', max_length=150, blank=True)
    is_featured = models.BooleanField('À la une', default=False)
    is_active = models.BooleanField('Actif', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Témoignage'
        verbose_name_plural = 'Témoignages'
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return f'{self.full_name} — {self.rating}★'


class FAQ(models.Model):
    """Foire aux questions"""
    CATEGORIES = [
        ('general', 'Général'),
        ('formation', 'Formations'),
        ('inscription', 'Inscription'),
        ('paiement', 'Paiement'),
        ('certificat', 'Certificats'),
    ]
    question = models.CharField('Question', max_length=300)
    answer = RichTextField('Réponse')
    category = models.CharField('Catégorie', max_length=20, choices=CATEGORIES, default='general')
    display_order = models.IntegerField('Ordre', default=0)
    is_active = models.BooleanField('Actif', default=True)

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'
        ordering = ['category', 'display_order']

    def __str__(self):
        return self.question


class BlogPost(models.Model):
    """Articles de blog / actualités"""
    STATUS = [('draft', 'Brouillon'), ('published', 'Publié')]
    title = models.CharField('Titre', max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.TextField('Résumé', max_length=300)
    content = RichTextField('Contenu')
    thumbnail = ProcessedImageField(
        upload_to='blog/',
        processors=[ResizeToFill(800, 450)],
        format='JPEG',
        options={'quality': 85},
        null=True, blank=True
    )
    author_name = models.CharField('Auteur', max_length=100, default='Équipe CFI-TECH')
    category = models.CharField('Catégorie', max_length=100, blank=True)
    tags = models.CharField('Tags (séparés par virgule)', max_length=300, blank=True)
    status = models.CharField('Statut', max_length=10, choices=STATUS, default='draft')
    is_featured = models.BooleanField('À la une', default=False)
    meta_description = models.CharField('Meta description', max_length=160, blank=True)
    views_count = models.IntegerField('Vues', default=0)
    published_at = models.DateTimeField('Date de publication', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Article de blog'
        verbose_name_plural = 'Articles de blog'
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('core:blog_detail', kwargs={'slug': self.slug})


class NewsletterSubscriber(models.Model):
    """Abonnés à la newsletter"""
    email = models.EmailField('Email', unique=True)
    full_name = models.CharField('Nom complet', max_length=100, blank=True)
    is_active = models.BooleanField('Actif', default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Abonné Newsletter'
        verbose_name_plural = 'Abonnés Newsletter'
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email


class GalleryItem(models.Model):
    """Galerie photo/vidéo"""
    MEDIA_TYPES = [('photo', 'Photo'), ('video', 'Vidéo')]
    title = models.CharField('Titre', max_length=150)
    media_type = models.CharField('Type', max_length=10, choices=MEDIA_TYPES, default='photo')
    image = ProcessedImageField(
        upload_to='gallery/',
        processors=[ResizeToFit(1200, 800)],
        format='JPEG',
        options={'quality': 85},
        null=True, blank=True
    )
    video_url = models.URLField('URL Vidéo YouTube/Vimeo', blank=True)
    description = models.TextField('Description', blank=True)
    event_name = models.CharField('Événement', max_length=150, blank=True)
    is_active = models.BooleanField('Actif', default=True)
    display_order = models.IntegerField('Ordre', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Élément galerie'
        verbose_name_plural = 'Galerie'
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    """Membres de l'équipe CFI-TECH"""
    full_name = models.CharField('Nom complet', max_length=100)
    job_title = models.CharField('Poste', max_length=100)
    bio = models.TextField('Biographie', blank=True)
    photo = ProcessedImageField(
        upload_to='team/',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 85},
        null=True, blank=True
    )
    linkedin_url = models.URLField('LinkedIn', blank=True)
    speciality = models.CharField('Spécialité', max_length=200, blank=True)
    display_order = models.IntegerField('Ordre', default=0)
    is_active = models.BooleanField('Actif', default=True)

    class Meta:
        verbose_name = 'Membre équipe'
        verbose_name_plural = "Membres de l'équipe"
        ordering = ['display_order']

    def __str__(self):
        return f'{self.full_name} — {self.job_title}'


class ContactMessage(models.Model):
    """Messages reçus via le formulaire de contact"""
    STATUS_CHOICES = [
        ('new',     'Nouveau'),
        ('read',    'Lu'),
        ('replied', 'Répondu'),
        ('closed',  'Fermé'),
    ]
    name    = models.CharField('Nom complet', max_length=100)
    email   = models.EmailField('Email', blank=True)
    phone   = models.CharField('Téléphone', max_length=30, blank=True)
    subject = models.CharField('Objet', max_length=200, blank=True)
    message = models.TextField('Message')
    status  = models.CharField(
        'Statut', max_length=10,
        choices=STATUS_CHOICES, default='new'
    )
    notes_admin = models.TextField('Notes admin', blank=True)
    ip_address  = models.GenericIPAddressField('IP', null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name          = 'Message de contact'
        verbose_name_plural   = 'Messages de contact'
        ordering              = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.subject or "Sans objet"} ({self.created_at.strftime("%d/%m/%Y")})'