document.addEventListener('DOMContentLoaded', () => {

    // 1. Delete Confirmation
    const deleteForms = document.querySelectorAll('.delete-form');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function (e) {
            const confirmed = confirm("Are you sure you want to delete this course? This action cannot be undone.");
            if (!confirmed) {
                e.preventDefault();
            }
        });
    });

    // 2. Client-side Form Validation
    const courseForm = document.getElementById('courseForm');
    if (courseForm) {
        courseForm.addEventListener('submit', function (e) {
            const durationInput = document.getElementById('duration_hours');
            if (durationInput) {
                const duration = parseInt(durationInput.value, 10);
                if (isNaN(duration) || duration <= 0) {
                    alert("Course duration must be a positive number greater than 0.");
                    e.preventDefault();
                    durationInput.focus();
                }
            }
        });
    }

    // 3. Dynamic UI - Highlight Inactive Rows
    const courseRows = document.querySelectorAll('.course-row');
    courseRows.forEach(row => {
        const status = row.getAttribute('data-status');
        if (status === 'Inactive') {
            row.classList.add('inactive-row');
        }
    });

});
