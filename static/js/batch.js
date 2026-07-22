document.addEventListener('DOMContentLoaded', function () {
    const courseSelect = document.getElementById('course_id');
    const startDateInput = document.getElementById('start_date');
    const slotTypeSelect = document.getElementById('slot_type');
    const endDateInput = document.getElementById('end_date');
    const endDateBadge = document.getElementById('calculated_end_date_badge');
    const projectDateBadge = document.getElementById('calculated_project_date_badge');

    function calculateEstimatedEndDate() {
        if (!courseSelect || !startDateInput || !slotTypeSelect || !endDateInput) return;

        const courseId = courseSelect.value;
        const startDate = startDateInput.value;
        const slotType = slotTypeSelect.value;

        if (courseId && startDate && slotType) {
            if (endDateBadge) {
                endDateBadge.innerText = 'Calculating...';
                endDateBadge.style.display = 'inline-block';
            }

            fetch(`/api/calculate-end-date?course_id=${encodeURIComponent(courseId)}&start_date=${encodeURIComponent(startDate)}&slot_type=${encodeURIComponent(slotType)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success && data.end_date) {
                        endDateInput.value = data.end_date;
                        if (endDateBadge) {
                            endDateBadge.innerText = `Auto-calculated: ${data.end_date}`;
                            endDateBadge.className = 'badge badge-info';
                        }
                        if (projectDateBadge && data.project_date) {
                            projectDateBadge.innerText = `Project Submission: ${data.project_date}`;
                            projectDateBadge.className = 'badge badge-info';
                            projectDateBadge.style.display = 'inline-block';
                        }
                    } else {
                        if (endDateBadge) {
                            endDateBadge.innerText = data.error || 'Calculation unavailable';
                            endDateBadge.className = 'badge badge-warning';
                        }
                    }
                })
                .catch(err => {
                    console.error('Error calculating end date:', err);
                    if (endDateBadge) {
                        endDateBadge.innerText = 'Calculation failed';
                        endDateBadge.className = 'badge badge-warning';
                    }
                });
        }
    }

    if (courseSelect) courseSelect.addEventListener('change', calculateEstimatedEndDate);
    if (startDateInput) startDateInput.addEventListener('change', calculateEstimatedEndDate);
    if (slotTypeSelect) slotTypeSelect.addEventListener('change', calculateEstimatedEndDate);

    // Initial calculation if editing or pre-filled
    if (courseSelect && courseSelect.value && startDateInput && startDateInput.value && slotTypeSelect && slotTypeSelect.value && (!endDateInput || !endDateInput.value)) {
        calculateEstimatedEndDate();
    }
});

