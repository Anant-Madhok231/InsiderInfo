// Add event listeners when the document is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Search functionality
    const searchInputs = document.querySelectorAll('input[type="text"]');
    searchInputs.forEach(input => {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                // Implement search functionality
                console.log('Searching for:', this.value);
            }
        });
    });

    // Login/Signup button handlers
    const loginBtn = document.querySelector('.login-btn');
    const signupBtn = document.querySelector('.signup-btn');
    
    loginBtn.addEventListener('click', () => {
        window.location.href = '/login';
    });

    signupBtn.addEventListener('click', () => {
        window.location.href = '/signup';
    });

    // Action button handlers
    const actionButtons = document.querySelectorAll('.action-buttons button');
    actionButtons.forEach(button => {
        button.addEventListener('click', function() {
            console.log(this.textContent.trim(), 'clicked');
            // Implement respective functionality
        });
    });

    // Animate elements when they come into view
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });

    // Observe all stock cards
    document.querySelectorAll('.stock-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        observer.observe(card);
    });

    // Animate score numbers
    document.querySelectorAll('.score').forEach(score => {
        const finalValue = parseInt(score.textContent);
        let currentValue = 0;
        const duration = 2000; // 2 seconds
        const increment = finalValue / (duration / 16); // 60fps

        function updateCounter() {
            if (currentValue < finalValue) {
                currentValue += increment;
                score.textContent = Math.round(currentValue);
                requestAnimationFrame(updateCounter);
            } else {
                score.textContent = finalValue;
            }
        }

        updateCounter();
    });

    // Add hover animation for the stocks button
    const stocksButton = document.querySelector('.stocks-button');
    if (stocksButton) {
        stocksButton.addEventListener('mousemove', (e) => {
            const rect = e.target.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            stocksButton.style.setProperty('--x', `${x}px`);
            stocksButton.style.setProperty('--y', `${y}px`);
        });
    }
}); 