// Janah Customer Segmentation - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Janah Segmentation Web App loaded successfully!');
    
    // Initialize components
    initializeFileUpload();
    initializeDataSourceToggle();
    initializeProgressTracking();
    initializeNotifications();
    
    // Add page-specific functionality
    const currentPage = window.location.pathname;
    if (currentPage.includes('segmentation')) {
        initializeSegmentationPage();
    } else if (currentPage.includes('results')) {
        initializeResultsPage();
    }
});

// File Upload Handling
function initializeFileUpload() {
    const fileInput = document.getElementById('fileInput');
    const uploadArea = document.getElementById('uploadArea');
    const fileLabel = document.getElementById('fileLabel');
    
    if (!fileInput || !uploadArea) return;
    
    // Drag and drop functionality
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelection(files[0]);
        }
    });
    
    // Click to upload
    uploadArea.addEventListener('click', function() {
        fileInput.click();
    });
    
    // File selection
    fileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            handleFileSelection(e.target.files[0]);
        }
    });
}

function handleFileSelection(file) {
    const fileLabel = document.getElementById('fileLabel');
    const uploadArea = document.getElementById('uploadArea');
    
    if (fileLabel) {
        fileLabel.textContent = `📁 ${file.name} (${formatFileSize(file.size)})`;
    }
    
    if (uploadArea) {
        uploadArea.classList.add('file-selected');
        uploadArea.innerHTML = `
            <i class="fas fa-check-circle text-success fa-2x mb-2"></i>
            <h6 class="text-success">File Selected Successfully!</h6>
            <p class="text-muted mb-0">${file.name}</p>
            <small class="text-muted">${formatFileSize(file.size)}</small>
        `;
    }
    
    showNotification(`File "${file.name}" selected successfully!`, 'success');
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Data Source Toggle
function initializeDataSourceToggle() {
    const dataSourceRadios = document.querySelectorAll('input[name="dataSource"]');
    const uploadSection = document.getElementById('uploadSection');
    
    dataSourceRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'upload') {
                uploadSection.style.display = 'block';
                uploadSection.classList.add('fade-in-up');
            } else {
                uploadSection.style.display = 'none';
            }
        });
    });
}

// Progress Tracking
function initializeProgressTracking() {
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    
    if (progressBar && progressText) {
        // Simulate progress updates
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 10;
            if (progress >= 100) {
                progress = 100;
                clearInterval(interval);
            }
            
            progressBar.style.width = progress + '%';
            progressBar.setAttribute('aria-valuenow', progress);
            
            if (progress < 30) {
                progressText.textContent = '📥 Fetching dataset...';
            } else if (progress < 60) {
                progressText.textContent = '🧹 Cleaning data...';
            } else if (progress < 90) {
                progressText.textContent = '🎯 Running segmentation...';
            } else {
                progressText.textContent = '✅ Analysis completed!';
            }
        }, 500);
    }
}

// Run Analysis Function
function runAnalysis() {
    const form = document.getElementById('segmentationForm');
    const progressSection = document.getElementById('progressSection');
    const resultsSection = document.getElementById('resultsSection');
    
    if (!form) return;
    
    // Show progress section
    if (progressSection) {
        progressSection.style.display = 'block';
        progressSection.classList.add('fade-in-up');
    }
    
    // Hide results section
    if (resultsSection) {
        resultsSection.style.display = 'none';
    }
    
    // Get form data
    const formData = new FormData(form);
    
    // Show loading state
    showNotification('🚀 Starting analysis...', 'info');
    
    // Send AJAX request
    fetch('/run_segmentation', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('✅ Analysis started successfully!', 'success');
            pollAnalysisProgress();
        } else {
            showNotification('❌ Error starting analysis: ' + data.error, 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('❌ Network error occurred', 'danger');
    });
}

