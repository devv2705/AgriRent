function pop(event) {
    event.preventDefault(); // Prevent the form from submitting

    let y = document.getElementById('equ').value;
    let z = document.getElementById('villages').selectedIndex;
    let b = document.getElementById('n_eq').value;
    let a = document.getElementById('price').value;
    let w = document.getElementById('pincode').value;
    let c = document.getElementById('image').files.length;
    let d = document.getElementById('exampleCheck1').checked;

    if ( y === '' || z === 0 || w === '' || b === '' || a === '' || c === 0 || !d) {
        alert('Please fill in all the information correctly');
    } else {
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
}
document.getElementById('form').addEventListener('submit', pop1);

window.onload = function () {
    document.getElementById('form').reset();
};