#coding: iso-8859-1 -*-
import cv2, numpy as np, os, json
from time import sleep
from listaGer import deteccoes as dt
from processamento import processaFrame
from datetime import datetime
from uuid import uuid4



#valores minimo para detecção
largura_min=40 #Largura minima do retangulo
altura_min=40 #Altura minima do retangulo

#pos_linha= 550 #Posição da linha de contagem 
dir_atual = os.getcwd()
ENDERECO_VIDEO = dir_atual+os.sep+"filmagens"+os.sep+"film04.mp4"
LARGURA = 1000
ALTURA = 600
resize = (LARGURA,ALTURA)
offset=6 #Erro permitido entre pixel  

deteccoes = dt.instance()
cap = cv2.VideoCapture(ENDERECO_VIDEO)
delay= int(cap.get(cv2.CAP_PROP_FPS))

#contantes temporarias
detec = []
carros = 0
linhas = []

def newId():
    return datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())

def novaLinha(id, orientacao, x0,x1, y0,y1, descricao = ''):
    linhas.append(id)
    deteccoes.novaLinha(id, orientacao, x0,x1,y0,y1, descricao)

def pega_centro(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy

#função que desenha a escala de referencia na imagem
def drawEscala(image):
    image[0:600, 0:2] = (0, 0, 255)
    image[0:2, 0:1000] = (0, 0, 255)
    fonte = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
    escala = 0.5
    grossura = 2
    for n in range(0, 6):
        texto1 = '- {}'.format(n*100)
        cv2.putText(image, texto1, (1, n*100), fonte, escala, (0, 0, 255), grossura)
    pass
    for n in range(0, 10):
        # Desenha o texto com a variavel em preto, no centro
        texto2 = '| {}'.format(n*100)
        tamanho, _ = cv2.getTextSize(texto2, fonte, escala, grossura)
        cv2.putText(image, texto2, (n*100, 5+tamanho[1]), fonte, escala, (0, 0, 255), grossura)
    pass
    return image

#gera Algoritmo de segmentação de fundo / primeiro plano baseado em mistura gaussiana.
#subtracao = cv2.bgsegm.createBackgroundSubtractorMOG()
processamento_frames = processaFrame(newId())
processamento_frames.start()
#gera as linhas
novaLinha(newId(),'h',380,620,550,550, 'Fim da Rua principal')
novaLinha(newId(),'h',585,730,510,510, 'cruzamento a esquerda')
novaLinha(newId(),'h',510,720,350,350, 'subindo a rua principal')

contador = 0
intervalo = 3

while True:
    ret , frame1 = cap.read()
    #redimensiona a imagem
    frame1 = cv2.resize(frame1, resize)

    #mantem um intervalo de tempo, para o video não ultrapassar a leitura
    tempo = float(1/(delay))
    sleep(tempo)
    
    if(contador >= intervalo):
        processamento_frames.incluirFrame(frame1)
        contador = 0
 
    contorno = processamento_frames.getContornos()

    #desenha as linhas de contagem
    lin = json.loads(deteccoes.getAllLinhas())
    for ll in lin:
        cv2.line(frame1, (ll['eixoX'][0],ll['eixoY'][0]), (ll['eixoX'][1], ll['eixoY'][1]), (255,127,0), 3)
    
    if contorno is not None:
        for(i,c) in enumerate(contorno):
            (x,y,w,h) = cv2.boundingRect(c)
            validar_contorno = (w >= largura_min) and (h >= altura_min)
            if not validar_contorno:
                continue

            cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)        
            centro = pega_centro(x, y, w, h)
            cv2.circle(frame1, centro, 4, (0, 0,255), -1)
        
            #mover a deteção para a gerList incluir o id da linha como flag e utilizar da similariedade para não duplicar detecções
            deteccoes.novoCarro(centro[0],centro[1])
            
    novo = json.loads(deteccoes.conferePassLine())
    for nv in novo:
        cv2.line(frame1, (nv['eixoX'][0],nv['eixoY'][0]), (nv['eixoX'][1], nv['eixoY'][1]), nv['det'], 3)
        cv2.putText(frame1, "VEICULOS: "+str(nv['qtd']), (nv['eixoX'][0], nv['eixoY'][0]+20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),3)
    deteccoes.removeInativos()
    
    #visualizar o frame redimensionado
    cv2.imshow("Video Original" , drawEscala(frame1))
    #cv2.imshow("Detectar",cv2.resize(dilatada, (400,300)))
    contador = contador + 1
    if cv2.waitKey(1) == 27:
        break
    
cv2.destroyAllWindows()
cap.release()