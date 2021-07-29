# bluesky_practice

## create a new virtual environment "bleusky-tutorial"

## install mongodb, bluesky, ophyd, bluesky_queueserver, ariadne.


## open mongodb, create user and password in mongodb.

## activate the virtual environment.
    conda activate bluesky-tutorial

## open bluesky with initial settings
    ipython --matplotlib=qt5

## open bluesky with the existing profile "profile_gui_dev" from Willam.
    cd .ipython
    ls
    cd profile_gui_dev
    cd startup
    sudo nano 00-start.py
### the content in 00-start.py are used to initial the bluesky RE environment. we can add epics motor
### "IOCsim:m1" into ophyd, and then we can see it , move it or use it to scan in bluesky.

