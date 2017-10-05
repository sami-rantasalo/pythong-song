####################################################
# Tile imagefiles to one image in given dimensions #
#                                                  #
# sami.rantasalo@iki.fi                            #
# 2017                                             #
# v03                                              #
####################################################
import os, math, sys
from PIL import Image, ImageOps

resultImageSize = 100; #default image side length
resultImageSide = 1; #number of images per column / row

acceptedFileExtension = [".", ".png"]
acceptedFileList = []


if (len(sys.argv)!=5):
    print "Please use format blot <directory> <result image side length in px> <number of files to process> <filename>"
    print ""
    print "Number of files should be a square of a number (1, 4, 9, 16 etc.)"
    sys.exit(-1)

try:
    if (int(sys.argv[2])<1 or float(sys.argv[3])<1):
        print "Please use positive integers as parameters"
        sys.exit(-1)
except ValueError:
    print "Use integers in parameter values"
    sys.exit(-1)

try:
    rootDir = sys.argv[1]
    resultImageSize=int(sys.argv[2])
    resultFileCnt=int(sys.argv[3]);
    resultFileName=sys.argv[4];

    print "Will process %s files in directory %s to create an image sized %spx x %spx." % (resultFileCnt, rootDir, resultImageSize, resultImageSize)

    fileCount = 0
    #Calculate accepted files (extension match)
    for subdir, dirs, files in os.walk(rootDir):
        for file in files:
            filepath = subdir + os.sep + file
            for extension in acceptedFileExtension:
                if filepath.endswith(extension):
                    acceptedFileList.append(filepath)
                    break


    fileCnt = len(acceptedFileList)
    # NOT ENOUGH FILES MATCHING THE EXTENSION TO CREATE THE IMAGE
    if (fileCnt<resultFileCnt):
        print "Not enough files (%s) to create the result image" % fileCnt
        sys.exit(-2)

    # INIT RESULT IMAGE
    result = Image.new("RGB", (resultImageSize, resultImageSize))

    # NOT CHECKED TODO: CHECK 'EM
    tileNum = int(math.sqrt(resultFileCnt))
    tileSize = int(resultImageSize/tileNum)


    # TILE IMAGES AS WE GO
    for index, file in enumerate(acceptedFileList):
        print "Processing %s" % (file)
        img = Image.open(file)
        #img = img.resize((tileSize,tileSize), Image.ANTIALIAS) #Don't care about aspect ratio
        img.thumbnail((tileSize,tileSize), Image.ANTIALIAS) #Obamacare
        w, h = img.size
        x = index // tileNum * tileSize
        #y = index % tileNum * tileSize
        y = index % tileNum * h

        print('pos {0},{1} size {2},{3}'.format(x, y, w, h))
        result.paste(img, (x, y, x + w, y + h))

    result.save(resultFileName)
    print "Files processed and file %s was created." % resultFileName
    sys.exit(0)

except IOError:
    print "Vituiks men.."
    sys.exit(-1)
