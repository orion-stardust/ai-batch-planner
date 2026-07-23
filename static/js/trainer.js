document.addEventListener('DOMContentLoaded', () => {

    // 1. Delete Confirmation
    const deleteForms = document.querySelectorAll('.delete-form');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function (e) {
            const confirmed = confirm("Are you sure you want to delete this trainer? This action cannot be undone.");
            if (!confirmed) {
                e.preventDefault();
            }
        });
    });

    // 2. Client-side Form Validation
    const trainerForm = document.getElementById('trainerForm');
    if (trainerForm) {
        trainerForm.addEventListener('submit', function (e) {
            // Validate Phone
            const phoneInput = document.getElementById('phone');
            if (phoneInput) {
                const phoneVal = phoneInput.value.trim();
                const cleanedPhone = phoneVal.replace(/\D/g, ''); // strip non-digits
                if (cleanedPhone.length !== 10) {
                    alert("Phone number must contain exactly 10 digits.");
                    e.preventDefault();
                    phoneInput.focus();
                    return;
                }
            }

            // Validate Previous Experience
            const expInput = document.getElementById('previous_experience');
            if (expInput) {
                const expVal = parseFloat(expInput.value);
                if (isNaN(expVal) || expVal < 0) {
                    alert("Previous experience cannot be negative.");
                    e.preventDefault();
                    expInput.focus();
                    return;
                }
            }
        });
    }

    // 3. Skills/Course Search Filter
    const skillsSearch = document.getElementById('skills_search');
    if (skillsSearch) {
        skillsSearch.addEventListener('input', function () {
            const query = this.value.toLowerCase().trim();
            const items = document.querySelectorAll('.skills-checkbox-item');
            
            items.forEach(item => {
                const label = item.querySelector('.skills-checkbox-label');
                if (label) {
                    const text = label.textContent.toLowerCase();
                    if (text.includes(query)) {
                        item.style.display = 'flex';
                    } else {
                        item.style.display = 'none';
                    }
                }
            });
        });
    }

});
