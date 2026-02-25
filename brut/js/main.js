// ==================== БУРГЕР-МЕНЮ ====================
const burger = document.getElementById('burger');
const nav = document.getElementById('nav');

burger.addEventListener('click', () => {
    nav.classList.toggle('active');
    burger.classList.toggle('active');
});

// Закрытие меню при клике на ссылку
document.querySelectorAll('.nav__link').forEach(link => {
    link.addEventListener('click', () => {
        nav.classList.remove('active');
        burger.classList.remove('active');
    });
});

// ==================== ПЛАВНЫЙ СКРОЛЛ ====================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ==================== ФОРМА ЛИД-МАГНИТА ====================
const leadForm = document.getElementById('leadForm');

leadForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(leadForm);
    const data = Object.fromEntries(formData);

    // Здесь будет отправка на сервер / в CRM / в Telegram
    console.log('Форма отправлена:', data);

    // Показать сообщение об успехе
    alert('Спасибо! Гайд отправлен вам на почту. Проверьте также папку "Спам".');

    leadForm.reset();
});

// ==================== АНИМАЦИЯ ПРИ СКРОЛЛЕ ====================
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Применяем анимацию ко всем карточкам
document.querySelectorAll('.about__card, .process__step, .story-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'all 0.6s ease';
    observer.observe(el);
});

// ==================== ХЕДЕР ПРИ СКРОЛЛЕ ====================
const header = document.getElementById('header');

window.addEventListener('scroll', () => {
    if (window.scrollY > 100) {
        header.style.boxShadow = '0 4px 20px rgba(56, 25, 23, 0.15)';
    } else {
        header.style.boxShadow = '0 4px 20px rgba(56, 25, 23, 0.08)';
    }
});