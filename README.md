# 360° Image and Video Navigator
This repository contains a simple pedestrian tracker implemented as an assignment for the Computer Vision course attended at [UniPa](https://www.unipa.it/dipartimenti/ingegneria/cds/ingegneriainformatica2035/?template=responsive&pagina=insegnamento&idInsegnamento=171775&idDocente=155776&idCattedra=167762).

## Overview

This project is a tool designed to navigate images captured by 360° cameras (equirectangular images). The tool provides functionalities to rectify and display these images, allowing the user to change the field of view, latitude, longitude, and apply zoom to focus on near or far objects.

## Features

- **Image and Video Support**: Load and process both images and videos captured by 360° cameras.
- **Interactive Navigation**: Use keyboard controls to navigate the view:
  - `W`/`S`: Move up/down
  - `A`/`D`: Move left/right
  - `Q`/`E`: Increase/decrease field of view (FOV)
  - `Z`/`X`: Zoom in/out
  - `P`: Take a screenshot
  - `Space`: Pause/resume video
- **User Interface**: A simple Tkinter-based GUI to select files and set initial parameters (FOV, latitude, longitude).

## Showcase example

This example demonstrates how the navigator allows you to focus on specific areas within a 360° image.

### Original 360° Image

### Navigated View

This view is achieved using the following settings:

- FOV: 90°
- Latitude: 90°
- Longitude: 65°
- Zoom: 1x


## Usage

1. Clone the repository:
   ```sh
   git clone https://github.com/dqvid3/360-navigator.git
   cd 360-navigator```
2. Load an Image or Video:
  - Run the application using python main.py.
  - Use the GUI to select an image or video file either by entering the path or using the file dialog.
  - Set the initial FOV, latitude, and longitude.
3. Navigate the Image or Video:
  - Use the provided keyboard controls to navigate and zoom the image or video.
  - Press `P` to take a screenshot at any point.
  - For videos, use the `Space` bar to pause and resume playback.

## File Structure

- `elaborazioni.py`: Contains the core functions for processing frames, reading images and videos, adding text to frames, taking screenshots, and handling navigation.
- `interfaccia.py`: Implements the Tkinter-based GUI for selecting files and input parameters.
- `main.py`: The entry point of the application that launches the GUI.
- `trasformazioni.py`: Provides utility functions for coordinate
transformations and image projections.
