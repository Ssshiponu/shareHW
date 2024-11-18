document.addEventListener('DOMContentLoaded', function() {
    const signupForm = document.getElementById('signup-form');
    const errorContainer = document.getElementById('error-container');
    const successContainer = document.getElementById('success-container');
    const togglePasswordBtns = document.querySelectorAll('.toggle-password');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    const classSelect = document.getElementById('class_name');
    const sectionSelect = document.getElementById('section');
    const roleRadios = document.querySelectorAll('.role-radio');
    const roleInput = document.getElementById('role');
    const loadingOverlay = document.querySelector('.loading-overlay');

    // Password visibility toggle
    togglePasswordBtns.forEach((btn) => {
        btn.addEventListener('click', function() {
            const input = this.closest('.form-floating').querySelector('input');
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);
            
            // Toggle icon
            const icon = this.querySelector('i');
            icon.classList.toggle('fa-eye');
            icon.classList.toggle('fa-eye-slash');
        });
    });

    // Role selection
    roleRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            // Remove selected class from all cards
            document.querySelectorAll('.role-card').forEach(card => {
                card.classList.remove('selected');
            });
            
            // Add selected class to chosen card
            this.closest('label').querySelector('.role-card').classList.add('selected');
            
            // Update hidden role input
            roleInput.value = this.value;
            validateRole();
        });
    });

    // Update available sections based on selected class
    function updateSections() {
        const selectedClass = classSelect.value;
        const sections = {
            'XI': ['Science A', 'Science B', 'Arts A', 'Arts B', 'Commerce A', 'Commerce B'],
            'XII': ['Science A', 'Science B', 'Arts A', 'Arts B', 'Commerce A', 'Commerce B']
        };
        
        // Clear current options
        sectionSelect.innerHTML = '<option value="">Select Section</option>';
        
        // Add new options
        if (selectedClass && sections[selectedClass]) {
            sections[selectedClass].forEach(section => {
                const option = document.createElement('option');
                option.value = section;
                option.textContent = section;
                sectionSelect.appendChild(option);
            });
        }

        // Validate section after updating options
        validateSection();
    }

    // Add event listener for class selection
    if (classSelect) {
        classSelect.addEventListener('change', updateSections);
        // Initialize sections on page load
        updateSections();
    }

    // Password strength indicator
    function checkPasswordStrength(password) {
        let strength = 0;
        const strengthBar = document.querySelector('.password-strength');
        const strengthText = document.querySelector('.password-strength-text');

        if (password.length >= 8) strength++;
        if (password.match(/[A-Z]/)) strength++;
        if (password.match(/[a-z]/)) strength++;
        if (password.match(/[0-9]/)) strength++;
        if (password.match(/[^A-Za-z0-9]/)) strength++;

        switch (strength) {
            case 0:
            case 1:
                strengthBar.style.width = '20%';
                strengthBar.style.backgroundColor = '#dc3545';
                strengthText.textContent = 'Very Weak';
                strengthText.style.color = '#dc3545';
                break;
            case 2:
                strengthBar.style.width = '40%';
                strengthBar.style.backgroundColor = '#ffc107';
                strengthText.textContent = 'Weak';
                strengthText.style.color = '#ffc107';
                break;
            case 3:
                strengthBar.style.width = '60%';
                strengthBar.style.backgroundColor = '#fd7e14';
                strengthText.textContent = 'Medium';
                strengthText.style.color = '#fd7e14';
                break;
            case 4:
                strengthBar.style.width = '80%';
                strengthBar.style.backgroundColor = '#20c997';
                strengthText.textContent = 'Strong';
                strengthText.style.color = '#20c997';
                break;
            case 5:
                strengthBar.style.width = '100%';
                strengthBar.style.backgroundColor = '#198754';
                strengthText.textContent = 'Very Strong';
                strengthText.style.color = '#198754';
                break;
        }

        return strength >= 3;
    }

    // Helper functions for messages
    function showError(message) {
        errorContainer.innerHTML = `<div class="alert alert-danger">${message}</div>`;
        errorContainer.style.display = 'block';
        successContainer.style.display = 'none';
    }

    function showSuccess(message) {
        successContainer.innerHTML = `<div class="alert alert-success">${message}</div>`;
        successContainer.style.display = 'block';
        errorContainer.style.display = 'none';
    }

    function clearMessages() {
        errorContainer.innerHTML = '';
        errorContainer.style.display = 'none';
        successContainer.innerHTML = '';
        successContainer.style.display = 'none';
    }

    // Validation functions
    function validateEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const input = document.getElementById('email');
        const isValid = regex.test(email);
        
        updateValidationState(input, isValid, 'Please enter a valid email address');
        return isValid;
    }

    function validatePassword(password) {
        const input = document.getElementById('password');
        const isValid = password.length >= 8 && /[A-Za-z]/.test(password) && /\d/.test(password);
        
        updateValidationState(input, isValid, 'Password must be at least 8 characters long and include letters and numbers');
        return isValid && checkPasswordStrength(password);
    }

    function validateConfirmPassword(confirmPassword) {
        const input = document.getElementById('confirm_password');
        const isValid = confirmPassword === passwordInput.value;
        
        updateValidationState(input, isValid, 'Passwords do not match');
        return isValid;
    }

    function validateRollNumber(rollNumber) {
        const input = document.getElementById('roll_number');
        const isValid = /^\d+$/.test(rollNumber) && rollNumber.length >= 6 && rollNumber.length <= 20;
        
        updateValidationState(input, isValid, 'Roll number must contain only digits (6-20 characters)');
        return isValid;
    }

    function validateFullName(name) {
        const input = document.getElementById('full_name');
        const isValid = /^[A-Za-z\s]{2,100}$/.test(name);
        
        updateValidationState(input, isValid, 'Full name must contain only letters and spaces (2-100 characters)');
        return isValid;
    }

    function validateClass() {
        const input = document.getElementById('class_name');
        const isValid = !!input.value;
        
        updateValidationState(input, isValid, 'Please select your class');
        return isValid;
    }

    function validateSection() {
        const input = document.getElementById('section');
        const isValid = !!input.value;
        
        updateValidationState(input, isValid, 'Please select your section');
        return isValid;
    }

    function validateRole() {
        const isValid = !!roleInput.value;
        const roleCards = document.querySelectorAll('.role-card');
        
        roleCards.forEach(card => {
            if (!isValid) {
                card.classList.add('border-danger');
            } else {
                card.classList.remove('border-danger');
            }
        });
        
        return isValid;
    }

    function updateValidationState(input, isValid, errorMessage) {
        input.classList.remove('is-valid', 'is-invalid');
        input.classList.add(isValid ? 'is-valid' : 'is-invalid');
        
        const feedbackDiv = input.nextElementSibling;
        if (feedbackDiv && feedbackDiv.classList.contains('invalid-feedback')) {
            feedbackDiv.textContent = isValid ? '' : errorMessage;
        }
    }

    // Real-time validation
    if (signupForm) {
        const inputs = {
            'full_name': validateFullName,
            'email': validateEmail,
            'roll_number': validateRollNumber,
            'class_name': validateClass,
            'section': validateSection,
            'password': validatePassword,
            'confirm_password': validateConfirmPassword
        };

        Object.entries(inputs).forEach(([id, validator]) => {
            const input = document.getElementById(id);
            if (input) {
                input.addEventListener('input', function() {
                    validator(this.value);
                    clearMessages();
                });
            }
        });

        // Special handling for password strength
        passwordInput.addEventListener('input', function() {
            checkPasswordStrength(this.value);
        });

        // Update confirm password validation when password changes
        passwordInput.addEventListener('input', function() {
            if (confirmPasswordInput.value) {
                validateConfirmPassword(confirmPasswordInput.value);
            }
        });
    }

    // Form submission handling
    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            e.preventDefault();
            clearMessages();

            // Get form values
            const formData = new FormData(signupForm);
            const values = Object.fromEntries(formData.entries());

            // Validate all fields
            const validations = {
                fullName: validateFullName(values.full_name),
                email: validateEmail(values.email),
                rollNumber: validateRollNumber(values.roll_number),
                className: validateClass(),
                section: validateSection(),
                role: validateRole(),
                password: validatePassword(values.password),
                confirmPassword: validateConfirmPassword(values.confirm_password)
            };

            // Check if all validations pass
            if (Object.values(validations).every(v => v)) {
                // Show loading overlay
                loadingOverlay.style.display = 'flex';
                
                // Disable form submission while processing
                const submitButton = signupForm.querySelector('button[type="submit"]');
                const spinner = submitButton.querySelector('.spinner-border');
                submitButton.disabled = true;
                spinner.classList.remove('d-none');
                submitButton.querySelector('span:not(.spinner-border)').textContent = 'Creating Account...';

                // Submit form
                fetch('/auth/signup', {
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
                        
                        // Redirect after successful signup
                        if (data.redirect) {
                            setTimeout(() => {
                                window.location.href = data.redirect;
                            }, 1500);
                        }
                    } else {
                        handleErrors(data);
                    }
                })
                .catch(error => {
                    console.error('Signup error:', error);
                    showError('An error occurred. Please try again later.');
                })
                .finally(() => {
                    // Hide loading overlay
                    loadingOverlay.style.display = 'none';
                    
                    // Reset button state
                    submitButton.disabled = false;
                    spinner.classList.add('d-none');
                    submitButton.querySelector('span:not(.spinner-border)').textContent = 'Create Account';
                });
            } else {
                // Show first validation error
                const firstError = Object.entries(validations).find(([_, valid]) => !valid)[0];
                showError(`Please fix the following error: ${getErrorMessage(firstError)}`);
            }
        });
    }

    // Error handling
    function getErrorMessage(field) {
        const messages = {
            fullName: 'Full name must contain only letters and spaces (2-100 characters)',
            email: 'Please enter a valid email address',
            rollNumber: 'Roll number must contain only digits (6-20 characters)',
            className: 'Please select your class',
            section: 'Please select your section',
            role: 'Please select your role',
            password: 'Password must be at least 8 characters long and include letters and numbers',
            confirmPassword: 'Passwords do not match'
        };
        return messages[field] || 'Please check your input';
    }

    function handleErrors(data) {
        if (data.message) {
            showError(data.message);
        }
        
        if (data.errors) {
            Object.entries(data.errors).forEach(([field, errors]) => {
                const input = document.getElementById(field);
                if (input) {
                    updateValidationState(input, false, errors[0]);
                }
            });
        }
    }
});
