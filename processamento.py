import threading
import cv2, numpy as np, os, json
from collections import deque

class processaFrame (threading.Thread):
    def __init__(self, threadID ):
        threading.Thread.__init__(self)
        
        #fila de frames
        self.filaFrame = deque()

        #contornos
        self.contornos = None
        
        #contante que define o encerramento das treads
        self.closeAll = True

        #gera Algoritmo de segmentação de fundo / primeiro plano baseado em mistura gaussiana.
        self.subtracao = cv2.bgsegm.createBackgroundSubtractorMOG()
        
        #cria uma matriz 5x5 onde o formato de 0 e 1 forma uma elipse
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    def run(self):
        while self.closeAll:
            if not self.isEmpty():
                frame = self.OperacoesMorfologicas(self.filaFrame.popleft())
                contorno, h = cv2.findContours(frame,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                self.setContornos(contorno)
                
        print("Thread finalizada")
        pass

    def isEmpty(self):
        
        if(len(self.filaFrame) <= 0):
            return True
        return False

    def OperacoesMorfologicas(self, frame):
        #transforma em escala de cinza
        grey = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        
        #aplica o filtro gaussiano para suavizar a imagem e remover ruidos
        blur = cv2.GaussianBlur(grey,(3,3),5)
        
        #aplica o algoritmo de segmentaçãoa imagem retornada do filtro gaussian
        img_sub = self.subtracao.apply(blur)
        
        #preenche imperfeições realizada 2X preenchendo espaços vazios
        dilatada = cv2.morphologyEx (img_sub, cv2.MORPH_CLOSE , self.kernel)
        dilatada = cv2.morphologyEx (dilatada, cv2.MORPH_CLOSE , self.kernel)
        
        #remove imperfeições na imagem
        dilat = cv2.dilate(dilatada, self.kernel) #np.ones((5,5))
        retvalbin, bins = cv2.threshold(dilat, 220, 255, cv2.THRESH_BINARY)  # removes the shadows
        return bins
    
    def incluirFrame(self, frame):
        self.filaFrame.append(frame)
        pass

    def setContornos(self, contornos):
        self.contornos = contornos
        pass

    def getContornos(self):
        return self.contornos
