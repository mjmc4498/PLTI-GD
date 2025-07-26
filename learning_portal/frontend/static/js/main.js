document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/courses')
        .then(response => response.json())
        .then(data => {
            const courseCards = document.getElementById('course-cards');
            data.forEach(course => {
                const card = document.createElement('div');
                card.className = 'course-card';
                card.innerHTML = `
                    <div class="course-card-content">
                        <h3>${course.name}</h3>
                        <p>${course.description}</p>
                        <p><strong>Instructor:</strong> ${course.instructor}</p>
                        <p><strong>Duración:</strong> ${course.duration} horas</p>
                        <span class="status status-in_progress">En progreso</span>
                    </div>
                `;
                card.addEventListener('click', () => {
                    window.location.href = `/courses/${course.id}`;
                });
                courseCards.appendChild(card);
            });
        });
});
