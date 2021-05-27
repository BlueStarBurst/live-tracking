import React from 'react'
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

const imageElement = document.getElementById('cat');

const pose = estimatePoseOnImage(imageElement);

console.log(pose);

render(
    <>
        <h1> Hello </h1>
    </>, document.getElementById("root"));