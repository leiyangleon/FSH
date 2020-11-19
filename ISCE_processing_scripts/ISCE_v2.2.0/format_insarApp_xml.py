#!/usr/bin/env python3

def cmdLineParse():
    '''
    Command line parser.
    '''
    import argparse

    parser = argparse.ArgumentParser(description='construct xml file for ISCE insarApp run')
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
    
    if sensor == 'ALOS':
        insarApp_xml = '''<?xml version="1.0" encoding="UTF-8"?>
    <insarApp>
        <component name="insar">
            <property name="sensor name">{0}</property>
            <property name="range looks">{1}</property>
            <property name="azimuth looks">{2}</property>
    <!--        <property  name="Culling error limit">60</property>-->
            <component name="master">
                <catalog>master.xml</catalog>
            </component>
            <component name="slave">
                <catalog>slave.xml</catalog>
            </component>
    <!--        <property name="demFilename">-->
    <!--            <value>/Users/fattahi/process/test_roiApp/Alos_Maule_T116/demLat_S39_S35_Lon_W074_W071.dem.wgs84</value>-->
    <!--        </property>-->
            <component name="insarproc">
                <property name="applyWaterMask">
                    <value>False</value>
                </property>
            </component>
        </component>
    </insarApp>
    '''.format(sensor,rlks,alks)
    elif sensor == 'ALOS2':
        insarApp_xml = '''<?xml version="1.0" encoding="UTF-8"?>
    <insarApp>
        <component name="insar">
            <property name="sensor name">{0}</property>
            <property  name="doppler method">useDEFAULT</property>
            <property name="range looks">{1}</property>
            <property name="azimuth looks">{2}</property>
            <property  name="Culling error limit">60</property>
    <!--        <property name="slc offset method">ampcor</property>-->
            <component name="master">
                <catalog>master.xml</catalog>
            </component>
            <component name="slave">
                <catalog>slave.xml</catalog>
            </component>
    <!--        <property name="demFilename">-->
    <!--            <value>/Users/fattahi/process/test_roiApp/Alos_Maule_T116/demLat_S39_S35_Lon_W074_W071.dem.wgs84</value>-->
    <!--        </property>-->
            <component name="insarproc">
                <property name="applyWaterMask">
                    <value>False</value>
                </property>
            </component>
        </component>
    </insarApp>
    '''.format(sensor,rlks,alks)
    else:
        raise Exception('Unknown sensor; Supported sensors include ALOS and ALOS2 only')


    fid=open('insarApp.xml','w')

    fid.write(insarApp_xml)

    fid.close()
