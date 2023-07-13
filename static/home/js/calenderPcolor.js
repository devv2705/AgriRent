$(document).ready(function () {
    $('#dob').datepicker({
        showOn: "button",
        buttonImage: "calendar.png",
        buttonImageOnly: true,
        buttonText: "Select date",
        beforeShow: function (input, inst) {
            setTimeout(function () {
                inst.dpDiv.css({
                    'left': 'auto',
                    'right': '0'
                });
            }, 0);
        }
    });
});
var dobInput = document.getElementById("dob");
dobInput.addEventListener("change", function () {
    if (dobInput.value) {
        dobInput.style.color = "black";
    } else {
        dobInput.style.color = "#757575";
    }
});