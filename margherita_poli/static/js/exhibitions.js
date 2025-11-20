document.addEventListener("DOMContentLoaded", () => {
  const images = document.querySelectorAll(".e-gallery__content-modal");
  const overlay = document.querySelector(".e-overlay");
  const modal = document.querySelector(".e-modal");
  const modalImage = document.querySelector(".e-modal__content-img");

  function openModal(src) {
    modalImage.src = src;
    overlay.classList.add("active");
    modal.classList.add("active");
    document.body.style.overflow = "hidden";
  }

  function closeModal() {
    overlay.classList.remove("active");
    modal.classList.remove("active");
    document.body.style.overflow = "";
  }

  images.forEach((img) => {
    img.addEventListener("click", () => {
      const src = img.dataset.src;
      openModal(src);
    });
  });

  overlay.addEventListener("click", closeModal);

  modal.addEventListener("click", closeModal);

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeModal();
  });
});
