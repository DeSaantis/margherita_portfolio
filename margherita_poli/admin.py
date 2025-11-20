from django.contrib import admin
from django.utils.html import format_html
from django.utils.text import Truncator
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import SectionPainting, Painting, Poem, Illustration, Exhibition, SectionExhibition, Order, OrderItem, ContactMessage

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
