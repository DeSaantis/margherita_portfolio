document.addEventListener("DOMContentLoaded", () => { 
    initNavCanvas();
});

function initNavCanvas () {
    /*    -------------- MENU OFFCANVAS -------------- */
    const OC_btnMenu = document.querySelector('.sl .btnMenu');
    const OC_overlay = document.querySelector('.sl .overlay');
    const OC_offcanvas = document.querySelector('.sl .offcanvas');
    const OC_btnClose = document.querySelector('.sl .btnClose');
    const navSlim = document.querySelector('.nav.sl');

    // -------- Funzione per aprire il menu --------
    function openMenu() {
        document.body.style.overflow = 'hidden';
        navSlim.style.position = '';
        navSlim.style.top = 'auto';
        OC_overlay.classList.add('active');
        OC_offcanvas.classList.add('active');
        OC_offcanvas.appendChild(OC_social);
    }

    // -------- Funzione per chiudere il menu --------
    function closeMenu() {
        document.body.style.overflow = '';
        navSlim.style.position = 'sticky';
        navSlim.style.top = '0';
        OC_overlay.classList.remove('active');
        OC_offcanvas.classList.remove('active');
        document.activeElement.blur();
    }

    OC_btnMenu.addEventListener('click', openMenu);
    OC_btnClose.addEventListener('click', closeMenu);
    OC_overlay.addEventListener('click', closeMenu);
    window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape'){closeMenu();}
    });
}