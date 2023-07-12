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

var x = document.getElementById("pincode").value
$(document).ready(function () {
    var pincodeInput = $('#pincode');
    var villagesSelect = $('#villages');
    var villageLabel = $('label[for="villages"]');

    pincodeInput.on('input', function () {
        var pincode = pincodeInput.val();

        if (pincode.length === 6 && /^\d+$/.test(pincode)) {
            validatePincode(pincode);
        } else {
            resetForm();
        }
    });

    villagesSelect.on('change', function () {
        var selectedOption = villagesSelect.find('option:selected').text();
        villagesSelect.val(selectedOption);
    });

    function validatePincode(pincode) {
        $.ajax({
            url: `https://api.postalpincode.in/pincode/${pincode}`,
            success: function (data) {
                if (data[0].Status === 'Success') {
                    var postOffice = data[0].PostOffice;
                    var villages = postOffice.map(function (office) {
                        var village = office.Name;
                        var city = office.Block;
                        var state = office.State;
                        var country = office.Country;
                        var optionText = village + ', ' + city + ', ' + state + ', ' + country;
                        return $('<option>').text(optionText);
                    });

                    pincodeInput.removeClass('error');
                    villageLabel.show();
                    villagesSelect.empty().append($('<option>').text('Select a village')).append(villages).prop('disabled', false);
                    villagesSelect.show();
                    pincodeInput.css('border-bottom-colour', 'blue');
                } else {
                    resetForm();
                    pincodeInput.addClass('error');
                }
            },
            error: function () {
                resetForm();
                pincodeInput.addClass('error');
            }
        });
    }

    function resetForm() {
        villageLabel.hide();
        villagesSelect.empty().prop('disabled', true);
        villagesSelect.hide();
        pincodeInput.css('border-color', 'red');
    }
});