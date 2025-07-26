document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/courses')
        .then(response => response.json())
        .then(data => {
            const courseCards = document.getElementById('course-cards');
            data.forEach(course => {
                const cardCol = document.createElement('div');
                cardCol.className = 'col-md-4 mb-4';

                const card = document.createElement('div');
                card.className = 'card h-100 shadow-sm course-card';

                card.innerHTML = `
                    <div class="card-body">
                        <h5 class="card-title">${course.name}</h5>
                        <p class="card-text">${course.description}</p>
                        <p class="card-text"><small class="text-muted">Instructor: ${course.instructor}</small></p>
                        <p class="card-text"><small class="text-muted">Duración: ${course.duration} horas</small></p>
                        <span class="badge bg-warning text-dark">En progreso</span>
                    </div>
                `;

                card.addEventListener('click', () => {
                    window.location.href = `/courses/${course.id}`;
                });

                cardCol.appendChild(card);
                courseCards.appendChild(cardCol);
            });
        });
});
