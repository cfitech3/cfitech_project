"""
CFI-TECH — Modèles des formations
Domaines, Formations, Formateurs, Inscriptions
"""

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit, ResizeToFill


class Domain(models.Model):
    """Domaines de formation"""
    ICONS = [
        ('monitor', 'Informatique générale'),
        ('code', 'Programmation'),
        ('globe', 'Développement Web'),
        ('wifi', 'Réseau'),
        ('shield', 'Cybersécurité'),
        ('cpu', 'Intelligence Artificielle'),
        ('file-text', 'Bureautique'),
        ('zap', 'Électricité'),
        ('sun', 'Énergie Solaire'),
        ('package', 'Logistique'),
        ('trending-up', 'Comptabilité'),
        ('bar-chart', 'Marketing'),
        ('message-square', 'Anglais'),
        ('star', 'Développement Personnel'),
        ('settings', 'Autres'),
    ]
    name = models.CharField('Nom du domaine', max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField('Icône', max_length=30, choices=ICONS, default='monitor')
    color = models.CharField('Couleur accent (hex)', max_length=7, default='#1565C0')
    description = models.TextField('Description', blank=True)
    display_order = models.IntegerField('Ordre', default=0)
    is_active = models.BooleanField('Actif', default=True)

    class Meta:
        verbose_name = 'Domaine'
        verbose_name_plural = 'Domaines de formation'
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_active_formations(self):
        return self.formations.filter(is_active=True)


class Trainer(models.Model):
    """Formateurs / Instructeurs"""
    full_name = models.CharField('Nom complet', max_length=100)
    title = models.CharField('Titre / Expertise', max_length=150)
    bio = models.TextField('Biographie', blank=True)
    photo = ProcessedImageField(
        upload_to='trainers/',
        processors=[ResizeToFill(200, 200)],
        format='JPEG',
        options={'quality': 85},
        null=True, blank=True
    )
    linkedin_url = models.URLField('LinkedIn', blank=True)
    email = models.EmailField('Email professionnel', blank=True)
    years_experience = models.IntegerField('Années d\'expérience', default=0)
    certifications = models.TextField('Certifications', blank=True)
    is_active = models.BooleanField('Actif', default=True)

    class Meta:
        verbose_name = 'Formateur'
        verbose_name_plural = 'Formateurs'

    def __str__(self):
        return f'{self.full_name} — {self.title}'


class Formation(models.Model):
    """Formation / Cours"""
    LEVELS = [
        ('debutant', 'Débutant'),
        ('intermediaire', 'Intermédiaire'),
        ('avance', 'Avancé'),
        ('tous', 'Tous niveaux'),
    ]
    MODES = [
        ('presentiel', 'Présentiel'),
        ('distance', 'À distance'),
        ('hybride', 'Hybride'),
    ]
    STATUS = [
        ('coming_soon', 'Bientôt disponible'),
        ('open', 'Inscriptions ouvertes'),
        ('full', 'Complet'),
        ('ongoing', 'En cours'),
        ('finished', 'Terminé'),
    ]

    # Informations de base
    domain = models.ForeignKey(Domain, on_delete=models.SET_NULL, null=True, related_name='formations', verbose_name='Domaine')
    title = models.CharField('Titre de la formation', max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    subtitle = models.CharField('Sous-titre', max_length=200, blank=True)
    description = RichTextField('Description complète')
    excerpt = models.TextField('Résumé court', max_length=300)

    # Visuel
    affiche = ProcessedImageField(
        upload_to='formations/affiches/',
        processors=[ResizeToFit(1024, 1024)],
        format='JPEG',
        options={'quality': 90},
        null=True, blank=True,
        verbose_name='Affiche (1024x1024)'
    )

    # Détails pédagogiques
    level = models.CharField('Niveau', max_length=20, choices=LEVELS, default='tous')
    mode = models.CharField('Mode', max_length=20, choices=MODES, default='presentiel')
    duration = models.CharField('Durée (ex: 3 mois, 40h)', max_length=100)
    schedule = models.CharField('Horaires', max_length=200, blank=True, help_text='Ex: Lun/Mer/Ven 18h-20h')
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, blank=True, related_name='formations', verbose_name='Formateur')

    # Inscription & Disponibilité
    status = models.CharField('Statut', max_length=20, choices=STATUS, default='coming_soon')
    start_date = models.DateField('Date de début', null=True, blank=True)
    end_date = models.DateField('Date de fin', null=True, blank=True)
    registration_deadline = models.DateField('Date limite d\'inscription', null=True, blank=True)
    total_spots = models.IntegerField('Places totales', default=30)
    registered_count = models.IntegerField('Inscrits', default=0)

    # Prix
    price = models.DecimalField('Prix (FCFA)', max_digits=10, decimal_places=0, default=0)
    price_note = models.CharField('Note sur le prix', max_length=200, blank=True, help_text='Ex: Facilités de paiement disponibles')
    is_free = models.BooleanField('Formation gratuite', default=False)

    # Programme
    program = RichTextField('Programme / Contenu', blank=True)
    prerequisites = models.TextField('Prérequis', blank=True)
    objectives = models.TextField('Objectifs', blank=True)
    certification = models.CharField('Certification délivrée', max_length=200, blank=True)

    # SEO & Affichage
    meta_description = models.CharField('Meta description', max_length=160, blank=True)
    is_featured = models.BooleanField('Formation à la une', default=False)
    is_active = models.BooleanField('Active', default=True)
    views_count = models.IntegerField('Vues', default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Formation'
        verbose_name_plural = 'Formations'
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('formations:detail', kwargs={'slug': self.slug})

    @property
    def available_spots(self):
        return max(0, self.total_spots - self.registered_count)

    @property
    def is_full(self):
        return self.available_spots == 0

    @property
    def is_registration_open(self):
        if self.status != 'open':
            return False
        if self.registration_deadline and self.registration_deadline < timezone.now().date():
            return False
        return not self.is_full

    @property
    def occupancy_percent(self):
        if self.total_spots == 0:
            return 0
        return min(100, int((self.registered_count / self.total_spots) * 100))

    def get_price_display(self):
        if self.is_free:
            return 'Gratuit'
        return f'{int(self.price):,} FCFA'.replace(',', ' ')


class Inscription(models.Model):
    """Inscriptions aux formations"""
    LEVELS = [
        ('aucun', 'Aucun'),
        ('primaire', 'Primaire'),
        ('college', 'Collège'),
        ('lycee', 'Lycée'),
        ('bac', 'Baccalauréat'),
        ('licence', 'Licence / BTS'),
        ('master', 'Master / Ingénieur'),
        ('doctorat', 'Doctorat'),
        ('professionnel', 'Professionnel'),
    ]
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmé'),
        ('cancelled', 'Annulé'),
        ('completed', 'Terminé'),
    ]

    # Informations personnelles
    last_name = models.CharField('Nom', max_length=100)
    first_name = models.CharField('Prénom', max_length=100)
    phone = models.CharField('Téléphone', max_length=30)
    email = models.EmailField('Email')
    address = models.CharField('Adresse / Quartier', max_length=200, blank=True)

    # Formation
    formation = models.ForeignKey(Formation, on_delete=models.SET_NULL, null=True, related_name='inscriptions', verbose_name='Formation')
    level = models.CharField('Niveau d\'études', max_length=20, choices=LEVELS, default='lycee')
    message = models.TextField('Message / Questions', blank=True)

    # Gestion
    status = models.CharField('Statut', max_length=20, choices=STATUS_CHOICES, default='pending')
    reference = models.CharField('Référence', max_length=20, unique=True, blank=True)
    notes_admin = models.TextField('Notes administrateur', blank=True)
    synced_to_sheets = models.BooleanField('Synchronisé Google Sheets', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Inscription'
        verbose_name_plural = 'Inscriptions'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.last_name} {self.first_name} — {self.formation}'

    def save(self, *args, **kwargs):
        if not self.reference:
            import random, string
            self.reference = 'CFI-' + ''.join(random.choices(string.digits, k=6))
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
