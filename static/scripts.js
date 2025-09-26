document.addEventListener('DOMContentLoaded', function() {
    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');

    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('navbar-scrolled');
            navbar.classList.remove('navbar-transparent');
        } else {
            navbar.classList.remove('navbar-scrolled');
            navbar.classList.add('navbar-transparent');
        }
    });

    // Method toggles
    const methodToggles = document.querySelectorAll('.method-toggle');

    methodToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const content = this.parentElement.nextElementSibling;

            if (content.style.display === 'block') {
                content.style.display = 'none';
                this.classList.remove('fa-chevron-up');
                this.classList.add('fa-chevron-down');
            } else {
                content.style.display = 'block';
                this.classList.remove('fa-chevron-down');
                this.classList.add('fa-chevron-up');
            }
        });
    });

    // Testimonial carousel
    const nextBtn = document.querySelector('.next-btn');
    const prevBtn = document.querySelector('.prev-btn');
    const slides = document.querySelectorAll('.testimonial-slide');

    let currentSlide = 0;

    function showSlide(index) {
        slides.forEach(slide => slide.classList.remove('active'));
        slides[index].classList.add('active');
    }

    if (nextBtn && prevBtn) {
        nextBtn.addEventListener('click', function() {
            currentSlide = (currentSlide + 1) % slides.length;
            showSlide(currentSlide);
        });

        prevBtn.addEventListener('click', function() {
            currentSlide = (currentSlide - 1 + slides.length) % slides.length;
            showSlide(currentSlide);
        });
    }

    // Smooth scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                const navbarHeight = document.querySelector('.navbar').offsetHeight;
                const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - navbarHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });

                // Close mobile menu if open
                const navbarToggler = document.querySelector('.navbar-toggler');
                const navbarCollapse = document.querySelector('.navbar-collapse');

                if (navbarCollapse.classList.contains('show')) {
                    navbarToggler.click();
                }
            }
        });
    });

    // Form submission
    const contactForm = document.getElementById('contact-form');

    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // Aqui você adicionaria o código para enviar o formulário via AJAX
            // Por enquanto, apenas um alerta de sucesso
            alert('Obrigado pelo seu interesse! Seu e-book será enviado em breve.');
            this.reset();
        });
    }

    // Animation on scroll
    const animateElements = document.querySelectorAll('.feature-item, .method-item, .learning-english-box, .teacher-image-container');

    function checkIfInView() {
        animateElements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementVisible = 150;

            if (elementTop < window.innerHeight - elementVisible) {
                element.classList.add('fadeIn');
            }
        });
    }

    window.addEventListener('scroll', checkIfInView);
    checkIfInView();
});

