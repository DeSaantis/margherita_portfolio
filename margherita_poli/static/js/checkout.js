// =========================
// VARIABILI GLOBALI STRIPE
// =========================
let stripe = null;
let cardNumber = null;
let cardExp = null;
let cardCvc = null;


// =========================
// INIZIALIZZAZIONE PAGINA
// =========================
document.addEventListener("DOMContentLoaded", () => {
    initStripe();       // DEVE ESSERE PRIMO
    initSubtotal();
    initAutoCompile();
    initCollapse();
    initPaymentSubmit();
});


// =========================
// AUTO-COMPILE PROVINCE/REGIONI
// =========================
function initAutoCompile() {
    document.querySelectorAll(".custom-select").forEach(select => {
        
        const input = select.querySelector(".select-input");
        const dropdown = select.querySelector(".select-dropdown");
        const jsonURL = select.dataset.json;

        let options = [];

        fetch(jsonURL)
            .then(res => res.json())
            .then(data => {
                options = data;
                renderOptions("");
            });

        input.addEventListener("click", () => {
            dropdown.classList.toggle("open");
        });

        input.addEventListener("input", e => {
            renderOptions(e.target.value);
            dropdown.classList.add("open");
        });

        document.addEventListener("click", e => {
            if (!select.contains(e.target)) dropdown.classList.remove("open");
        });

        function renderOptions(filter) {
            dropdown.innerHTML = "";

            options
                .filter(opt => {
                    const text = typeof opt === "string"
                        ? opt
                        : (opt.sigla + " " + opt.nome);

                    return text.toLowerCase().includes(filter.toLowerCase());
                })
                .forEach(opt => {
                    const option = document.createElement("div");
                    option.classList.add("select-option");

                    if (typeof opt === "string") {
                        option.textContent = opt;
                        option.addEventListener("click", () => {
                            input.value = opt;
                            dropdown.classList.remove("open");
                        });
                    } else {
                        option.textContent = `${opt.sigla} - ${opt.nome}`;
                        option.addEventListener("click", () => {
                            input.value = opt.nome;
                            dropdown.classList.remove("open");
                        });
                    }

                    dropdown.appendChild(option);
                });
        }
    });
}



// =========================
// SISTEMA DI COLLASSO A STEP
// =========================
function initCollapse() {

    const form = document.getElementById("c-checkout__form-details");
    const sections = document.querySelectorAll(".step-section");
    let currentStep = 0;

    // Mostra solo la prima sezione
    sections.forEach((sec, i) => {
        if (i !== 0) sec.classList.remove("active");
    });

    // Tasti "Continua"
    form.querySelectorAll(".c-continue button").forEach(btn => {

        btn.addEventListener("click", (e) => {
            e.preventDefault();

            const section = sections[currentStep];

            if (!validateSection(section)) return;

            collapseSection(section);

            currentStep++;
            if (currentStep < sections.length) {
                expandSection(sections[currentStep]);
            }
        });

    });


    function expandSection(section) {
        section.classList.add("active");
        section.classList.remove("collapsed");
    }

    function collapseSection(section) {
        section.classList.remove("active");
        section.classList.add("collapsed");

        const summary = section.querySelector(".section-summary");

        if (summary) {
            summary.innerHTML = generateSummary(section);

            const editBtn = summary.querySelector(".edit-section");
            if (editBtn) {
                editBtn.addEventListener("click", () => {

                    expandSection(section);

                    currentStep = Array.from(sections).indexOf(section);

                    sections.forEach((sec, i) => {
                        if (i > currentStep) {
                            sec.classList.remove("active");
                            sec.classList.remove("collapsed");
                        }
                    });
                });
            }
        }
    }


    function validateSection(section) {
        let valid = true;

        const inputs = section.querySelectorAll("input[required]");
        inputs.forEach(input => {
            input.classList.remove("error");
            if (!input.value.trim()) {
                input.classList.add("error");
                valid = false;
            }
        });

        return valid;
    }


    function generateSummary(section) {
        let html = "";

        const inputs = section.querySelectorAll("input");

        inputs.forEach(input => {
            const label = section.querySelector(`label[for="${input.id}"]`);
            if (!label) return;

            const labelText = label.innerText.replace("*", "");
            let value = input.value.trim();

            if (input.name === "shipping_method" && input.checked) {
                const desc = input.closest("label").innerText.trim().replace(/\s+/g, " ");
                html += `<p><strong>Metodo di consegna:</strong> ${desc}</p>`;
                return;
            }

            html += `<p><strong>${labelText}:</strong> ${value}</p>`;
        });

        html += `<button type="button" class="edit-section">Modifica</button>`;
        return html;
    }
}





