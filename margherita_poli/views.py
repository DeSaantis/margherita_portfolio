from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import translation
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

from decimal import Decimal
import json

from .models import Painting, SectionPainting, Illustration, Poem, SectionExhibition, Order, OrderItem



artist_sections = ['paintings', 'poems', 'illustration', 'exhibition']


def index(request):
    """La home page di Margherita Poli."""
    return render(request, 'margherita_poli/index.html', {'current_section':'home'})

# ===================== sezione paintings  ================

def paintings(request):
    lang = translation.get_language()
    sections = SectionPainting.objects.prefetch_related('painting_set').all()

    # Lista piatta con tutti i dipinti
    all_paintings = Painting.objects.select_related('section').all()

    # 🔥 Carrello: prendo il numero di oggetti nella sessione
    cart = request.session.get("cart", {})
    cart_count = len(cart)

    return render(request, 'margherita_poli/paintings.html', {
        'sections': sections,
        'all_paintings': all_paintings,
        'current_section': 'paintings',
        'artist_sections': artist_sections,  # ← già presente nel tuo codice
        'lang': lang,

        # 🔥 Nuovo: passa la quantità nel carrello al template
        'cart_count': cart_count,
    })


# ========= Sezione del carrello ===================
def add_to_cart(request, painting_id):
    painting = get_object_or_404(Painting, id=painting_id)

    cart = request.session.get("cart", {})

    cart[str(painting.id)] = {
        "id": painting.id,
        "title": painting.localized_title,
        "price": float(painting.price) if painting.price else 0,
        "details": painting.localized_details,
        "image": painting.image.url
    }

    request.session["cart"] = cart
    request.session.modified = True

    return JsonResponse({
        "success": True,
        "cart_count": len(cart)
    })



def cart(request):
    cart = request.session.get("cart", {})

    items = []
    subtotal = Decimal("0.00")

    for item in cart.values():
        # item è un dict tipo:
        # {"id": ..., "title": ..., "price": ..., "details": ..., "image": ...}

        # prendiamo il prezzo in modo sicuro
        raw_price = item.get("price", 0)  # se manca, 0

        # lo convertiamo in Decimal in modo robusto (gestisce int / float / string)
        try:
            price = Decimal(str(raw_price))
        except Exception:
            price = Decimal("0.00")

        subtotal += price
        items.append(item)

    return render(request, "margherita_poli/cart.html", {
        "items": items,
        "subtotal": subtotal,
        "total": subtotal,  # per ora totale = subtotale
    })

def remove_from_cart(request, painting_id):
    cart = request.session.get("cart", {})

    if str(painting_id) in cart:
        del cart[str(painting_id)]
        request.session["cart"] = cart
        request.session.modified = True

    return redirect("margherita_poli:cart")

# ============ SEZIONE CHECKOUT ===========

def checkout_cart(request):
    cart = request.session.get("cart", {})

    items = list(cart.values())  # lista dei dipinti nel carrello
    subtotal = sum(float(item["price"]) for item in items)
    shipping = None
    total = subtotal


    return render(request, "margherita_poli/checkout.html", {
        "items": items,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total,
    })

# ========== COLLEGAMENTO A STRIPE ===========
@csrf_exempt
def create_payment_intent(request):
    cart = request.session.get("cart", {})

    # Subtotale
    subtotal = sum(float(item["price"]) for item in cart.values())

    # Spedizione fissa
    shipping = 10.00

    # Totale
    total = subtotal + shipping

    # Stripe richiede centesimi
    amount = int(total * 100)

    try:
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="eur",
            automatic_payment_methods={
                "enabled": True
            },
        )
        return JsonResponse({"clientSecret": intent.client_secret})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


#========== post conferma pagamento ==========

