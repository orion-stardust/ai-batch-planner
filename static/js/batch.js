document.addEventListener('DOMContentLoaded', function () {
    const courseSelect = document.getElementById('course_id');
    const startDateInput = document.getElementById('start_date');
    const slotTypeSelect = document.getElementById('slot_type');
    const endDateInput = document.getElementById('end_date');
    const endDateBadge = document.getElementById('calculated_end_date_badge');
    const projectDateBadge = document.getElementById('calculated_project_date_badge');

    const trainerSelect = document.getElementById('trainer_id');
    const batchForm = document.getElementById('batchForm');
    const studentListContainer = document.getElementById('student_list_container');
    const studentEnrollmentSection = document.getElementById('student_enrollment_section');
    const studentCountHint = document.getElementById('student_count_hint');
    const maxCapacityInput = document.getElementById('max_capacity');

    let initialTrainerId = '';
    let initialStudentIds = [];

    if (batchForm) {
        initialTrainerId = batchForm.getAttribute('data-initial-trainer') || '';
        try {
            initialStudentIds = JSON.parse(batchForm.getAttribute('data-initial-students') || '[]');
        } catch (e) {
            console.error('Error parsing initial students:', e);
        }
    }

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
                        updateTrainersAndStudents();
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

    function updateTrainersAndStudents() {
        if (!courseSelect) return;
        const courseId = courseSelect.value;

        if (!courseId) {
            if (trainerSelect) {
                trainerSelect.innerHTML = '<option value="">-- Unassigned --</option>';
            }
            if (studentEnrollmentSection) {
                studentEnrollmentSection.style.display = 'none';
            }
            return;
        }

        const slotType = slotTypeSelect ? slotTypeSelect.value : '';
        const startDate = startDateInput ? startDateInput.value : '';
        const endDate = endDateInput ? endDateInput.value : '';
        const batchId = batchForm ? (batchForm.getAttribute('data-batch-id') || '') : '';

        // Build query params
        let queryParams = `?slot_type=${encodeURIComponent(slotType)}&start_date=${encodeURIComponent(startDate)}&end_date=${encodeURIComponent(endDate)}`;
        if (batchId) {
            queryParams += `&exclude_batch_id=${encodeURIComponent(batchId)}`;
        }

        // Fetch Trainers
        fetch(`/api/courses/${courseId}/trainers${queryParams}`)
            .then(res => res.json())
            .then(data => {
                if (data.success && trainerSelect) {
                    let html = '<option value="">-- Unassigned --</option>';
                    let warningHtml = '';
                    
                    data.trainers.forEach(t => {
                        const isSelected = (t.trainer_id.toString() === trainerSelect.value.toString() || t.trainer_id.toString() === initialTrainerId.toString());
                        const selectedAttr = isSelected ? 'selected' : '';
                        
                        if (!t.has_conflict) {
                            html += `<option value="${t.trainer_id}" ${selectedAttr}>${t.full_name} (Skills: ${t.skills})</option>`;
                        } else {
                            if (isSelected) {
                                html += `<option value="${t.trainer_id}" ${selectedAttr} disabled>${t.full_name} (Conflict: already booked in ${t.conflict_batch_name})</option>`;
                                warningHtml = `<div style="color: #ff4d4d; margin-top: 0.25rem; font-size: 0.85rem;">Trainer ${t.full_name} is already assigned to batch "${t.conflict_batch_name}" during that time.</div>`;
                            }
                        }
                    });
                    trainerSelect.innerHTML = html;
                    
                    let warningEl = document.getElementById('trainer_conflict_warning');
                    if (!warningEl) {
                        warningEl = document.createElement('div');
                        warningEl.id = 'trainer_conflict_warning';
                        trainerSelect.parentNode.appendChild(warningEl);
                    }
                    warningEl.innerHTML = warningHtml;
                }
            })
            .catch(err => console.error('Error fetching trainers:', err));

        // Fetch Students
        fetch(`/api/courses/${courseId}/students${queryParams}`)
            .then(res => res.json())
            .then(data => {
                if (data.success && studentListContainer && studentEnrollmentSection) {
                    if (data.students.length === 0) {
                        studentListContainer.innerHTML = '<div style="color: var(--text-muted); font-size: 0.9rem; padding: 0.5rem 0;">No active students enrolled in this course.</div>';
                    } else {
                        let html = '';
                        data.students.forEach(s => {
                            const isChecked = initialStudentIds.includes(s.student_id) ? 'checked' : '';
                            
                            if (s.has_conflict) {
                                const labelText = `${s.full_name} &mdash; Already enrolled in "${s.conflict_batch_name}" (${s.conflict_slot})`;
                                html += `
                                    <label class="student-checkbox-item student-conflict" style="color: var(--text-muted); cursor: not-allowed; opacity: 0.6;">
                                        <input type="checkbox" name="student_ids" value="${s.student_id}" ${isChecked} class="student-checkbox student-checkbox-disabled" disabled>
                                        <div class="student-info">
                                            <span class="student-name" style="text-decoration: line-through;">${labelText}</span>
                                            <span class="student-details">${s.email} | ${s.phone}</span>
                                        </div>
                                    </label>
                                `;
                            } else {
                                html += `
                                    <label class="student-checkbox-item">
                                        <input type="checkbox" name="student_ids" value="${s.student_id}" ${isChecked} class="student-checkbox">
                                        <div class="student-info">
                                            <span class="student-name">${s.full_name}</span>
                                            <span class="student-details">${s.email} | ${s.phone}</span>
                                        </div>
                                    </label>
                                `;
                            }
                        });
                        studentListContainer.innerHTML = html;

                        const checkboxes = studentListContainer.querySelectorAll('.student-checkbox:not(.student-checkbox-disabled)');
                        checkboxes.forEach(cb => {
                            cb.addEventListener('change', validateCapacity);
                        });
                    }
                    studentEnrollmentSection.style.display = 'block';
                    validateCapacity();
                }
            })
            .catch(err => console.error('Error fetching students:', err));
    }

    function validateCapacity() {
        if (!studentListContainer || !maxCapacityInput) return;
        const selectedCount = studentListContainer.querySelectorAll('.student-checkbox:checked').length;
        const maxCapacity = parseInt(maxCapacityInput.value, 10) || 30;

        if (studentCountHint) {
            studentCountHint.innerText = `${selectedCount} / ${maxCapacity} student(s) selected`;
            if (selectedCount > maxCapacity) {
                studentCountHint.style.color = '#ff4d4d';
                studentCountHint.innerText += ' (Exceeds Max Capacity!)';
            } else {
                studentCountHint.style.color = '';
            }
        }
    }

    if (courseSelect) {
        courseSelect.addEventListener('change', calculateEstimatedEndDate);
        courseSelect.addEventListener('change', updateTrainersAndStudents);
    }
    if (startDateInput) {
        startDateInput.addEventListener('change', calculateEstimatedEndDate);
        startDateInput.addEventListener('change', updateTrainersAndStudents);
    }
    if (slotTypeSelect) {
        slotTypeSelect.addEventListener('change', calculateEstimatedEndDate);
        slotTypeSelect.addEventListener('change', updateTrainersAndStudents);
    }
    if (endDateInput) {
        endDateInput.addEventListener('change', updateTrainersAndStudents);
    }
    if (maxCapacityInput) {
        maxCapacityInput.addEventListener('input', validateCapacity);
    }

    if (batchForm) {
        batchForm.addEventListener('submit', function (e) {
            const trainerConflict = document.getElementById('trainer_conflict_warning');
            if (trainerConflict && trainerConflict.innerHTML.trim() !== '') {
                alert("Cannot save batch: Trainer has a schedule conflict.");
                e.preventDefault();
                return;
            }
            
            const selectedCount = studentListContainer ? studentListContainer.querySelectorAll('.student-checkbox:checked').length : 0;
            const maxCapacity = parseInt(maxCapacityInput.value, 10) || 30;
            if (selectedCount > maxCapacity) {
                alert("Cannot save batch: Selected student count exceeds max capacity.");
                e.preventDefault();
                return;
            }
        });
    }

    // Initial calculation & list fetch if editing or pre-filled
    if (courseSelect && courseSelect.value) {
        updateTrainersAndStudents();
        if (startDateInput && startDateInput.value && slotTypeSelect && slotTypeSelect.value && (!endDateInput || !endDateInput.value)) {
            calculateEstimatedEndDate();
        }
    }
});

