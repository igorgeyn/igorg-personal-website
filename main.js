// Mobile navigation, theme controls, and lightweight page interactions.
document.addEventListener('DOMContentLoaded', function() {
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

    const themeToggle = document.querySelector('.theme-toggle');

    function updateThemeControl() {
        if (!themeToggle) return;
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        const label = isDark ? 'Switch to light mode' : 'Switch to dark mode';
        themeToggle.setAttribute('aria-label', label);
        themeToggle.setAttribute('title', label);
    }

    if (themeToggle) {
        updateThemeControl();
        themeToggle.addEventListener('click', function() {
            const current = document.documentElement.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);
            updateThemeControl();
        });
    }

    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (navToggle && navLinks) {
        if (!navLinks.id) navLinks.id = 'primary-navigation';
        navToggle.setAttribute('aria-controls', navLinks.id);
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.setAttribute('aria-label', 'Open navigation menu');

        const spans = navToggle.querySelectorAll('span');

        function renderMenuState(isOpen) {
            navLinks.classList.toggle('open', isOpen);
            navToggle.setAttribute('aria-expanded', String(isOpen));
            navToggle.setAttribute('aria-label', isOpen ? 'Close navigation menu' : 'Open navigation menu');

            spans[0].style.transform = isOpen ? 'rotate(45deg) translate(5px, 5px)' : '';
            spans[1].style.opacity = isOpen ? '0' : '';
            spans[2].style.transform = isOpen ? 'rotate(-45deg) translate(5px, -5px)' : '';
        }

        navToggle.addEventListener('click', function() {
            renderMenuState(!navLinks.classList.contains('open'));
        });

        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => renderMenuState(false));
        });

        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape' && navLinks.classList.contains('open')) {
                renderMenuState(false);
                navToggle.focus();
            }
        });

        window.addEventListener('resize', function() {
            if (window.innerWidth > 768 && navLinks.classList.contains('open')) {
                renderMenuState(false);
            }
        });
    }

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(event) {
            const href = this.getAttribute('href');
            if (href === '#') return;

            const target = document.querySelector(href);
            if (target) {
                event.preventDefault();
                target.scrollIntoView({
                    behavior: reducedMotion.matches ? 'auto' : 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Keep wide data tables available without making the whole page scroll sideways.
    document.querySelectorAll('table').forEach(table => {
        const parent = table.parentElement;
        const parentOverflow = parent ? getComputedStyle(parent).overflowX : 'visible';
        const scroller = parent && ['auto', 'scroll'].includes(parentOverflow) ? parent : table;

        if (!scroller.hasAttribute('tabindex')) scroller.setAttribute('tabindex', '0');
        if (scroller !== table && !scroller.hasAttribute('role')) scroller.setAttribute('role', 'region');
        if (!scroller.hasAttribute('aria-label')) scroller.setAttribute('aria-label', 'Scrollable data table');
    });

    document.querySelectorAll('.code-tabs').forEach(tabContainer => {
        const buttons = tabContainer.querySelectorAll('.tab-btn');
        const contents = tabContainer.querySelectorAll('.tab-content');

        buttons.forEach(btn => {
            btn.addEventListener('click', () => {
                const lang = btn.dataset.lang;
                buttons.forEach(button => button.classList.remove('active'));
                btn.classList.add('active');

                contents.forEach(content => {
                    content.classList.toggle('active', content.dataset.lang === lang);
                });
            });
        });
    });
});
