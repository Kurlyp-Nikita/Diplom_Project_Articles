document.addEventListener('DOMContentLoaded', function() {
    // Мобильное меню
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const nav = document.querySelector('nav');
    const body = document.body;
    
    // Создаем оверлей если его еще нет
    let overlay = document.querySelector('.overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.classList.add('overlay');
        document.body.appendChild(overlay);
    }
    
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            this.classList.toggle('active');
            nav.classList.toggle('active');
            overlay.classList.toggle('active');
            body.classList.toggle('menu-open');
        });
        
        // Закрываем меню при клике на оверлей
        overlay.addEventListener('click', function() {
            closeMenu();
        });
        
        // Закрываем меню при нажатии Escape
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeMenu();
            }
        });
    }
    
    function closeMenu() {
        if (mobileMenuBtn) mobileMenuBtn.classList.remove('active');
        if (nav) nav.classList.remove('active');
        if (overlay) overlay.classList.remove('active');
        body.classList.remove('menu-open');
    }
    
    // Обработчик для выпадающих меню на мобильных
    const dropdownToggles = document.querySelectorAll('.has-dropdown > a');
    
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            if (window.innerWidth <= 992) {
                e.preventDefault();
                e.stopPropagation();
                
                const parent = this.parentElement;
                
                // Закрываем другие меню
                dropdownToggles.forEach(otherToggle => {
                    const otherParent = otherToggle.parentElement;
                    if (otherParent !== parent && otherParent.classList.contains('active')) {
                        otherParent.classList.remove('active');
                    }
                });
                
                parent.classList.toggle('active');
            }
        });
    });
    
    // Обработчик для выпадающего меню пользователя
    const userDropdown = document.querySelector('.user-dropdown > a');
    if (userDropdown) {
        userDropdown.addEventListener('click', function(e) {
            if (window.innerWidth > 992) {
                e.preventDefault();
                e.stopPropagation();
                this.parentElement.classList.toggle('show-dropdown');
                
                // Закрываем меню при клике вне его
                document.addEventListener('click', function closeDropdown(evt) {
                    if (!evt.target.closest('.user-dropdown')) {
                        userDropdown.parentElement.classList.remove('show-dropdown');
                        document.removeEventListener('click', closeDropdown);
                    }
                });
            }
        });
    }
    
    // Инициализация всех компонентов
    initScrollHeader();
    setupAnimations();
    setupCardEffects();
    
    // Проверка формы перед отправкой
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let hasErrors = false;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    hasErrors = true;
                    field.classList.add('error');
                    
                    // Создаем сообщение об ошибке, если его еще нет
                    if (!field.nextElementSibling || !field.nextElementSibling.classList.contains('error-message')) {
                        const errorMessage = document.createElement('div');
                        errorMessage.classList.add('error-message');
                        errorMessage.textContent = 'Это поле обязательно для заполнения';
                        field.parentNode.insertBefore(errorMessage, field.nextSibling);
                    }
                } else {
                    field.classList.remove('error');
                    if (field.nextElementSibling && field.nextElementSibling.classList.contains('error-message')) {
                        field.nextElementSibling.remove();
                    }
                }
            });
            
            if (hasErrors) {
                e.preventDefault();
            }
        });
    });
    
    // Запускаем анимацию при загрузке
    animateOnScroll();
    // И при скролле
    window.addEventListener('scroll', animateOnScroll);
});

// Функция для интерактивного хедера
function initScrollHeader() {
    const header = document.querySelector('header');
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Проверка направления скролла
        if (scrollTop > lastScrollTop && scrollTop > 150) {
            // Скролл вниз
            header.classList.add('header-hidden');
        } else {
            // Скролл вверх
            header.classList.remove('header-hidden');
        }
        
        // Добавляем тень и уменьшаем padding при скролле
        if (scrollTop > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        
        lastScrollTop = scrollTop;
    }, false);
}

// Функция для настройки анимаций
function setupAnimations() {
    const articleCards = document.querySelectorAll('.article-card');
    const categoryCards = document.querySelectorAll('.category-card');
    const sectionHeaders = document.querySelectorAll('.articles-title, .main-title, .section-header, .profile-header, .hero-content');
    
    // Добавляем классы для анимаций
    articleCards.forEach((card, index) => {
        card.classList.add('animate-on-scroll');
        card.style.animationDelay = `${index * 0.1}s`;
    });
    
    categoryCards.forEach((card, index) => {
        card.classList.add('animate-on-scroll');
        card.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Добавляем эффекты для заголовков
    sectionHeaders.forEach(header => {
        header.classList.add('animate-on-scroll');
    });
}

// Функция для эффектов карточек
function setupCardEffects() {
    const cards = document.querySelectorAll('.article-card, .category-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('hover');
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('hover');
        });
    });
}

// Оптимизированная функция анимации элементов при скролле
function animateOnScroll() {
    const elements = document.querySelectorAll('.animate-on-scroll:not(.animated)');
    const viewportHeight = window.innerHeight;
    
    elements.forEach(element => {
        const elementPosition = element.getBoundingClientRect().top;
        
        if (elementPosition < viewportHeight - 100) {
            element.classList.add('animated');
        }
    });
}

// Плавная прокрутка к секциям
document.addEventListener('DOMContentLoaded', () => {
    const smoothScrollLinks = document.querySelectorAll('a[href^="#"]:not(.dropdown-toggle)');
    smoothScrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                e.preventDefault();
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 80,
                        behavior: 'smooth'
                    });
                    
                    // Закрываем мобильное меню при навигации
                    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
                    const nav = document.querySelector('nav');
                    const overlay = document.querySelector('.overlay');
                    
                    if (mobileMenuBtn && mobileMenuBtn.classList.contains('active')) {
                        mobileMenuBtn.classList.remove('active');
                        nav.classList.remove('active');
                        overlay.classList.remove('active');
                        document.body.classList.remove('menu-open');
                    }
                }
            }
        });
    });
}); 