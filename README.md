# Bluesky_practice

## create a new virtual environment "bleusky-tutorial", install mongodb, bluesky, ophyd, bluesky_queueserver, ariadne.

Install MongoDB on debian 10 system:

https://docs.mongodb.com/manual/tutorial/install-mongodb-on-debian/

(The installation on debian is different with other systems!! The mongodb package provided by Debian is not maintained by MongoDB Inc. and conflicts with the official mongodb-org package. If you have already installed the mongodb package on your Debian system, you must first uninstall the mongodb package before proceeding with these instructions. )

bluesky: 

https://blueskyproject.io/bluesky/

bluesky queueserver:

https://blueskyproject.io/bluesky-queueserver/

bluesky widgets:  

https://github.com/NSLS-II/bluesky-widgets-demo

ariadne: 

https://github.com/NSLS-II-BMM/ariadne

xraylib:

https://anaconda.org/conda-forge/xraylib

If the error occurs: 
    
    Error: qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.

 use the following command:

    sudo ln -s /usr/lib/x86_64-linux-gnu/libxcb-util.so.0  /usr/lib/x86_64-linux-gnu/libxcb-util.so.1

## Advices from Willam:
"""
1. Install a mongoDB on your machine

2. Create the configuration files so that the databroker can access it use your credentials and not the ones shown in this manual

3. Create an ipython environment that connects a run engine to the mongoDB you have just set up (Use this repo)

4. Pull a version of the queue server, run the tutorial

5. Pull a version of the existing GUI, try and run it ariadne --catalog your_catalog_name -zmq your_hostname:zmq_port

I think the first objective, once this is all running is first to just run a plan with the simulated detectors and motors, and check it works. 

RE(scan([det],motor,-1,1,10))

Then work on implementing the same thing in the GUI with the bluesky widgets. 

"""


##  pip upgrade ?? Caution: Do not use it if you have alread installed some packages in the virtual environment! Pip upgrade may destroy the installed packages in ipython and qt and the restore takes a lot of time. The best way is to create a new clean virtual environment and install Bluesky step by step according to the documentation. I use conda install in the end.

    /hzb/huiling/anaconda3/envs/bluesky-tutorial/bin/python3.7 -m pip install --upgrade pip

## activate the virtual environment with conda.

    conda activate bluesky-tutorial


## open bluesky with initial settings
    ipython --matplotlib=qt5

## open bluesky with the existing profile "profile_gui_dev" from Willam.
    ipython --profile=gui_dev

## connect with EPICS PV using EpicsMotor and EpicsSignal in Bluesky. change the startup file. 
    cd .ipython
    ls
    cd profile_gui_dev
    cd startup
    sudo nano 00-start.py

The content in "00-start.py" is used to initial the bluesky RE environment. We can add epics motor "IOCsim:m1" into ophyd, and then we can see it , move it or use it to scan in bluesky. After restarting bluesky, we can see m1 als bluesky motor using "wa", and the position of m1 is 1.00 using "m1.position". Actually m1 stands for the epics PV "IOCsim:m1"(Epics virtual motor). EpicsSignal is called "EMILEL:test:rdCurE3", it is used in bluesky RE environment. Epics Motor and Epics Signal must be opened at first before opening bluesky.

open epics virtual motor:

    cd /hzb/EPICS01/motor-6.11-old/iocBoot/iocSim
    ./st.cmd.unix

open keithley 6517 and open the epics PV using the Website. Actually we opened the EPICS PV prefix with "EMILEL:test". All relevant PV are opened, we only choose EPICS PV "EMILEL:test:rdCurE3" as a testing signal in Bluesky. 

    caget EMILEL:test:rdCurE3

# mongo/ mongodb/ mongodb-compass
Note the limit: set "ulimit -n 64000" with mongo db installation.

Mongo db must be restarted after reboot.

We can use mongodb-compass to see which are contained in the mongo DB. 

