// Basic UI JavaScript - No AJAX, simple interactions
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initScrollEffects();
    initImageZoom();
    initAnimations();
    initMobileMenu();
    initScrollToTop();
    initFormValidation();
    initCartInteractions();
});

// Scroll Effects
function initScrollEffects() {
    const navbar = document.querySelector('.navbar-modern');
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Hide/show navbar on scroll
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            navbar.style.transform = 'translateY(-100%)';
        } else {
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
        
        // Add shadow when scrolled
        if (scrollTop > 10) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

// Image Zoom
function initImageZoom() {
    const productImages = document.querySelectorAll('.product-image');
    
    productImages.forEach(img => {
        img.style.cursor = 'pointer';
        img.addEventListener('click', function() {
            createImageModal(this.src, this.alt);
        });
    });
}

function createImageModal(src, alt) {
    // Remove existing modal if any
    const existingModal = document.querySelector('.image-modal');
    if (existingModal) {
        existingModal.remove();
    }
    
    const modal = document.createElement('div');
    modal.className = 'image-modal';
    modal.style.cssText = `
        display: flex;
        position: fixed;
        z-index: 9999;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.9);
        justify-content: center;
        align-items: center;
        animation: fadeIn 0.3s;
    `;
    
    modal.innerHTML = `
        <div style="position: relative; max-width: 90%; max-height: 90%;">
            <span style="
                position: absolute;
                top: -40px;
                right: 0;
                color: #fff;
                font-size: 40px;
                font-weight: bold;
                cursor: pointer;
                transition: 0.3s;
            " class="close-modal">&times;</span>
            <img src="${src}" alt="${alt}" style="
                width: 100%;
                height: auto;
                border-radius: 12px;
            ">
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Close modal events
    const closeBtn = modal.querySelector('.close-modal');
    closeBtn.addEventListener('click', function() {
        modal.remove();
    });
    
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.remove();
        }
    });
    
    // Close on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            modal.remove();
        }
    });
}

// Animations
function initAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements with animation classes
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
}

// Mobile Menu
function initMobileMenu() {
    const mobileToggle = document.querySelector('.navbar-toggler');
    const mobileSearch = document.querySelector('.mobile-search');
    
    if (mobileToggle && mobileSearch) {
        mobileToggle.addEventListener('click', function() {
            setTimeout(() => {
                if (mobileSearch.style.display === 'none' || !mobileSearch.style.display) {
                    mobileSearch.style.display = 'block';
                } else {
                    mobileSearch.style.display = 'none';
                }
            }, 300);
        });
    }
}

// Scroll to Top
function initScrollToTop() {
    const scrollButton = createScrollToTopButton();
    document.body.appendChild(scrollButton);
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollButton.classList.add('visible');
        } else {
            scrollButton.classList.remove('visible');
        }
    });
    
    scrollButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

function createScrollToTopButton() {
    const button = document.createElement('div');
    button.className = 'scroll-top';
    button.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: var(--secondary-color);
        color: #fff;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s;
        z-index: 1000;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    `;
    button.innerHTML = '<i class="fas fa-arrow-up"></i>';
    
    // Add hover effect
    button.addEventListener('mouseenter', function() {
        this.style.background = 'var(--accent-color)';
        this.style.transform = 'translateY(-3px)';
        this.style.boxShadow = '0 8px 20px rgba(0, 0, 0, 0.3)';
    });
    
    button.addEventListener('mouseleave', function() {
        this.style.background = 'var(--secondary-color)';
        this.style.transform = 'translateY(0)';
        this.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.2)';
    });
    
    return button;
}

// Form Validation
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(form)) {
                e.preventDefault();
            }
        });
    });
}

function validateForm(formElement) {
    const inputs = formElement.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Cart Interactions (Basic, no AJAX)
function initCartInteractions() {
    // Quantity controls
    const quantityControls = document.querySelectorAll('.quantity-control');
    
    quantityControls.forEach(control => {
        const minusBtn = control.querySelector('.quantity-minus');
        const plusBtn = control.querySelector('.quantity-plus');
        const input = control.querySelector('.quantity-input');
        
        if (minusBtn && plusBtn && input) {
            minusBtn.addEventListener('click', function() {
                const currentValue = parseInt(input.value) || 1;
                if (currentValue > 1) {
                    input.value = currentValue - 1;
                    triggerCartUpdate();
                }
            });
            
            plusBtn.addEventListener('click', function() {
                const currentValue = parseInt(input.value) || 1;
                input.value = currentValue + 1;
                triggerCartUpdate();
            });
            
            input.addEventListener('change', function() {
                const value = parseInt(this.value) || 1;
                if (value < 1) {
                    this.value = 1;
                }
                triggerCartUpdate();
            });
        }
    });
    
    // Remove buttons
    const removeButtons = document.querySelectorAll('.remove-btn');
    removeButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            if (confirm('¿Estás seguro de que quieres eliminar este producto del carrito?')) {
                // Submit the form or navigate to remove URL
                const form = this.closest('form');
                if (form) {
                    form.submit();
                } else {
                    window.location.href = this.dataset.url || '#';
                }
            }
        });
    });
    
    // Add to cart buttons
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    addToCartButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const productId = this.dataset.productId;
            if (productId) {
                // Submit the form or navigate to add URL
                const form = this.closest('form');
                if (form) {
                    form.submit();
                } else {
                    window.location.href = `/cart/carrito/add/${productId}/`;
                }
            }
        });
    });
}

function triggerCartUpdate() {
    // Add visual feedback when cart is updated
    const cartBadge = document.querySelector('.cart-badge');
    if (cartBadge) {
        cartBadge.style.transform = 'scale(1.2)';
        setTimeout(() => {
            cartBadge.style.transform = 'scale(1)';
        }, 200);
    }
}

// Utility Functions
function showLoading(element) {
    element.disabled = true;
    element.innerHTML = '<span class="loading-spinner"></span> Cargando...';
}

function hideLoading(element, originalText) {
    element.disabled = false;
    element.innerHTML = originalText;
}

function formatPrice(price) {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(price);
}

// Add CSS animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .animate-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .scroll-top.visible {
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);
