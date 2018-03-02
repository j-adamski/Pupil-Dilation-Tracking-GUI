# Pupil Dilation Tracker

Pupil Dilation Tracker simplifies the process of measuring the change of pupil constriction and dilation from video files.

## Table of Contents
1. [Basic Overview](#basic-overview)
2. [Features](#features)
3. [Installation](#installation)

## Basic Overview

This program is designed for clinical application to speed up the process of extracting pupil diameter data from video files. It extracts video frames and imports them into the program. Data can be saved by *manually selecting the ROI* (region of interest) around the pupil or with the help of a *Kalman filter for automatic detection* (More details in [features](#features) section). The change in diameter vs. time at frame is plotted as data is saved. Diameter data from each frame can be saved to a cvs file.


## Features
**Manual Selection**

The user can manually select the ROI around the pupil by first clicking the center of the pupil and then clicking anywhere on the outside of the pupil. After being drawn, the ROI selection can be dragged and adjusted into the correct spot. Data is automatically saved as the ROI selection is drawn/adjusted. Pupil selection from the previous frame is carried over to the next to make data collection quick and easy. In cases where the pupil is not visable (e.g. blinking eye), the ROI widget can be removed and data is automatically deleted for that frame.


**Pupil tracking using Kalman filter**

To be implemented in the future


## Installation

Placeholder