def process_checkout(request):
    if request.method != "POST":
        return redirect("margherita_poli:checkout")

    cart = request.session.get("cart", {})
    if not cart:
        return redirect("margherita_poli:cart")

    # === DATI CLIENTE ===
    customer_name = request.POST.get("nome") + " " + request.POST.get("cognome")
    email = request.POST.get("email")
    address = request.POST.get("indirizzo")
    city = request.POST.get("citta")
    region = request.POST.get("regione")
    cap = request.POST.get("cap")
    country = request.POST.get("stato")

    payment_method = request.POST.get("payment_method")
    payment_intent_id = request.POST.get("payment_intent_id")

    # Calcola totale
    subtotal = sum(Decimal(str(item["price"])) for item in cart.values())
    shipping = Decimal("10.00")
    total = subtotal + shipping

    # === NON confermare il PaymentIntent — solo recuperarlo ===
    intent = stripe.PaymentIntent.retrieve(payment_intent_id)

    if intent.status != "succeeded":
        return JsonResponse({"error": "Pagamento non riuscito"}, status=400)

    # === CREA L’ORDINE NEL DATABASE ===
    order = Order.objects.create(
        customer_name=customer_name,
        customer_email=email,
        customer_address=address,
        customer_city=city,
        customer_region=region,
        customer_zip=cap,
        customer_country=country,
        total_amount=total,
        payment_intent_id=payment_intent_id,
        status="paid"
    )

    # === CREA GLI ITEM ===
    for item in cart.values():
        order_item = OrderItem.objects.create(
            order=order,
            painting_id=item["id"],
            title=item["title"],
            price=Decimal(str(item["price"]))
        )

        # 🔥 MARCARE IL DIPINTO COME VENDUTO
        painting = Painting.objects.get(id=item["id"])
        painting.status = "sold"
        painting.save()


    # Svuota carrello
    request.session["cart"] = {}

    # ============================
    # 📧 INVIO EMAIL DI CONFERMA
    # ============================
    subject = f"Conferma ordine #{order.id} - Margherita Poli"

    # ============================
    # 📧 INVIO EMAIL DI CONFERMA
    # ============================

    # Creiamo un array di item con URL assoluto per l’immagine
    email_items = []
    for item in order.items.all():
        email_items.append({
            "title": item.title,
            "price": item.price,
            "image": request.build_absolute_uri(item.painting.image.url)
        })

    html_message = render_to_string("emails/order_confirmation.html", {
        "order": order,
        "items": email_items,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total,
    })


    # 📨 INVIA AL CLIENTE
    email = EmailMultiAlternatives(
        subject=subject,
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],  # <-- email cliente
    )
    email.attach_alternative(html_message, "text/html")
    email.send()

    # 📨 INVIA A TE (il venditore)
    email_owner = EmailMultiAlternatives(
        subject=f"[COPIA] Nuovo ordine #{order.id}",
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.DEFAULT_FROM_EMAIL]
    )
    email_owner.attach_alternative(html_message, "text/html")
    email_owner.send()



    return redirect("margherita_poli:checkout_success", order_id=order.id)

def checkout_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Recupera gli item dell'ordine
    items = order.items.select_related("painting").all()

    # Calcola subtotale
    subtotal = sum(item.price for item in items)

    # Spedizione fissa → se lo vuoi dinamico dimmelo
    shipping = 10

    total = subtotal + shipping

    return render(request, "margherita_poli/checkout_success.html", {
        "order": order,
        "items": items,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total
    })




# ---------- FORM PAGINA TEACHER.HTML ----------

def contatto(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        messaggio = request.POST.get("messaggio")

        # HTML email
        html_content = render_to_string("emails/contact_teacher.html", {
            "fullname": fullname,
            "email": email,
            "messaggio": messaggio,
        })

        try:
            email_message = EmailMultiAlternatives(
                subject="📩 Nuovo messaggio dalla pagina Insegnante",
                body="",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.DEFAULT_FROM_EMAIL],  # arriva a te
            )

            email_message.attach_alternative(html_content, "text/html")
            email_message.send()

            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Metodo non consentito"})




def poems(request):
    poems = Poem.objects.all()  # già ordinati grazie al Meta.ordering
    poem_of_the_day = Poem.objects.first()  # <-- la più recente
    
    # Escludiamo la poesia del giorno dalla lista
    #poems_without_daily = poems.exclude(id=poem_of_the_day.id) if poem_of_the_day else poems    # ex: remove

    return render(
        request,
        'margherita_poli/poems.html',
        {
            'current_section': 'poems',
            'artist_sections': artist_sections,
            'poems': poems, #poems_without_daily,   # <-- qui usiamo la lista filtrata.  //ex:poems
            'poem_of_the_day': poem_of_the_day,  # <-- passiamo la poesia del giorno
        }
    )


def illustration(request):
    illustration = Illustration.objects.all()
    
    return render(
        request,
        'margherita_poli/illustrator.html',
        {
            'current_section': 'illustration',
            'artist_sections': artist_sections,
            'illustration': illustration,
        }
    )

def exhibition(request):
    lang = translation.get_language()

    sections = SectionExhibition.objects.prefetch_related('exhibition_set').order_by('order')

    # Ultima sezione = esposizione in corso
    current_exhibition = sections.last()

    # Tutte le altre
    past_exhibitions = sections.exclude(id=current_exhibition.id)

    return render(request, 'margherita_poli/exhibitions.html', {
        'current_exhibition': current_exhibition,
        'past_exhibitions': past_exhibitions,
        'current_section': 'exhibition',
        'artist_sections': artist_sections,
        'lang': lang,
    })



def teacher(request):
    """La home page di Margherita Poli."""
    return render(request, 'margherita_poli/teacher.html', {'current_section':'teacher'})

def prova(request):
    """La home page di Margherita Poli."""
    return render(request, 'admin/prova.html')


# ============ LOGIN ==============

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("margherita_poli:dashboard")  # cambia con la tua pagina dopo il login
        else:
            return render(request, "login.html", {"error": "Credenziali non valide"})

    return render(request, "login.html")
