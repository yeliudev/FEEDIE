var servoA_characteristic = null;
var servoB_characteristic = null;
var servoC_characteristic = null;
var servoD_characteristic = null;
var servoE_characteristic = null;
var servoF_characteristic = null;
var servoG_characteristic = null;
var reset_characteristic = null;

var servoA_default = 60;
var servoB_default = 100;
var servoC_default = 100;
var servoD_default = 100;
var servoE_default = 100;
var servoF_default = 100;
var servoG_default = 10;

function onDiscoverService() {//start searching for BLE devices
    var discoverservice = document.getElementById("discover");//hide the button
    discoverservice.hidden = true;

    // Validate services UUID entered by user first.
    let optionalServices = ['47452000-0f63-5b27-9122-728099603712'];//Robotic Arm (note UUID lower case)
    console.log('Requesting any Bluetooth Device...');
    navigator.bluetooth.requestDevice({
        acceptAllDevices: true,
        optionalServices: optionalServices//BSN IoT
    })
        .then(device => {
            console.log('Connecting to GATT Server...');
            return device.gatt.connect();
        })
        .then(server => {
            // Note that we could also get all services that match a specific UUID by
            // passing it to getPrimaryServices().
            console.log('Getting Services...');
            return server.getPrimaryServices();
        })
        .then(services => {
            console.log('Getting Characteristics...');
            let queue = Promise.resolve();
            services.forEach(service => {
                queue = queue.then(_ => service.getCharacteristics().then(characteristics => {
                    if (service.uuid == ['47452000-0f63-5b27-9122-728099603712']) {
                        console.log("> Service: Robotic Arm");
                    }
                    else if (service.uuid == ['0000180a-0000-1000-8000-00805f9b34fb'])
                    {
                        console.log("> Service: Device Info");
                    }
                    else console.log('> Service: ' + service.uuid);
                    characteristics.forEach(characteristic => {
                        if (characteristic.uuid == ['47452001-0f63-5b27-9122-728099603712']) {
                            servoA_characteristic = characteristic;
                            var servoA_control = document.getElementById("servoA");
                            servoA_control.hidden = false;
                        }
                        else if (characteristic.uuid == ['47452002-0f63-5b27-9122-728099603712']) {
                            //console.log("servo B");
                            servoB_characteristic = characteristic;
                            var servoB_control = document.getElementById("servoB");
                            servoB_control.hidden = false;
                        }
                        else if (characteristic.uuid == ['47452003-0f63-5b27-9122-728099603712']) {
                            //console.log("servo C");
                            servoC_characteristic = characteristic;
                            var servoC_control = document.getElementById("servoC");
                            servoC_control.hidden = false;
                        }
                        else if (characteristic.uuid == ['47452004-0f63-5b27-9122-728099603712']) {
                            //console.log("servo D");
                            servoD_characteristic = characteristic;
                            var servoD_control = document.getElementById("servoD");
                            servoD_control.hidden = false;
                        }
                        else if (characteristic.uuid == ['47452005-0f63-5b27-9122-728099603712']) {
                            //console.log("servo E");
                            servoE_characteristic = characteristic;
                            var servoE_control = document.getElementById("servoE");
                            servoE_control.hidden = false;
                        }
                        else if (characteristic.uuid == ['47452006-0f63-5b27-9122-728099603712']) {
                            //console.log("servo F");
                            servoF_characteristic = characteristic;
                            var servoF_control = document.getElementById("servoF");
                            servoF_control.hidden = false;
                        }
                        else if (characteristic.uuid == ['47452008-0f63-5b27-9122-728099603712']) {
                            //console.log("servo G");
                            servoG_characteristic = characteristic;
                            var servoG_control = document.getElementById("servoG");
                            servoG_control.hidden = false;
                        }
                        else if (characteristic.uuid == ['47452007-0f63-5b27-9122-728099603712']) {
                            //console.log("Reset");
                            reset_characteristic = characteristic;
                            var reset_control = document.getElementById("reset");
                            reset_control.hidden = false;
                        }
                        else
                            console.log('>> Characteristic: ' + characteristic.uuid + ' ' +
                                getSupportedProperties(characteristic));//other characteristics
                    });
                }));
            });
            return queue;
        })
        .catch(error => {
            console.log('Argh! ' + error);
        });
}

var servoA_state = 0;
function onButtonClick() {
    var newvalue = Uint8Array.of(0);
    if (servoA_state == 0)
        newvalue = Uint8Array.of(1);
    servoA_state = !servoA_state;
    if (servoA_characteristic != null)
        servoA_characteristic.writeValue(newvalue);
}

function onSliderA(value) {
    if (servoA_characteristic == null) return;
    console.log("servoA:" + value);
    newvalue = Uint8Array.of(value);
    servoA_characteristic.writeValue(newvalue);
}

function onSliderB(value) {
    if (servoB_characteristic == null) return;
    console.log("servoB:" + value);
    newvalue = Uint8Array.of(value);
    servoB_characteristic.writeValue(newvalue);
}

function onSliderC(value) {
    if (servoC_characteristic == null) return;
    console.log("servoC:" + value);
    newvalue = Uint8Array.of(value);
    servoC_characteristic.writeValue(newvalue);
}

function onSliderD(value) {
    if (servoD_characteristic == null) return;
    console.log("servoD:" + value);
    newvalue = Uint8Array.of(value);
    servoD_characteristic.writeValue(newvalue);
}

function onSliderE(value) {
    if (servoE_characteristic == null) return;
    console.log("servoE:" + value);
    newvalue = Uint8Array.of(value);
    servoE_characteristic.writeValue(newvalue);
}

function onSliderF(value) {
    if (servoF_characteristic == null) return;
    console.log("servoF:" + value);
    newvalue = Uint8Array.of(value);
    servoF_characteristic.writeValue(newvalue);
}

function onSliderG(value) {
    if (servoG_characteristic == null) return;
    console.log("servoG:" + value);
    newvalue = Uint8Array.of(value);
    servoG_characteristic.writeValue(newvalue);
}

function onReset() {
    if (reset_characteristic == null) return;
    console.log("reset");
    newvalue = Uint8Array.of(0);
    reset_characteristic.writeValue(newvalue);
}

function getSupportedProperties(characteristic) {//find the details of a characteristic
    let supportedProperties = [];
    for (const p in characteristic.properties) {
        if (characteristic.properties[p] === true) {
            supportedProperties.push(p.toUpperCase());
        }
    }
    return '[' + supportedProperties.join(', ') + ']';
}
