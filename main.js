// Mobile navigation toggle
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (navToggle && navLinks) {
        navToggle.addEventListener('click', function() {
            navLinks.classList.toggle('open');
            
            // Animate hamburger to X
            const spans = navToggle.querySelectorAll('span');
            if (navLinks.classList.contains('open')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
            } else {
                spans[0].style.transform = '';
                spans[1].style.opacity = '';
                spans[2].style.transform = '';
            }
        });
        
        // Close menu when clicking a link
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('open');
                const spans = navToggle.querySelectorAll('span');
                spans[0].style.transform = '';
                spans[1].style.opacity = '';
                spans[2].style.transform = '';
            });
        });
    }
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // Code tabs for language switching
    document.querySelectorAll('.code-tabs').forEach(tabContainer => {
        const buttons = tabContainer.querySelectorAll('.tab-btn');
        const contents = tabContainer.querySelectorAll('.tab-content');

        buttons.forEach(btn => {
            btn.addEventListener('click', () => {
                const lang = btn.dataset.lang;

                // Update buttons
                buttons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                // Update content
                contents.forEach(c => {
                    c.classList.remove('active');
                    if (c.dataset.lang === lang) {
                        c.classList.add('active');
                    }
                });
            });
        });
    });
});
