"""CFI-TECH — Modèles des services"""

from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from ckeditor.fields import RichTextField


class Service(models.Model):
    """Services proposés par CFI-TECH"""
    ICONS = [
        ('monitor', '🖥️ Installation informatique'),
        ('tool', '🔧 Maintenance'),
        ('wifi', '📶 Réseau & Sécurité'),
        ('globe', '🌐 Développement Web'),
        ('smartphone', '📱 Développement Mobile'),
        ('shopping-bag', '🛍️ Vente matériels'),
        ('briefcase', '💼 Conseil IT'),
        ('trending-up', '📈 Consulting Digital'),
        ('headphones', '🎧 Support Technique'),
    ]
    title = models.CharField('Titre du service', max_length=150)
    icon = models.CharField('Icône', max_length=30, choices=ICONS, default='monitor')
    short_description = models.CharField('Description courte', max_length=200)
    description = RichTextField('Description complète', blank=True)
    image = ProcessedImageField(
        upload_to='services/',
        processors=[ResizeToFit(800, 500)],
        format='JPEG',
        options={'quality': 85},
        null=True, blank=True
    )
    features = models.TextField('Fonctionnalités (une par ligne)', blank=True)
    price_info = models.CharField('Info tarif', max_length=200, blank=True)
    cta_text = models.CharField('Texte bouton CTA', max_length=50, default='Demander un devis')
    display_order = models.IntegerField('Ordre', default=0)
    is_active = models.BooleanField('Actif', default=True)
    is_featured = models.BooleanField('Mis en avant', default=False)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['display_order']

    def __str__(self):
        return self.title

    def get_features_list(self):
        return [f.strip() for f in self.features.split('\n') if f.strip()]


class Logiciel(models.Model):
    """Logiciels utilisés ou vendus par CFI-TECH"""
    CATEGORIES = [
        ('bureautique',   'Bureautique'),
        ('comptabilite',  'Comptabilité'),
        ('gestion',       'Gestion'),
        ('securite',      'Sécurité'),
        ('developpement', 'Développement'),
        ('design',        'Design & Création'),
        ('reseau',        'Réseau & Système'),
        ('autre',         'Autre'),
    ]
    name           = models.CharField('Nom du logiciel', max_length=100)
    category       = models.CharField('Catégorie', max_length=20,
                                       choices=CATEGORIES, default='bureautique')
    logo           = models.ImageField('Logo', upload_to='logiciels/',
                                        null=True, blank=True)
    description    = models.TextField('Description', blank=True)
    version        = models.CharField('Version', max_length=50, blank=True)
    editor         = models.CharField('Éditeur', max_length=100, blank=True)
    website_url    = models.URLField('Site officiel', blank=True)
    is_free        = models.BooleanField('Gratuit / Open source', default=False)
    price_info     = models.CharField('Info tarif', max_length=200, blank=True)
    is_formation   = models.BooleanField('Utilisé en formation', default=True)
    is_sale        = models.BooleanField('Disponible à la vente', default=False)
    is_featured    = models.BooleanField('Mis en avant', default=False)
    is_active      = models.BooleanField('Actif', default=True)
    display_order  = models.IntegerField('Ordre', default=0)

    class Meta:
        verbose_name          = 'Logiciel'
        verbose_name_plural   = 'Logiciels'
        ordering              = ['display_order', 'name']

    def __str__(self):
        return f'{self.name} — {self.get_category_display()}'