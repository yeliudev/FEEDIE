<p align="center">
  <img width="450" src="Supporting%20files/logo-color.png" />
</p>

## Introduction

FEEDIE (pronounced `/ˈfi:di/`, combination of **feed** and **foodie**) is a feeding robot specially designed for people who couldn't eat or drink independently. According to our [survey](https://github.com/c1aris/Feeding-Robot-Demo/blob/master/Supporting%20files/DataAnalysis.pptx?raw=true), over 15% of the families have at least one person who couldn't take care of himself and over 20% of them have a great demand for a robot to help them. One can interact and control the robot by natural language instructions. After receiving message from a user, FEEDIE can extract keywords from the instructions, find what the user want on the table, and feed it into his mouth.

Our core techniques consist of **Speech Recognition**, **Image Recognition**, **Grabbing Algorithm** and **Human Computer Interaction**.

You can [click here](https://youtu.be/WOYQ2A6ZiRU) to watch a video of demo or download our [product introduction](https://github.com/c1aris/Feeding-Robot-Demo/blob/master/Supporting%20files/Product%20Introducton%20v3.pptx?raw=true).

<p align="center">
  <img width="300" src="Supporting%20files/preview.gif" hspace="50px" />
  <img width="247" src="Supporting%20files/UI.gif" hspace="50px" />
</p>

## Hardware Configuration

* SainSmart DIY 6-Axis Servos Control Palletizing Robot Arm
* Arduino/Genuino 101 Board
* Logitech c270 web camera
* AC adapter

## Code Catalog

* Arduino - Serial communication logic & object grabbing algorithm
* Classifier - [OpenCV](https://opencv.org/) cascade classifiers
* Flask - User Interaction module
* Modules *(abandoned)* - Speech & Object recognition models
* Training - Cascade classifier training tool

## License

[MIT License](LICENSE)

Copyright (c) 2019 c1aris
