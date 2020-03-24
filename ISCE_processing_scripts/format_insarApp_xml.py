#!/usr/bin/env python3

def cmdLineParse():
    '''
    Command line parser.
    '''
    import argparse

    parser = argparse.ArgumentParser(description='construct xml file for ISCE insarApp run')


    return parser.parse_args()




if __name__ == '__main__':
    '''
    Main driver.
    '''

    inps = cmdLineParse()
    
    insarApp_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<insarApp>
    <component name="insar">
        <property name="sensor name">ALOS</property>
        <property name="range looks">1</property>
        <property name="azimuth looks">5</property>
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
'''

    fid=open('insarApp.xml','w')

    fid.write(insarApp_xml)

    fid.close()
