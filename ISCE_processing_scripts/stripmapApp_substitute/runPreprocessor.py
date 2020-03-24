#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright 2012, by the California Institute of Technology. ALL RIGHTS RESERVED.
# United States Government Sponsorship acknowledged. Any commercial use must be
# negotiated with the Office of Technology Transfer at the California Institute of
# Technology.  This software is subject to U.S. export control laws and regulations
# and has been classified as EAR99.  By accepting this software, the user agrees to
# comply with all applicable U.S. export laws and regulations.  User has the
# responsibility to obtain export licenses, or other export authority as may be
# required before exporting such information to foreign countries or providing
# access to foreign persons.
#
# Author: Brett George
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~






import logging
import isceobj
import mroipac
from mroipac.baseline.Baseline import Baseline
import copy
import os

logger = logging.getLogger('isce.insar.runPreprocessor')

def runPreprocessor(self):

    from .Factories import isRawSensor, isZeroDopplerSLC, getDopplerMethod    

    ###Unpack master
    sensor = copy.deepcopy(self.master)

    dirname = sensor.output

    if self.masterSensorName is None:
        self.masterSensorName = self.sensorName

    israwdata = isRawSensor(self.masterSensorName)


    if self.masterDopplerMethod is None:
        mdop = getDopplerMethod(self.masterSensorName)
    else:
        mdop = self.masterDopplerMethod
    
    masterdop = isceobj.Doppler.createDoppler(mdop)

    if israwdata:
        print('Master data is in RAW format. Adding _raw to output name.')
        sensor.output = os.path.join(dirname + '_raw', os.path.basename(dirname)+'.raw')
        if not os.path.isdir( os.path.dirname(sensor.output)):
            os.makedirs( os.path.dirname(sensor.output))
        #sensor._resampleFlag = 'single2dual'
        master = make_raw(sensor, masterdop)

        ###Weird handling here because of way make_raw is structured
        ###DOPIQ uses weird dict to store coeffs
        if mdop == 'useDOPIQ':
            #master._dopplerVsPixel = [masterdop.quadratic[x]*master.PRF for x in ['a','b','c']]
            master.frame._dopplerVsPixel = [masterdop.quadratic[x]*master.PRF for x in ['a','b','c']]

        if self._insar.masterRawProduct is None:
            self._insar.masterRawProduct = dirname + '_raw.xml'

        self._insar.saveProduct(master.frame, self._insar.masterRawProduct)

    else:
        print('Master data is in SLC format. Adding _slc to output name.')
        iszerodop = isZeroDopplerSLC(self.masterSensorName) 
        sensor.output =  os.path.join(dirname + '_slc', os.path.basename(dirname)+'.slc')

        if not os.path.isdir( os.path.dirname(sensor.output)):
            os.makedirs( os.path.dirname(sensor.output))
        
        master = make_raw(sensor, masterdop)
        
        if self._insar.masterSlcProduct is None:
            self._insar.masterSlcProduct = dirname + '_slc.xml'

        if iszerodop:
            self._insar.masterGeometrySystem = 'Zero Doppler'
        else:
            self._insar.masterGeometrySystem = 'Native Doppler'

        self._insar.saveProduct(master.frame, self._insar.masterSlcProduct)


    ###Unpack slave
    sensor = copy.deepcopy(self.slave)
    dirname = sensor.output

    if self.slaveSensorName is None:
        self.slaveSensorName = self.sensorName

    israwdata = isRawSensor(self.slaveSensorName)

    if self.slaveDopplerMethod is None:
        sdop = getDopplerMethod( self.slaveSensorName)
    else:
        sdop = self.slaveDopplerMethod

    slavedop = isceobj.Doppler.createDoppler(sdop)

    if israwdata:
        print('Slave data is in RAW format. Adding _raw to output name.')
        sensor.output = os.path.join(dirname + '_raw', os.path.basename(dirname)+'.raw')

        if not os.path.isdir( os.path.dirname(sensor.output)):
            os.makedirs( os.path.dirname(sensor.output))

        slave = make_raw(sensor, slavedop)

        ###Weird handling here because of make_raw structure
        ###DOPIQ uses weird dict to store coefficients
        if sdop == 'useDOPIQ':
            #slave._dopplerVsPixel = [slavedop.quadratic[x]*slave.PRF for x in ['a','b','c']]
            slave.frame._dopplerVsPixel = [slavedop.quadratic[x]*slave.PRF for x in ['a','b','c']]

        if self._insar.slaveRawProduct is None:
            self._insar.slaveRawProduct = dirname + '_raw.xml'

        self._insar.saveProduct(slave.frame, self._insar.slaveRawProduct)

    else:
        print('Master data is in SLC format. Adding _slc to output name.')
        iszerodop = isZeroDopplerSLC(self.slaveSensorName)
        sensor.output =  os.path.join(dirname + '_slc', os.path.basename(dirname)+'.slc')

        if not os.path.isdir( os.path.dirname(sensor.output)):
            os.makedirs( os.path.dirname(sensor.output))

        slave = make_raw(sensor, slavedop)
        
        if self._insar.slaveSlcProduct is None:
            self._insar.slaveSlcProduct = dirname + '_slc.xml'

        
        if iszerodop:
            self._insar.slaveGeometrySystem = 'Zero Doppler'
        else:
            self._insar.slaveGeometrySystem = 'Native Doppler'

        self._insar.saveProduct(slave.frame, self._insar.slaveSlcProduct)
    

    catalog = isceobj.Catalog.createCatalog(self._insar.procDoc.name)
    frame = master.frame
    instrument = frame.getInstrument()
    platform = instrument.getPlatform()

    catalog.addInputsFrom(master.sensor, 'master.sensor')
    catalog.addItem('width', frame.numberOfSamples, 'master')
    catalog.addItem('iBias', instrument.getInPhaseValue(), 'master')
    catalog.addItem('qBias', instrument.getQuadratureValue(), 'master')
    catalog.addItem('range_sampling_rate', instrument.getRangeSamplingRate(), 'master')
    catalog.addItem('prf', instrument.getPulseRepetitionFrequency(), 'master')
    catalog.addItem('pri', 1.0/instrument.getPulseRepetitionFrequency(), 'master')
    catalog.addItem('pulse_length', instrument.getPulseLength(), 'master')
    catalog.addItem('chirp_slope', instrument.getChirpSlope(), 'master')
    catalog.addItem('wavelength', instrument.getRadarWavelength(), 'master')
    catalog.addItem('lookSide', platform.pointingDirection, 'master')
    catalog.addInputsFrom(frame, 'master.frame')
    catalog.addInputsFrom(instrument, 'master.instrument')
    catalog.addInputsFrom(platform, 'master.platform')
    catalog.addInputsFrom(frame.orbit, 'master.orbit')

    frame = slave.frame
    instrument = frame.getInstrument()
    platform = instrument.getPlatform()

    catalog.addInputsFrom(slave.sensor, 'slave.sensor')
    catalog.addItem('width', frame.numberOfSamples, 'slave')
    catalog.addItem('iBias', instrument.getInPhaseValue(), 'slave')
    catalog.addItem('qBias', instrument.getQuadratureValue(), 'slave')
    catalog.addItem('range_sampling_rate', instrument.getRangeSamplingRate(), 'slave')
    catalog.addItem('prf', instrument.getPulseRepetitionFrequency(), 'slave')
    catalog.addItem('pri', 1.0/instrument.getPulseRepetitionFrequency(), 'slave')
    catalog.addItem('pulse_length', instrument.getPulseLength(), 'slave')
    catalog.addItem('chirp_slope', instrument.getChirpSlope(), 'slave')
    catalog.addItem('wavelength', instrument.getRadarWavelength(), 'slave')
    catalog.addItem('lookSide', platform.pointingDirection, 'slave')
    catalog.addInputsFrom(frame, 'slave.frame')
    catalog.addInputsFrom(instrument, 'slave.instrument')
    catalog.addInputsFrom(platform, 'slave.platform')
    catalog.addInputsFrom(frame.orbit, 'slave.orbit')
    
    # NEW COMMANDS added by YL --start
    optlist = ['all', 'top', 'middle', 'bottom']
    success=False
    baseLocation = None
    
    for option in optlist:
        baseObj = Baseline()
        baseObj.configure()
        baseObj.baselineLocation = option
        baseObj.wireInputPort(name='masterFrame',object=master.frame)
        baseObj.wireInputPort(name='slaveFrame',object=slave.frame)
        try:
            baseObj.baseline()
            success=True
            baseLocation=option
        except:
            print('Baseline computation with option {0} Failed'.format(option))
            pass
        
        if success:
            break

    if not success:
        raise Exception('Baseline computation failed with all possible options. Images may not overlap.')
    
    catalog.addItem('horizontal_baseline_top', baseObj.hBaselineTop, 'baseline')
    catalog.addItem('horizontal_baseline_rate', baseObj.hBaselineRate, 'baseline')
    catalog.addItem('horizontal_baseline_acc', baseObj.hBaselineAcc, 'baseline')
    catalog.addItem('vertical_baseline_top', baseObj.vBaselineTop, 'baseline')
    catalog.addItem('vertical_baseline_rate', baseObj.vBaselineRate, 'baseline')
    catalog.addItem('vertical_baseline_acc', baseObj.vBaselineAcc, 'baseline')
    catalog.addItem('perp_baseline_top', baseObj.pBaselineTop, 'baseline')
    catalog.addItem('perp_baseline_bottom', baseObj.pBaselineBottom, 'baseline')
    catalog.addItem('baseline_location', baseLocation, 'baseline')
    # NEW COMMANDS added by YL --end

    catalog.printToLog(logger, "runPreprocessor")
    self._insar.procDoc.addAllFromCatalog(catalog)

