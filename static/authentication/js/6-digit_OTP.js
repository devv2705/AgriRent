document.getElementById('otp').addEventListener('input', function () {
    let value = this.value;
    if (value.length > 6) {
        value = value.slice(0, 6);
    }
    this.value = value;
});