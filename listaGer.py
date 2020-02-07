from similariedade import similariedade as sm
import json

class veiculos:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visitas = 0
        self.detectado = True
        self.listContado = []
    
    def adicionarContado(self,id):
        self.listContado.append(id)

    def checkContadoPor(self, id):
        for lista in self.listContado:
            if(lista == id ):
               return False
            pass
        return True


    def checkVeiculo(self, x, y, limiar):
        if(sm.dist_cosseno([self.x, self.y],[x,y]) >= limiar):
            self.visitas = 0
            self.detectado = True
            self.x = x
            self.y = y
            return True
        else:
            return False

    def checkDetectado(self):
        return self.detectado

    def checkStatus(self):
        if(not(self.detectado)):
            self.visitas += 1
        else:
            self.detectado = False
            pass
        pass

    def getVisitas(self):
        return self.visitas



class deteccoes:
    _instance = None
    linhas = []
    carros = []
    _limiar = 0.74
    _inative = 3
    _offset=10 #Erro permitido entre pixel
    detectado = (0,127,255)
    nao_detectado = (255,127,0)

    def __init__(self):
        self.some_attribute = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def conferePassLine(self):
        infos = []
        for i, obj in enumerate(self.linhas):
            line = {}
            line['id'] = obj['id']
            line['det'] = self.nao_detectado
            for j, obj2 in enumerate(self.carros):
                if((obj2.x >= obj['eixoX'][0]) and (obj2.x <= obj['eixoX'][1]) and (obj2.y >= (obj['eixoY'][0]-self._offset)) and (obj2.y <= (obj['eixoY'][1]+-self._offset))):
                    if obj2.checkContadoPor(obj['id']):
                        self.carros[j].adicionarContado(obj['id'])
                        self.linhas[i]['carros'] += 1
                        line['det'] = self.detectado
                        pass
                    pass
                pass
            line['qtd'] = self.linhas[i]['carros']
            line['eixoX'] = self.linhas[i]['eixoX']
            line['eixoY'] = self.linhas[i]['eixoY']
            infos.append(line)
            pass
        return json.dumps(infos)


    def confecionaListaDados(self):
        pass

    def novaLinha(self, id, orientacao, x0, x1, y0, y1, descricao = ''):
        linha = {
            'id':id,
            'orientacao': orientacao,
            'eixoX':[x0,x1],
            'eixoY':[y0, y1],
            'desc': descricao,
            'carros':0,
            'vazao': 0
        }
        self.linhas.append(linha)
        
    def getAllLinhas(self):
        return json.dumps(self.linhas)

    def getLinhaById(self, id):
        indice = -1
        for i, obj in enumerate(self.listas):
            if(obj['id'] == id):
                indice = id
            pass
        if(indice != -1):
            return json.dumps(self.linhas[indice])
        else:
            return json.dump({'erro':'Nenhum item corresponde a esse id'})

    def removeLinhaById(self, id):
        indice = -1
        for i, obj in enumerate(self.listas):
            if(obj['id'] == id):
                indice = id
            pass
        if(indice != -1):
            self.linhas.pop(indice)
            return json.dump({'sucesso':'O item correspondente a esse id foi excluido'})
        else:
            return json.dump({'erro':'Nenhum item corresponde a esse id'})


    def novoCarro(self, x, y):
        if(len(self.carros) > 0):
            if(not self.checkCarro(x,y)):
                self.carros.append(veiculos(x=x,y=y))
        else:
            self.carros.append(veiculos(x=x,y=y))

        for i, obj in enumerate(self.carros):
            obj.checkStatus()

    def checkCarro(self, x, y):
        for i, obj in enumerate(self.carros):
            if(not obj.checkDetectado):
                if(obj.checkVeiculo(x,y, self._limiar)):
                    return True
                pass
            pass
        return False

    def removeInativos(self):
        inatives = []
        for i, obj in enumerate(self.carros):
            if(obj.getVisitas() > self._inative):
                inatives.append(obj)
                pass
            pass
        for ina in inatives:
            self.carros.remove(ina)
            pass
        pass




