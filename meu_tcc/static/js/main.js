// Bootstrap JS Bundle should be included in your HTML, not in this JS file.

        // Script para mostrar/esconder senha (será implementado na página de login)
        document.addEventListener('DOMContentLoaded', function() {
            // Smooth scrolling para links de navegação
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
        });
    
