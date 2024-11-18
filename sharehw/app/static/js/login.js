document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const errorContainer = document.getElementById('error-container');
    const successContainer = document.getElementById('success-container');
    const togglePasswordBtn = document.getElementById('togglePassword');
    const passwordInput = document.querySelector('input[type="password"]');

    // Password visibility toggle
    if (togglePasswordBtn && passwordInput) {
        togglePasswordBtn.addEventListener('click', function() {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            
            // Toggle icon
            const icon = this.querySelector('i');
            icon.classList.toggle('fa-eye');
            icon.classList.toggle('fa-eye-slash');
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Clear previous messages
            clearMessages();
            
            // Basic client-side validation
            const email = loginForm.querySelector('input[name="email"]').value;
            const password = loginForm.querySelector('input[name="password"]').value;
            
            if (!email || !isValidEmail(email)) {
                showError('Please enter a valid email address');
                return;
            }
            
            if (!password) {
                showError('Please enter your password');
                return;
            }
            
            // Disable form submission while processing
            const submitButton = loginForm.querySelector('button[type="submit"]');
            setLoading(submitButton, true);

            const formData = new FormData(loginForm);

            fetch('/auth/login', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    showSuccess(data.message);
                    
                    // Redirect after successful login
                    if (data.redirect) {
                        setTimeout(() => {
                            window.location.href = data.redirect;
                        }, 1000);
                    }
                } else {
                    handleErrors(data);
                }
            })
            .catch(error => {
                console.error('Login error:', error);
                showError('An error occurred. Please try again later.');
            })
            .finally(() => {
                setLoading(submitButton, false);
            });
        });

        // Clear validation state on input
        loginForm.querySelectorAll('input').forEach(input => {
            input.addEventListener('input', function() {
                this.classList.remove('is-invalid');
                const feedbackDiv = this.nextElementSibling;
                if (feedbackDiv && feedbackDiv.classList.contains('invalid-feedback')) {
                    feedbackDiv.textContent = '';
                }
                clearMessages();
            });
        });
    }

    // Helper functions
    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    function clearMessages() {
        errorContainer.innerHTML = '';
        errorContainer.style.display = 'none';
        successContainer.innerHTML = '';
        successContainer.style.display = 'none';
    }

    function showError(message) {
        errorContainer.innerHTML = `<div class="alert alert-danger">${message}</div>`;
        errorContainer.style.display = 'block';
    }

    function showSuccess(message) {
        successContainer.innerHTML = `<div class="alert alert-success">${message}</div>`;
        successContainer.style.display = 'block';
    }

    function setLoading(button, isLoading) {
        button.disabled = isLoading;
        button.innerHTML = isLoading ? 
            '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Logging in...' : 
            'Log In';
    }

    function handleErrors(data) {
        if (data.message) {
            showError(data.message);
        }
        
        if (data.errors) {
            Object.entries(data.errors).forEach(([field, messages]) => {
                const inputField = loginForm.querySelector(`[name="${field}"]`);
                if (inputField) {
                    inputField.classList.add('is-invalid');
                    const feedbackDiv = inputField.nextElementSibling;
                    if (feedbackDiv && feedbackDiv.classList.contains('invalid-feedback')) {
                        feedbackDiv.textContent = messages[0];
                    }
                }
            });
        }
    }
});
