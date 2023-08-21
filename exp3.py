import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import curve_fit

def gaussiana(x, mi, A, sigma):

    return A*np.exp(-((x-mi)**2)/(2*(sigma**2)))

def fnct(x,a,b,m,A,s):
    return a*x + b + A*np.exp(-((x-m)**2/(2*s**2)))

def fit(diretorio, fname):

    tempo = float(fname.split('.')[0].split('_')[2].replace(',', '.'))
    path = diretorio + fname
    dados = np.loadtxt(path)/tempo

    #dados
    x = np.linspace(700,1050, 1050-700)
    y = dados[700:1050]
    #gaussiana
    xg = np.linspace(800,1020,1020-800)
    yg = dados[800:1020]
    #reta
    xr = np.concatenate((x[0:90],x[320:]))
    yr = np.concatenate((dados[700:790],dados[1020:1050]))

    #valores pros chutes:
    mean_data = np.mean(xg)
    sigma_data = np.std(xg)
    n = len(x)

    a = (yr[110] - yr[25])/(xr[110] - xr[25]) 
    b = yr[75] - a*xr[75]

    
    chute = [a, b, mean_data, yg.max(), sigma_data]
    fit, cov = curve_fit(fnct, x, y, sigma = [1/np.sqrt(n)]*n, p0 = chute, absolute_sigma = True)

    a, b, mean, amplitude, sigma = fit
    a_unc, b_unc, dm, da, ds = cov[0][0], cov[1][1], cov[2][2], cov[3][3], cov[4][4]
    
    return dados, x, a, b, mean, amplitude, sigma, dm, da, ds

def areas(mean, amplitude, sigma, dm, da, ds):
  #Calcula área com parâmetros fitados
  area, err1 = quad(gaussiana,750,1001,args=(mean,amplitude,sigma))

  #Calcula maior e menor área possível, tirando a diferença como incerteza
  area_sup, err2 = quad(gaussiana,750,1001,args=(mean+dm,amplitude+da,sigma+ds))
  area_inf, err3 = quad(gaussiana,750,1001,args=(mean-dm,amplitude-da,sigma-ds))
  d_area = abs(area_sup - area_inf)

  return area, d_area

def al():

  diretorio = './Dados/Aluminio/'
  arquivos = os.listdir(diretorio)

  fig, ax = plt.subplots(3,2,figsize=(10,10))

  #Indices para graficos
  i,j,k = 0,0,1

  #Titulos dos graficos
  titulos = ['Al 3.20mm','Al 7.45mm','Al 12.48mm','Al 17.63mm','Al 22.88mm','Al 29.18mm']
  for fname in arquivos:
    #Funções de Ajuste e Área
    dados, x, a, b, mean, amplitude, sigma, dm, da, ds = fit(diretorio, fname)
    area,darea = areas(mean, amplitude, sigma, dm, da, ds)

    xd = np.linspace(0,len(dados),len(dados))

    ax[i][j].plot(xd, dados)
    ax[i][j].set_xlim(600,1200)
    ax[i][j].plot(x,fnct(x,a,b,mean,amplitude,sigma),c='k')
    ax[i][j].set_title(titulos[k-1])

    print(f'Área do arquivo {k}: {area} +/- {darea}')
    #Definindo qual o próximo grafico a ser plotado
    #Coluna um ou dois1050
    j += 1
    #Se passar da coluna 2, muda a linha e reseta coluna
    if j>1:
      i+=1
      j=0
    #Contador
    k+=1

  #Titulo de cada eixo (x,y)
  fig.text(0.5, 0.08, 'Canal', ha='center', fontsize = 13)
  fig.text(0.08, 0.5, 'Contagens', va='center', rotation='vertical', fontsize = 13)  
  
  return

