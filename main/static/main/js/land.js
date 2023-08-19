
// Script that handles the sidebar toggling

$(document).ready(function() {
    // Your JS code here
    $('#sidebarToggler').on('click', function() {
        $('#sidebar').toggleClass('sidebar-retracted');
    });
});