// =========================
// STRIPE — ELEMENTS
// =========================
function initStripe() {

    stripe = Stripe("pk_test_51SUtYRGtFhE88jYDzneGUjpCTMqXpkfQRgN2ownK3G10wyYBUUOkJ6pAgn9yzPRvH32jlTKo8pJxIdlpB8Tv1YRd00UPhHnwp5");

    const elements = stripe.elements();

    const style = {
        base: {
            color: "#003049",
            fontFamily: "Lato",
            fontSize: "16px",
            "::placeholder": { color: "#A0A0A0" }
        },
        invalid: { color: "#e74c3c" }
    };

    cardNumber = elements.create("cardNumber", { style });
    cardExp = elements.create("cardExpiry", { style });
    cardCvc = elements.create("cardCvc", { style });

    cardNumber.mount("#card-number-element");
    cardExp.mount("#card-exp-element");
    cardCvc.mount("#card-cvc-element");
}





// =========================
// CALCOLO SUBTOTALE
// =========================
function initSubtotal() {

  const shippingContinue = document.getElementById("shipping-continue");
  const shippingInput = document.getElementById("shipping-standard");

  const summarySubtotal = document.getElementById("summary-subtotal");
  const summaryShipping = document.getElementById("summary-shipping");
  const summaryTotal = document.getElementById("summary-total");

  if (shippingContinue) {
    shippingContinue.addEventListener("click", () => {

      if (!shippingInput.checked) {
        alert("Seleziona un metodo di consegna.");
        return;
      }

      const shippingCost = 10;
      const subtotalValue = parseFloat(summarySubtotal.textContent.replace("€", "").trim());

      summaryShipping.textContent = shippingCost + " €";
      summaryTotal.textContent = (subtotalValue + shippingCost) + " €";
    });
  }
}





// =========================
// 🔥 PAGAMENTO COMPLETO
// =========================
function initPaymentSubmit() {

    document.querySelector(".c-checkout__payment button").addEventListener("click", async (e) => {
        e.preventDefault();

        // evita click multipli
        e.target.disabled = true;

        // 1️⃣ Crea PaymentMethod
        const { paymentMethod, error } = await stripe.createPaymentMethod({
            type: "card",
            card: cardNumber,
            billing_details: {
                name: document.getElementById("card-owner").value,
                email: document.getElementById("email").value
            }
        });

        if (error) {
            alert(error.message);
            e.target.disabled = false;
            return;
        }

        document.getElementById("payment_method").value = paymentMethod.id;

        // 2️⃣ Richiedi PaymentIntent
        const res = await fetch("/create-payment-intent/", {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        });

        const data = await res.json();
        if (data.error) {
            alert(data.error);
            e.target.disabled = false;
            return;
        }

        const clientSecret = data.clientSecret;

        // 3️⃣ Conferma Pagamento
        const result = await stripe.confirmCardPayment(clientSecret, {
            payment_method: paymentMethod.id
        });

        if (result.error) {
            alert(result.error.message);
            e.target.disabled = false;
            return;
        }

        // 4️⃣ Se OK invia PaymentIntent ID a Django
        document.getElementById("payment_intent_id").value = result.paymentIntent.id;

        // 5️⃣ Invia form
        document.getElementById("c-checkout__form-details").submit();
    });

}
