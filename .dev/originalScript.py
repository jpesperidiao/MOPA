## IMPORTACOES

# importacoes bloco de funcionamento geral
import urllib as req
import zipfile
import os
from osgeo import gdal

# importacoes bloco de solucao
import numpy as np
from osgeo import gdal
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# importacoes do bloco de testes
import math
import time
import os		
		
## BLOCO DE SOLUCAO

## definicao de regiao possivel de posicionamento do atirador (todos os quadrantes)
def defRegInteresse2(posRec, dataset, resolEspacial, distMaxDisparo=1000.0):
    
    gt = dataset.GetGeoTransform()
    elevation = dataset.ReadAsArray()
    limiteDisparo = int((distMaxDisparo / resolEspacial)) # para limitar por regiao de real possibilidade de disparo
    xMax = len(elevation)
    yMax = len(elevation[0])
    
    # converter coordenadas de campo para pixel
    denominador = 1. / (gt[1] * gt[5] - gt[2] * gt[4])
    px = int((gt[5] * (posRec[0] - gt[0]) - gt[2] * (posRec[1] - gt[3])) * denominador - 0.5)
    py = int(-(gt[4] * (posRec[0] - gt[0]) - gt[1] * (posRec[1] - gt[3])) * denominador - 0.5)
    
    (xMin, xMax, yMin, yMax) = (max(0, px - limiteDisparo), min(xMax, px + limiteDisparo), 
                                max(0, py - limiteDisparo), min(yMax, py + limiteDisparo))
    
    return (int(xMin), int(xMax), int(yMin),int(yMax))

## coordenadas (Long, Lat) da regiao possivel
def coordPossivel(dataset, height, width, hmin=0, wmin=0): #funcionando - testada em 06/06/2016
    coordPoss = np.zeros(((width-wmin)*(height-hmin),4))
    gt = dataset.GetGeoTransform()
    k=0
    for j in range(wmin,width):
        for i in range(hmin,height):
            (coordPoss[k,0], coordPoss[k,1], coordPoss[k,2], coordPoss[k,3]) = (gt[0] + j*gt[1] + i*gt[2], \
                                                                                gt[3] + j*gt[4] + i*gt[5], \
                                                                                j, i)
            k = k+1
    return coordPoss #saida e um vetor de coordenadas x,y > (X[],Y[]) e colunas e linhas originais

## retorna as alturas das coordenadas da area de interesse pelo metodo ANALITICO
def reta(posRec, vetDir, XY, dataset, tolReta = 0.5): #funcionando - testada em 04/07/16
    # obs.: para a solucao do problema, o algoritmo obteve melhor rendimento com eixos unitarizados!
    (Zen, Az) = np.array((vetDir[0],vetDir[1])) * np.pi / 180
    versorDir = np.array([np.sin(Zen) * np.cos(Az), np.sin(Zen) * np.sin(Az), np.cos(Zen)])
    gt = dataset.GetGeoTransform()
    elevation = dataset.ReadAsArray()
    
    maxX = max(abs(gt[0]), abs(gt[0] + len(elevation)*gt[1] + len(elevation[0])*gt[2]))
    maxX = maxX * (gt[0] / abs(gt[0]))
    maxY = max(abs(gt[3]), abs(gt[3] + len(elevation)*gt[4] + len(elevation[0])*gt[5]))
    maxY = maxY * (gt[3] / abs(gt[3]))
    maxZ = abs(elevation.max())
    
    vetMaximos = np.array((maxX, maxY, maxZ))
    
    # os 3 eixos devem ser unitarizados a fim de nao depender de escala / sistema de coordenadas adotado / unidades
    
    posRecUnitarizado = posRec / vetMaximos
    xyUnitarizado = np.array((XY[:,0] / maxX, XY[:,1] / maxY)).transpose()
    
    possHght = np.zeros((len(XY[1:])+1))
    for i in range(0,len(XY[1:])+1):
        if versorDir[0] <> np.float64(0) and versorDir[1] <> np.float64(0): #solucionando o problema de vetor diretor com coordenada 0 
            tx = (xyUnitarizado[i,0]-posRecUnitarizado[0]) / versorDir[0]
            ty = (xyUnitarizado[i,1]-posRecUnitarizado[1]) / versorDir[1]
            t = (tx+ty)/2
            if abs(tx - t) > tolReta:
                t = "null"
                
        if versorDir[0] == 0 and versorDir[1] <> 0:
            t = (xyUnitarizado[i,1] - posRecUnitarizado[1]) / versorDir[1]
            
        if versorDir[0] <> 0 and versorDir[1] == 0:
            t = (xyUnitarizado[i,0] - posRecUnitarizado[0]) / versorDir[0]
        if t <> "null": # condicao para se restringir o universo de pontos possiveis
            possHght[i] = (posRecUnitarizado[2] + t * versorDir[2]) * maxZ
        else:
            possHght[i] = 10000.0 # ponto mais alto da Terra tem 8800m
        
    return possHght

