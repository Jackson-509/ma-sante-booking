document.addEventListener('DOMContentLoaded', () => {
    // Ajouter une animation sur les cartes de services au survol
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px)';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });

    // Afficher le prix total en temps réel
    const form = document.querySelector('.booking-form');
    const totalDisplay = document.createElement('div');
    totalDisplay.style.margin = '20px 0';
    totalDisplay.style.fontWeight = 'bold';
    totalDisplay.style.color = '#002f5f';
    form.insertBefore(totalDisplay, form.lastElementChild);

    form.addEventListener('change', (e) => {
        if (e.target.name === 'service') {
            const selectedService = document.querySelector('input[name="service"]:checked');
            if (selectedService) {
                const prix = selectedService.closest('.service-card').querySelector('p:last-child').textContent;
                totalDisplay.textContent = `Prix total : ${prix}`;
            }
        }
    });
});
