## AMRL System Monitor

### Introduction

System monitoring tools for ROS.
This project provides system monitoring tools for ROS. Every node in ROS has a process ID and some more details. With this information, we can fetch CPU/MEM usage and TCP/UDP connections for each node.

**Note** this repository is not a ROS package right now, maybe later it will be.

### Installation

```bash
$ wget -q -O - https://mrl-amrl.ir/rosmonitor.sh | bash
```

or 

```bash
$ wget -q -O - https://raw.githubusercontent.com/mrl-amrl/system-monitor/master/install.sh | bash
```

### Usage

To monitor ROS nodes use:

```
$ python rosmonitor.py
$ # or if you installed rosmonitor in your system just run rosmonitor.
```

```
name                         pid  cpu    mem    UDP connections
-------------------------  -----  -----  -----  --------------------------------------
/mercury_joy                8558  2.2%   0.8%
/manipulator                8568  0.9%   1.1%   aiden-desktop:3037 aiden-desktop:3030
/rosmaster                  8539  0.6%   0.6%
/mercury_state_controller   8573  0.6%   0.6%
/mercury_trajectory         8565  0.5%   0.8%   aiden-desktop:3020
/ros_joy                    8557  0.4%   0.1%   *:59529
/mercury_dynparam           8572  0.1%   0.8%
/mercury_feedback           8569  0.1%   0.6%   *:3031 *:3033
/mercury_netping            8574  0.1%   0.6%
/mercury_ocu_driver         8571  0.1%   1.0%   aiden-desktop:10131 aiden-desktop:9000
/mercury_power_management   8570  0.1%   0.6%   aiden-desktop:3024
/xbox_rumble_controller     8564  0.1%   0.6%
/rosout                     8550  0.0%   0.1%   *:58463
```
