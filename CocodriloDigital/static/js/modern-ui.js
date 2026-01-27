// Modern UI JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initCartCounter();
    initScrollEffects();
    initSearchFunctionality();
    initTooltips();
    initAnimations();
    initMobileMenu();
    initScrollToTop();
    initLazyLoading();
    initToastNotifications();
});

// Cart Counter Management
function initCartCounter() {
    updateCartCounter();
    
    // Update counter when page loads
    window.addEventListener('load', updateCartCounter);
    
    // Update counter when cart is modified
    document.addEventListener('cartUpdated', updateCartCounter);
}

function updateCartCounter() {
    fetch('/cart/api/count/', {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    .then(response => response.json())
    .then(data => {
        const badges = document.querySelectorAll('.cart-badge');
        badges.forEach(badge => {
            badge.textContent = data.count || '0';
            if (data.count > 0) {
                badge.style.display = 'inline-block';
            } else {
                badge.style.display = 'none';
            }
        });
    })
    .catch(error => console.log('Error updating cart counter:', error));
}

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

// Search Functionality
function initSearchFunctionality() {
    const searchInputs = document.querySelectorAll('.search-form input');
    
    searchInputs.forEach(input => {
        // Add search suggestions
        input.addEventListener('input', debounce(function(e) {
            const query = e.target.value.trim();
            if (query.length > 2) {
                showSearchSuggestions(query);
            } else {
                hideSearchSuggestions();
            }
        }, 300));
        
        // Handle enter key
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.target.form.submit();
            }
        });
    });
}

function showSearchSuggestions(query) {
    // Implementation for search suggestions
    console.log('Searching for:', query);
}

function hideSearchSuggestions() {
    // Hide search suggestions
}

// Tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
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
                mobileSearch.style.display = mobileSearch.style.display === 'none' ? 'block' : 'none';
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
    button.innerHTML = '<i class="fas fa-arrow-up"></i>';
    return button;
}

// Lazy Loading
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => {
        img.classList.add('lazy');
        imageObserver.observe(img);
    });
}

// Toast Notifications
function initToastNotifications() {
    // Auto-hide Django messages after 5 seconds
    const messages = document.querySelectorAll('.alert');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });
}

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Cart Functions
function addToCart(productId, quantity = 1) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/cart/carrito/add/${productId}/`;
    
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfToken) {
        form.appendChild(csrfToken.cloneNode());
    }
    
    const quantityInput = document.createElement('input');
    quantityInput.type = 'hidden';
    quantityInput.name = 'quantity';
    quantityInput.value = quantity;
    form.appendChild(quantityInput);
    
    document.body.appendChild(form);
    form.submit();
}

function updateCart(productId, quantity) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/cart/carrito/update/${productId}/`;
    
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfToken) {
        form.appendChild(csrfToken.cloneNode());
    }
    
    const quantityInput = document.createElement('input');
    quantityInput.type = 'hidden';
    quantityInput.name = 'quantity';
    quantityInput.value = quantity;
    form.appendChild(quantityInput);
    
    document.body.appendChild(form);
    form.submit();
}

function removeFromCart(productId) {
    if (confirm('¿Estás seguro de que quieres eliminar este producto del carrito?')) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/cart/carrito/remove/${productId}/`;
        
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfToken) {
            form.appendChild(csrfToken.cloneNode());
        }
        
        document.body.appendChild(form);
        form.submit();
    }
}

// Loading States
function showLoading(element) {
    element.disabled = true;
    element.innerHTML = '<span class="loading-spinner"></span> Cargando...';
}

function hideLoading(element, originalText) {
    element.disabled = false;
    element.innerHTML = originalText;
}

// Form Validation
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

// Price Formatting
function formatPrice(price) {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(price);
}

// Copy to Clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showToast('¡Copiado al portapapeles!', 'success');
    }).catch(function(err) {
        console.error('Error al copiar: ', err);
    });
}

// Custom Toast
function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `modern-toast toast toast-${type}`;
    toast.innerHTML = `
        <div class="toast-body">
            <i class="fas fa-${getToastIcon(type)} me-2"></i>
            ${message}
            <button type="button" class="btn-close btn-close-white ms-2" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
}

function getToastIcon(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// Product Image Zoom
function initImageZoom() {
    const productImages = document.querySelectorAll('.product-image');
    
    productImages.forEach(img => {
        img.addEventListener('click', function() {
            const modal = createImageModal(this.src, this.alt);
            document.body.appendChild(modal);
            modal.style.display = 'flex';
        });
    });
}

function createImageModal(src, alt) {
    const modal = document.createElement('div');
    modal.className = 'image-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <img src="${src}" alt="${alt}">
        </div>
    `;
    
    modal.querySelector('.close-modal').addEventListener('click', function() {
        modal.remove();
    });
    
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.remove();
        }
    });
    
    return modal;
}

// Initialize on page load
window.addEventListener('load', function() {
    initImageZoom();
});

// Export functions for global use
window.CartUtils = {
    addToCart,
    updateCart,
    removeFromCart
};

window.UIUtils = {
    showLoading,
    hideLoading,
    showToast,
    copyToClipboard,
    formatPrice
};
