$(document).ready(function () {
    var pincodeInput = $('#pincode');
    var cityInput = $('#city');
    var stateInput = $('#state');
    var countryInput = $('#country');
    var villagesSelect = $('#villages');
    var addressFields = $('#addressFields');
    var villagesContainer = $('#villagesContainer');

    pincodeInput.on('input', function () {
        var pincode = pincodeInput.val();

        if (/^\d{6}$/.test(pincode)) {
            pincodeInput.removeClass('error');
            validatePincode(pincode);
        } else {
            pincodeInput.addClass('error');
            resetForm();
            document.getElementById("perror").style.display = "block";
        }

        if (pincode.length > 6) {
            pincodeInput.val(pincode.substring(0, 6));
        }
    });

    function validatePincode(pincode) {
        $.ajax({
            url: `https://api.postalpincode.in/pincode/${pincode}`,
            success: function (data) {
                if (data[0].Status === 'Success') {
                    var postOffice = data[0].PostOffice;
                    var city = postOffice[0].Block;
                    var state = postOffice[0].State;
                    var country = postOffice[0].Country;
                    var villages = postOffice.map(function (office) {
                        return office.Name;
                    });

                    cityInput.val(city);
                    stateInput.val(state);
                    countryInput.val(country);

                    addressFields.css('display', 'block');
                    villagesContainer.css('display', 'block');

                    villagesSelect.empty().append($('<option>').text('Select a village'));
                    villages.forEach(function (village) {
                        villagesSelect.append($('<option>').text(village));
                    });
                    document.getElementById("perror").style.display = "none";
                    villagesSelect.prop('disabled', false);
                } else {
                    resetForm();
                    document.getElementById("perror").style.display = "block";
                }
            },
            error: function () {
                resetForm();
                document.getElementById("perror").style.display = "block";
            }
        });
    }

    function resetForm() {
        cityInput.val('');
        stateInput.val('');
        countryInput.val('');
        villagesSelect.empty().append($('<option>').text('Select a village')).prop('disabled', true);
        addressFields.css('display', 'none');
        villagesContainer.css('display', 'none');
    }
});
