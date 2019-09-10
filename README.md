# Zybo-Z7-10-Roadtest
This repository contains the artifacts created for the face recognition project mentioned in the Element14 Roadtest (you ca read the review at https://www.element14.com/community/roadTestReviews/3060/l/digilent-zybo-z7-pcam-5c-review)

The folder tensorflow_1.14.1 contains the wheels package for Tensorflow 1.14.1, built natively on the Zybo Z7-10, targeting Python v2.7.

The folder SD-files contains the BOOT.BIN and the image.ub files (boot and kernel) generated with the Petalinux build.

The folder zybo-files contains the sode for running the demo application.
to run the demo, use 
   >python inference_tflite_facecascade.py

The Vivado project and the Petalinux project files have not been included, as I have used the Digilent own project, that can be found at:
  - Vivado project: https://github.com/Digilent/Zybo-Z7-20-base-linux
  - Petalinux project: https://github.com/Digilent/Petalinux-Zybo-Z7-20
  
Both project have been adapted for the Zybo Z7-10, following the instruction on the post https://forum.digilentinc.com/topic/17074-pcam-elf-on-petalinux-from-sd-card/

I haven't included the root file system, needed for the SD card, but I have used a Debian Buster distro (instead of the Petalinux). The version of Python used for the project is v2.7.
