

// TITLE: Duration buttons

// get buttons
const durationButtons = document.querySelectorAll('.btn-duration');

// loop through each button
durationButtons.forEach(button => {
    button.addEventListener('click', function() {
        const duration = this.getAttribute('data-duration');

        // Set value to the hidden input
        document.getElementById('duration').value = duration;
    })
})