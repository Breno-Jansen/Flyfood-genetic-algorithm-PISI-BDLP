import os
from tkinter import filedialog
import itertools
import re
import numpy as np
import time
import random

def selecionar_arquivo(entry_widget):
    
    """
    Recebe o widget de texto como parâmetro para poder escrever nele.
    Reconhece quando o arquivo é carregado.
    """
    global caminho_do_arquivo
    #escolher arquivo txt ou tsp
    filetypes = (('Text files', '*.txt'), ('TSP files', '*.tsp'))
    fpath = filedialog.askopenfilename(title="Selecione o arquivo de matriz", filetypes=filetypes,)
    if fpath:
        caminho_do_arquivo = fpath
        entry_widget.delete("1.0", "end")
        entry_widget.insert("1.0", f"Arquivo carregado:\n{os.path.basename(caminho_do_arquivo)}")


def executar_calculo(entry_widget):
    contador_de_tempo = time.perf_counter()    
    global caminho_do_arquivo
    # Verifica se um arquivo foi selecionado primeiro
    if not caminho_do_arquivo:
        entry_widget.delete("1.0", "end")
        entry_widget.insert("1.0", "Erro: Por favor, carregue um arquivo .txt primeiro.")
        return

    try:
            
        entry_widget.delete("1.0", "end")
        entry_widget.insert("1.0", f"Calculando....")
        entry_widget.update_idletasks()
        def tornarTSPLIB(): # Se a entrada for txt, transforma em TSP
            pontos = [] # Todos os pontos do txt

            letraCasas = []
            cordenadas = []

            with open(caminho_do_arquivo, "r", encoding="utf-8") as arquivo:
                matriz_linhas = arquivo.readlines()
                linha0_entradas = matriz_linhas[0]
                separar_linhas_colunas = linha0_entradas.split(' ')
                qntd_linhas = int(separar_linhas_colunas[0])
                qntd_colunas = int(separar_linhas_colunas[1])
                linhas_sem_a_primeira = matriz_linhas[1:]

                for i in range(qntd_linhas):
                    pontos_por_linha = linhas_sem_a_primeira[i].split()
                    pontos.append(pontos_por_linha)

                    for j in range(qntd_colunas):
                        elemento = pontos[i][j]

                        if elemento == 'R':
                            cord_origem = (i, j)
                            letraCasas.insert(0, elemento)
                            cordenadas.insert(0, cord_origem)

                        elif elemento != '0':
                            cord_casa = (i, j)
                            letraCasas.append(elemento)                            
                            cordenadas.append(cord_casa)

            # Depois de ler o txt, começa a transformação:
            dicCasas = dict(zip(letraCasas,cordenadas))
            n = len(cordenadas)
            dicDistancias = {}

            with open ('created_file.tsp', "w", encoding="utf-8") as tsp:
                for i in range(0, n-1): # linha inicial até n-1 pois a linha n não terá aresta
                    
                    for j in range(i+1, n): # coluna i+1 até a ultima
                        x1, y1 = cordenadas[i]
                        x2, y2 = cordenadas[j]
                        distancia = abs(x1 - x2) + abs(y1 - y2)
                        tsp.write(f'{distancia} ')  # escreve as distancias num arquivo TSPLIB
                        dicDistancias[(i, j)] = distancia
                    tsp.write('\n')

            with open ('created_file.tsp', "r", encoding="utf-8") as tsp_read:
                return tsp_read.readlines(), dicDistancias, dicCasas
        
        
        

        def custoCaminho(permutacao, dicDistancias):
                caminho = permutacao.split(' ')
                soma_individual = 0
                for i in range(len(caminho)):
                    try:
                        a = int(caminho[i])
                        b = int(caminho[i + 1])
                        if a < b:
                            soma_individual += dicDistancias[(a, b)]
                        elif a > b:
                            soma_individual += dicDistancias[(b, a)]
                    except:
                        continue                        
                        
                return soma_individual


        def inicializaPopulacao(tamanho, qtdeCidades):
            # Estrutura base completa, precisa ver variavel tamanho
            populacao = []
            lista_iniciar = []

            for i in range(1, qtdeCidades):
                lista_iniciar.append(i) # Cria uma lista com n cidades de 1 até n

            for i in range(tamanho): 
                random.shuffle(lista_iniciar)   # Embaralha a lista (novo caminho aleatório)
                individuo_base = "0 "+" ".join(map(str, lista_iniciar))+" 0"

                populacao.append(individuo_base)    # Transforma numa string e adiciona na população
            
            return populacao
    


        def calculaAptidao(populacao, dicDistancias):
            custos = []
            menor_custo = np.inf
            menor_caminho = ''
            for permutacao in populacao:
                custo_individual = custoCaminho(permutacao, dicDistancias)
                custos.append(custo_individual)
                if custo_individual < menor_custo:
                    menor_custo = custo_individual
                    menor_caminho = permutacao
                
            return custos, menor_custo, menor_caminho
            

        
        # Execução das funções
        if caminho_do_arquivo.endswith('.txt'):
            tsp, dicDistancias, dicCasas = tornarTSPLIB() 
            print(dicCasas)
            #print(*tsp, sep='')
            qtdeCidades = len(dicCasas)
            menores_caminhos_iniciais = {}
            for i in range(6):
                populacao = inicializaPopulacao(100, qtdeCidades)
                custo, menor_custo, menor_caminho = (calculaAptidao(populacao, dicDistancias))
                menores_caminhos_iniciais[menor_caminho] = menor_custo
            
            # a partir do menor_caminho aplicar as mutações
            print(menores_caminhos_iniciais)
        elif caminho_do_arquivo.endswith('.tsp'):
            print('tsp')
        else:
            entry_widget.delete("1.0", "end")
            entry_widget.insert("1.0", f"Ocorreu um erro:\nTecnicamente: {e}\n\nVerifique se o formato do arquivo .txt está na forma certa:\n"
            "EX:\n"
            "33\n"
            "C00\n00B\nR0A\n")

        # cronometro de execução
        fim_contador = time.perf_counter()
        tempo_de_execucao = fim_contador - contador_de_tempo

        # Saída final
        output_formatado = (
            f""
            f""
            f"Tempo gasto no cálculo:\n{tempo_de_execucao:.4f} s"
        )

        entry_widget.delete("1.0", "end")
        entry_widget.insert("1.0", output_formatado)


        
    except Exception as e:
        if not MemoryError:
            entry_widget.delete("1.0", "end")
            entry_widget.insert("1.0", f"Ocorreu um erro:\nTecnicamente: {e}\n\nVerifique se o formato do arquivo .txt está na forma certa:\n"
            "EX:\n"
            "33\n"
            "C00\n00B\nR0A\n")

