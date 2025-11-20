document.addEventListener("DOMContentLoaded", () => {
  initLottieIcons();
});

function initLottieIcons() {
  const icons = [
    { selector: ".globe", speed: 0.8 },
    { selector: ".slack", speed: 2.5, autoPlayInterval: 5000 },
    { selector: ".social", speed: 2 },
    { selector: "#arrow", speed: 1 },

    // ❤️ L'icona heart deve essere statica
    { selector: ".heart", static: true },
  ];

  icons.forEach(({ selector, speed = 1, autoPlayInterval, static: isStatic }) => {
    document.querySelectorAll(selector).forEach((icon) => {
      const animation = lottie.loadAnimation({
        container: icon,
        renderer: "svg",
        loop: false,
        autoplay: false,     // mai autoplay
        path: icon.dataset.json,
      });

      animation.setSpeed(speed);

      if (isStatic) {
        // 🔥  STOPPA l'animazione al frame 0 NON appena viene caricata
        animation.addEventListener("DOMLoaded", () => {
          animation.goToAndStop(0, true);
        });
        return; // non aggiungere listener hover
      }

      // 🎬 Riproduzione al passaggio del mouse
      icon.addEventListener("mouseenter", () => {
        animation.goToAndPlay(0, true);
      });

      // 🔁 Riproduzione automatica se configurata
      if (autoPlayInterval) {
        setInterval(() => {
          animation.goToAndPlay(0, true);
        }, autoPlayInterval);
      }
    });
  });
}
