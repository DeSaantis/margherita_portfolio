document.addEventListener("DOMContentLoaded", () => {
  initFilter();
  initOpenImage();
  initTop();
});
function initFilter() {
  const series = document.querySelector('[data-filter="series"]');
  const all = document.querySelector('[data-filter="all"]');
  const section = document.querySelector(".p-section");
  const content = document.querySelector(".p-section--all");

  series.addEventListener("click", () => {
    series.classList.add("active");
    all.classList.remove("active");
    section.style.display = "block";
    content.style.display = "none";
  });
  all.addEventListener("click", () => {
    series.classList.remove("active");
    all.classList.add("active");
    section.style.display = "none";
    content.style.display = "block";

    setTimeout(() => {
      content.style.display = "block"; // oppure semplicemente forzi il reflow
    }, 10);
  });
}

function initOpenImage() {
  const images = document.querySelectorAll(".p-section__image-openModal");
  const overlay = document.querySelector(".p-overlay");
  const modal = document.querySelector(".p-modal");

  const modalImage = document.querySelector(".p-modal__image img");
  const modalTitle = document.querySelector(".p-modal__content-title");
  const modalDesc = document.querySelector(".p-modal__content-desc");
  const modalDetails = document.querySelector(".p-modal__content-details");
  const modalPrice = document.querySelector(".p-modal__content-price");
  const modalClose = document.querySelector(".p-modal__close");
  const modalCartBtn = document.querySelector(".p-modal__content-cart"); // 🔥 pulsante acquista

  let currentPaintingId = null; // 🔥 salvo l'id del quadro aperto nel modale

  images.forEach((img) => {
    img.addEventListener("click", () => {
      const image = img.dataset.src;
      const title = img.dataset.title;
      const desc = img.dataset.description;
      const details = img.dataset.details;
      const price = img.dataset.price;
      const status = img.dataset.status;
      const id = img.dataset.id;

      currentPaintingId = id;

      modalImage.src = image;
      modalTitle.innerHTML = title;
      modalDesc.innerHTML = desc;
      modalDetails.innerHTML = details;
      modalPrice.innerHTML = price;
      modalCartBtn.dataset.id = id;

      /* 🔥 RESET DEL PULSANTE AD OGNI APERTURA DEL MODALE */
      modalCartBtn.innerText = "Acquista";
      modalCartBtn.disabled = false;

      /* 🔥 Mostro o nascondo il pulsante Acquista */
      if (status === "available") {
        modalCartBtn.style.display = "block";
      } else {
        modalCartBtn.style.display = "none";
      }

      overlay.classList.add("active");
      modal.classList.add("active");
    });
  });


  // 🔥 Quando clicchi il pulsante "Acquista" → Checkout del dipinto
  modalCartBtn.addEventListener("click", () => {
    if (!currentPaintingId) return;

    fetch(`/cart/add/${currentPaintingId}/`)
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          modalCartBtn.innerText = "Aggiunto!";
          modalCartBtn.disabled = true;

          // 🔥 aggiorna numero del carrello
          const cartCounter = document.getElementById("cart-count");
          if (cartCounter) {
            cartCounter.textContent = data.cart_count > 0 ? data.cart_count : "";
          }
        }
      })
      .catch(() => alert("Errore nell'aggiunta al carrello"));
  });



  function closeModal() {
    overlay.classList.remove("active");
    modal.classList.remove("active");
    document.body.style.overflow = "";
  }

  overlay.addEventListener("click", closeModal);
  modalClose.addEventListener("click", closeModal);

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeModal();
  });
}
function initTop() {
  document.getElementById("arrow").addEventListener("click", (e) => {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}