## retorna as coordenadas dos pontos possiveis pelo metodo MOPA-ANALITICO
def posAtirador(posRec, vetDir, dataset, resolEspacial = 90, distMaxDisparo=1000.0, tolAltAtir=0.5):
    
    elevation = dataset.ReadAsArray()
    iniXInteresse, fimXInteresse, iniYInteresse, fimYInteresse = defRegInteresse2(posRec, dataset, resolEspacial,\
                                                                                 distMaxDisparo)
    regPoss = coordPossivel(dataset, fimYInteresse, fimXInteresse, iniYInteresse, iniXInteresse)
    areInt = elevation[iniXInteresse:fimXInteresse, iniYInteresse:fimYInteresse]
    matrizAltPoss = np.reshape(reta(posRec, vetDir, regPoss, dataset), (fimXInteresse - iniXInteresse, \
                                                                        fimYInteresse - iniYInteresse))
    posAtir = []
    for i in range(0, fimXInteresse - iniXInteresse):
        for j in range(0, fimYInteresse - iniYInteresse):
            temp = prmtsPx2Coord(i + iniXInteresse, j + iniYInteresse, dataset)
            if ((abs(matrizAltPoss[i,j] - areInt[i,j]) < tolAltAtir)) and (temp[0],temp[1]) <> (posRec[0],posRec[1]): # ignorar pos. rec.
                posAtir.append((i + iniXInteresse, j + iniYInteresse, temp[0], temp[1], matrizAltPoss[i, j], areInt[i,j]))
    posAtir = np.array(posAtir)
    return posAtir  # retorna as posicoes na matriza original (col,lin) e (Long,Lat,Alt) e altura do ponto sobre o terreno

## reta ajustada pelo metodo de Helmert
def planeAdjustHelmert(posRec, vetDir, XY, dataset, expScale=75, nPontos=150): # funcionando - atualizada em 30/07/16
    # obs.: para a solucao do problema, o algoritmo obteve melhor rendimento com eixos unitarizados!
    
    gt = dataset.GetGeoTransform()
    elevation = dataset.ReadAsArray()

    maxX = max(abs(gt[0]), abs(gt[0] + len(elevation)*gt[1] + len(elevation[0])*gt[2]))
    maxX = maxX * (gt[0] / abs(gt[0]))
    maxY = max(abs(gt[3]), abs(gt[3] + len(elevation)*gt[4] + len(elevation[0])*gt[5]))
    maxY = maxY * (gt[3] / abs(gt[3]))
    maxZ = abs(elevation.max())
    
    vetMaximos = np.array((maxX, maxY, maxZ))
    
    # os 3 eixos devem ser unitarizados a fim de nao depender de escala / sistema de coordenadas adotado
    posRecUnitarizado = posRec / vetMaximos

    # ajustamento de pontos a reta
    (Zen, Az) = np.array((vetDir[0],vetDir[1])) * np.pi / 180
    versDir = np.array([np.sin(Zen) * np.cos(Az), np.sin(Zen) * np.sin(Az), np.cos(Zen)])
    
    # criar vetor de observacoes
    t = np.random.exponential(expScale,nPontos)
    pontos = []
    for i in range(0,nPontos):
        pontos.append([(posRecUnitarizado + t[i]*versDir)[0], (posRecUnitarizado + t[i]*versDir)[1], \
                       (posRecUnitarizado + t[i]*versDir)[2], 1])
    pontos = np.array(pontos)
    
    # identificando matrizes do sistema AX = B com retricoes definidas pela matriz de coeficientes C
    A = np.array([pontos[:,0], pontos[:,1], pontos[:,3]]).transpose()
    B = np.array(pontos[:,2], posRecUnitarizado[2])
    C = np.array([posRecUnitarizado[0], posRecUnitarizado[1], 1])
    
    w = np.zeros((nPontos,nPontos)) # definindo matriz peso assumindo variancias iguais de 0.04 m
    
    #variancia = 1/(.004**2)
    np.fill_diagonal(w,1/(.04**2))
    
    H = A.transpose().dot(w).dot(B)
    H = [H[0], H[1], H[2], posRecUnitarizado[2]]
    
    A = A.transpose().dot(w).dot(A)
    M=[]
    for i in range (0,3):
        M.append([A[i,0], A[i,1], A[i,2], C[i]])
    M.append([C[0], C[1], C[2], 0])
    M = np.array(M)
    
    coef = np.linalg.solve(M,H) # os 3 primeiros argumentos sao (a,b,c) - Z = aX + bY + c
    #return [coef[0], coef[1], coef[2]]
    
    # calculo das possiveis alturas dos pontos
    possHgt = ( coef[0]*(XY[:, 0] / maxX) + coef[1]*(XY[:, 1] / maxY) + coef[2] ) * maxZ
    return possHgt

