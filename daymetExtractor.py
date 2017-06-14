# -------------------------------------------------------------------------------
# Name:        daymetFileDownload.py
# Purpose:
#
# Author:      jmitzelfelt
#
# Created:     7/2/2017
# Copyright:   (c) jmitzelfelt 2017
# Licence:     Unlicense
# -------------------------------------------------------------------------------

import numpy as np
from osgeo import gdal
from osgeo import gdalconst
from osgeo import osr
import os
import re
import fnmatch
import datetime


def fileRetrieve(inDir, inFilters):
    returnFileInfos = []
    includes = r'|'.join([fnmatch.translate('*.' + x.upper()) for x in inFilters])
    for root, dirs, files in os.walk(inDir):
        files = [(root, f) for f in files]
        files = [f for f in files if re.match(includes, f[1].upper())]
        returnFileInfos.extend(files)
    return returnFileInfos


def filterFileInfoList(inFileInfos, inDirFilters, inFileFilter):
    dirIncludes = r'|'.join([fnmatch.translate('*' + x.upper() + '*') for x in inDirFilters])
    fileInclude = fnmatch.translate('*' + inFileFilter.upper() + '*')
    returnFileInfos = [f for f in inFileInfos if re.match(dirIncludes, f[0].upper()) and re.match(fileInclude, f[1].upper())]
    return returnFileInfos


def getFileInfoYear(inFileInfo):
    return re.search(r'\d{4}', inFileInfo[1]).group()


def sortFileInfoList(inFileInfo, inDataTypes):
    year = getFileInfoYear(inFileInfo)
    testType = '0'
    if len(inDataTypes) > 1:
        for DataType in inDataTypes:
            if inFileInfo[0].find(DataType) >= 0:
                testType = str(inDataTypes.index(DataType))
                break
    return year + testType


# Adapted from http://stackoverflow.com/questions/10454316/how-to-project-and-resample-a-grid-to-match-another-grid-with-gdal-python
def projectFile(
    inDataLayer,
    inMaskLayer,
    inOutLayer='',
    inDriverType="MEM"
    ):
    dataLayer = gdal.Open(inDataLayer, gdalconst.GA_ReadOnly)
    dataProj = osr.SpatialReference()
    dataProj.ImportFromWkt(dataLayer.GetProjection())
    maskLayer = gdal.Open(inMaskLayer, gdalconst.GA_ReadOnly)
    maskProj = osr.SpatialReference()
    maskProj.ImportFromWkt(maskLayer.GetProjection())
    maskGeoTrans = maskLayer.GetGeoTransform()
    xSize = maskLayer.RasterXSize
    ySize = maskLayer.RasterYSize
    bandCount = dataLayer.RasterCount
    destLayer = gdal.GetDriverByName(inDriverType).Create(inOutLayer, xSize, ySize, bandCount, gdalconst.GDT_Float32)
    destLayer.SetGeoTransform(maskGeoTrans)
    destLayer.SetProjection(maskProj.ExportToWkt())
    gdal.ReprojectImage(dataLayer, destLayer, dataProj.ExportToWkt(), maskProj.ExportToWkt(), gdalconst.GRA_NearestNeighbour)
    return destLayer


def main(
    inDataDir,
    inMaskLayer,
    inOutDataDir,
    inDataParms=['tmax', 'tmin', 'prcp'],
    inDataTypes={'daily': ['Daily'], 'monthly': ['Monthly', 'Annual']},
    inFileExts=['nc4']
    ):

    fileInfos = fileRetrieve(inDataDir, inFileExts)
    maskData = gdal.Open(inMaskLayer)
    maskArray = maskData.GetRasterBand(1).ReadAsArray().ravel()
    for DataType in inDataTypes:
        for DataParm in inDataParms:
            outDataFile = '{}{}_DAYMET_GYE_{}.csv'.format(inOutDataDir, DataType.upper(), DataParm.upper())
            with open(outDataFile, 'w+') as outputFile:
                print('Writing {}'.format(outDataFile))
                # Write dataFile Header
                outputFile.write('point number ->,')
                if DataType == 'daily':
                    outputFile.write('month,year,')
                maskArray.tofile(outputFile, sep=',')
                outputFile.write('\n')
                filteredFileInfos = sorted(filterFileInfoList(fileInfos, inDataTypes[DataType], DataParm), key=lambda fileInfo: sortFileInfoList(fileInfo, inDataTypes[DataType]))
                for FileInfo in filteredFileInfos:
                    dataLayer = '/'.join(FileInfo)
                    print(dataLayer)
                    rasterData = projectFile(dataLayer, inMaskLayer)
                    rasterCount = rasterData.RasterCount
                    for band in range(1, rasterCount + 1):
                        bandArray = rasterData.GetRasterBand(band).ReadAsArray().ravel().tolist()
                        if DataParm == 'prcp':
                            roundedArray = np.round(np.multiply(bandArray, 100), 1)
                        else:
                            roundedArray = np.round(bandArray, 2)

                        year = getFileInfoYear(FileInfo)

                        if DataType == 'daily':

                            dataLine = (datetime.datetime(int(year), 1, 1) + datetime.timedelta(band - 1)).strftime('%m/%d/%Y,%m,%Y,')

                        else:

                            month = band if (FileInfo[0].find('Monthly') > -1) else 14
                            dataLine = '{}_{}{},'.format(DataParm, year, str(month).zfill(2))

                        print(dataLine)
                        outputFile.write(dataLine)
                        roundedArray.tofile(outputFile, sep=',')
                        outputFile.write('\n')
            outputFile.close()
            del outputFile


main('F:/daymet/', 'F:/daymetDataExtraction/daymetmask', 'F:/daymetData/')
