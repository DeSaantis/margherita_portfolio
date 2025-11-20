document.addEventListener('DOMContentLoaded', () => {
    initOpenMenu();
    initLottieIcons();
    initButton();
});

/* ============ Apre il menu offcanvas =========== */
function initOpenMenu() {
    const overlay = document.querySelector('.i-overlay');
    const menu = document.querySelector('.i-nav__mobile');
    const modale = document.querySelector('.i-nav__menu')

    menu.addEventListener('click', () => {
        overlay.classList.add('active');
        modale.classList.add('active');
        document.body.style.overflow = "hidden"
    });

    function closeMenu() {
        overlay.classList.remove('active');
        modale.classList.remove('active');
        document.body.style.overflow = ""
    }

    overlay.addEventListener('click', closeMenu);
}
/* ============ Iniziallizza le icone .json =========== */
function initLottieIcons() {
    // Definizione unica delle icone e relative impostazioni
    const icons = [
        { selector: '.social', speed: 2 },
        { selector: '.globe', speed: 0.8 },
    ];

    icons.forEach(({ selector, speed = 1, autoPlayInterval }) => {
        document.querySelectorAll(selector).forEach((icon) => {
            const animation = lottie.loadAnimation({
                container: icon,
                renderer: 'svg',
                loop: false,
                autoplay: false,
                path: icon.dataset.json,
            });

            animation.setSpeed(speed);

            // Riproduzione al passaggio del mouse
            icon.addEventListener('mouseenter', () => {
                animation.goToAndPlay(0, true);
            });

            // Riproduzione automatica se configurata
            if (autoPlayInterval) {
                setInterval(() => {
                    animation.goToAndPlay(0, true);
                }, autoPlayInterval);
            }
        });
    });
}
/* ============ timer pulsante x mobile =========== */
function initButton() {
    document.querySelectorAll(".i-button").forEach(btn => {
        btn.addEventListener("click", () => {
        btn.classList.add("pressed");

        setTimeout(() => {
            btn.classList.remove("pressed");
            }, 200); // durata dell'effetto
        });
    });
}