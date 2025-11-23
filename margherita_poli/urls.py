from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'margherita_poli'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    
    
    path('prova/', views.prova, name='prova'),
    
    
    path('paintings/', views.paintings, name='paintings_all'),

    path("cart/", views.cart, name="cart"),
    path("cart/add/<int:painting_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:painting_id>/", views.remove_from_cart, name="remove_from_cart"),

    path("checkout/", views.checkout_cart, name="checkout_cart"),
    path("create-payment-intent/", views.create_payment_intent, name="create-payment-intent"),
    path("checkout/process/", views.process_checkout, name="process_checkout"),
    path("checkout/success/<int:order_id>/", views.checkout_success, name="checkout_success"),

    path('poems/', views.poems, name='poems'),
    
    
    path('teacher/', views.teacher, name='teacher'),
    path('contatto/', views.contatto, name='contatto'),
    
    
    path('illustrator/', views.illustration, name='illustrator'),
    
    
    path('exhibitions/', views.exhibition, name='exhibitions'),


    # ====== Control Panel
    path('login/', views.login_view, name='login'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)