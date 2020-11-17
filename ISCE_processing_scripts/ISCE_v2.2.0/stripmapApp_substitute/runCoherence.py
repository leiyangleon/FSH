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
import operator
import isceobj


from iscesys.ImageUtil.ImageUtil import ImageUtil as IU
from mroipac.correlation.correlation import Correlation
from isceobj.Util.decorators import use_api

logger = logging.getLogger('isce.insar.runCoherence')

## mapping from algorithm method to Correlation instance method name
CORRELATION_METHOD = {
    'phase_gradient' : operator.methodcaller('calculateEffectiveCorrelation'),
    'cchz_wave' : operator.methodcaller('calculateCorrelation')
    }

@use_api
def runCoherence(self, method="phase_gradient"):
                          
    logger.info("Calculating Coherence")
    
    import os
    
    resampAmpImage = os.path.join(self.insar.ifgDirname , self.insar.ifgFilename)
    topoflatIntFilename = os.path.join(self.insar.ifgDirname , self.insar.ifgFilename)
    
    if '.flat' in resampAmpImage:
        resampAmpImage = resampAmpImage.replace('.flat', '.amp')
    elif '.int' in resampAmpImage:
        resampAmpImage = resampAmpImage.replace('.int', '.amp')
    else:
        resampAmpImage += '.amp'

    # Initialize the amplitude
#    resampAmpImage =  self.insar.resampAmpImage
#    ampImage = isceobj.createAmpImage()
#    IU.copyAttributes(resampAmpImage, ampImage)
#    ampImage.setAccessMode('read')
#    ampImage.createImage()
#    ampImage = self.insar.getResampOnlyAmp().copy(access_mode='read')
    ampImage = isceobj.createImage()
    ampImage.load( resampAmpImage + '.xml')
    ampImage.setAccessMode('READ')
    ampImage.createImage()
    
    # Initialize the flattened inteferogram
#    topoflatIntFilename = self.insar.topophaseFlatFilename
    intImage = isceobj.createImage()
    intImage.load ( topoflatIntFilename + '.xml')
    intImage.setAccessMode('READ')
    intImage.createImage()

#    widthInt = self.insar.resampIntImage.getWidth()
#    intImage.setFilename(topoflatIntFilename)
#    intImage.setWidth(widthInt)
#    intImage.setAccessMode('read')
#    intImage.createImage()

    # Create the coherence image
    cohFilename = topoflatIntFilename.replace('.flat', '.cor')
    cohImage = isceobj.createOffsetImage()
    cohImage.setFilename(cohFilename)
    cohImage.setWidth(intImage.width)
    cohImage.setAccessMode('write')
    cohImage.createImage()

    cor = Correlation()
    cor.configure()
    cor.wireInputPort(name='interferogram', object=intImage)
    cor.wireInputPort(name='amplitude', object=ampImage)
    cor.wireOutputPort(name='correlation', object=cohImage)
   
    cohImage.finalizeImage()
    intImage.finalizeImage()
    ampImage.finalizeImage()

    cor.calculateCorrelation()

    # NEW COMMANDS added by YL --start
    import subprocess
    subprocess.getoutput('MULTILOOK_FILTER_ISCE.py -a ./interferogram/topophase.amp -c ./interferogram/topophase.cor')
    subprocess.getoutput('CROP_ISCE_stripmapApp.py -a ./interferogram/topophase.amp -c ./interferogram/topophase.cor')
    subprocess.getoutput('imageMath.py -e="a_0;a_1" --a ./interferogram/topophase.amp -o ./interferogram/resampOnlyImage1.amp -s BIL -t FLOAT')
    self.geocode_list += ['./interferogram/resampOnlyImage1.amp']
    # NEW COMMANDS added by YL --end

#    try:
#        CORRELATION_METHOD[method](cor)
#    except KeyError:
#        print("Unrecognized correlation method")
#        sys.exit(1)
#        pass
    return None
