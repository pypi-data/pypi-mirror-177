# azcam_arc

*azcam_arc* is an *azcam* extension for Astronomical Research Cameras, Inc. gen1, gen2, and gen3 controllers. See https://www.astro-cam.com/.

## Installation

`pip install azcam-arc`

Or download from github: https://github.com/mplesser/azcam-arc.git.

## Example Code

The code below is for example only.

### Controller Setup
```python
import azcam.server
from azcam_arc.controller_arc import ControllerArc
controller = ControllerArc()
controller.timing_board = "arc22"
controller.clock_boards = ["arc32"]
controller.video_boards = ["arc45", "arc45"]
controller.utility_board = None
controller.set_boards()
controller.pci_file = os.path.join(azcam.db.systemfolder, "dspcode", "dsppci3", "pci3.lod")
controller.video_gain = 2
controller.video_speed = 1
```

### Exposure Setup
```python
import azcam.server
from azcam_arc.exposure_arc import ExposureArc
exposure = ExposureArc()
exposure.filetype = azcam.db.filetypes["MEF"]
exposure.image.filetype = azcam.db.filetypes["MEF"]
exposure.set_remote_imageserver("localhost", 6543)
exposure.image.remote_imageserver_filename = "/data/image.fits"
exposure.image.server_type = "azcam"
exposure.set_remote_imageserver()
```

## Camera Servers
*Camera servers* are separate executable programs which manage direct interaction with 
controller hardware on some systems. Communication with a camera server takes place over a socket via 
communication protocols defined between *azcam* and a specific camera server program. These 
camera servers are necessary when specialized drivers for the camera hardware are required.  They are 
usually written in C/C++. 

## DSP Code
The DSP code which runs in the ARC controllers is assembled and linked with
Motorola software tools. These tools are typically installed in the folder `/azcam/motoroladsptools/` on a
Windows machine as required by the batch files which assemble and link the code.

While the AzCam application code for the ARC timing board is typically downloaded during
camera initialization, the boot code must be compatible for this to work properly. Therefore
AzCam-compatible DSP boot code may need to be burned into the timing board EEPROMs before use, depending on configuration. 

The gen3 PCI fiber optic interface boards and the gen3 utility boards use the original ARC code and do not need to be changed. The gen1 and gen2 situations are more complex.

For ARC system, the *xxx.lod* files are downlowded to the boards.
