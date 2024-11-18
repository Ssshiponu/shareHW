// Dark Mode Toggle
document.addEventListener('DOMContentLoaded', function() {
    // Check for saved dark mode preference
    const darkMode = localStorage.getItem('darkMode') === 'true';
    if (darkMode) {
        document.body.classList.add('dark-mode');
    }

    // Add dark mode toggle button to navbar if it doesn't exist
    const navbar = document.querySelector('.navbar-nav');
    if (navbar && !document.getElementById('darkModeToggle')) {
        const darkModeToggle = document.createElement('li');
        darkModeToggle.className = 'nav-item';
        darkModeToggle.innerHTML = `
            <button class="nav-link btn btn-link" id="darkModeToggle">
                <i class="fas ${darkMode ? 'fa-sun' : 'fa-moon'}"></i>
            </button>
        `;
        navbar.appendChild(darkModeToggle);

        // Add click event listener
        document.getElementById('darkModeToggle').addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            const isDarkMode = document.body.classList.contains('dark-mode');
            localStorage.setItem('darkMode', isDarkMode);
            this.querySelector('i').className = `fas ${isDarkMode ? 'fa-sun' : 'fa-moon'}`;
        });
    }
});

// File Upload Preview
document.addEventListener('DOMContentLoaded', function() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name;
            const label = input.nextElementSibling;
            if (label && label.classList.contains('custom-file-label')) {
                label.textContent = fileName || 'Choose file';
            }
        });
    });
});

// Form Validation
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
});

// Toast Notifications
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) {
        const container = document.createElement('div');
        container.id = 'toastContainer';
        container.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 1050;';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast bg-${type} text-white`;
    toast.innerHTML = `
        <div class="toast-header bg-${type} text-white">
            <strong class="me-auto">Notification</strong>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
        </div>
        <div class="toast-body">${message}</div>
    `;

    document.getElementById('toastContainer').appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();

    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

// Confirm Dialog
function confirmDialog(message, callback) {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Confirm Action</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">${message}</div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary" id="confirmYes">Yes</button>
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(modal);
    const modalInstance = new bootstrap.Modal(modal);
    modalInstance.show();

    document.getElementById('confirmYes').addEventListener('click', function() {
        modalInstance.hide();
        callback(true);
    });

    modal.addEventListener('hidden.bs.modal', function() {
        modal.remove();
        if (!document.getElementById('confirmYes')) {
            callback(false);
        }
    });
}

// Timeago
document.addEventListener('DOMContentLoaded', function() {
    const timeElements = document.querySelectorAll('time.timeago');
    timeElements.forEach(element => {
        const datetime = element.getAttribute('datetime');
        element.textContent = timeago.format(datetime);
    });
});

// Search Functionality
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        let timeout = null;
        searchInput.addEventListener('input', function(e) {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                const query = e.target.value.trim();
                if (query.length >= 2) {
                    fetch(`/content/search?q=${encodeURIComponent(query)}`)
                        .then(response => response.json())
                        .then(data => {
                            const resultsContainer = document.getElementById('searchResults');
                            resultsContainer.innerHTML = '';
                            data.forEach(item => {
                                const div = document.createElement('div');
                                div.className = 'list-group-item list-group-item-action';
                                div.innerHTML = `
                                    <div class="d-flex w-100 justify-content-between">
                                        <h6 class="mb-1">${item.title}</h6>
                                        <small class="text-muted">${item.type}</small>
                                    </div>
                                    <p class="mb-1">${item.subject}</p>
                                `;
                                div.addEventListener('click', () => {
                                    window.location.href = item.url;
                                });
                                resultsContainer.appendChild(div);
                            });
                        })
                        .catch(error => console.error('Error:', error));
                }
            }, 300);
        });
    }
});
