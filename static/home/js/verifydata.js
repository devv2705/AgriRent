function pop(event) {
    event.preventDefault(); // Prevent the form from submitting

    let x = document.getElementById('num').value;
    let y = document.getElementById('equ').value;
    let z = document.getElementById('villages').selectedIndex;
    let b = document.getElementById('n_eq').value;
    let a = document.getElementById('price').value;
    let w = document.getElementById('pincode').value;
    let c = document.getElementById('image').files.length;
    let d = document.getElementById('exampleCheck1').checked;

    if (x.length !== 10 || y === '' || z === 0 || w === '' || b === '' || a === '' || c === 0 || !d) {
        if (x.length !== 10) {
            alert('Mobile number must be exactly 10 digits');
        } else {
            alert('Please fill in all the information correctly');
        }
    } else {
        alert('Equipment saved successfully');
        document.getElementById('form').submit();
    }
}
document.getElementById('form').addEventListener('submit', pop);



function pop1(event) {
    event.preventDefault();
    let x = document.getElementById("dob").value
    let y = document.getElementById("pincode").value
    let z = document.getElementById("address").value
    let w = document.getElementById("image").value
    let b = document.getElementById("villages").selectedIndex
    let a = document.getElementById("exampleCheck").checked
    if (x === '' || y === '' || z === '' || w === '' || b === 0 || !a) {
        alert('Please fill in all the information');
    }
    else {
        alert('Your details have been successfully saved');
    }
}
document.getElementById('form').addEventListener('submit', pop1);

window.onload = function () {
    document.getElementById('form').reset();
};