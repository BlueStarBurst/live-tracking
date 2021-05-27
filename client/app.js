import React, { useEffect, useState } from 'react'
import { render } from 'react-dom'

import * as tf from "@tensorflow/tfjs";
import * as posenet from '@tensorflow-models/posenet';

async function estimatePoseOnImage(imageElement) {
    // load the posenet model from a checkpoint
    const net = await posenet.load();

    const pose = await net.estimateSinglePose(imageElement, {
        flipHorizontal: false
    });
    console.log(pose);
    return pose;
}

//const imageElement = document.getElementById('cat');

//const pose = estimatePoseOnImage(imageElement);

//console.log(pose);

var stream = ''

async function Media() {
    navigator.mediaDevices.getUserMedia({ audio: true, video: true })
        .then(function (str) {
            stream = str;
        })
        .catch(function (err) {
            console.log(err)
        });
}

function App(props) {

    const [state, setstate] = useState(<Loading />)

    useEffect(() => {
        Media().then(
            setstate(<h1> Hello </h1>)
        )
    }, [])

    return (state);
}

function Loading(props) {
    return <div style={{ backgroundColor: 'black', width: "100vw", height: "100vh" }}></div>
}

function Model(props) {
    
}




render(<App stream={stream} />, document.getElementById("root"));