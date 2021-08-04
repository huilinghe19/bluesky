# bluesky_practice

## create a new virtual environment "bleusky-tutorial", install mongodb, bluesky, ophyd, bluesky_queueserver, ariadne.

## open mongodb, create user and password. open mongodb.

##  pip upgrade ??  upgrade may destroy something like ipython and qt things. use conda install in the end. step by step in a clean environment is important.

    /hzb/huiling/anaconda3/envs/bluesky-tutorial/bin/python3.7 -m pip install --upgrade pip

## activate the virtual environment with conda.

    conda activate bluesky-tutorial

    

## open bluesky with initial settings
    ipython --matplotlib=qt5

## open bluesky with the existing profile "profile_gui_dev" from Willam.
    ipython --profile=gui_dev

## connect with EPICS motor. change the startup file. 
    cd .ipython
    ls
    cd profile_gui_dev
    cd startup
    sudo nano 00-start.py
The content in 00-start.py is used to initial the bluesky RE environment. We can add epics motor "IOCsim:m1" into ophyd, and then we can see it , move it or use it to scan in bluesky. After restart bluesky, we can get the m1 als bluesky motor using "wa", and the position of m1 is 1.00 using "m1.position". Actually m1 stands for the epics PV "IOCsim:m1". 
    