def acrilico():

  diretorio = './Dados/Acrilico/'
  arquivos = os.listdir(diretorio)

  fig, ax = plt.subplots(3,2,figsize=(10,10))

  #Indices para graficos
  i,j,k = 0,0,1

  #Titulos dos graficos
  titulos = ['Acrilico 9.45mm','Acrilico 18.95mm','Acrilico 28.55mm','Acrilico 38.5mm','Acrilico 53.75mm','Acrilico 69.2mm']
  for fname in arquivos:
    #Funções de Ajuste e Área
    dados, x, a, b, mean, amplitude, sigma, dm, da, ds = fit(diretorio, fname)
    area,darea = areas(mean, amplitude, sigma, dm, da, ds)

    xd = np.linspace(0,len(dados),len(dados))

    ax[i][j].plot(xd, dados)
    ax[i][j].set_xlim(600,1200)
    ax[i][j].plot(x,fnct(x,a,b,mean,amplitude,sigma),c='k')
    ax[i][j].set_title(titulos[k-1])

    print(f'Área do arquivo {k}: {area} +/- {darea}')
    #Definindo qual o próximo grafico a ser plotado
    #Coluna um ou dois
    j += 1
    #Se passar da coluna 2, muda a linha e reseta coluna
    if j>1:
      i+=1
      j=0
    #Contador
    k+=1

  #Titulo de cada eixo (x,y)
  fig.text(0.5, 0.08, 'Canal', ha='center', fontsize = 13)
  fig.text(0.08, 0.5, 'Contagens', va='center', rotation='vertical', fontsize = 13)  
  
  return

def concreto():

  diretorio = './Dados/Concreto/'
  arquivos = os.listdir(diretorio)

  fig, axs = plt.subplots(3,2, figsize = (10,10))
  gs = axs[1, 1].get_gridspec()
  # remove the underlying axes
  for ax in axs[1:, -1]:
      ax.remove()
  axbig = fig.add_subplot(gs[1:, -1])
  #Indices para graficos
  i,j,k = 0,0,1

  #Titulos dos graficos
  titulos = ['Concreto 10.2mm','Concreto 20.65mm','Concreto 31.1mm','Concreto 41.85mm','Concreto 52.7mm','Concreto mm']
  for fname in arquivos:
    #Funções de Ajuste e Área
    dados, x, a, b, mean, amplitude, sigma, dm, da, ds = fit(diretorio, fname)
    area,darea = areas(mean, amplitude, sigma, dm, da, ds)

    xd = np.linspace(0,len(dados),len(dados))
    if k <= 4:
      axs[i][j].plot(xd, dados)
      axs[i][j].set_xlim(600,1200)
      axs[i][j].plot(x,fnct(x,a,b,mean,amplitude,sigma),c='k')
      axs[i][j].set_title(titulos[k-1])
    else:
      axbig.plot(xd,dados)
      axbig.set_xlim(600,1200)
      axbig.plot(x,fnct(x,a,b,mean,amplitude,sigma),c='k')
      axbig.set_title(titulos[k-1])

    print(f'Área do arquivo {k}: {area} +/- {darea}')
    #Definindo qual o próximo grafico a ser plotado
    #Coluna um ou dois
    i += 1
    #Se passar da coluna 2, muda aConcreto a e reseta coluna
    if i>2:
      j+=1
      i=0
    #Contador
    k+=1

  #Titulo de cada eixo (x,y)
  fig.text(0.5, 0.08, 'Canal', ha='center', fontsize = 13)
  fig.text(0.08, 0.5, 'Contagens', va='center', rotation='vertical', fontsize = 13)  
  
  return

