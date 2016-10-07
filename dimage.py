# -*- coding: utf-8 -*-

"""
Leitura e gerenciamento de imagens DMC no Padrão ELITE

Exemplo de utilização::
    
    # Inicialização através de um arquivo txt (mais rápida)
    img1 = DMCImg(bmp = '001.bmp')
    
    # Inicialização atravé de um arquivo BMP
    img2 = DMCImg(txt = '002.txt')

    # Gravar imagem num arquivo txt
    img1.write_txt('001.txt')

    # Pegar array de bytes para gravar na memoria
    dump = img1.get_buffer()

"""

import sys
#from PIL import Image

class DanImg():
    """
    Classe para criação e leitura de arquivos de imagens no padrão ELITE

    Inicialize esse objeto com uma imagem BMP ou com um arquivo TXT

    """

    __IMAGE_COMPRESSION_NONE = 0
    __IMAGE_COMPRESSION_RLE_WITH_PALLET = 1
    __IMAGE_COMPRESSION_RLE_WITHOUT_PALLET = 2


    def __init__(self,txt=None,bmp=None):
        """
        Inicia uma imagem a partir de um arquivo BMP 
        """
        if bmp != None:
            self.__read_bmp(bmp)
        else:
            raise Exception("No input defined")

    def __read_bmp(self,fname_bmp):
        """
        Lê um arquivo de imagem a partir de um BMP e inicializa o objeto
        """
        self.pix = self.__bmp2pixmap(fname_bmp)
        self.pix24 = [map(lambda a: a[0]*256*256+a[1]*256+a[2], line) for line in self.pix]
        self.pm16 = self.__pixmap16(self.pix)           
        
        
    def rec_bmp_from_pix(self,name):
        figh = self.save_header
        fig = "".join(["".join(["".join(map(lambda a: chr(a) if a<=255 else chr(255),pixel)) for pixel in line]) for line in self.pix])
        with open(name,'wb') as f_bmp:
            f_bmp.write(figh+fig)
        
    def pix_from_pix24(self,pix24):
        self.pix24=pix24
        self.pix = [[[pix/256/256&0xFF, pix/256&(0xFF), pix&(0xFF)] for pix in line] for line in pix24]
            
    def __pixmap16(self,pixmap):
        """
        Faz leitura do mapa de pixel (3 bytes de cores RGB) e transforma em um mapa de 16 bits (padrão ELITE)
        """
        pix_map16 = []
        for line in pixmap:
            for rgb in line[::-1]:#lines are inverted
                cl16 = (rgb[2]&0xF8)*2**8 + (rgb[1]&0xFC)*2**3 + (rgb[0]&0xF8)/2**3#colors are inverted
                pix_map16.append(cl16)

        pix_map16 = pix_map16[::-1] # pixels are inverted
        #print "data: ", color_changes, len(colors_array)

        # length0 = 2*width*height
        # length1 = len(colors_array)*2 + color_changes*2
        # length2 = color_changes*3
        
        # self.length = min([length0,length1,length2])

        # if self.length == length0:
        #     self.compression = self.__IMAGE_COMPRESSION_NONE
        # elif self.length == length1:
        #     self.compression = self.__IMAGE_COMPRESSION_RLE_WITH_PALLET
        # elif self.length == length2:
        #     self.compression = self.__IMAGE_COMPRESSION_RLE_WITHOUT_PALLET

        self.pixmap16 = pix_map16
        return self.pixmap16
        #print length0,length1,length2

    def __bmp2pixmap(self,fname_bmp):
        """
        Faz leitura do arquivo BMP, inicializa as variaveis de tamanho do objeto e faz um pixmap RGB de 3 bytes da imagem
        """
        with open(fname_bmp,'rb') as f_bmp:
            bytes_map = f_bmp.read()
            header = [ord(b) for b in bytes_map[0:14]]
            self.header = header
            # print chr(header[0]),chr(header[1])
            # for b in header[2:]:
            #     print b,

            # print ""
            off_set = header[13]*256*256*256+header[12]*256*256+header[11]*256+header[10]
            size = header[5]*256*256*256+header[4]*256*256+header[3]*256+header[2]
            dip_header = [ord(b) for b in bytes_map[14:off_set]]
            width, height = dip_header[7]*256*256*256+dip_header[6]*256*256+dip_header[5]*256+dip_header[4],\
                            dip_header[11]*256*256*256+dip_header[10]*256*256+dip_header[9]*256+dip_header[8] 

            print off_set, width, height, size, width*height, size/(width*height)
            self.save_header = bytes_map[:off_set]
            pixby = bytes_map[off_set:]

            pix = []
            offset_pad = 0
            for l in range(0,height):
                pix.append([map(ord,pixby[l*width*3+offset_pad+i*3:l*width*3+offset_pad+i*3+3]) for i in range(0,width)])
                pad = (4-((width*3)%4))
                offset_pad += pad if pad < 4 else 0

            self.width = width
            self.height = height

        return pix



    def __count_colors(self,pm16):
        colors_array = []
        for cl16 in pm16:
            if cl16 not in colors_array:
                colors_array.append(cl16)
        # self.n_colors = len(colors_array)
        return len(colors_array)
