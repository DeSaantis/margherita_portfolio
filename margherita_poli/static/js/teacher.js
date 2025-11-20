document.addEventListener("DOMContentLoaded", () => {
  initSliderGallery();
  initOpenModal();
  initFormConfirmed();
});

function initSliderGallery() {
  const slidesContainer = document.querySelector(".t-gallery__content-slides");
  const rightBtn = document.querySelector(".t-gallery__content-arrow.right");
  const leftBtn = document.querySelector(".t-gallery__content-arrow.left");

  let currentIndex = 0;

  // Funzione per calcolare larghezza + gap automaticamente
  function getScrollAmount() {
    const firstImage = slidesContainer.querySelector("img");
    const style = getComputedStyle(firstImage);
    const width = firstImage.clientWidth;
    const gap = parseInt(style.marginRight);
    return width + gap;
  }

  rightBtn.addEventListener("click", () => {
    currentIndex++;

    if (currentIndex >= slidesContainer.children.length) {
      currentIndex = 0;
    }

    slidesContainer.scrollLeft = currentIndex * getScrollAmount();
  });

  leftBtn.addEventListener("click", () => {
    currentIndex--;

    if (currentIndex < 0) {
      currentIndex = slidesContainer.children.length - 1;
    }

    slidesContainer.scrollLeft = currentIndex * getScrollAmount();
  });
  let startX = 0;
  let isDown = false;

  slidesContainer.addEventListener("touchstart", (e) => {
    isDown = true;
    startX = e.touches[0].clientX; // punto di partenza del dito
  });

  slidesContainer.addEventListener("touchmove", (e) => {
    if (!isDown) return;
    e.preventDefault(); // evita scroll verticale della pagina
  });

  slidesContainer.addEventListener("touchend", (e) => {
    if (!isDown) return;
    isDown = false;

    const endX = e.changedTouches[0].clientX;
    const distance = endX - startX;

    const scrollAmount = getScrollAmount(); // usa la tua funzione già esistente

    if (distance < -50) {
      // swipe verso sinistra → immagine successiva
      currentIndex++;
      if (currentIndex >= slidesContainer.children.length) {
        currentIndex = 0;
      }
      slidesContainer.scrollLeft = currentIndex * scrollAmount;
    }

    if (distance > 50) {
      // swipe verso destra → immagine precedente
      currentIndex--;
      if (currentIndex < 0) {
        currentIndex = slidesContainer.children.length - 1;
      }
      slidesContainer.scrollLeft = currentIndex * scrollAmount;
    }
  });
}
function initOpenModal() {
  const buttons = document.querySelectorAll(".t-service__content-item-button");
  const overlay = document.querySelector(".t-overlay");
  const modalCloseButtons = document.querySelectorAll(".t-support__content-item-button");

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const modalClass = btn.dataset.desc; // es. "t-service--sup" o "t-service--uni"
      const modal = document.querySelector(`.t-modal--${modalClass.split("--")[1]}`);

      // Apri overlay + modale giusto
      overlay.classList.add("active");
      modal.classList.add("active");
      document.body.style.overflow = "hidden";
    });
  });

  // CHIUSURA
  modalCloseButtons.forEach((btn) => {
    btn.addEventListener("click", closeAllModals);
  });
  overlay.addEventListener("click", closeAllModals);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeAllModals();
  });

  function closeAllModals() {
    overlay.classList.remove("active");
    document.querySelectorAll(".t-modal").forEach((m) => m.classList.remove("active"));
    document.body.style.overflow = "";
  }
}

function initFormConfirmed() {
  const form = document.getElementById("t-form");
  const over = document.querySelector(".t-modal-form");

  if (!form) {
    console.error("❌ Form non trovato!");
    return;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    const url = form.dataset.url;

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken },
        body: formData,
      });

      const data = await response.json();

      if (data.success) {
        form.reset();
        apriModal("t-modal-success");
      } else {
        apriModal("t-modal-error");
      }
    } catch (err) {
      apriModal("t-modal-error");
    }
  });
  function apriModal(id) {
    const modal = document.getElementById(id);
    modal.classList.add("visible");

    setTimeout(() => {
      modal.classList.remove("visible");
    }, 3000);
  }
}
