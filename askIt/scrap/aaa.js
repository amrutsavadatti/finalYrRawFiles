import { Button } from '@material-ui/core';
import React from 'react'
import {useHistory} from 'react-router-dom';
import browser from 'browser-detect';
import SpeedTester from 'browser-speed-test';
import "./SystemCheck.css"
import icon from "./icon.png"

const SystemCheck = () => {

    if (navigator.mediaDevices && navigator.mediaDevices.enumerateDevices) {
        // Firefox 38+ seems having support of enumerateDevicesx
        navigator.enumerateDevices = function (callback) {
            navigator.mediaDevices.enumerateDevices().then(callback);
        };
    }

    var MediaDevices = [];
    var isHTTPs = Location.protocol === 'https:';
    var canEnumerate = false;

    if (typeof MediaStreamTrack !== 'undefined' && 'getSources' in MediaStreamTrack) {
        canEnumerate = true;
    } else if (navigator.mediaDevices && !!navigator.mediaDevices.enumerateDevices) {
        canEnumerate = true;
    }

 

    var hasMicrophone = false;
    var hasSpeakers = false;
    var hasWebcam = false;

    var isMicrophoneAlreadyCaptured = false;
    var isWebcamAlreadyCaptured = false;


    function isCamAlreadyActive() {

        if (navigator.getUserMedia) {
            navigator.getUserMedia({
                video: true
            }), function (stream) {
                // returns true if any tracks have active state of true
                var result = stream.getVideoTracks().some(function (track) {
                    return track.enabled && track.readyState === 'live';
                });
            }
    
            if (result) {
                alert("Already active");
                return true;
            }
        }
    
        alert("Not active");
        return false;
     }

    function checkDeviceSupport(callback) {
        if (!canEnumerate) {
            return;
        }

        if (!navigator.enumerateDevices && window.MediaStreamTrack && window.MediaStreamTrack.getSources) {
            navigator.enumerateDevices = window.MediaStreamTrack.getSources.bind(window.MediaStreamTrack);
        }

        if (!navigator.enumerateDevices && navigator.enumerateDevices) {
            navigator.enumerateDevices = navigator.enumerateDevices.bind(navigator);
        }

        if (!navigator.enumerateDevices) {
            if (callback) {
                callback();
            }
            return;
        }



        MediaDevices = [];
        navigator.enumerateDevices(function (devices) {
            devices.forEach(function (_device) {
                var device = {};
                for (var d in _device) {
                    device[d] = _device[d];
                }

                if (device.kind === 'audio') {
                    device.kind = 'audioinput';
                    console.log("checkcam: ","lolo3");
                }

                if (device.kind === 'video') {
                    device.kind = 'videoinput';
                }

                var skip;
                MediaDevices.forEach(function (d) {
                    if (d.id === device.id && d.kind === device.kind) {
                        skip = true;
                    }
                });

                if (skip) {
                    return;
                }

                if (!device.deviceId) {
                    device.deviceId = device.id;
                }

                if (!device.id) {
                    device.id = device.deviceId;
                }

                if (!device.label) {
                    device.label = 'Please invoke getUserMedia once.';
                     console.log("checkcam: ","lolo1");
                    if (!isHTTPs) {
                        device.label = 'HTTPs is required to get label of this ' + device.kind + ' device.';
                         console.log("checkcam: ","lolo2");
                    }
                    
                } else {
                    if (device.kind === 'videoinput' && !isWebcamAlreadyCaptured) {
                        console.log("checkcam: ","lolo");
                        isWebcamAlreadyCaptured = true;
                    }

                    if (device.kind === 'audioinput' && !isMicrophoneAlreadyCaptured) {
                        isMicrophoneAlreadyCaptured = true;
                    }
                }

                if (device.kind === 'audioinput') {
                    hasMicrophone = true;
                }

                if (device.kind === 'audiooutput') {
                    hasSpeakers = true;
                }

                if (device.kind === 'videoinput') {
                    hasWebcam = true;
                }

                // there is no 'videoouput' in the spec.

                MediaDevices.push(device);
            });
                
            if (callback) {
                callback();
            }
        });
    }

function handleClick(){
  history.push("/validate");
}
    
//     var elem = document.documentElement;

// /* View in fullscreen */
// function openFullscreen() {
//   if (elem.requestFullscreen) {
//     elem.requestFullscreen();
//     history.push("/instructions")
//   } else if (elem.webkitRequestFullscreen) { /* Safari */
//     elem.webkitRequestFullscreen();
//     history.push("/instructions")
//   } else if (elem.msRequestFullscreen) { /* IE11 */
//     elem.msRequestFullscreen();
//     history.push("/instructions")
//   }
// }

//browser speed test
const tester = new SpeedTester({ });
tester.start();
console.log('Browserspeed:', tester)

//Browser detection
const result = browser();
console.log('Browserdetect:',result);

//Camera Detection
var hell='lol';
if (isWebcamAlreadyCaptured===true){
    hell="Yes";
}else{
    hell="No";
}
console.log("Webcam", isWebcamAlreadyCaptured);

//Network speed
const net = `${navigator.connection.downlink} Mbps`
console.log('Networkspeed', net);
<div id="debugDiv"></div>

const history=useHistory();



  return (
    <body>
  <div class="main">
    <p class="sign" align="center">System Compatibility Check</p>
        <table align="center">
            <tbody><tr>
                <td class="text-center">
                    <div>
                        <img src={icon} id="classIcon" />
                    </div>
                </td>
                <td>
                    <ul>
                        <li class="test">
                            <span ><b>OS</b>  {"- " + JSON.stringify(result["os"],null,2 ).slice(1,-1)} </span>
                        </li>
                        <li class="test">
                            <span><b>Browser</b> {"- " + JSON.stringify(result["name"],null,2 ).slice(1,-1) +" "+ JSON.stringify(result["version"],null,2 ).slice(1,3) } </span>
                        </li>
                        <li class="test">
                            <span><b>Internet connection</b> {"- " + JSON.stringify(net,null,2 ).slice(1,-1) } </span>
                        </li>
                         <li class="test">
                            <span><b>Has Webcam</b> {"- " + JSON.stringify(isCamAlreadyActive,null,2 )} </span>
                        </li>
                        
                    </ul>
                </td>
            </tr>
        </tbody>
    </table>


            
                
    </div>
     
</body>

  )
}


export default SystemCheck;