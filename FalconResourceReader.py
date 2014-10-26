import png

class Resource(object):
    def __init__(self,ID,Typ,File,offset):
        self.resourceID = ID
        self.resourceTyp = Typ
        self.file = File
        self.offset = offset

    def getID(self):
        return self.resourceID

    def getTyp(self):
        return self.resourceTyp

class Image(Resource):
    def __init__(self,ID,Typ,File,offset):
        self.resourceID = ID
        self.resourceTyp = Typ
        self.file = File
        self.offset = offset
        
        self.Flag = None
        self.CenterX = None
        self.CenterY = None
        self.Width = None
        self.Height = None
        self.Offset = None
        self.PaletteSize = None
        self.PaletteOffset = None

        self.PixelData = ""
        self.PaletteData = ""
        
        self.readFlag()
        self.readCenterX()
        self.readCenterY()
        self.readWidth()
        self.readHeight()
        self.readOffset()
        self.readPaletteSize()
        self.readPaletteOffset()

    def readFlag(self):
        i = 47 + self.offset 
        flag = ""
        while i >=44 + self.offset:
            flag += self.file[i]
            i-=1
        self.Flag = flag.encode("hex")

    def readCenterX(self):
        i = 49 + self.offset 
        centerX =""
        while i >=48 + self.offset:
            centerX +=self.file[i]
            i-=1
        self.CenterX = int(centerX.encode("hex"),16)

    def readCenterY(self):
        i = 51 + self.offset 
        centerY =""
        while i >=50 + self.offset:
            centerY +=self.file[i]
            i-=1
        self.CenterY = int(centerY.encode("hex"),16)

    def readWidth(self):
        i = 53 + self.offset 
        width =""
        while i >=52 + self.offset :
            width +=self.file[i]
            i-=1
        self.Width = int(width.encode("hex"),16)

    def readHeight(self):
        i = 55 + self.offset 
        height =""
        while i >=54 + self.offset:
            height +=self.file[i]
            i-=1
        self.Height = int(height.encode("hex"),16)

    def readOffset(self):
        i = 59 + self.offset 
        offset = ""
        while i >=56 + self.offset:
            offset +=self.file[i]
            i-=1
        self.Offset = int(offset.encode("hex"),16)

    def readPaletteSize(self):
        i = 63 + self.offset 
        PaletteSize = ""
        while i >=60 + self.offset:
            PaletteSize +=self.file[i]
            i-=1
        self.PaletteSize = int(PaletteSize.encode("hex"),16)

    def readPaletteOffset(self):
        i = 67 + self.offset 
        PaletteOffset = ""
        while i >=64 + self.offset:
            PaletteOffset +=self.file[i]
            i-=1
        self.PaletteOffset = int(PaletteOffset.encode("hex"),16)

    def getFlag(self):
        return self.Flag

    def getCenterX(self):
        return self.CenterX

    def getCenterY(self):
        return self.CenterY

    def getWidth(self):
        return self.Width

    def getHeight(self):
        return self.Height

    def getOffset(self):
        return self.Offset

    def getLenght(self):
        if self.getFlag()[7] == "1":
            return self.Width * self.Height
        elif self.getFlag()[7] == "2":
            return self.Width * self.Height * 2
        
    def getPaletteSize(self):
        return self.PaletteSize

    def getPaletteOffset(self):
        return self.PaletteOffset

class Header(object):
    def __init__(self,File):
        self.Size = None
        self.Version = None
        self.file = File
        self.readSize()
        self.readVersion()

    def readSize(self):
        i = 3
        size = ""
        while i >= 0:
            size += self.file[i]
            i-=1
        self.Size = int(size.encode("hex"),16)

    def readVersion(self):
        i = 7
        version = ""
        while i >= 4:
            version += self.file[i]
            i-=1
        self.Version = int(version.encode("hex"),16)

    def getSize(self):
        return self.Size

    def getVersion(self):
        return self.Version

