/*
    User Interaction Logic v1
    for feeding robot arm
    By Ye Liu
    Aug 23 2018
*/

'use strict';

var id = '',
    input = '',
    flag = false,
    count = 0,
    food = ['Bread', 'Water'],
    probableFood = ['bread?', 'water?']

function onInit() {
    $.ajax({
        type: 'GET',
        url: 'app_init',
        success: function (res) {
            if (res) {
                console.log('App init successfully')
            }
        }
    })
}

function onStartClick() {
    // Display input box
    document.getElementById('input-box').style.display = ''
    document.getElementById('start-button').style.display = 'none'
    document.getElementById('output').style.display = ''
    document.getElementById('logo').style.display = 'none'
    document.getElementById('input-box').focus()

    // Request for speech recognition
    $.ajax({
        type: 'GET',
        url: 'start_recording',
        fail: function (err) {
            document.getElementById('output').innerHTML = 'Error'
            console.log(err)
        }
    })

    // Set interval
    id = setInterval('checkInput()', 800)
}

function checkInput() {
    var newInput = document.getElementById('input-box').value
    if (input === 'q') {
        document.getElementById('input-box').value = ''
    }
    else if (newInput) {
        if (newInput === input) {
            if (flag) {
                // Construct request data
                var data = {
                    'input': input
                }

                // Request for keyword
                $.ajax({
                    type: 'GET',
                    url: 'speech_recognition',
                    data: data,
                    success: function (res) {
                        if (res['keyword'] === 'hello') {
                            document.getElementById('output').innerHTML = 'Hello~'
                            document.getElementById('input-box').value = ''
                            count = 0
                        } else if (food.indexOf(res['keyword']) != -1) {
                            document.getElementById('output').innerHTML = res['keyword'] + '? Sure'
                            document.getElementById('input-box').value = ''
                            count = 0
                            setTimeout('switch2Video("' + res['keyword'] + '")', 1000)
                        } else if (probableFood.indexOf(res['keyword']) != -1) {
                            document.getElementById('output').innerHTML = 'Do you mean ' + res['keyword'] + '? Sure'
                            document.getElementById('input-box').value = ''
                            count = 0
                            setTimeout('switch2Video("' + res['keyword'] + '")', 1000)
                        } else if (res['keyword'] === 'thank') {
                            document.getElementById('output').innerHTML = 'You are welcome~'
                            document.getElementById('input-box').value = ''
                            count = 0
                        } else if (res['keyword']) {
                            document.getElementById('output').innerHTML = 'Sorry but what is ' + res['keyword'] + '?'
                            document.getElementById('input-box').value = ''
                            count = 0
                        } else {
                            document.getElementById('output').innerHTML = "Sorry, I don't understand"
                            count++
                            if (count >= 3) {
                                document.getElementById('input-box').value = ''
                                count = 0
                            }
                        }
                        document.getElementById('flipper').style.transform = ''
                        input = ''
                    },
                    fail: function (err) {
                        document.getElementById('output').innerHTML = 'Error'
                        console.log(err)
                    }
                })
                flag = false
            } else {
                flag = true
            }
        } else {
            input = newInput
        }
    }
}

function switch2Video(object) {
    document.getElementById('input-box').value = 'Searching for ' + object
    document.getElementById('flipper').style.transform = 'rotateY(180deg)'
    clearInterval(id)
    id = setInterval('checkStatus()', 100)
}

function checkStatus() {
    $.ajax({
        type: 'GET',
        url: '{{ url_for("status") }}',
        success: function (res) {
            if (!res) {
                document.getElementById('input-box').value = ''
                clearInterval(id)
                // Set interval
                id = setInterval('checkInput()', 800)
            }
        }
    })
}