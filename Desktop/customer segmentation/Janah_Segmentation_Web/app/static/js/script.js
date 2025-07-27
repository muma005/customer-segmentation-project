// Janah Customer Segmentation - JavaScript Functions

// Global variables
let currentPage = window.location.pathname;

// ===== PAGE LOAD FUNCTIONS =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Janah Segmentation App Loaded Successfully!');
    
    // Show welcome alert on home page
    if (currentPage === '/' || currentPage === '/home') {
        showWelcomeAlert();
    }
    
    // Initialize page-specific functions
    initializePageFunctions();
    
    // Add fade-in animation to cards
    addFadeInAnimation();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Add smooth scrolling
    addSmoothScrolling();
});

// ===== WELCOME ALERT =====
function showWelcomeAlert() {
    setTimeout(() => {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-info alert-dismissible fade show position-fixed';
        alertDiv.style.cssText = 'top: 100px; right: 20px; z-index: 1050; max-width: 300px;';
        alertDiv.innerHTML = `
            <i class="fas fa-info-circle me-2"></i>
            <strong>Welcome!</strong> Ready to analyze your customers?
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(alertDiv);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }, 1000);
}

// ===== PAGE INITIALIZATION =====
function initializePageFunctions() {
    // File upload validation
    const fileInput = document.getElementById('file');
    if (fileInput) {
        fileInput.addEventListener('change', validateFileUpload);
    }
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', validateForm);
    });
    
    // Navigation highlighting
    highlightCurrentNavItem();
    
    // Initialize charts if on results page
    if (currentPage === '/results') {
        initializeCharts();
    }
}

// ===== FILE UPLOAD VALIDATION =====
function validateFileUpload(e) {
    const file = e.target.files[0];
    if (file) {
        const allowedTypes = ['.csv', '.xlsx', '.xls'];
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        
        if (!allowedTypes.includes(fileExtension)) {
            showNotification('Please select a valid file type (CSV, XLSX, or XLS)', 'error');
            e.target.value = '';
            return false;
        }
        
        if (file.size > 16 * 1024 * 1024) { // 16MB limit
            showNotification('File size must be less than 16MB', 'error');
            e.target.value = '';
            return false;
        }
        
        showNotification(`File "${file.name}" selected successfully!`, 'success');
        return true;
    }
    return false;
}

// ===== FORM VALIDATION =====
function validateForm(e) {
    const form = e.target;
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    if (!isValid) {
        e.preventDefault();
        showNotification('Please fill in all required fields', 'error');
    }
    
    return isValid;
}

// ===== NAVIGATION FUNCTIONS =====
function highlightCurrentNavItem() {
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });
}

// ===== CHART INITIALIZATION =====
function initializeCharts() {
    const container = document.querySelector('.chart-container');
    if (container) {
        // Placeholder for chart initialization
        container.innerHTML = `
            <div class="text-center text-muted">
                <i class="fas fa-chart-pie fa-3x mb-3"></i>
                <p>Interactive charts will be displayed here</p>
                <small>Real visualizations coming in Phase 3</small>
            </div>
        `;
    }
}

// ===== ANIMATION FUNCTIONS =====
function addFadeInAnimation() {
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease-out';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// ===== UTILITY FUNCTIONS =====
function showNotification(message, type = 'info') {
    const alertClass = type === 'error' ? 'alert-danger' : 
                      type === 'success' ? 'alert-success' : 'alert-info';
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert ${alertClass} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 100px; right: 20px; z-index: 1050; max-width: 300px;';
    alertDiv.innerHTML = `
        <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : 
                          type === 'success' ? 'check-circle' : 'info-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-dismiss after 4 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 4000);
}

function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function addSmoothScrolling() {
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
}

// ===== EXPORT FUNCTIONS (Placeholders for Phase 5) =====
function downloadReport() {
    showNotification('Report download functionality will be implemented in Phase 5', 'info');
}

function exportData() {
    showNotification('Data export functionality will be implemented in Phase 5', 'info');
}

function shareResults() {
    showNotification('Share functionality will be implemented in Phase 5', 'info');
}

function previewCampaign() {
    const segment = document.getElementById('segmentSelect')?.value || 'loyal';
    const campaigns = {
        'loyal': 'Exclusive VIP offer: 15% off next purchase + free shipping',
        'regular': 'Special discount: 10% off on orders over $100',
        'at-risk': 'We miss you! 20% off to welcome you back',
        'inactive': 'Reactivation offer: 25% off + free gift with purchase'
    };
    
    showNotification(`Campaign for ${segment} customers: ${campaigns[segment]}`, 'info');
}

// ===== PROGRESS SIMULATION =====
function simulateProgress(progressBar, progressText, callback) {
    let progress = 0;
    const interval = setInterval(() => {
        progress += 10;
        progressBar.style.width = progress + '%';
        progressBar.textContent = progress + '%';
        
        if (progress >= 100) {
            clearInterval(interval);
            progressText.textContent = 'Analysis complete!';
            if (callback) callback();
        } else if (progress < 30) {
            progressText.textContent = 'Loading and cleaning data...';
        } else if (progress < 60) {
            progressText.textContent = 'Calculating RFM metrics...';
        } else if (progress < 90) {
            progressText.textContent = 'Running clustering analysis...';
        } else {
            progressText.textContent = 'Generating visualizations...';
        }
    }, 200);
}

// ===== UTILITY FUNCTIONS =====
function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(new Date(date));
}

// ===== ERROR HANDLING =====
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
    showNotification('An error occurred. Please try again.', 'error');
});

// ===== PAGE VISIBILITY API =====
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        console.log('Page hidden');
    } else {
        console.log('Page visible');
    }
});

// Export functions for use in templates
window.JanahSegmentation = {
    showNotification,
    downloadReport,
    exportData,
    shareResults,
    previewCampaign,
    simulateProgress,
    formatNumber,
    formatCurrency,
    formatDate
};
