// Main JavaScript for GameShop

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages after 5 seconds
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.style.transition = 'opacity 0.5s ease-in-out';
            alert.style.opacity = '0';
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.parentNode.removeChild(alert);
                }
            }, 500);
        });
    }, 5000);

    // Add smooth scrolling to all links
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

    // Form validation enhancement
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = this.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('border-red-500');
                    
                    // Add error message
                    if (!field.nextElementSibling?.classList.contains('error-message')) {
                        const errorMsg = document.createElement('p');
                        errorMsg.className = 'error-message text-red-500 text-sm mt-1';
                        errorMsg.textContent = 'Это поле обязательно для заполнения';
                        field.parentNode.appendChild(errorMsg);
                    }
                } else {
                    field.classList.remove('border-red-500');
                    const errorMsg = field.parentNode.querySelector('.error-message');
                    if (errorMsg) {
                        errorMsg.remove();
                    }
                }
            });

            if (!isValid) {
                e.preventDefault();
                
                // Show notification
                const notification = document.createElement('div');
                notification.className = 'fixed top-4 right-4 bg-red-500 text-white p-4 rounded-lg shadow-lg z-50';
                notification.innerHTML = `
                    <div class="flex items-center">
                        <i class="fas fa-exclamation-triangle mr-2"></i>
                        <span>Пожалуйста, заполните все обязательные поля</span>
                    </div>
                `;
                document.body.appendChild(notification);
                
                setTimeout(() => {
                    notification.remove();
                }, 3000);
            }
        });
    });

    // Password strength indicator
    const passwordInput = document.getElementById('password');
    if (passwordInput) {
        const strengthIndicator = document.createElement('div');
        strengthIndicator.className = 'password-strength mt-2';
        passwordInput.parentNode.appendChild(strengthIndicator);

        passwordInput.addEventListener('input', function() {
            const password = this.value;
            let strength = 0;
            let message = '';
            let color = 'red';

            if (password.length >= 8) strength++;
            if (/[A-Z]/.test(password)) strength++;
            if (/[a-z]/.test(password)) strength++;
            if (/[0-9]/.test(password)) strength++;
            if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) strength++;

            switch(strength) {
                case 0:
                case 1:
                    message = 'Слабый пароль';
                    color = 'red';
                    break;
                case 2:
                case 3:
                    message = 'Средний пароль';
                    color = 'yellow';
                    break;
                case 4:
                    message = 'Хороший пароль';
                    color = 'blue';
                    break;
                case 5:
                    message = 'Отличный пароль!';
                    color = 'green';
                    break;
            }

            strengthIndicator.innerHTML = `
                <div class="flex items-center">
                    <div class="w-full bg-gray-200 rounded-full h-2 mr-3">
                        <div class="h-2 rounded-full bg-${color}-500" style="width: ${strength * 20}%"></div>
                    </div>
                    <span class="text-sm text-${color}-600 font-semibold">${message}</span>
                </div>
            `;
        });
    }

    // Price formatting
    document.querySelectorAll('.price').forEach(priceElement => {
        const price = parseFloat(priceElement.textContent);
        if (!isNaN(price)) {
            priceElement.textContent = new Intl.NumberFormat('ru-RU', {
                style: 'currency',
                currency: 'RUB'
            }).format(price);
        }
    });

    // Mobile menu toggle (if needed in future)
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Add loading states to buttons
    document.querySelectorAll('button[type="submit"]').forEach(button => {
        button.addEventListener('click', function() {
            if (this.form.checkValidity()) {
                this.innerHTML = `
                    <i class="fas fa-spinner fa-spin mr-2"></i>
                    Обработка...
                `;
                this.disabled = true;
            }
        });
    });

    // Copy to clipboard functionality
    document.querySelectorAll('.copy-btn').forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-copy');
            navigator.clipboard.writeText(textToCopy).then(() => {
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-check mr-2"></i>Скопировано!';
                this.classList.add('bg-green-500');
                
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.classList.remove('bg-green-500');
                }, 2000);
            });
        });
    });

    console.log('GameShop JavaScript loaded successfully! 🎮');
});

// Utility functions
const GameShop = {
    // Format date
    formatDate: (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('ru-RU', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    },

    // Show notification
    showNotification: (message, type = 'info') => {
        const notification = document.createElement('div');
        const bgColor = type === 'success' ? 'bg-green-500' : 
                       type === 'error' ? 'bg-red-500' : 
                       type === 'warning' ? 'bg-yellow-500' : 'bg-blue-500';
        
        notification.className = `fixed top-4 right-4 ${bgColor} text-white p-4 rounded-lg shadow-lg z-50 transform translate-x-full transition-transform duration-300`;
        notification.innerHTML = `
            <div class="flex items-center">
                <i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'exclamation-triangle' : 'info'}-circle mr-2"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 100);
        
        // Animate out and remove
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    },

    // Confirm action
    confirmAction: (message) => {
        return confirm(message || 'Вы уверены, что хотите выполнить это действие?');
    }
};