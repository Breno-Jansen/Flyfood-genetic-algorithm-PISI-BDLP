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
                caminho = permutacao.split(' ') # Cria uma lista com cada casa
                soma_individual = 0 
                for i in range(len(caminho)):
                    try:
                        a = int(caminho[i])     # Lê a atual e próxima casa
                        b = int(caminho[i + 1])
                        if a < b:               # Calcula distância
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
            valor_padrao = None
            custos = [valor_padrao] * len(populacao)
            i = -1
            for permutacao in populacao:
                i+=1
                custo_individual = custoCaminho(permutacao, dicDistancias)
                custos[i] = custo_individual            
                
            return custos
            
        def mutacao(taxa_mutacao, caminhos):
            inversao = int(4*(taxa_mutacao / 5)) # Divide as mutações na proporção 4:1
            insert = int(1*(taxa_mutacao / 5))   # Entre a inversão e insert respectivamente
            
            mutacoes = []
            novo_custos = []

            #biblioteca gaussiana
            for i in range(inversao):
                
                try:
                    individuo = caminhos[i].split(' ')
                    valor_padrao = None
                    filho1 = [valor_padrao] * len(individuo)
                    filho2 = [valor_padrao] * len(individuo)
                    metade_pai = len(individuo) // 2        
                    index_aleatorio = random.randint(1, metade_pai) 
                    range_selecionado = index_aleatorio + metade_pai
                    for j in range(index_aleatorio, range_selecionado):
                        elemento = individuo[j]
                        filho1.insert(index_aleatorio, elemento)
                        filho1.pop(range_selecionado)

                    usados = set([x for x in filho1 if x is not None])
                    pos = 0

                    for cidade in individuo:
                        if cidade not in usados:
                            # achar o próximo None em filho1
                            while filho1[pos] is not None:
                                pos += 1
                            filho1[pos] = cidade

                      
                    filho1_str = " ".join(filho1)
                    # adiciona na lista de mutações
                    mutacoes.append(filho1_str)

                    # calcula custo e adiciona
                    novo_custos.append(custoCaminho(filho1_str, dicDistancias))
                 
                except:
                    print('erro')            
            return mutacoes, novo_custos

                




        
        # Execução das funções
        if caminho_do_arquivo.endswith('.txt'):
            tsp, dicDistancias, dicCasas = tornarTSPLIB() 
            print(dicCasas)
            #print(*tsp, sep='')
            qtdeCidades = len(dicCasas)
            

            nivel_de_geracoes = 0
            max_geracoes = 1600
            tamanho_populacao = 200
            
            while (nivel_de_geracoes <= max_geracoes):
                # selecionar pais usando torneio
                # cruzamento e mutacao em cada par
                # o melhor sobrevive e o restante sera preenchido usando o torneio
                # Calcula a taxa de mutação e crossover (soma deles = 1)
                taxa_mutacao = tamanho_populacao * (1 -(nivel_de_geracoes / max_geracoes))
                taxa_crossover = tamanho_populacao  *  (nivel_de_geracoes / max_geracoes)
                nivel_de_geracoes += tamanho_populacao  # Aumenta o nivel da geração

                populacao = inicializaPopulacao(tamanho_populacao, qtdeCidades)
                custos = (calculaAptidao(populacao, dicDistancias))

                dic_caminhos = dict(zip(populacao, custos)) # Adiciona todos os caminhos num dicionário
                
                mutacoes, novos_custos = mutacao(taxa_mutacao, populacao)
                #print(mutacoes)
                print(f'novos custos: {novos_custos}')
                

            
            # a partir do menor_caminho aplicar as mutações
            
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