## retorna as coordenadas dos pontos possiveis pelo metodo MOPA-HELMERT
def posAtirador2(posRec, vetDir, dataset, resolEspacial, distMaxDisparo=1000.0, tolAltAtir=0.5):
    
    elevation = dataset.ReadAsArray()
    iniXInteresse, fimXInteresse, iniYInteresse, fimYInteresse = defRegInteresse2(posRec, dataset, resolEspacial,\
                                                                                 distMaxDisparo)
    regPoss = coordPossivel(dataset, fimYInteresse, fimXInteresse, iniYInteresse, iniXInteresse)
    areInt = elevation[iniXInteresse:fimXInteresse, iniYInteresse:fimYInteresse]
    matrizAltPoss = np.reshape(planeAdjustHelmert(posRec,vetDir, regPoss, dataset), (fimXInteresse - iniXInteresse, \
                                                                                     fimYInteresse - iniYInteresse))
    posAtir = []
    for i in range(0, fimXInteresse - iniXInteresse):
        for j in range(0, fimYInteresse - iniYInteresse):
            temp = prmtsPx2Coord(i + iniXInteresse, j + iniYInteresse, dataset)
            if ((abs(matrizAltPoss[i,j] - areInt[i,j]) < tolAltAtir)) and (temp[0],temp[1]) <> (posRec[0],posRec[1]): # ignorar pos. rec.
                posAtir.append((i + iniXInteresse, j + iniYInteresse, temp[0], temp[1], matrizAltPoss[i, j], areInt[i,j]))
    posAtir = np.array(posAtir)
    return posAtir  # retorna as posicoes na matriza original (col,lin) e (Long,Lat,Alt) e altura do ponto sobre o terreno

# filtrar a lista de pontos possiveis por meio de restricao aos angulos azimutais e zenitais dos pontos    
def filtrarSolucoes(posRec, vetDir, vetPosAtir, dataset, tolZen = 1.5, tolAz = 1.5): # funcionando - testada em 10/08/2016
    
    (Zen, Az) = vetDir[0], vetDir[1]
    gt = dataset.GetGeoTransform()
    elevation = dataset.ReadAsArray()
    
    try:
        versores = vetPosAtir[:,2:5] - posRec
    except:
        versores = vetPosAtir[2:5] - posRec
    
    # normalizacao dos eixos
    v_norm = (np.multiply(versores, versores))
    
    try:
        v_norm = np.sqrt(v_norm[:,0] + v_norm[:,1] + v_norm[:,2])
    except:
        v_norm = np.sqrt(v_norm[0] + v_norm[1] + v_norm[2])
        
    versores = np.divide(versores.transpose(), v_norm).transpose()

    # calculo de raio em plano xy
    v_norm = np.multiply(versores, versores)
    try:
        r_xy = np.sqrt(v_norm[:,0] + v_norm[:,1])

        pntsFiltrados = []
        # aplicando restricao de angulos aos angulos de cada ponto gerado
        for i in range(0,len(versores)):
            zentemp = math.atan2(r_xy[i], versores[i,2])*180/np.pi
            aztemp = math.atan2(versores[i,1], versores[i,0])*180/np.pi
            if abs(zentemp - Zen) <= tolZen and abs(aztemp - Az) <= tolAz:
                pntsFiltrados.append(vetPosAtir[i])
            elif abs(abs(zentemp - Zen) - 180) <= tolZen and abs(abs(aztemp - Az) - 180) <= tolAz:
                pntsFiltrados.append(vetPosAtir[i])
    except:
        r_xy = np.sqrt(v_norm[0] + v_norm[1])

        zentemp = math.atan2(r_xy, versores[2])*180/np.pi
        aztemp = math.atan2(versores[1], versores[0])*180/np.pi
        if abs(zentemp - Zen) <= tolZen and abs(aztemp - Az) <= tolAz:
            pntsFiltrados.append(vetPosAtir)
        elif abs(abs(zentemp - Zen) - 180) <= tolZen and abs(abs(aztemp - Az) - 180) <= tolAz:
            pntsFiltrados.append(vetPosAtir)

    return np.array(pntsFiltrados)



	
## BLOCO DO RELATORIO

# Recupera o nome do arquivo, sem o diretorio
def getFileName(arq):
    if '/' in arq or '\\' in arq:
        i = -1
        while i >= -len(arq):
            if arq[i] in ('\\/'):
                break
            else:
                i = i - 1
        return arq[len(arq)+1+i:]
    else:
        return arq
    
# Funcao que calcula a distacia entre dois pontos dados no terreno (coordenadas de terreno - e.g.: (Long,Lat,ALt))
def distanciaPlan(p1, p2, dataset, resolEspacial):
    gt = dataset.GetGeoTransform()
    temp = ((p1 - p2) / np.array((gt[1], gt[5], 1))) ** 2
    try:
        temp = np.sqrt(temp[:, 1] + temp[:, 0]) * resolEspacial
    except:
        temp = np.sqrt(temp[1] + temp[0]) * resolEspacial
    return np.array(temp)