class rscFile(object):
    def __init__(self,filename):
        self.filename = filename
        self.file = []

        self.read_rsc()
        self.mHeader = Header(self.file)

    def read_rsc(self):
        bytes_read  = open(self.filename,mode="rb").read()
        for b in bytes_read:
            self.file.append(b)

    #move this to resource
    def readPixelData(self,start,lenght,height,width):
        
        returnData=[]
        for row in xrange(height): returnData += [[0]*width]
        
        i = 0
        h = 0
        w = 0 
        #8bit
        while i < lenght:
            if w == width:
                w = 0
                h +=1
            data = int(self.file[start + i].encode("hex"),16)
            returnData[h][w] = data          
            i +=1
            w +=1
        return returnData

    def readPaletteData(self,start):
        #Colour Information is stored in 2 bytes
        returnData = []
        i = 0
        offsetR = int("7C00",16)
        offsetG = int("3E0",16)
        offsetB = int("1F",16)
        #normaly i <256
        while i < 256:
            data =""
            data += self.file[start +1 + 2*i]
            data += self.file[start + 2*i]
            data2 = int(data.encode("hex"),16)
            
            color = []
            color.append((data2 & offsetR) >> 7)
            color.append((data2 & offsetG) >> 2)
            color.append((data2 & offsetB) << 3)
            
            returnData.append(color)
            i+=1
        return returnData

class idxFile(object):
    def __init__(self,filename):
        self.filename = filename
        self.file = []
        self.Resource = []
        
        self.read_idx()       
        self.mHeader = Header(self.file)         
        self.createResource()

    def read_idx(self):
        bytes_read  = open(self.filename,mode="rb").read()
        for b in bytes_read:
            self.file.append(b)

    def readResourceTyp(self,offset):
        i = 11 + offset
        typ = ""
        while i >=8 + offset:
            typ += self.file[i]
            i-=1
        return typ.encode("hex")

    def readResourceID(self,offset):
        i = 12 + offset
        ID = ""
        while i <=43 + offset:
            ID += self.file[i]
            i+=1
        return ID.strip(' \t\r\n\0')
    
    def createResource(self):
        #Hex Value Description
        #0x64 Image resource (i.e. an embedded bitmap)                      lenght  60 bytes
        #0x65 Sound resource (i.e. an embedded windows .WAV file)                   52 bytes 
        #0x66 Flat file resource (i.e. embedded arbitrary binary content)           44 bytes 
        loop = True
        offset = 0    
        while loop == True:
            typ = self.readResourceTyp(offset)
            if typ == "00000064":
                mImage = Image(self.readResourceID(offset),typ,self.file,offset)
                self.Resource.append(mImage)
                offset += 60
            elif typ =="00000065":
                offset += 52
            elif typ =="00000066":
                offfset += 44
                
            if self.mHeader.getSize() - offset == 0:
                loop = False

class metaFile(object):
    def __init__(self,filename):
        self.filename = filename
        self.mIdxFile = idxFile(filename + ".idx")
        self.mRscFile = rscFile(filename + ".rsc")

        if self.checkVersion() == True:
            self.readData()
        else:
            print "Error, Versions dont match!"

    def checkVersion(self):
        #idx and rsc file version must match
        if self.mIdxFile.mHeader.getVersion() != self.mRscFile.mHeader.getVersion():
            return False
        else:
            return True

    def readData(self):
        for entry in self.mIdxFile.Resource:
            if entry.getTyp() == "00000064":
                if entry.getFlag()[7] == "1":
                    #8bit palett
                    pass
                elif entry.getFlag()[7] == "2":
                    #16bit, no palett
                    pass
                if entry.getFlag()[0] == "4":
                    #first pixel transparency
                    pass
            entry.PaletteData = self.mRscFile.readPaletteData(entry.getPaletteOffset() +8)
            entry.PixelData = self.mRscFile.readPixelData(entry.getOffset() +8, entry.getLenght(),entry.getHeight(),entry.getWidth())
            f = open(entry.getID()+ '.png', 'wb')
            w = png.Writer(entry.getWidth(),entry.getHeight(), palette=entry.PaletteData)
            w.write(f,entry.PixelData)
            f.close()
        
mFile = metaFile("uimainbg")
