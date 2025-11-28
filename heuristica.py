import os
from tkinter import filedialog
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
            
        def torneioPais(populacao, custos, taxa_crossover):
            pass
        
        def crossover(pais, taxa_crossover):
            pass

        def mutacao(taxa_mutacao, caminhos): # adicionar parametro filhos_cross
            prop_inversao_cross = 0.50
            prop_inversao_pop = 0.30
            prop_insert_pop = 0.20

            inversao_cross = int(taxa_mutacao * prop_inversao_cross)
            inversao_pop = int(taxa_mutacao * prop_inversao_pop)
            insert_pop = int(taxa_mutacao - (inversao_cross + inversao_pop))

            
            #inversao_cross = int(2 * (taxa_mutacao / 5))
            inversao = int(4 * (taxa_mutacao / 5))  # 80% inversão
            insert = int(1 * (taxa_mutacao / 5))    # 20% inserção
        
            mutacoes = []
            novos_custos = []
        
            # Mutação de inversão
            for i in range(inversao):
                try:
                    individuo = caminhos[i].split(' ')
                    n_cidades = len(individuo)
        
                    if n_cidades <= 3:
                        mutacoes.append(" ".join(individuo))
                        novos_custos.append(custoCaminho(" ".join(individuo), dicDistancias))
                        continue
        
                    erro = True
                    tentativas = 0
                    while erro and tentativas < 30:
                        tentativas += 1
        
                        inicio = random.randint(1, n_cidades - 3)
        
                        tamanho = randomGaussiano(
                            media=2,
                            desvio_padrao=max(3, n_cidades // 6),
                            limite_superior=n_cidades // 2
                        )
                        tamanho = max(2, tamanho)
        
                        if inicio + tamanho >= n_cidades - 1:
                            tamanho = (n_cidades - 2) - inicio
        
                        fim = inicio + tamanho
        
                        if fim - inicio < 2:
                            continue
        
                        filho = individuo[:]
                        segmento = filho[inicio:fim]
                        filho[inicio:fim] = segmento[::-1]
        
                        filho_str = " ".join(filho)
        
                        if filho_str != " ".join(individuo):
                            mutacoes.append(filho_str)
                            novos_custos.append(custoCaminho(filho_str, dicDistancias))
                            erro = False
        
                    if erro:  # se não conseguir mutar diferente do pai
                        mutacoes.append(" ".join(individuo))
                        novos_custos.append(custoCaminho(" ".join(individuo), dicDistancias))
        
                except Exception as e:
                    print(f'erro inversão: {e}')
        
        
            # Mutação de inserção
            try:
                for l in range(inversao, inversao + insert):
                    individuo_insert = caminhos[l].split(' ')
                    n_cidades = len(individuo_insert)
        
                    erro = True
                    tentativas = 0
                    while erro and tentativas < 30:
                        tentativas += 1
        
                        pos_origem = random.randint(1, n_cidades - 2)
                        pos_destino = random.randint(1, n_cidades - 2)
        
                        if pos_origem == pos_destino:
                            continue
        
                        filho = individuo_insert[:]
                        cidade = filho.pop(pos_origem)
                        filho.insert(pos_destino, cidade)
        
                        filho_str = " ".join(filho)
        
                        if filho_str != " ".join(individuo_insert):
                            mutacoes.append(filho_str)
                            novos_custos.append(custoCaminho(filho_str, dicDistancias))
                            erro = False
        
                    if erro:
                        mutacoes.append(" ".join(individuo_insert))
                        novos_custos.append(custoCaminho(" ".join(individuo_insert), dicDistancias))
        
            except Exception as e:
                print('erro inserção:', e)
        
            return mutacoes, novos_custos
  
        def randomGaussiano(media, desvio_padrao, limite_superior):
            """
            Gera um número aleatório gaussiano usando rejeição até estar no limite.
            """
            while True:
                numero = abs(int(np.random.normal(media, desvio_padrao)))

                if 3 <= numero <= limite_superior:
                    return numero


        def melhorDaGeracao():
            pass
        
        def atualizarPopulacao(populacao, filhos, custos, novos_custos):
            pass
            
        # Execução das funções
        if caminho_do_arquivo.endswith('.txt'):
            tsp, dicDistancias, dicCasas = tornarTSPLIB() 
            print(dicCasas)
            #print(*tsp, sep='')
            qtdeCidades = len(dicCasas)
            
            
            nivel_de_geracoes = 0
            max_geracoes = 1600
            tamanho_populacao = 200
            populacao = inicializaPopulacao(tamanho_populacao, qtdeCidades)
            custos = (calculaAptidao(populacao, dicDistancias))
            dic_caminhos = dict(zip(populacao, custos)) # Adiciona todos os caminhos num dicionário
            #print(len(populacao),f'população inicial:\n{populacao}')

            while (nivel_de_geracoes <= max_geracoes):                
            
                taxa_mutacao = tamanho_populacao * (1 -(nivel_de_geracoes / max_geracoes))
                taxa_crossover = tamanho_populacao  *  (nivel_de_geracoes / max_geracoes)
                nivel_de_geracoes += tamanho_populacao  # Aumenta o nivel da geração
                


                

                if taxa_crossover != 0:
                    #pais = torneioPais(populacao, custos, taxa_crossover)
                    #filhos = crossover(pais, taxa_crossover)
                    pass
                if taxa_mutacao != 0:
                    filhos, novos_custos = mutacao(taxa_mutacao, populacao)
                
                #populacao = atualizarPopulacao(populacao, filhos, custos, novos_custos)
                #melhor_caminho, melhor_da_geracao = melhorDaGeracao()


            # cronometro de execução
            fim_contador = time.perf_counter()
            tempo_de_execucao = fim_contador - contador_de_tempo  

            
            
        elif caminho_do_arquivo.endswith('.tsp'):
            print('tsp')
        else:
            entry_widget.delete("1.0", "end")
            entry_widget.insert("1.0", f"Ocorreu um erro:\nTecnicamente: {e}\n\nVerifique se o formato do arquivo .txt está na forma certa:\n"
            "EX:\n"
            "33\n"
            "C00\n00B\nR0A\n")



        # Saída final
        output_formatado = (
            f""
            f""
            f"Tempo gasto no cálculo:\n{tempo_de_execucao:.4f} s"
        )

        entry_widget.delete("1.0", "end")
        entry_widget.insert("1.0", output_formatado)


        
    except Exception as e:
        print(e)
        if not MemoryError:
            entry_widget.delete("1.0", "end")
            entry_widget.insert("1.0", f"Ocorreu um erro:\nTecnicamente: {e}\n\nVerifique se o formato do arquivo .txt está na forma certa:\n"
            "EX:\n"
            "33\n"
            "C00\n00B\nR0A\n")

