

// TITLE: Duration buttons

// get buttons
const durationButtons = document.querySelectorAll('.btn-duration');

// loop through each button
durationButtons.forEach(button => {
    button.addEventListener('click', function() {
        const duration = this.getAttribute('data-duration');

        // Remove 'selected' class from all buttons
        durationButtons.forEach(btn => {
            btn.classList.remove('selected');
        });

        // Add 'selected' class to the clicked button
        this.classList.add('selected');

        // Set value to the hidden input
        document.getElementById('duration').value = duration;
    })
})