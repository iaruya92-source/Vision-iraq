// ===== Vision Platform - Main JS =====

document.addEventListener('DOMContentLoaded', function() {
    // Gallery image switch
    const galleryMain = document.querySelector('.gallery-main img');
    const thumbs = document.querySelectorAll('.gallery-thumbs img');
    if (galleryMain && thumbs.length) {
        thumbs.forEach(thumb => {
            thumb.addEventListener('click', function() {
                galleryMain.src = this.src;
                thumbs.forEach(t => t.classList.remove('active'));
                this.classList.add('active');
            });
        });
    }

    // Mobile menu toggle
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const headerNav = document.querySelector('.header-nav');
    if (mobileMenuBtn && headerNav) {
        mobileMenuBtn.addEventListener('click', function() {
            headerNav.classList.toggle('open');
        });
    }

    // Auto-dismiss toast after 5 seconds
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(-100%)';
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    });

    // Price formatting helper
    const priceInputs = document.querySelectorAll('input[name="price"], input[name="price_min"], input[name="price_max"]');
    priceInputs.forEach(input => {
        input.addEventListener('blur', function() {
            let val = parseFloat(this.value);
            if (!isNaN(val)) {
                // No formatting change, just ensure it's a number
            }
        });
    });

    // Smooth scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) target.scrollIntoView({ behavior: 'smooth' });
        });
    });

    // Confirm delete on all forms
    document.querySelectorAll('form[onsubmit]').forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!confirm(this.getAttribute('onsubmit').replace('return confirm(\'', '').replace('\')', ''))) {
                e.preventDefault();
            }
        });
    });
});

// Format number with commas
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// Copy text to clipboard
function copyText(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('تم النسخ!', 'success');
    });
}

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i> ${message}`;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(-100%)';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}
