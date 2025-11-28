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

letraCasas = []
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
            
        def torneioPais(populacao, custos):
            """
            Seleção por torneio binário:
            Escolhe dois indivíduos aleatórios, compara os custos e retorna o de menor custo (melhor).
            Repete até formar uma lista com tamanho taxa_crossover.
            """
            pais = []
        
            # taxa_crossover é dinâmica no seu código, então convertemos para inteiro
            qtde_pais = int(taxa_crossover)
        
            for _ in range(qtde_pais):
                # escolhe dois candidatos aleatórios para o torneio
                idx1 = random.randint(0, len(populacao) - 1)
                idx2 = random.randint(0, len(populacao) - 1)
        
                # melhor custo vence
                if custos[idx1] <= custos[idx2]:
                    pais.append(populacao[idx1])
                else:
                    pais.append(populacao[idx2])
        
            return pais
                
        def crossover(caminho1, caminho2):
            # transforma pais de string para lista
            lista = caminho1.split(' ')
            lista_pai = caminho2.split(' ')

            # tamanho sem contar o 0 inicial/final
            tamanho_lista = len(lista)

            # nova lista vazia (mantendo 0 nas pontas)
            lista_nova = [None] * tamanho_lista
            lista_nova[0] = '0'
            lista_nova[-1] = '0'
            divisao_corte = tamanho_lista // 2

            # crossover só acontece entre as cidades 1..n-2
            indice = random.randint(1, tamanho_lista - divisao_corte - 1)   # mesma lógica do seu randint(0,5)
            corte_fim = indice + divisao_corte

            # copia trecho do pai 1
            for i in range(indice, corte_fim):
                lista_nova[i] = lista[i]

            # índices de leitura circular dos pais
            novo_indice = corte_fim % tamanho_lista
            indice_listaUm = corte_fim % tamanho_lista

            # preenche o resto
            for i in range(1, tamanho_lista-1):   # evita posições 0 e final
                if lista_nova[i] is None:
                    while True:
                        elemento_pai = lista_pai[novo_indice]

                        # elemento do pai 2 não existe no filho -> coloca
                        if elemento_pai not in lista_nova:
                            lista_nova[i] = elemento_pai
                            novo_indice = (novo_indice + 1) % tamanho_lista
                            break

                        # elemento já existe -> tenta elemento do pai 1
                        else:
                            elemento_principal = lista[indice_listaUm]

                            if elemento_principal not in lista_nova:
                                lista_nova[i] = elemento_principal
                                indice_listaUm = (indice_listaUm + 1) % tamanho_lista
                                break

                            # continua procurando
                            novo_indice = (novo_indice + 1) % tamanho_lista
                            indice_listaUm = (indice_listaUm + 1) % tamanho_lista

            # converte de volta para string
            return " ".join(lista_nova)
        
        def crossover_populacao(pais, taxa_crossover):
            filhos = []
            custos_filhos = []
            indice = 0
            
            while len(filhos) < taxa_crossover:
                pai1 = pais[indice % len(pais)]
                pai2 = pais[(indice + 1) % len(pais)]
                filho = crossover(pai1, pai2)
                filhos.append(filho)
                custos_filhos.append(custoCaminho(filho, dicDistancias))
                indice += 1
            #print('crossovers: ', len(filhos))
            return filhos, custos_filhos

        def inversao(caminhos, mutacoes, novos_custos, prop):
            total = min(prop, len(caminhos))
            for i in range(total):
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
                    print(f'erro inversão (i={i}, total={total}): {e}')

                
        def mutacao(taxa_mutacao, caminhos, filhos_cross):
            prop_inversao_cross = 0.50
            prop_inversao_pop = 0.30
            prop_insert_pop = 0.20

            inversao_cross = int(taxa_mutacao * prop_inversao_cross)
            inversao_pop = int(taxa_mutacao * prop_inversao_pop)
            insert_pop = int(taxa_mutacao - (inversao_cross + inversao_pop))

            mutacoes = []
            novos_custos = []

            # inversão população (limitada dentro da função inversao)
            inversao(caminhos, mutacoes, novos_custos, inversao_pop)

            # inversão filhos crossover (apenas se houver filhos)
            if filhos_cross:
                inversao(filhos_cross, mutacoes, novos_custos, inversao_cross)

            # inserção: não tentar mais do que há em 'caminhos'
            max_inserts = min(insert_pop, len(caminhos))
            try:
                for l in range(max_inserts):
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
                    # garantir número exato
                if len(mutacoes) > taxa_mutacao:
                    mutacoes = mutacoes[:taxa_mutacao]
                
                elif len(mutacoes) < taxa_mutacao:
                    while len(mutacoes) < taxa_mutacao:
                        mutacoes.append(caminhos[random.randint(0, len(caminhos) - 1)])
                        novos_custos.append(custoCaminho(mutacoes[-1], dicDistancias))

            except Exception as e:
                print('erro inserção:', e)

            #print('mutações: ', len(mutacoes))
            return mutacoes, novos_custos
  
        def randomGaussiano(media, desvio_padrao, limite_superior):
            """
            Gera um número aleatório gaussiano usando rejeição até estar no limite.
            """
            while True:
                numero = abs(int(np.random.normal(media, desvio_padrao)))

                if 3 <= numero <= limite_superior:
                    return numero


        def melhorDaGeracao(populacao, custos):
            """
            Retorna uma tupla contendo:
            (melhor_caminho, melhor_custo)
            """
            melhor_indice = custos.index(min(custos))
            melhor_caminho = populacao[melhor_indice]
            melhor_custo = custos[melhor_indice]
            return melhor_caminho, melhor_custo

        
        def atualizarPopulacao(populacao, filhos, custos, novos_custos):
            """
            Usa elitismo: combina a população atual com filhos da mutação,
            ordena pelo custo e mantém somente os 'tamanho_populacao' melhores.
            """
            global tamanho_populacao

            # junta caminhos e custos dos pais + novos indivíduos
            nova_pop = populacao + filhos
            nova_custos = custos + novos_custos

            # empacota, ordena e desempacota
            unidos = list(zip(nova_pop, nova_custos))
            unidos.sort(key=lambda x: x[1])   # menor custo primeiro

            # mantém só os top 200
            selecionados = unidos[:tamanho_populacao]

            # separa novamente caminhos e custos
            populacao = [caminho for caminho, custo in selecionados]
            custos = [custo for caminho, custo in selecionados]

            return populacao, custos

            
        # Execução das funções
        if caminho_do_arquivo.endswith('.txt'):
            tsp, dicDistancias, dicCasas = tornarTSPLIB() 
            print(dicCasas)
            #print(*tsp, sep='')
            qtdeCidades = len(dicCasas)
            
            global tamanho_populacao
            nivel_de_geracoes = 0
            max_geracoes = 1600
            tamanho_populacao = 200
            populacao = inicializaPopulacao(tamanho_populacao, qtdeCidades)
            custos = (calculaAptidao(populacao, dicDistancias))
            dic_caminhos = dict(zip(populacao, custos)) # Adiciona todos os caminhos num dicionário
            #print(len(populacao),f'população inicial:\n{populacao}')
            filhos_cross = None
            while (nivel_de_geracoes <= max_geracoes):                
            
                taxa_mutacao = int(tamanho_populacao * (1 -(nivel_de_geracoes / max_geracoes)))
                taxa_crossover = tamanho_populacao  *  (nivel_de_geracoes / max_geracoes)
                nivel_de_geracoes += tamanho_populacao  # Aumenta o nivel da geração
                
                if taxa_crossover != 0:
                    pais = torneioPais(populacao, custos)           # Seleciona num torneio binário
                    filhos_cross, custos_filhos_cross = crossover_populacao(pais, taxa_crossover)  # Ajuste: passar a quantidade
                    #print(f"{len(filhos_cross)} filhos gerados por crossover: \n{filhos_cross}")

                    #for i, filho in enumerate(filhos_cross):
                    #    print(f"  Filho {i+1}: {filho}, Custo: {custos_filhos_cross[i]}")

                if taxa_mutacao != 0:
                    filhos, novos_custos = mutacao(taxa_mutacao, populacao, filhos_cross)
                
                populacao, custos = atualizarPopulacao(populacao, filhos, custos, novos_custos)
                melhor_caminho, melhor_custo = melhorDaGeracao(populacao, custos)



            
            
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

        
        caminho_numerado = melhor_caminho.split(' ')
        caminho_letrado = [letraCasas[int(cidade)] for cidade in caminho_numerado]
        caminho_formatado = " -> ".join(caminho_letrado)

        # Saída final
        output_formatado = (
            f"Melhor caminho encontrado:\n{caminho_formatado}\n"
            f"Custo do caminho:\n{melhor_custo}\n"
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

