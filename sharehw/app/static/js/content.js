// Content Search and Filter Handling
class ContentSearch {
    constructor(formId, resultsContainerId) {
        this.form = document.getElementById(formId);
        this.resultsContainer = document.getElementById(resultsContainerId);
        this.setupEventListeners();
    }

    setupEventListeners() {
        if (!this.form) return;

        // Debounce search input
        const searchInput = this.form.querySelector('input[name="q"]');
        if (searchInput) {
            searchInput.addEventListener('input', this.debounce(() => {
                this.submitSearch();
            }, 500));
        }

        // Handle filter changes
        const filterSelects = this.form.querySelectorAll('select');
        filterSelects.forEach(select => {
            select.addEventListener('change', () => {
                this.submitSearch();
            });
        });
    }

    debounce(func, wait) {
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

    async submitSearch() {
        const formData = new FormData(this.form);
        const queryString = new URLSearchParams(formData).toString();
        const currentPath = window.location.pathname;

        try {
            const response = await fetch(`${currentPath}?${queryString}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (response.ok) {
                const html = await response.text();
                this.resultsContainer.innerHTML = html;
                // Update URL without page reload
                window.history.pushState({}, '', `${currentPath}?${queryString}`);
            }
        } catch (error) {
            console.error('Search error:', error);
        }
    }
}

// File Upload Handling
class FileUpload {
    constructor(inputId, options = {}) {
        this.input = document.getElementById(inputId);
        this.options = {
            maxSize: 8 * 1024 * 1024, // 8MB default
            allowedTypes: [
                'application/pdf',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'text/plain',
                'image/jpeg',
                'image/png',
                'image/gif',
                'application/vnd.ms-excel',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'application/vnd.ms-powerpoint',
                'application/vnd.openxmlformats-officedocument.presentationml.presentation'
            ],
            ...options
        };
        this.setupEventListeners();
    }

    setupEventListeners() {
        if (!this.input) return;

        this.input.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (!file) return;

            if (!this.validateFileSize(file)) {
                alert('File size exceeds the maximum limit of 8MB');
                this.input.value = '';
                return;
            }

            if (!this.validateFileType(file)) {
                alert('Invalid file type. Please upload a supported document format.');
                this.input.value = '';
                return;
            }
        });
    }

    validateFileSize(file) {
        return file.size <= this.options.maxSize;
    }

    validateFileType(file) {
        return this.options.allowedTypes.includes(file.type);
    }
}

// Notes Visibility Toggle
class NotesVisibility {
    constructor() {
        this.setupEventListeners();
    }

    setupEventListeners() {
        const toggleButtons = document.querySelectorAll('[data-toggle-visibility]');
        toggleButtons.forEach(button => {
            button.addEventListener('click', async (e) => {
                e.preventDefault();
                const notesId = button.dataset.toggleVisibility;
                await this.toggleVisibility(notesId);
            });
        });
    }

    async toggleVisibility(notesId) {
        try {
            const response = await fetch(`/content/notes/${notesId}/toggle-visibility`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.updateVisibilityUI(notesId, data.is_public);
            }
        } catch (error) {
            console.error('Toggle visibility error:', error);
        }
    }

    updateVisibilityUI(notesId, isPublic) {
        const badge = document.querySelector(`[data-notes-id="${notesId}"] .visibility-badge`);
        const button = document.querySelector(`[data-toggle-visibility="${notesId}"]`);

        if (badge) {
            badge.textContent = isPublic ? 'Public' : 'Private';
            badge.classList.toggle('bg-success', isPublic);
            badge.classList.toggle('bg-secondary', !isPublic);
        }

        if (button) {
            const icon = button.querySelector('i');
            icon.classList.toggle('fa-lock', !isPublic);
            icon.classList.toggle('fa-globe', isPublic);
            button.querySelector('span').textContent = isPublic ? 'Make Private' : 'Make Public';
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Handle search form submission
    const searchForm = document.querySelector('#content-search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            updateContent();
        });

        // Handle filter changes
        const filterInputs = searchForm.querySelectorAll('select, input[type="search"]');
        filterInputs.forEach(input => {
            input.addEventListener('change', function() {
                updateContent();
            });
        });
    }

    // Handle visibility toggle
    document.addEventListener('click', function(e) {
        if (e.target.closest('.visibility-toggle')) {
            const button = e.target.closest('.visibility-toggle');
            const notesId = button.dataset.notesId;
            toggleNotesVisibility(notesId, button);
        }
    });

    // Handle pagination clicks
    document.addEventListener('click', function(e) {
        const pageLink = e.target.closest('.page-link');
        if (pageLink && !pageLink.closest('.disabled')) {
            e.preventDefault();
            const url = new URL(pageLink.href);
            updateContent(url.search);
        }
    });
});

function updateContent(queryString = '') {
    const searchForm = document.querySelector('#content-search-form');
    const contentList = document.querySelector('#content-list');
    const loadingSpinner = document.querySelector('#loading-spinner');

    if (!searchForm || !contentList) return;

    // Show loading spinner
    if (loadingSpinner) loadingSpinner.classList.remove('d-none');

    // Build query string from form data if not provided
    if (!queryString) {
        const formData = new FormData(searchForm);
        queryString = '?' + new URLSearchParams(formData).toString();
    }

    // Update URL without reloading
    const newUrl = `${window.location.pathname}${queryString}`;
    window.history.pushState({ path: newUrl }, '', newUrl);

    // Make AJAX request
    fetch(newUrl, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.text())
    .then(html => {
        contentList.innerHTML = html;
        // Reinitialize tooltips
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl)
        });
    })
    .catch(error => {
        console.error('Error:', error);
        contentList.innerHTML = `
            <div class="alert alert-danger" role="alert">
                An error occurred while loading content. Please try again.
            </div>
        `;
    })
    .finally(() => {
        if (loadingSpinner) loadingSpinner.classList.add('d-none');
    });
}

function toggleNotesVisibility(notesId, button) {
    const icon = button.querySelector('i');
    
    fetch(`/content/notes/${notesId}/toggle-visibility`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        // Update icon
        icon.classList.remove('fa-globe', 'fa-lock');
        icon.classList.add(data.is_public ? 'fa-globe' : 'fa-lock');
        
        // Show toast notification
        const toast = new bootstrap.Toast(document.querySelector('.toast'));
        document.querySelector('.toast-body').textContent = data.message;
        toast.show();
    })
    .catch(error => {
        console.error('Error:', error);
        const toast = new bootstrap.Toast(document.querySelector('.toast'));
        document.querySelector('.toast-body').textContent = 'An error occurred. Please try again.';
        toast.show();
    });
}

// File upload validation
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.querySelector('input[type="file"]');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            validateFile(this);
        });
    }
});

function validateFile(input) {
    const maxSize = 8 * 1024 * 1024; // 8MB
    const allowedTypes = [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain',
        'image/jpeg',
        'image/png',
        'image/gif',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-powerpoint',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation'
    ];

    const file = input.files[0];
    const errorElement = document.querySelector('#file-error');
    const submitButton = document.querySelector('button[type="submit"]');

    if (!errorElement || !submitButton) return;

    let error = '';

    if (file) {
        if (file.size > maxSize) {
            error = 'File size must be less than 8MB';
        } else if (!allowedTypes.includes(file.type)) {
            error = 'Invalid file type. Please upload a PDF, Word, Text, Excel, PowerPoint or image file.';
        }
    }

    errorElement.textContent = error;
    submitButton.disabled = error !== '';
}

// Delete confirmation
document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.delete-content');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this content? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
});