def make_raw(sensor, doppler):
    from make_raw import make_raw

    objMakeRaw = make_raw()
    objMakeRaw(sensor=sensor, doppler=doppler)

    return objMakeRaw

def initRawImage(makeRawObj):
    from isceobj.Image import createSlcImage
    from isceobj.Image import createRawImage
    #the "raw" image in same case is an slc.
    #for now let's do it in this way. probably need to make this a factory
    #instantiated based on the sensor type
    imageType = makeRawObj.frame.getImage()
    if isinstance(imageType, createRawImage().__class__):
        filename = makeRawObj.frame.getImage().getFilename()
        bytesPerLine = makeRawObj.frame.getImage().getXmax()
        goodBytes = makeRawObj.frame.getImage().getXmax() - makeRawObj.frame.getImage().getXmin()
        logger.debug("bytes_per_line: %s" % (bytesPerLine))
        logger.debug("good_bytes_per_line: %s" % (goodBytes))
        objRaw = createRawImage()
        objRaw.setFilename(filename)

        objRaw.setNumberGoodBytes(goodBytes)
        objRaw.setWidth(bytesPerLine)
        objRaw.setXmin(makeRawObj.frame.getImage().getXmin())
        objRaw.setXmax(bytesPerLine)
    elif(isinstance(imageType,createSlcImage().__class__)):
        objRaw = createSlcImage()
        filename = makeRawObj.frame.getImage().getFilename()
        bytesPerLine = makeRawObj.frame.getImage().getXmax()
        objRaw.setFilename(filename)
        objRaw.setWidth(bytesPerLine)
        objRaw.setXmin(makeRawObj.frame.getImage().getXmin())
        objRaw.setXmax(bytesPerLine)
    return objRaw