# Funcao para retornar os angulos horizontais e verticais para cada ponto do vetor solucao 
def angulosPntsCalculados(vetPosAtir, posRec, dataset):
    gt = dataset.GetGeoTransform()
    elevation = dataset.ReadAsArray()
    
    try:
        versores = vetPosAtir[:,2:5] - posRec
    except:
        versores = vetPosAtir[2:5] - posRec
    
    # normalizacao dos eixos
    v_norm = (np.multiply(versores, versores))
    try:
        v_norm = np.sqrt(v_norm[:,0] + v_norm[:,1] + v_norm[:,2])
    except:
        v_norm = np.sqrt(v_norm[0] + v_norm[1] + v_norm[2])
        
    versores = np.divide(versores.transpose(), v_norm).transpose()

    # calculo de raio em plano xy
    v_norm = np.multiply(versores, versores)
    try:
        r_xy = np.sqrt(v_norm[:,0] + v_norm[:,1])

        angsZen = []
        angsAz = []
        for i in range(0, len(versores)):
            tempZen = np.arctan2(r_xy[i], versores[i,2])*180/np.pi
            tempAz = np.arctan2(versores[i,1], versores[i,0])*180/np.pi      
            angsZen.append(tempZen)
            angsAz.append(tempAz)
    except:
        r_xy = np.sqrt(v_norm[0] + v_norm[1])

        angsZen = np.arctan2(r_xy, versores[2])*180/np.pi
        angsAz = np.arctan2(versores[1], versores[0])*180/np.pi
        
    return np.array(angsZen), np.array(angsAz)

