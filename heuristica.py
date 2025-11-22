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
        casas = {}
        def tornarTSPLIB(): # Se a entrada for txt, transforma em TSP
            pontos = []
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
                            casas[elemento] = (i, j)
                            cord_origem = (i, j)
                            cordenadas.append(cord_origem)

                        elif elemento != '0':
                            casas[elemento] = (i, j)
                            cord_casa = (i, j)
                            cordenadas.append(cord_casa)

            
            
            # Depois de ler o txt, começa a transformação:
            print(casas)
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
                return tsp_read.readlines(), dicDistancias
        
        
        

        def custoCaminho(permutacao, dicDistancias):
                #caminho = ['R'] + list(permutacao) + ['R']
                caminho = permutacao.split(' ')
                print(caminho, '\n')
                soma_individual = 0
                for i in range(len(caminho)):
                    a = caminho[i]
                    b = caminho[i + 1]
                    try:
                        soma_individual += dicDistancias[(a, b)]
                        print(f'distancia da casa {a} para {b} é igual a: {soma_individual}')
                    except:
                        #soma_individual += dicDistancias[(b, a)]
                        print('erro')
                return soma_individual


        def inicializaPopulacao(tamanho, qtdeCidades):
            # Estrutura base completa, precisa ver variavel tamanho
            populacao = []
            lista_iniciar = []
            for i in range(qtdeCidades):
                lista_iniciar.append(i)
            for i in range(tamanho): 
                random.shuffle(lista_iniciar) 
                individuo_base = " ".join(map(str, lista_iniciar))
                populacao.append(individuo_base)
            
            return populacao
    


        def calculaAptidao(populacao, dicDistancias):
            custos = []
            for permutacao in populacao:
                custo_individual = custoCaminho(permutacao, dicDistancias)
                custos.append(custo_individual)
            return custos
            

        
        # Execução das funções
        if caminho_do_arquivo.endswith('.txt'):
            print(caminho_do_arquivo)
            tsp, dicDistancias = tornarTSPLIB() 
            
            print(*tsp, sep='')
            print(dicDistancias)
            qtdeCidades = len(casas)
            populacao = inicializaPopulacao(5, qtdeCidades)
            print(calculaAptidao(populacao, dicDistancias))
        else:
            print('tsp')

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
            entry_widget.insert("1.0", "bruh")
            entry_widget.insert("1.0", f"Ocorreu um erro:\nTecnicamente: {e}\n\nVerifique se o formato do arquivo .txt está na forma certa:\n"
            "EX:\n"
            "33\n"
            "C00\n00B\nR0A\n")

