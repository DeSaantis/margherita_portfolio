from django.contrib import admin
from django.db.models import Count
from django.urls import path
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay
from django.template.response import TemplateResponse
from django.utils.html import format_html
from django.utils.text import Truncator
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import SectionPainting, Painting, Poem, Illustration, Exhibition, SectionExhibition, Order, OrderItem, ContactMessage, QRScan

@admin.register(QRScan)
class QRScanAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "ip_address", "user_agent")
    ordering = ("-timestamp",)


class QRReportsAdminSite(admin.AdminSite):
    site_header = "QR Reports"

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path("qr-report/", self.admin_view(self.qr_daily_report), name="qr_daily_report")
        ]
        return custom + urls

    def qr_daily_report(self, request):
        summary = (
            QRScan.objects.annotate(
                year=ExtractYear("timestamp"),
                month=ExtractMonth("timestamp"),
                day=ExtractDay("timestamp"),
            )
            .values("year", "month", "day")
            .annotate(total=Count("id"))
            .order_by("-year", "-month", "-day")
        )

        context = dict(
            self.each_context(request),
            summary=summary,
        )
        return TemplateResponse(request, "admin/qr_daily_summary.html", context)

# crea un'istanza CUSTOM dell'admin
qr_reports_admin = QRReportsAdminSite(name="qr_reports")


# crea un'istanza CUSTOM dell'admin
qr_reports_admin = QRReportsAdminSite(name="qr_reports")

class SectionPaintingAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        
    readonly_fields = ('id', 'localized_preview',)
    list_display = ('section', 'description', 'painting_count', 'localized_preview', 'order', 'id')
    
    fieldsets = (
        ('Italiano', {
            'fields': ('section','description'),
        }),
        ('English', {
            'fields': ('section_en','description_en'),
        }),
        ('Info', {
            'fields': ('id', 'localized_preview', 'order'),
        }),
    )
    
    def painting_count(self, obj):
        return obj.painting_set.count()
    painting_count.short_description = 'Total Paintings'
    
    def short_description(self, obj):
        return Truncator(obj.description).chars(50)
    short_description.short_description = 'Description'
    
    def localized_preview(self, obj):
        return obj.localized_section  # usa la property definita nel modello
    localized_preview.short_description = "Anteprima (Lingua attiva)"
    
admin.site.register(SectionPainting, SectionPaintingAdmin)

@admin.register(Painting)
class PaintingAdmin(admin.ModelAdmin):

    readonly_fields = ('id',)
    list_display = (
        'section', 'title',
        'short_image', 'display_price', 'order'
    )

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            ('Italiano', {
                'fields': ('title', 'description', 'details'),
            }),
            ('English', {
                'fields': ('title_en', 'description_en', 'details_en'),
            }),
        )

        other_fields = ['section', 'image', 'status', 'order', 'id']

        # 🔥 Campi dinamici in base allo stato
        if obj:
            if obj.status == 'available':
                other_fields.insert(2, 'price')
            elif obj.status == 'custom':
                other_fields.insert(2, 'custom_price_text')
                other_fields.insert(3, 'custom_price_text_en')

        fieldsets += (
            ('Altri campi', {
                'fields': tuple(other_fields),
            }),
        )

        return fieldsets

    # Helpers
    def short_description(self, obj):
        return Truncator(obj.description).chars(50)

    def short_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:30px;"/>', obj.image.url)
        return 'x'
    short_image.short_description = 'Image'

    def display_price(self, obj):
        return obj.display_price
    display_price.short_description = "Prezzo / Stato"


@admin.register(Poem)
class PoemAdmin(admin.ModelAdmin):
    list_display = ('date', 'image')
    ordering = ('-date',)  # opzionale, tanto già ordinato nel modello
    readonly_fields = ('id',)
    
    def short_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:30px;"/>', obj.image.url)
        return 'x'
    short_image.short_description = 'Poem'

@admin.register(Illustration)
class IllustrationAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('order', 'short_image',)
    
    def short_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:30px;"/>', obj.image.url)
        return 'x'
    short_image.short_description = 'Illustration'
    
    

@admin.register(SectionExhibition)
class SectionExhibitionAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        
    readonly_fields = ('id', 'localized_preview',)
    list_display = ('section', 'description', 'painting_count', 'localized_preview', 'order', 'id')
    
    fieldsets = (
        ('Italiano', {
            'fields': ('section','description'),
        }),
        ('English', {
            'fields': ('section_en','description_en'),
        }),
        ('Info', {
            'fields': ('id', 'localized_preview', 'order'),
        }),
    )
    
    def painting_count(self, obj):
        return obj.exhibition_set.count()
    painting_count.short_description = 'Total Exhibition'
    
    def short_description(self, obj):
        return Truncator(obj.description).chars(50)
    short_description.short_description = 'Description'
    
    def localized_preview(self, obj):
        return obj.localized_section  # usa la property definita nel modello
    localized_preview.short_description = "Anteprima (Lingua attiva)"
    
    
@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        
    readonly_fields = ('id',)
    list_display = ('section', 'short_image', 'id')
    
    fieldsets = (
        ('Altri campi', {
            'fields': ('section', 'image', 'order', 'id'),
        }),
    )
    
    def short_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:30px;"/>', obj.image.url)
        return 'x'
    short_image.short_description = 'Image'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "customer_email", "total_amount", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("customer_name", "customer_email", "id")
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("fullname", "email", "created_at", "status")
    list_filter = ("status", "created_at")
    search_fields = ("fullname", "email", "message")

    ordering = ("-created_at",)
