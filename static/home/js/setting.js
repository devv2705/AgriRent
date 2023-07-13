document.getElementById("reset").style.display = "none"
document.getElementById("delete").style.display = "none"
function rs() {
    let x = document.getElementById("reset")
    let y = document.getElementById("delete")
    if (x.style.display === "none") {
        x.style.display = "block"
        y.style.display = 'none';

    }
    else {
        x.style.display = "none"
    }
}
function del() {

    let x = document.getElementById("delete")
    let y = document.getElementById("reset")
    if (x.style.display === "none") {
        x.style.display = "block"
        y.style.display = "none"

    }
    else {
        x.style.display = "none"
    }

}