def resultadosFinais(arq, colLinRecpt, anglesRealUnit, tolAltitude, resolEspacial, distMaxDisparo, tolZen, tolAz, plot=False):
    
    [colRec,linRec] = colLinRecpt
    [Zen, Az, zenUnit, azUnit] = anglesRealUnit
    dataset = gdal.Open(arq)
    elevation = dataset.ReadAsArray()
    posRec = np.array((prmtsPx2Coord(colRec,linRec,dataset)[0],\
                       prmtsPx2Coord(colRec,linRec,dataset)[1],elevation[colRec,linRec]))
    vetDir = np.array([Zen, Az])
    vetDirUnit = np.array((zenUnit, azUnit))
    gt = dataset.GetGeoTransform()
    maximos = np.array((gt[0] + len(elevation) * gt[1] + len(elevation[0]) * gt[2], \
                    gt[3] + len(elevation) * gt[4] + len(elevation[0]) * gt[5], elevation.max()))


    # definicao da regiao de interesse
    (iniXInteresse, fimXInteresse, iniYInteresse, fimYInteresse) = defRegInteresse2(posRec, dataset, resolEspacial,\
                                                                                 distMaxDisparo)

    # determinacao de possiveis posicoes
    iniHel = time.time()
    vetHel = posAtirador2(posRec, vetDirUnit, dataset, resolEspacial, distMaxDisparo, tolAltitude)
    fimHel = time.time() - iniHel

    iniAna = time.time()
    vetAna = posAtirador(posRec, vetDirUnit, dataset, resolEspacial, distMaxDisparo, tolAltitude)
    fimAna = time.time() - iniAna

    # bool para checar se os metodos retornaram algum ponto
    mopaHel = len(vetHel) <> 0
    mopaAna = len(vetAna) <> 0
    
    # determinando as distancias dos pontos encontrados ao ponto simulado, dist. min. e nr. de pnts de cada solucao
    if mopaHel:
        distRecHel = distanciaPlan(vetHel[:,2:5], posRec, dataset, resolEspacial)
        distMinHel = distRecHel.min()
        nrPntsHel = len(distRecHel)
        for i in range(0, nrPntsHel):
            if (distRecHel[i] == distMinHel):
                pntMaisProx_Hel = vetHel[i]
                break
        zenHel, azHel = angulosPntsCalculados(vetHel, posRec, dataset)
        resultHel = np.array([vetHel[:,2], vetHel[:,3], vetHel[:,4], vetHel[:,4] - vetHel[:,5], zenHel - Zen,\
                          azHel - Az, distRecHel]).transpose()
        
        # filtrar a solucao de Helmert
        iniHelFilt = time.time()
        helmFilt = filtrarSolucoes(posRec, vetDir, vetHel, dataset, tolZen, tolAz)
        fimHelFilt = time.time() - iniHelFilt
    else:
        distRecHel = None
        distMinHel = None
        nrPntsHel = None
        pntMaisProx_Hel = None
        resultHel = None
        
        # nao ha filtro a ser realizado
        helmFilt = None
        fimHelFilt = None
        print 'MOPA-Helmert nao obteve solucoes.\n'

    if mopaAna:
        distRecAna = distanciaPlan(vetAna[:,2:5], posRec, dataset, resolEspacial)
        distMinAna = distRecAna.min()
        nrPntsAna = len(distRecAna)        
        for i in range(0, nrPntsAna):
            if (distRecAna[i] == distMinAna):
                pntMaisProx_Ana = vetAna[i]
                break
        zenAna, azAna = angulosPntsCalculados(vetAna, posRec, dataset)
        resultAna = np.array([vetAna[:,2], vetAna[:,3], vetAna[:,4], vetAna[:,4] - vetAna[:,5], zenAna - Zen,\
                          azAna - Az, distRecAna]).transpose()
        
        # filtrar a solucao Analitica
        iniAnaFilt = time.time()
        anaFilt = filtrarSolucoes(posRec, vetDir, vetAna, dataset, tolZen, tolAz)
        fimAnaFilt = time.time() - iniAnaFilt
    else:
        distRecAna = None
        distMinAna = None
        nrPntsAna = None
        pntMaisProx_Ana = None
        resultAna = None
        
        # nao ha filtro a ser realizado
        anaFilt = None
        fimAnaFilt = None
        print 'MOPA-Analitico nao obteve solucoes.\n'    

    # bool para checar se o filtro foi efetivo
    filtroHel =  helmFilt is not None and len(helmFilt) <> 0
    filtroAna = anaFilt is not None and len(anaFilt) <> 0
    
    # determinar os residuos para os pontos filtrados
    if filtroHel:
        distRecHelFilt = distanciaPlan(helmFilt[:,2:5], posRec, dataset, resolEspacial)
        distMinHelFilt = distRecHelFilt.min()
        nrPntsHelFilt = len(distRecHelFilt)        
        for i in range(0, nrPntsHelFilt):
            if (distRecHelFilt[i] == distMinHelFilt):
                pntMaisProx_HelFilt = helmFilt[i]
                break
        zenHelFilt, azHelFilt = angulosPntsCalculados(helmFilt, posRec, dataset)
        resultHelFilt = np.array([helmFilt[:,2], helmFilt[:,3], helmFilt[:,4], helmFilt[:,4] - helmFilt[:,5], \
                                  zenHelFilt - Zen, azHelFilt - Az, distRecHelFilt]).transpose()
    else:
        residuoHelFilt = None
        distMinHelFilt = None
        nrPntsHelFilt = None
        pntMaisProx_HelFilt = None
        resultHelFilt = None
        print '\nFiltro para MOPA-Helmert nao reduziu o numero de pontos.\n'

    if filtroAna:
        distRecAnaFilt = distanciaPlan(anaFilt[:,2:5], posRec, dataset, resolEspacial)
        distMinAnaFilt = distRecAnaFilt.min()
        nrPntsAnaFilt = len(distRecAnaFilt)
        zenAnaFilt, azAnaFilt = angulosPntsCalculados(anaFilt, posRec, dataset)
        for i in range(0, nrPntsAnaFilt):
            if (distRecAnaFilt[i] == distMinAnaFilt):
                pntMaisProx_AnaFilt = anaFilt[i]
                break
        resultAnaFilt = np.array([anaFilt[:,2], anaFilt[:,3], anaFilt[:,4], anaFilt[:,4] - anaFilt[:,5], \
                                  zenAnaFilt - Zen, azAnaFilt - Az, distRecAnaFilt]).transpose()
    else:
        distRecAnaFilt = None
        distMinAnaFilt = None
        nrPntsAnaFilt = None
        pntMaisProx_AnaFilt = None
        resultAnaFilt = None
        print '\nFiltro para MOPA-Analitico nao reduziu o numero de pontos.\n'
   
    # para entrar na funcao de relatorio
    resultados = [resultHel, resultHelFilt, resultAna, resultAnaFilt]
    distMin = [distMinHel, distMinHelFilt, distMinAna, distMinAnaFilt]
    pntMaisProx = [pntMaisProx_Hel, pntMaisProx_HelFilt, pntMaisProx_Ana, pntMaisProx_AnaFilt]
    tempExec = [fimHel, fimHelFilt, fimAna, fimAnaFilt]
    nrPnts = [nrPntsHel, nrPntsHelFilt, nrPntsAna, nrPntsAnaFilt]
    entrada = [colRec, linRec, Zen, Az, zenUnit, azUnit, resolEspacial, tolAltitude, tolZen, tolAz]
    
    if not mopaHel and not mopaAna:
        gerarRelatorio(arq, entrada, [None, None, None, None], distMin, pntMaisProx, tempExec, nrPnts)
        return False
    else:
        # gerar o relatorio final
        gerarRelatorioFinal(arq, entrada, resultados, distMin, pntMaisProx, tempExec, nrPnts)
        
        imprimirSolucoes(vetHel, 'MOPA-Helmert')
        imprimirSolucoes(helmFilt, 'MOPA-Helmert Filtrado')
        imprimirSolucoes(vetAna, 'MOPA-Analitico')
        imprimirSolucoes(anaFilt, 'MOPA-Analitico Filtrado')
        
        if plot:
            # plotagem comparativas dos pontos obtidos/filtrados, receptor e ponto simulado
            plt.figure(1).gca(projection='3d').scatter(resultHel[:,0], resultHel[:,1], resultHel[:,2], c='blue')
            plt.figure(1).gca(projection='3d').scatter(posRec[0], posRec[1], posRec[2], c='red')
            plt.title('Pontos Encontrados, Receptor e Pnt. Simulado - MOPA-Helmert')

            if filtroHel:
                plt.figure(2).gca(projection='3d').scatter(resultHelFilt[:,0], resultHelFilt[:,1], resultHelFilt[:,2], c='blue')
                plt.figure(2).gca(projection='3d').scatter(posRec[0], posRec[1], posRec[2], c='red')
                plt.title('Pontos Encontrados, Receptor e Pnt. Simulado - MOPA-Helmert Filtrado')

            plt.figure(3).gca(projection='3d').scatter(resultAna[:,0], resultAna[:,1], resultAna[:,2], c='blue')
            plt.figure(3).gca(projection='3d').scatter(posRec[0], posRec[1], posRec[2], c='red')
            plt.title('Pontos Encontrados, Receptor e Pnt. Simulado - MOPA-Analitico')

            if filtroAna:
                plt.figure(4).gca(projection='3d').scatter(resultAnaFilt[:,0], resultAnaFilt[:,1], resultAnaFilt[:,2], c='blue')
                plt.figure(4).gca(projection='3d').scatter(posRec[0], posRec[1], posRec[2], c='red')
                plt.title('Pontos Encontrados, Receptor e Pnt. Simulado - MOPA-Analitico Filtrado')
            #plt.show()

            showTerrainShooter(elevation, vetHel, rowStride=10, columnStride=10, iniX=iniXInteresse, \
                               fimX=fimXInteresse, iniY=iniYInteresse, fimY=fimYInteresse, terrain=True)
        return True

