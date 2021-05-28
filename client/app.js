import React, { useEffect, useState } from 'react'
import { render } from 'react-dom'

import * as tf from "@tensorflow/tfjs";
import * as posenet from '@tensorflow-models/posenet';

var canvas = '';
var ctx = '';
var height = 0;
var width = 0;

var net = null;

async function loadNet() {
    net = await posenet.load();
}

async function estimatePoseOnImage(imageElement) {
    // load the posenet model from a checkpoint
    const pose = await net.estimateSinglePose(imageElement, {
        flipHorizontal: false
    });
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    var points = {};

    if (pose.score < 0.5) {
        return pose;
    }

    //console.log("split")
    pose.keypoints.forEach(element => {
        //console.log(element);
        if (element.score > 0.5) {
            ctx.fillStyle = "blue";
            ctx.fillRect(element.position.x / width * canvas.width, element.position.y / height * canvas.height, 10, 10);

        }

    });


    return pose;
}

//const imageElement = document.getElementById('cat');

//const pose = estimatePoseOnImage(imageElement);

//console.log(pose);

var stream = null

function App(props) {

    const [state, setstate] = useState(<Loading />)

    useEffect(function () {
        navigator.mediaDevices.getUserMedia({ audio: true, video: true })
            .then(function (str) {
                stream = str;
                setstate(<Model />);
            })
            .catch(function (err) {
                console.log(err)
            });
    }, [])

    return (state);
}

function Loading(props) {
    return <div style={{ backgroundColor: 'black', width: "100vw", height: "100vh" }}></div>
}

var imageCapture = null;

function Model(props) {

    const style = {
        width: "min-content",
        height: "80vh",
        margin: "auto",
        position: "relative",
        backgroundColor: "blue"
    }

    const video = {
        height: "100%"
    }
    const div = {
        height: "100%",
        width: "100%",
        position: "absolute",
        top: "0",
        left: "0",
        backgroundColor: "transparent",
        objectFit: "contain"
    }

    useEffect(() => {
        document.getElementById("video").srcObject = stream;
        imageCapture = new ImageCapture(stream.getTracks()[1]);

        canvas = document.getElementById('canvas');
        ctx = canvas.getContext('2d');
        height = stream.getVideoTracks()[0].getSettings().height
        width = stream.getVideoTracks()[0].getSettings().width

        //var fps = (1 / stream.getVideoTracks()[0].getSettings().frameRate) * 2000
        var fps = 33.333 * 3;
        setInterval(() => {
            if (imageCapture != null) {
                imageCapture.grabFrame()
                    .then(imageBitmap => {
                        estimatePoseOnImage(imageBitmap);
                    })
                    .catch(error => console.log(error));
            }
        }, 100);

    }, [])

    return (
        <div style={style}>
            <video id="video" src={stream} autoPlay muted style={video} ></video>
            <canvas id="canvas" style={div}></canvas>
        </div>);
}




loadNet();

render(<App stream={stream} />, document.getElementById("root"));