I created a db called "test", with username "AdminSammy" and Password "password" in mongodb. These createUser operations must be done in the mongo db. "test" is a mongo db name, is also a catalog in databroker, which is used in bluesky queueserver and ariadne GUI.

    mongo -u AdminSammy -p --authenticationDatabase admin

It will be used in the catalog definition in bluesky intake. add the test catalog in bluesky.

    cd /hzb/huiling/anaconda3/envs/bluesky-tutorial/share/intake/
    sudo nano test.yml
    """
    sources:
    test:
    driver: bluesky-mongo-normalized-catalog
    args:
    metadatastore_db: mongodb://AdminSammy:password@localhost:27017/test?authSource=admin
    asset_registry_db: mongodb://AdminSammy:password@localhost:27017/test?authSource=admin

    """
    (The indentation above is omitted)
# bluesky widgets / ariadne

Terminal 1: 

    start-re-manager --databroker-config test

Ternimal 2: 

    ariadne --catalog test --zmq localhost:60615

With at least these two commands, ariadne GUI will be opened, in the GUI we can do the plans like scan and mv, which are already stored in the bluesky queueserver, I try to understand the theroy of the communications and know how to create/change a GUI. Due to the lack of the relevant documentation, I can just explore the programs and the structure by myself. 

bluesky widgets:  https://github.com/NSLS-II/bluesky-widgets-demo
ariadne:  https://github.com/NSLS-II-BMM/ariadne

PyCharm:

    /snap/pycharm-community/current/bin/pycharm.sh

The ariadne package is installed in "/hzb/huiling/anaconda3/envs/bluesky-tutorial/lib/python3.7/site-packages/ariadne". I download ariadne in a modifiable environment again and use pycharm to explore/change them.

    cd work/Bluesky/ariadne/ariadne
    __init__.py  main.py  models.py  __pycache__  settings.py  tests  _version.py  viewer.py  widgets.py  widget_xafs.py
   

# bluesky_queueserver

The container of the settings from bluesky things into ariadne is here:
    
    cd /hzb/huiling/anaconda3/envs/bluesky-tutorial/lib/python3.7/site-packages/bluesky_queueserver/profile_collection_sim
    00-ophyd.py  15-plans.py  99-custom.py  existing_plans_and_devices.yaml  __pycache__  user_group_permissions.yaml

We can change the plans here: 

    sudo nano /hzb/huiling/anaconda3/envs/bluesky-tutorial/lib/python3.7/site-packages/bluesky/plans.py


## After reboot on dide17:

Terminal 1(to start mongo db) on dide17: 

    systemctl start mongod.service

Terminal 2(to start Epics PV "IOCsim:m1" for simulation epicsmotors) on dide17: 

    conda activate bluesky-tutorial
    cd /hzb/EPICS01/motor-6.11-old/iocBoot/iocSim
    ./st.cmd.unix

Start Epics PV for keithley6517 on the website) on raspberrypi(192.168.1.101):

    ## start keithley6517 with the button "start", then we can get the current value with "caget EMILEL:test:rdCurE3" 

Terminal 3(to start bluesky queueserver ) on dide17: 

    start-re-manager --databroker-config test

Terminal 4(to start bluesky GUI) on dide17:

    bluesky-widgets-demo --catalog test --zmq localhost:60615


### Important:

Keithley6517 epics server is on the raspberry pi, epics motor server is on dide17, the GUI can be also opened on a third computer, for instance, "edono". Then we should use SSH to go to the dide17 at first and set the epics ca address, because we have two different epics servers(dide17 and raspberrypi). 

    export EPICS_CA_ADDR_LIST=192.168.1.101  (ip address of raspberry pi)
    caget EMILEL:test:rdCurE3
    export EPICS_CA_ADDR_LIST=XXX.XX.XXX.XX   (ip address of dide17)
    caget IOCsim:m1
    export EPICS_CA_AUTO_ADDR_LIST=YES
Terminal 1 on edono: 

    start-re-manager --databroker-config test

Terminal 2 on edono:

    bluesky-widgets-demo --catalog test --zmq localhost:60615
    
    