def desconhecido():

  diretorio = './Dados/Desconhecido/'
  arquivos = os.listdir(diretorio)

  fig, ax = plt.subplots(3,2,figsize=(10,10))

  #Indices para graficos
  i,j,k = 0,0,1

  #Titulos dos graficos
  titulos = ['XX 2mm','XX 4mm','XX 6mm','XX 8mm','XX 10mm','XX 12mm']
  for fname in arquivos:
    #Funções de Ajuste e Área
    dados, x, a, b, mean, amplitude, sigma, dm, da, ds = fit(diretorio, fname)
    area,darea = areas(mean, amplitude, sigma, dm, da, ds)

    xd = np.linspace(0,len(dados),len(dados))

    ax[i][j].plot(xd, dados)
    ax[i][j].set_xlim(600,1200)
    ax[i][j].plot(x,fnct(x,a,b,mean,amplitude,sigma),c='k')
    ax[i][j].set_title(titulos[k-1])

    print(f'Área do arquivo {k}: {area} +/- {darea}')
    #Definindo qual o próximo grafico a ser plotado
    #Coluna um ou dois
    j += 1
    #Se passar da coluna 2, muda a linha e reseta coluna
    if j>1:
      i+=1
      j=0
    #Contador
    k+=1

  #Titulo de cada eixo (x,y)
  fig.text(0.5, 0.08, 'Canal', ha='center', fontsize = 13)
  fig.text(0.08, 0.5, 'Contagens', va='center', rotation='vertical', fontsize = 13)  
  
  return
def grafite():

  diretorio = './Dados/Grafite/'
  arquivos = os.listdir(diretorio)

  fig, ax = plt.subplots(1,3,figsize=(10,5))

  #Indices para graficos
  i,k = 0,1

  #Titulos dos graficos
  titulos = ['Grafite 1.5mm','Grafite 3mm','Grafite 4.5mm']
  for fname in arquivos:
    #Funções de Ajuste e Área
    dados, x, a, b, mean, amplitude, sigma, dm, da, ds = fit(diretorio, fname)
    area,darea = areas(mean, amplitude, sigma, dm, da, ds)

    xd = np.linspace(0,len(dados),len(dados))

    ax[i].plot(xd, dados)
    ax[i].set_xlim(650,1200)
    ax[i].plot(x,fnct(x,a,b,mean,amplitude,sigma),c='k')
    ax[i].set_title(titulos[k-1])

    print(f'Área do arquivo {k}: {area} +/- {darea}')
    #Definindo qual o próximo grafico a ser plotado
    #Coluna um ou dois
    i += 1
    #Contador
    k+=1

  #Titulo de cada eixo (x,y)
  fig.text(0.5, 0.05, 'Canal', ha='center', fontsize = 13)
  fig.text(0.08, 0.5, 'Contagens', va='center', rotation='vertical', fontsize = 13)  
  
  return

def pb():

  diretorio = './Dados/Chumbo/'
  arquivos = os.listdir(diretorio)

  fig, ax = plt.subplots(3,2,figsize=(10,10))

  #Indices para graficos
  i,j,k = 0,0,1

  #Titulos dos graficos
  titulos = ['Pb 2.35mm','Pb 3.10mm','Pb 3.11mm','Pb 3.25mm','Pb 8.50mm','Pb 2.40mm']
  for fname in arquivos:
    #Funções de Ajuste e Área
    dados, x, a, b, mean, amplitude, sigma, dm, da, ds = fit(diretorio, fname)
    area,darea = areas(mean, amplitude, sigma, dm, da, ds)

    xd = np.linspace(0,len(dados),len(dados))

    ax[i][j].plot(xd, dados)
    ax[i][j].set_xlim(600,1200)
    ax[i][j].plot(x,fnct(x,a,b,mean,amplitude,sigma),c='k')
    ax[i][j].set_title(titulos[k-1])

    print(f'Área do arquivo {k}: {area} +/- {darea}')
    #Definindo qual o próximo grafico a ser plotado
    #Coluna um ou dois
    j += 1
    #Se passar da coluna 2, muda a linha e reseta coluna
    if j>1:
      i+=1
      j=0
    #Contador
    k+=1

  #Titulo de cada eixo (x,y)
  fig.text(0.5, 0.08, 'Canal', ha='center', fontsize = 13)
  fig.text(0.08, 0.5, 'Contagens', va='center', rotation='vertical', fontsize = 13)  
  
  return