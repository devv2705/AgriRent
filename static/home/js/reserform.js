
// Wait for the document to be fully loaded
document.addEventListener("DOMContentLoaded", function () {
    // Get the form element
    var form = document.getElementById("form");

    // Clear the form when it is submitted
    form.addEventListener("submit", function () {
        form.reset();
    });
});
