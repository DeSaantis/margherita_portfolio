from django.db import models
from django.utils import translation, timezone
from django_ckeditor_5.fields import CKEditor5Field

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

from bs4 import BeautifulSoup

def strip_outer_p(html):
    """Rimuove il <p> esterno se è l'unico tag che avvolge tutto il contenuto."""
    if not html:
        return html
    soup = BeautifulSoup(html, "html.parser")
    if len(soup.contents) == 1 and soup.contents[0].name == 'p':
        # Ritorna solo il contenuto interno del <p>, mantenendo eventuali tag interni
        return ''.join(str(c) for c in soup.contents[0].contents)
    return html


class SectionPainting(models.Model):
    section = CKEditor5Field(
        max_length=50,
        config_name='title',  # editor piccolo per titoli
        default=""
    )
    section_en = CKEditor5Field(
        max_length=50,
        blank=True,
        config_name='title',
        default=""
    )
    
    # Descrizioni facoltative, default vuoto
    description = CKEditor5Field(
        blank=True,
        config_name='description',  # editor più grande per descrizioni
        default=""
    )
    description_en = CKEditor5Field(
        blank=True,
        config_name='description',
        default=""
    )
    
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        
    def save(self, *args, **kwargs):
        # Pulizia dei <p> esterni
        self.section = strip_outer_p(self.section)
        self.section_en = strip_outer_p(self.section_en)
        self.description = strip_outer_p(self.description)
        self.description_en = strip_outer_p(self.description_en)
        super().save(*args, **kwargs)

    def __str__(self):
        # fallback sicuro se description è vuoto
        desc_preview = self.description[:50] if self.description else ''
        return f"{self.section} - {desc_preview}"

    @property
    def localized_section(self):
        lang = translation.get_language()
        if lang == 'en' and self.section_en:
            return self.section_en
        return self.section

    @property
    def localized_description(self):
        lang = translation.get_language()
        if lang == 'en' and self.description_en:
            return self.description_en
        return self.description


class Painting(models.Model):

    STATUS_CHOICES = [
        ('available', 'Disponibile'),
        ('sold', 'Venduto'),
        ('not_for_sale', 'Non in vendita'),
        ('custom', 'Testo personalizzato'),
    ]
    
    section = models.ForeignKey(SectionPainting, on_delete=models.PROTECT)

    title = CKEditor5Field(max_length=50, config_name='title', default="")
    title_en = CKEditor5Field(max_length=50, blank=True, config_name='title', default="")
    
    description = CKEditor5Field(blank=True, config_name='description', default="")
    description_en = CKEditor5Field(blank=True, config_name='description', default="")
    
    details = CKEditor5Field(blank=True, config_name='details', default="")
    details_en = CKEditor5Field(blank=True, config_name='details', default="")
    
    image = models.ImageField(
        upload_to='margherita_poli/files/painting',
        blank=True,
        null=True
    )
    
    thumb = ImageSpecField(
        source='image',
        processors=[ResizeToFit(width=600)],
        format='JPEG',
        options={'quality': 70}
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )

    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True
    )

    custom_price_text = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="'Testo personalizzato'"
    )
    
    custom_price_text_en = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="'Custom text'"
    )
    
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

        
    def save(self, *args, **kwargs):
        # Pulizia dei <p> esterni
        self.title = strip_outer_p(self.title)
        self.title_en = strip_outer_p(self.title_en)
        self.description = strip_outer_p(self.description)
        self.description_en = strip_outer_p(self.description_en)
        self.details = strip_outer_p(self.details)
        self.details_en = strip_outer_p(self.details_en)
        super().save(*args, **kwargs)

    def __str__(self):
        desc_preview = self.description[:50] if self.description else ''
        return f"{self.title} - {desc_preview} - {self.details}"

    @property
    def display_price(self):
        lang = translation.get_language()

        if self.status == 'sold':
            return "Sold" if lang == "en" else "Venduto"

        if self.status == 'not_for_sale':
            return "Not for sale" if lang == "en" else "Non in vendita"

        if self.status == 'custom':
            # Versione custom bilingue
            if lang == "en" and self.custom_price_text_en:
                return self.custom_price_text_en
            return self.custom_price_text or ""

        if self.price is not None:
            return f"{self.price} €"

        return ""

    @property
    def localized_title(self):
        lang = translation.get_language()
        if lang == 'en' and self.title_en:
            return self.title_en
        return self.title

    @property
    def localized_description(self):
        lang = translation.get_language()
        if lang == 'en' and self.description_en:
            return self.description_en
        return self.description
    
    @property
    def localized_details(self):
        lang = translation.get_language()
        if lang == 'en' and self.details_en:
            return self.details_en
        return self.details


