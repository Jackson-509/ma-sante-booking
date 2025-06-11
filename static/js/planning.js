document.addEventListener('DOMContentLoaded', () => {
  // Gestion des clics sur les créneaux horaires
  const buttons = document.querySelectorAll('.slot-btn');
  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      const date = btn.dataset.date;
      const heure = btn.dataset.heure;
      const praticienId = new URLSearchParams(window.location.search).get('id');
      window.location.href = `/services/${praticienId}?date=${date}&heure=${heure}`;
    });
  });

  // Gestion de la navigation entre les semaines
  const prevWeekBtn = document.getElementById('prev-week');
  const nextWeekBtn = document.getElementById('next-week');
  const currentMonthElement = document.querySelector('.current-month');
  
  if (prevWeekBtn && nextWeekBtn && currentMonthElement) {
    // Récupérer la date de référence (premier jour affiché)
    const dateText = document.querySelector('.day-date')?.textContent;
    const monthYearText = currentMonthElement.textContent;
    
    // Convertir en objet Date (format: JJ/MM/AAAA)
    const [day, month, year] = dateText ? 
      [parseInt(dateText), ...monthYearText.split('/').map(Number)] : 
      [1, new Date().getMonth() + 1, new Date().getFullYear()];
    
    let currentDate = new Date(year, month - 1, day);
    
    // Mettre à jour l'affichage du mois/année
    const updateMonthDisplay = (date) => {
      const options = { month: 'long', year: 'numeric' };
      const monthYear = date.toLocaleDateString('fr-FR', options).replace(' ', ' ');
      currentMonthElement.textContent = monthYear;
    };
    
    // Navigation vers la semaine précédente
    prevWeekBtn.addEventListener('click', () => {
      currentDate.setDate(currentDate.getDate() - 7);
      updateMonthDisplay(currentDate);
      loadWeekData(currentDate);
    });
    
    // Navigation vers la semaine suivante
    nextWeekBtn.addEventListener('click', () => {
      currentDate.setDate(currentDate.getDate() + 7);
      updateMonthDisplay(currentDate);
      loadWeekData(currentDate);
    });
    
    // Fonction pour charger les données de la semaine
    const loadWeekData = (date) => {
      const praticienId = new URLSearchParams(window.location.search).get('id');
      const startDate = new Date(date);
      // Ajuster pour commencer au lundi
      const dayOfWeek = startDate.getDay() || 7; // 0 (dimanche) devient 7
      startDate.setDate(startDate.getDate() - (dayOfWeek - 1));
      
      // Simuler un chargement
      const loadingElement = document.createElement('div');
      loadingElement.className = 'loading';
      loadingElement.textContent = 'Chargement...';
      document.querySelector('.planning-grid')?.replaceWith(loadingElement);
      
      // Dans une vraie application, vous feriez une requête AJAX ici
      // Par exemple :
      // fetch(`/api/availability/${praticienId}?startDate=${startDate.toISOString()}`)
      //   .then(response => response.json())
      //   .then(data => updateCalendar(data))
      //   .catch(error => console.error('Erreur:', error));
      
      // Simulation de chargement
      setTimeout(() => {
        // Recharger la page avec les nouvelles dates
        // Dans une vraie application, vous mettriez à jour uniquement le DOM nécessaire
        window.location.href = `/reserver/${praticienId}?week=${startDate.toISOString().split('T')[0]}`;
      }, 500);
    };
    
    // Initialiser l'affichage du mois
    updateMonthDisplay(currentDate);
  }
});