// Poll for analysis progress
function pollAnalysisProgress() {
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const resultsSection = document.getElementById('resultsSection');
    
    let attempts = 0;
    const maxAttempts = 60; // 5 minutes max
    
    const poll = () => {
        fetch('/api/analysis-progress')
            .then(response => response.json())
            .then(data => {
                attempts++;
                
                if (data.status === 'completed') {
                    // Analysis completed
                    if (progressBar) progressBar.style.width = '100%';
                    if (progressText) progressText.textContent = '✅ Analysis completed!';
                    
                    showNotification('🎉 Analysis completed successfully!', 'success');
                    
                    // Show results after a short delay
                    setTimeout(() => {
                        if (resultsSection) {
                            resultsSection.style.display = 'block';
                            resultsSection.classList.add('fade-in-up');
                        }
                        loadResults();
                    }, 1000);
                    
                } else if (data.status === 'processing') {
                    // Still processing
                    const progress = Math.min(90, 30 + (attempts * 2));
                    if (progressBar) progressBar.style.width = progress + '%';
                    
                    if (attempts < maxAttempts) {
                        setTimeout(poll, 2000); // Poll every 2 seconds
                    } else {
                        showNotification('⏰ Analysis is taking longer than expected...', 'warning');
                    }
                    
                } else {
                    // Not started or error
                    if (attempts < maxAttempts) {
                        setTimeout(poll, 3000); // Poll every 3 seconds
                    } else {
                        showNotification('❌ Analysis failed to start', 'danger');
                    }
                }
            })
            .catch(error => {
                console.error('Polling error:', error);
                if (attempts < maxAttempts) {
                    setTimeout(poll, 5000); // Poll every 5 seconds on error
                }
            });
    };
    
    poll();
}

// Load Results
function loadResults() {
    const resultsContainer = document.getElementById('resultsContainer');
    
    if (!resultsContainer) return;
    
    fetch('/api/results')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayResults(data.results);
            } else {
                showNotification('❌ Error loading results', 'danger');
            }
        })
        .catch(error => {
            console.error('Error loading results:', error);
            showNotification('❌ Network error loading results', 'danger');
        });
}

// Display Results
function displayResults(results) {
    const resultsContainer = document.getElementById('resultsContainer');
    
    if (!resultsContainer) return;
    
    resultsContainer.innerHTML = `
        <div class="row">
            <div class="col-12">
                <div class="alert alert-success">
                    <h5><i class="fas fa-check-circle me-2"></i>Analysis Summary</h5>
                    <p class="mb-0">Total customers: ${results.total_customers || 'N/A'}</p>
                    <p class="mb-0">Segments: ${results.n_clusters || 'N/A'}</p>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-chart-bar me-2"></i>Segment Details</h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-hover">
                                <thead>
                                    <tr>
                                        <th>Segment</th>
                                        <th>Count</th>
                                        <th>Percentage</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${Object.entries(results.cluster_sizes || {}).map(([segment, count]) => `
                                        <tr>
                                            <td><span class="badge bg-primary">${segment}</span></td>
                                            <td>${count}</td>
                                            <td>${((count / results.total_customers) * 100).toFixed(1)}%</td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Notification System
function initializeNotifications() {
    // Create notification container if it doesn't exist
    if (!document.getElementById('notificationContainer')) {
        const container = document.createElement('div');
        container.id = 'notificationContainer';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 400px;
        `;
        document.body.appendChild(container);
    }
}

function showNotification(message, type = 'info') {
    const container = document.getElementById('notificationContainer');
    if (!container) return;
    
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show`;
    notification.style.cssText = `
        margin-bottom: 10px;
        box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.1);
        border: none;
        border-radius: 8px;
    `;
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    container.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Page-specific initializations
function initializeSegmentationPage() {
    console.log('📊 Segmentation page initialized');
    
    // Add form submission handler
    const form = document.getElementById('segmentationForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            runAnalysis();
        });
    }
    
    // Add reset functionality
    const resetBtn = document.getElementById('resetBtn');
    if (resetBtn) {
        resetBtn.addEventListener('click', resetForm);
    }
}

function initializeResultsPage() {
    console.log('📈 Results page initialized');
    
    // Add animation classes
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in-up');
    });
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Reset Form
function resetForm() {
    const form = document.getElementById('segmentationForm');
    const uploadArea = document.getElementById('uploadArea');
    const progressSection = document.getElementById('progressSection');
    const resultsSection = document.getElementById('resultsSection');
    
    if (form) {
        form.reset();
    }
    
    if (uploadArea) {
        uploadArea.classList.remove('file-selected');
        uploadArea.innerHTML = `
            <i class="fas fa-cloud-upload-alt fa-3x text-primary mb-3"></i>
            <h5>Drag & Drop your file here</h5>
            <p class="text-muted">or click to browse</p>
            <small class="text-muted">Supports CSV, XLSX files</small>
        `;
    }
    
    if (progressSection) {
        progressSection.style.display = 'none';
    }
    
    if (resultsSection) {
        resultsSection.style.display = 'none';
    }
    
    showNotification('🔄 Form reset successfully!', 'info');
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

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Export functions for global access
window.JanahSegmentation = {
    runAnalysis,
    resetForm,
    showNotification,
    handleFileSelection
};