class Poem(models.Model):
    image = models.ImageField(
        upload_to='margherita_poli/files/poem',
        blank=False,
    )
    
    thumb = ImageSpecField(
        source='image',
        processors=[ResizeToFit(width=600)],
        format='JPEG',
        options={'quality': 70}
    )
    
    date = models.DateField(blank=False)

    class Meta:
        ordering = ['-date']   # <-- Ordina automaticamente dal più recente al meno recente

    def __str__(self):
        # restituisce una stringa per evitare errori (dato che date è un oggetto date)
        return self.date.strftime("%d/%m/%Y")
    
class Illustration(models.Model):
    image = models.ImageField(
        upload_to='margherita_poli/files/illustration',
        blank=False,
        )
    
    thumb = ImageSpecField(
        source='image',
        processors=[ResizeToFit(width=600)],
        format='JPEG',
        options={'quality': 70}
    )
        
    order = models.PositiveIntegerField(default=0, help_text="Ordine di visualizzazione")

    class Meta:
        ordering = ['order']
    
class SectionExhibition(models.Model):
    section = CKEditor5Field(
        max_length=60,
        config_name='title',  # editor piccolo per titoli
        default=""
    )
    section_en = CKEditor5Field(
        max_length=60,
        blank=True,
        config_name='title',
        default=""
    )
    
    # Descrizioni facoltative, default vuoto
    description = CKEditor5Field(
        blank=True,
        config_name='description',  # editor più grande per descrizioni
        default=""
    )
    description_en = CKEditor5Field(
        blank=True,
        config_name='description',
        default=""
    )
    
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        
    def save(self, *args, **kwargs):
        # Pulizia dei <p> esterni
        self.section = strip_outer_p(self.section)
        self.section_en = strip_outer_p(self.section_en)
        self.description = strip_outer_p(self.description)
        self.description_en = strip_outer_p(self.description_en)
        super().save(*args, **kwargs)

    def __str__(self):
        # fallback sicuro se description è vuoto
        desc_preview = self.description[:50] if self.description else ''
        return f"{self.section} - {desc_preview}"

    @property
    def localized_section(self):
        lang = translation.get_language()
        if lang == 'en' and self.section_en:
            return self.section_en
        return self.section

    @property
    def localized_description(self):
        lang = translation.get_language()
        if lang == 'en' and self.description_en:
            return self.description_en
        return self.description
    
    
class Exhibition(models.Model):
    section = models.ForeignKey(SectionExhibition, on_delete=models.PROTECT)
    
    image = models.ImageField(
        upload_to='margherita_poli/files/exhibition',
        blank=True,
        null=True
    )
    
    thumb = ImageSpecField(
        source='image',
        processors=[ResizeToFit(width=600)],
        format='JPEG',
        options={'quality': 70}
    )
    
    order = models.PositiveIntegerField(default=0, help_text="Ordine di visualizzazione")

    class Meta:
        ordering = ['order']

class Post(models.Model):
    titolo_it = models.CharField("Titolo (Italiano)", max_length=200)
    titolo_en = models.CharField("Titolo (Inglese)", max_length=200, blank=True, null=True)
    contenuto_it = models.TextField("Contenuto (Italiano)")
    contenuto_en = models.TextField("Contenuto (Inglese)", blank=True, null=True)

    def titolo(self, lang):
        if lang == 'en' and self.titolo_en:
            return self.titolo_en
        return self.titolo_it

    def contenuto(self, lang):
        if lang == 'en' and self.contenuto_en:
            return self.contenuto_en
        return self.contenuto_it

    def __str__(self):
        return self.titolo_it
    
    
# =========== modello per gli ordini =========

class Order(models.Model):
    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    customer_address = models.CharField(max_length=200)
    customer_city = models.CharField(max_length=100)
    customer_region = models.CharField(max_length=100)
    customer_zip = models.CharField(max_length=10)
    customer_country = models.CharField(max_length=100)

    created_at = models.DateTimeField(default=timezone.now)

    STATUS = [
        ("pending", "In attesa"),
        ("paid", "Pagato"),
        ("failed", "Fallito"),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default="pending")

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    payment_intent_id = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Ordine #{self.id} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    painting = models.ForeignKey(Painting, on_delete=models.PROTECT)

    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item #{self.id} - {self.title}"
    
# modello per messaggi dalla sezione teacher

class ContactMessage(models.Model):
    fullname = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Messaggio ricevuto"
        verbose_name_plural = "Messaggi ricevuti"

    STATUS = [
        ("unread", "Non letto"),
        ("read", "Letto"),
    ]
    status = models.CharField(max_length=10, choices=STATUS, default="unread")

    def __str__(self):
        return f"Messaggio da {self.fullname} - {self.email}"
