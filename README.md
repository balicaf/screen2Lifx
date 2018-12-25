# screen2Lifx

Originally reproduce your screen mean color onto your LIFX bulb.
Demo: [THIS!](https://youtu.be/WHCtUvEJXq0)
*original code from lifxscreen is https://github.com/frakman1/lifxscreen2*)

With this version, LIFX is synced with iTune's BPMs (obtained thanks to Mixxx app)
Use the branch firstTodo to use it with two lifx bulbs!!!!
Tested on a MacOs 10.13.4. and 10.11.6 Python version 2.7.14

##Prerequisites:

* Pillow- Screen Grabber https://pypi.python.org/simple/pillow/ 
download the wheel (.whl): 5.0 for 10.11.6 and 5.1 for 10.13.4.

* Colour - Colour Convertions and Manipulations  (https://pypi.python.org/pypi/colour/)

* Lazylights - The actual LIFX driver.  https://github.com/mpapi/lazylights/tree/2.0

on terminal:<br />
pip install git+https://github.com/mpapi/lazylights@2.0<br />
pip install colour<br />
pip install (drag&drop downloaded wheel into your terminal to obtain the path)<br />




