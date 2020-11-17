#!/usr/bin/env python3

def cmdLineParse():
    '''
    Command line parser.
    '''
    import argparse

    parser = argparse.ArgumentParser(description='construct xml file for ISCE stripmapApp run')
    parser.add_argument('-s', '--sensor', dest='sensor', type=str, required=True,
                        help='Sensor type, e.g. ALOS, ALOS2')

    return parser.parse_args()




if __name__ == '__main__':
    '''
    Main driver.
    '''

    inps = cmdLineParse()
    
    sensor = inps.sensor

    if sensor == 'ALOS':
        rlks = 1
        alks = 5
    elif sensor == 'ALOS2':
        rlks = 2
        alks = 4
    else:
        raise Exception('Unknown sensor; Supported sensors include ALOS and ALOS2 only')
    
    stripmapApp_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<insarApp>
    <component name="insar">
        <property name="sensor name">{0}</property>
        <property name="range looks">{1}</property>
        <property name="azimuth looks">{2}</property>
        <component name="master">
            <catalog>master.xml</catalog>
        </component>
        <component name="slave">
            <catalog>slave.xml</catalog>
        </component>
<!--        <property name="demFilename">-->
<!--            <value>/Users/fattahi/process/test_roiApp/Alos_Maule_T116/demLat_S39_S35_Lon_W074_W071.dem.wgs84</value>-->
<!--        </property>-->
        <property name="do rubbersheeting">True</property>
        <property name="do denseoffsets">True</property>
<!--        <property name="do split spectrum">True</property>-->
<!--        <property name="unwrapper name">snaphu</property>-->
<!--        <property name="do dispersive">True</property>-->
<!--        <property name="dispersive filter kernel x-size">800</property>-->
<!--        <property name="dispersive filter kernel y-size">800</property>-->
<!--        <property name="dispersive filter kernel sigma_x">100</property>-->
<!--        <property name="dispersive filter kernel sigma_y">100</property>-->
<!--        <property name="dispersive filter kernel rotation">0</property>-->
<!--        <property name="dispersive filter number of iterations">5</property>-->
<!--        <property name="dispersive filter mask type">connected_components</property>-->
<!--        <property name="dispersive filter coherence threshold">0.6</property>-->
    </component>
</insarApp>
'''.format(sensor,rlks,alks)

    fid=open('stripmapApp.xml','w')

    fid.write(stripmapApp_xml)

    fid.close()
