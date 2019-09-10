import os
import mmap

class UIO(object):
    def __init__(self, uioNum,mapNum):
        if (uioNum < 0) or (mapNum < 0):
            raise Exception("Invalid UIO device or map number. Check /sys/class/uio for more information about the available UIO devices")
        self.uioNum=uioNum
        self.mapNum=mapNum
        filename = '/sys/class/uio/uio%d/maps/map%d/size' % (uioNum, mapNum)
        uiofile= '/dev/uio%d' % uioNum
        if os.path.isfile(filename) == False:
            raise Exception("UIO device or map number not found. Check /sys/class/uio for more information about the available UIO devices")
        fileObj = open(filename)
        self.mapSize = int(fileObj.readline(),0)
        fileObj.close()
        try:
            self.uio_fd = os.open(uiofile, os.O_RDWR)
            self.mmap = mmap.mmap(self.uio_fd,self.mapSize, mmap.MAP_SHARED,mmap.PROT_READ | mmap.PROT_WRITE, os.sysconf("SC_PAGE_SIZE")*self.mapNum)
        except:
            raise Exception("UIO device not found in /dev/uio*")

    def release(self):
        self.mmap.close()
        os.close(self.uio_fd)

