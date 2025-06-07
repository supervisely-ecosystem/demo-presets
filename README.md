<div align="center" markdown>
<img src="https://github.com/supervisely-ecosystem/demo-presets/releases/download/sly-release-v0.0.9/poster.png"/>  

# Demo Presets

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#Avaiable presets">Avaiable presets</a> •
  <a href="#How-To-Run">How To Run</a> •
  <a href="#Stopping-tasks">Stopping tasks</a>
</p>

[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervisely.com/slack)

</div>

# Overview
This application is needed to run a bunch of Supervisely apps related to the specific demo preset. The presets are the lists of module IDs, representing the applications in Supervisely Ecosystem.

# Avaiable presets
All the presets are stored in the `presets.json` files with the following structure:
```json
{
  "images": [95, 315, 327],
  "videos": [315, 342, 283, 312],
  "volumes": [50, 315],
  "pointclouds": []
}
```
Where the key is a modality and the value is a list of module IDs. The module IDs are the IDs of the applications in Supervisely Ecosystem.  
As an exanple, if the **videos** preset will be used then the applications with IDs 315, 342, 283, and 312 will be run.

# How-To-Run

Launch the app from the Ecosystem and select one or multiple presets you want to run. Click the **Run** button to start the tasks.


# Stopping tasks
Once you don't need the tasks anymore, you can stop all of them by launching the app again and enabling `Stop all demo sessions` option. In this case, the app will ignore all other options (will not start any tasks) and will stop all the tasks that were started by this app earlier.