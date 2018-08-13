"use strict";

function onStartClick() {
    // Display input
    document.getElementById('input-box').style.display = ""
    document.getElementById('start-button').style.display = "none"
}

function checkInput() {
    console.log(document.getElementById('input-box').value);
}