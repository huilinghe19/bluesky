# bluesky_practice

## create a new virtual environment "bleusky-tutorial", install mongodb, bluesky, ophyd, bluesky_queueserver, ariadne.

## open mongodb, create user and password. open mongodb.

##  pip upgrade ?? Do not use it! upgrade may destroy something like ipython and qt things. use conda install in the end. step by step in a clean virtual environment to install bluesky is important.

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

# mongo/ mogodb/ mongodb-compass
we can use it to see which are contained in the mongo DB. I created a db called "test", with username "AdminSammy" and Password "password" in mongodb. "test" is a mongo db name, is also a catalog in databroker. 

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

ariadne GUI will be opened, in the GUI we can do the plans like scan and mv, which are already stored in the bluesky queueserver, I try to understand the theroy of the communications and know how to create/change a GUI. 

bluesky widgets:  https://github.com/NSLS-II/bluesky-widgets-demo
ariadne:  https://github.com/NSLS-II-BMM/ariadne

Due to the lack of the relevant documentation, I can just explore the programs and the structure by myself.    
