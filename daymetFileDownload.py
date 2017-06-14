# -------------------------------------------------------------------------------
# Name:        daymetFileDownload.py
# Purpose:
#
# Author:      jmitzelfelt
#
# Created:     17/11/2016
# Copyright:   (c) jmitzelfelt 2016
# Licence:     Unlicense
# -------------------------------------------------------------------------------

import urllib.request
import os
from datetime import date as dt

types = ['dayl', 'prcp', 'srad', 'swe', 'tmax', 'tmin', 'vp']
# http://thredds.daac.ornl.gov/thredds/catalog/ornldaac/1345/catalog.html?dataset=1345/daymet_v3_prcp_monttl_1980_na.nc4

def downloadError(inUrl, inFileName, e):
    print("Error downloading {}".format(inFileName))
    print("Errorcode is {}".format(e.getcode()))
    os.remove(inFileName)
    download(inUrl, inFileName)


def download(inUrl, inFileName):
    try:
        print("Downloading {}".format(inFileName))
        urllib.request.urlretrieve(inUrl, inFileName)
        print("{} download complete".format(inFileName))
    except urllib.error.HTTPError as e:
        if e.getcode() == 404:
            print("{} not found".format(e.geturl()))
        else:
            downloadError(inUrl, inFileName, e)
    except Exeception as e:
        downloadError(inUrl, inFileName, e)

def getDailyFiles(inYear, inTypes):
    urlTemplate = 'http://thredds.daac.ornl.gov/thredds/fileServer/ornldaac/1328/{0}/daymet_v3_{1}_{0}_na.nc4'
#    fileTemplate = 'E:/daymet/Daily/{1}/daymet_v3_{1}_{0}_na.nc4'
    fileTemplate = '../daymet/Daily/{1}/daymet_v3_{1}_{0}_na.nc4'
    for type in inTypes:
        if not os.path.isfile(fileTemplate.format(inYear, type)):
            download(urlTemplate.format(inYear, type), fileTemplate.format(inYear, type))
        else:
            print("Skipping {} - {}".format(inYear, type))


def getMonthFiles(inYear, inTypes):
    urlTemplate = 'http://thredds.daac.ornl.gov/thredds/fileServer/ornldaac/1345/daymet_v3_{1}_mon{2}_{0}_na.nc4'
    fileTemplate = '../daymet/Monthly/{1}/daymet_v3_{1}_mon{2}_{0}_na.nc4'
    for type in inTypes:
        sumName = 'ttl' if (type == 'prcp') else 'avg'
        if not os.path.isfile(fileTemplate.format(inYear, type, sumName)):
            download(urlTemplate.format(inYear, type, sumName), fileTemplate.format(inYear, type, sumName))
        else:
            print("Skipping {} - {} - mon{}".format(inYear, type, sumName))


def getAnnualFiles(inYear, inTypes):
    urlTemplate = 'http://thredds.daac.ornl.gov/thredds/fileServer/ornldaac/1343/daymet_v3_{1}_ann{2}_{0}_na.nc4'
    fileTemplate = '../daymet/Annual/{1}/daymet_v3_{1}_ann{2}_{0}_na.nc4'
    for type in inTypes:
        sumName = 'ttl' if (type == 'prcp') else 'avg'
        if not os.path.isfile(fileTemplate.format(inYear, type, sumName)):
            download(urlTemplate.format(inYear, type, sumName), fileTemplate.format(inYear, type, sumName))
        else:
            print("Skipping {} - {} - anl{}".format(inYear, type, sumName))


def downloadDaymet(inStartYear=1980, inEndYear=dt.today().year):
    for year in range(inStartYear, inEndYear):
        getDailyFiles(year, ['dayl', 'prcp', 'srad', 'swe', 'tmax', 'tmin', 'vp'])
        getMonthFiles(year, ['prcp', 'tmax', 'tmin', 'vp'])
        getAnnualFiles(year, ['prcp', 'tmax', 'tmin', 'vp'])