# funcao para gerar relatorio final de resultados
def gerarRelatorioFinal(arq, entrada, resultados, distMin, pntMaisProx, tempExec, nrPnts):

    [colRec, linRec, Zen, Az, zenUnit, azUnit, resolEspacial, tolAltitude, tolZen, tolAz] = entrada
    [resultHel, resultHelFilt, resultAna, resultAnaFilt] = resultados
    [distMinHel, distMinHelFilt, distMinAna, distMinAnaFilt] = distMin
    [pntMaisProx_Hel, pntMaisProx_HelFilt, pntMaisProx_Ana, pntMaisProx_AnaFilt] = pntMaisProx
    [fimHel, fimHelFilt, fimAna, fimAnaFilt] = tempExec
    [nrPntsHel, nrPntsHelFilt, nrPntsAna, nrPntsAnaFilt] = nrPnts
    
    
    tempo = time.localtime()
    
    dirRelatorio = os.getcwd() + '\\Relatorios\\'
    arqSaida = str(tempo[0]) + str(tempo[1]) + str(tempo[2]) + '-' +    str(tempo[3]) +\
               str(tempo[4]) + str(tempo[5]) + '-' + getFileName(arq) + '.txt'
    
    dataset = gdal.Open(arq)
    gt = dataset.GetGeoTransform()
    elevation = dataset.ReadAsArray()
    posRec = np.array((prmtsPx2Coord(colRec,linRec,dataset)[0],\
                       prmtsPx2Coord(colRec,linRec,dataset)[1],elevation[colRec,linRec]))
    
    minx = gt[0]
    miny = gt[3] + len(elevation)*gt[4] + len(elevation[0])*gt[5] 
    maxx = gt[0] + len(elevation)*gt[1] + len(elevation[0])*gt[2]
    maxy = gt[3]
    
    # criar pasta de relatorios caso seja necessario
    try:
        os.system('mkdir Relatorios > nul 2> nul')
    except:
        print ''
    
    # preenchimento do arquivo
    with open(dirRelatorio + arqSaida, 'w') as f_handle:
        # Cabecalho
        f_handle.write('RELATORIO FINAL DE EXECUCAO - MOPA\n\n')
        f_handle.write('Versao do programa: MOPA_v0.3.3\n')
        f_handle.write('Data de execucao: {0}-{1}-{2} as {3}:{4}\n'.format(tempo[2], tempo[1], \
                                                                         tempo[0], tempo[3], tempo[4]))

        # Dados de entrada
        f_handle.write('\n>DADOS DE ENTRADA\n\nArquivo lido: {}\n'.format(getFileName(arq)))
        f_handle.write('Sistema de coordenadas e projecao: {}\n'.format(dataset.GetProjection()))
        f_handle.write('Minimo eixo X: {0}\tMaximo eixo X: {1}\n'.format(minx, maxx))
        f_handle.write('Minimo eixo Y: {0}\tMaximo eixo Y: {1}\n'.format(miny, maxy))
        f_handle.write('Minimo eixo Z: {0} m\tMaximo eixo Z: {1} m\n'.format(elevation.min(), elevation.max()))

        # Dados inseridos
        f_handle.write('\n\n>DADOS INSERIDOS\n\nPosicao do Receptor: ({0}, {1}, {2})\n'\
                       .format(posRec[0], posRec[1], posRec[2]))
        f_handle.write('Angulo Vertical: {0} graus\nAngulo Horizontal: {1} graus\n'.format(zenUnit, azUnit))
        f_handle.write('Tolerancia do angulo Vertical: {0} graus\nTolerancia do angulo Horizontal: {1} graus\n'\
                       .format(tolZen, tolAz))
        f_handle.write('Tolerancia de altitude: {} m\n'.format(tolAltitude))
        f_handle.write('Tamanho de pixel do arquivo: {} m\n'.format(resolEspacial))

        # Resultados obtidos - Metodo de Helmert
        if resultHel is not None:
            f_handle.write('\n\n>RESULTADOS OBTIDOS - METODO DE HELMERT\n\n')
            f_handle.write('|       Longitude        |        Latitude         |        Altitude        |'\
                            '     Difer. Altim.      |   Difer. Ang. Vert.    |   Difer. Ang. Horiz.    |'\
                            '     Dist. Planim.      |\n')
            np.savetxt(f_handle, resultHel)
            f_handle.write('Tempo de execucao MOPA-Helmert: {} s\n'.format(fimHel))
            f_handle.write('Nr. de sol. encontradas pelo MOPA-Helmert: {} ponto(s)\n'.format(nrPntsHel))
            f_handle.write('Ponto mais proximo ao sensor encontrado pelo MOPA-Helmert: ({0}, {1}, {2})\t'.\
                            format(pntMaisProx_Hel[2], pntMaisProx_Hel[3], pntMaisProx_Hel[4]))
            f_handle.write('Distancia ao sensor: {} m\n'.format(distMinHel))
        else:
            f_handle.write('\n\n>RESULTADOS OBTIDOS - METODO DE HELMERT\n\nMOPA-Helmert nao encontrou solucao\n')
        

        # Resultados obtidos - Metodo de Helmert Filtrado (somente se o filtro for efetivo)
        if resultHelFilt is None:
            f_handle.write('\n\n>RESULTADOS OBTIDOS - METODO DE HELMERT FILTRADO\n\n'\
                           'O filtro para o MOPA-Helmert nao foi aplicado\n')
        elif len(resultHelFilt) == 0:
            f_handle.write('\n\n>RESULTADOS OBTIDOS - METODO DE HELMERT FILTRADO\n\n'\
                           'Nenhum dos pontos encontrados obedece os criterios de fitro adotados\n')
        else:
            f_handle.write('\n\n>RESULTADOS OBTIDOS - METODO DE HELMERT FILTRADO\n\n')
            f_handle.write('|       Longitude        |        Latitude         |        Altitude        |'\
                       '     Difer. Altim.      |   Difer. Ang. Vert.    |   Difer. Ang. Horiz.    |'\
                       '     Dist. Planim.      |\n')
            np.savetxt(f_handle, resultHelFilt)
            f_handle.write('Tempo de execucao do filtro para MOPA-Helmert: {} s\n'.format(fimHelFilt))
            f_handle.write('Nr. de sol. encontradas pelo MOPA-Helmert Filtrado: {} ponto(s)\n'.format(nrPntsHelFilt))
            f_handle.write('Ponto mais proximo encontradas pelo MOPA-Helmert Filtrado: ({0}, {1}, {2})\t'\
                           .format(pntMaisProx_HelFilt[2], pntMaisProx_HelFilt[3], pntMaisProx_HelFilt[4]))
            f_handle.write('Distancia ao ponto simulado: {} m\n'.format(distMinHelFilt))

        # Resultados obtidos - Metodo Analitico
        if resultAna is not None:
            f_handle.write('\n\n>RESULTADOS OBTIDOS - METODO ANALITICO\n\n')
            f_handle.write('|       Longitude        |        Latitude         |        Altitude        |'\
                           '     Difer. Altim.      |   Difer. Ang. Vert.    |   Difer. Ang. Horiz.    |'\
                           '     Dist. Planim.      |\n')
            np.savetxt(f_handle, resultAna)
            f_handle.write('Tempo de execucao MOPA-Analitico: {} s\n'.format(fimAna))
            f_handle.write('Nr. de sol. encontradas pelo MOPA-Analitico: {} ponto(s)\n'.format(nrPntsAna))
            f_handle.write('Ponto mais proximo encontradas pelo MOPA-Analitico: ({0}, {1}, {2})\t'.\
                           format(pntMaisProx_Ana[2], pntMaisProx_Ana[3], pntMaisProx_Ana[4]))
            f_handle.write('Distancia ao ponto simulado: {} m\n'.format(distMinAna))
        else:
            f_handle.write('\n\n>RESULTADOS OBTIDOS - METODO ANALITICO\n\n'\
                           'MOPA-Analitico nao encontrou solucao\n')


        # Resultados obtidos - Metodo Analitico Filtrado (somente se o filtro for efetivo)
        if resultAnaFilt is None:
            f_handle.write('\n\n>RESULTADOS OBTIDOS - ANALITICO FILTRADO\n\n'\
                           'O filtro para o MOPA-Analitico nao foi aplicado\n')
        elif len(resultAnaFilt) == 0:
            f_handle.write('\n\n>RESULTADOS OBTIDOS - ANALITICO FILTRADO\n\n'\
                           'Nenhum dos pontos encontrados obedece os criterios de fitro adotados\n')
        else:
            f_handle.write('\n\n>RESULTADOS OBTIDOS - ANALITICO FILTRADO\n\n')
            f_handle.write('|       Longitude        |        Latitude         |        Altitude        |'\
                       '     Difer. Altim.      |   Difer. Ang. Vert.    |   Difer. Ang. Horiz.    |'\
                       '     Dist. Planim.      |\n')
            np.savetxt(f_handle, resultAnaFilt)
            f_handle.write('Tempo de execucao do filtro para MOPA-Analitico: {} s\n'.format(fimAnaFilt))
            f_handle.write('Nr. de sol. encontradas pelo MOPA-Analitico Filtrado: {} ponto(s)\n'.format(nrPntsAnaFilt))
            f_handle.write('Ponto mais proximo encontradas pelo MOPA-Analitico Filtrado: ({0}, {1}, {2})\t'\
                           .format(pntMaisProx_AnaFilt[2], pntMaisProx_AnaFilt[3], pntMaisProx_AnaFilt[4]))
            f_handle.write('Distancia ao ponto simulado: {} m\n'.format(distMinAnaFilt))

        print '\n\nArquivo ' + dirRelatorio + arqSaida + ' gerado!\n'


