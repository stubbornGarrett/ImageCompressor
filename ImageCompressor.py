import getopt
import glob
import logging
from sys import argv, stdout
from os import listdir, mkdir, path
from PIL import Image
from argparse import ArgumentParser

class ImageCompressor:
    def __init__(self):
        self.progressCount = 0  # Counts up for each compressed image
        self.progressGoal  = 0  # Gets total number of images to compress
        self.failedCompression = 0
        self.validExtensions = (".jpg", ".png", " ")

    def compress(self, dir, ext, qual):
        dirPath           = dir   if path.isdir(dir)              else self.quitProgram(1, str(dir))
        compressExtension = ext   if ext in self.validExtensions  else self.quitProgram(2, str(ext))
        compressQuality   = qual  if qual in range(1, 101)        else self.quitProgram(3, str(qual))
        keepType          = True  if compressExtension == " "     else False
        logging.info(" ---- Settings ----")
        logging.info("Directory: {}\\".format(dirPath))
        if keepType:
            logging.info("Extension: keep original")
        else:
            logging.info("Extension: {}".format(compressExtension))
        logging.info("Quality: {}%".format(compressQuality))
        logging.info(" ------------------")

        # Create subfolder to store compressed images
        if not path.isdir(dirPath + "\\compressed\\"):
            mkdir(dirPath + "\\compressed")

        imageList = self.filterForExtension(dirPath, self.validExtensions)
        self.progressGoal = len(imageList)
        self.updateProgressbar(0)

        for image in imageList:
            try:
                name, ext = path.splitext(image)
                tempImage = Image.open(dirPath + "\\" + image)
                ext = compressExtension if not keepType else ext
                savePath = dirPath + "\\compressed\\" + name + ext
                if compressExtension == ".png" or tempImage.mode != "RGBA":
                        tempImage.save(savePath, optimize=True, quality=compressQuality)
                else:
                        tempImage.convert("RGB").save(savePath, optimize=True, quality=compressQuality)
                self.updateProgressbar(1)
            except:
                self.progressGoal -= 1
                self.failedCompression += 0
            
        self.quitProgram(0)

    def filterForExtension(self, dir, ext):
        logging.info("Search for images...")
        listOfFiles = listdir(dir)
        listOfFiles = [file for file in listOfFiles if file.endswith(ext)]
        logging.info("{} images found".format(len(listOfFiles)))
        return listOfFiles

    def updateProgressbar(self, stepSize):
        self.progressCount += stepSize
        loadedCount = int(((self.progressCount/self.progressGoal)*100)*0.5) if self.progressCount is not 0 else 0
        emptyCount  = 50 - loadedCount
        stdout.write('\r[{0}{1}]'.format('#'*loadedCount , '-'*emptyCount))

    def quitProgram(self, exitCode, info=None):
        if exitCode == 0:
            print("")
            print("Finished successfully! {} images compressed".format(self.progressGoal))
            logging.info("Finished successfully! {} images compressed".format(self.progressGoal))
            if self.failedCompression > 0:
                print("{} images failed to compress".format(self.failedCompression))
                logging.info("{} images failed to compress".format(self.failedCompression))
            quit()
        elif exitCode == 1:
            print("Something went wrong! Check ImageCompressor.log for more information")
            logging.error('Filepath "{}" is not valid!'.format(info))
            quit()
        elif exitCode == 2:
            print("Something went wrong! Check ImageCompressor.log for more information")
            logging.error("Extension must be .jpg, .png or empty for original extension! {} is not valid".format(info))
            quit()
        elif exitCode == 3:
            print("Something went wrong! Check ImageCompressor.log for more information")
            logging.error("Quality must be an integer between 1 and 100! {} is not valid".format(info))
            quit()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename='ImageCompressor.log')
    parser = ArgumentParser()
    parser.add_argument("-p", "--path", default=".", help="Filepath to directory with images. Default: .\\")
    parser.add_argument("-e", "--extension", "--format", default=" ", help="Extenion for outputfiles (.jpg .png). Default: original")
    parser.add_argument("-q", "--quality", default=90, type=int, help="Quality of the output file in percent. Default: 100")
    args = parser.parse_args()
    
    application = ImageCompressor()
    logging.info(" ###### Start setup ###### ")
    application.compress(args.path, args.extension, args.quality)