## BLOCO DE DEFINICAO DA MAIN()

##main para quando se quer um unico arquivo por vez
def main(): #funcionando, mas tem que melhorar o readTIF
    tipo=0
    while tipo not in [1,2,3,4]:
        try:
            tipo = int(raw_input('Fonte de dados:\n1-Link para arquivo .ZIP\n2-Arquivo .ZIP local\n3-Link para arquivo .TIF\n4-Arquivo .TIF local\n'))
            if  tipo not in [1,2,3,4]:
                print 'Insira um numero entre 1 e 4.\n'
        except:
            print 'Numero invalido.\n'
            continue
    while True:
        try:
            dataset, arq = acao(tipo)
            if dataset <> 'NULL':
                break
            else:
                print '\nErro na leitura do TIF ou arquivo invalido.\n'
                opcao = 2
                while opcao not in [0,1]:
                    try:
                        opcao = int(raw_input('Deseja inserir novamente o caminho do arquivo do arquivo?\n1-Sim\t 0-Nao\n'))
                        if opcao not in [0,1]:
                            print '\nInsira 0 ou 1.\n'
                    except:
                        print 'Insira 0 ou 1.\n'
                if opcao:
                    continue
                else:
                    return None
        except:
            print 'Erro na leitura do TIF.\n'
            opcao = 2
            while opcao not in [0,1]:
                try:
                    opcao = int(raw_input('Deseja inserir novamente o caminho do arquivo do arquivo?\n1-Sim\t 0-Nao\n'))
                    if opcao not in [0,1]:
                        print 'Insira 0 ou 1.\n'
                except:
                    print 'Insira 0 ou 1.\n'
        if opcao:
            continue
        else:
            return None

    # coleta de variaveis
    Zen, Az, zenUnitarizado, azUnitarizado, tolAltitude, resolEspacial, tolZen, tolAz, plotGraficos = collectVariables()
    vetDir = np.array([Zen, Az])
    elevation = dataset.ReadAsArray()
    
    print '\nAguarde, programa em execucao...\n'
    
    ## comeco de variaveis globais temporarias
    (colRec,linRec) = (841,123)
    distMaxDisparo = 1000.
    posRec = np.array((prmtsPx2Coord(colRec,linRec,dataset)[0],prmtsPx2Coord(colRec,linRec,dataset)[1],elevation[colRec,linRec]))
    ## fim de variaveis globais temporarias
    
    # gerar relatorio
    resultadosFinais(arq, [colRec, linRec], [Zen, Az, zenUnitarizado, azUnitarizado], tolAltitude,\
                 resolEspacial, distMaxDisparo, tolZen, tolAz, plotGraficos)

## EXECUCAO

main()