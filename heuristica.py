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
    global caminho_do_arquivo, letraCasas
    letraCasas = []  # limpa sempre
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
        
        def lerTSP(caminho_arquivo):
            """
            Lê um arquivo .tsp no formato triangular superior das distâncias
            e retorna (linhas_tsp, dicDistancias, dicCasas),
            igual à função tornarTSPLIB().
            """

            # Lê todas as linhas do arquivo .tsp
            with open(caminho_arquivo, "r", encoding="utf-8") as tsp:
                linhas_tsp = tsp.readlines()

            # Reconstrói o dicionário de distâncias
            dicDistancias = {}
            n = len(linhas_tsp) + 1  # número de nós (triangular superior tem n-1 linhas)

            for i, linha in enumerate(linhas_tsp):
                valores = linha.split()
                for j, valor in enumerate(valores):
                    dicDistancias[(i, i + j + 1)] = int(valor)

            # Como não temos as casas/letras no .tsp, apenas criamos um mapeamento simples
            # Exemplo: {0: (0,0), 1: (1,0), ...} ou apenas índices
            dicCasas = {str(k): k for k in range(n)}

            return linhas_tsp, dicDistancias, dicCasas

        

        def custoCaminho(permutacao, dicDistancias):
                caminho = permutacao.split(' ') # Cria uma lista com cada casa
                soma_individual = 0 
                for i in range(len(caminho)- 1):
                    a = int(caminho[i])     # Lê a atual e próxima casa
                    b = int(caminho[i + 1])
                    try:
                        soma_individual += dicDistancias[(min(a, b), max(a, b))]
                    except KeyError:
                        print(f"Par {(a,b)} não encontrado no dicionário")
                        
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
            melhor_indice = custos.index(min(custos))
            melhor_caminho = populacao[melhor_indice]
            melhor_custo = custos[melhor_indice]
            return custos, melhor_caminho, melhor_custo
            
        def torneioPais(populacao, custos, taxa_crossover, melhor_caminho=None, k=3,):
            """
            Seleção por torneio com fitness integrado.
            Fitness = 1 / custo  (menor custo ⇒ maior aptidão)
            Retorna os pais para crossover já ordenados por qualidade relativa.
            """
            taxa_crossover
            
            pais = []

            # cálculo implícito do fitness
            fitness = [1 / c if c > 0 else float('inf') for c in custos]

            # número de pais que serão selecionados (90% da população)
            num_pais = int(taxa_crossover)

            # índice de referência
            indices = list(range(len(populacao)))

            for _ in range(num_pais - 1):
                competidores  = random.sample(indices, k)
                # seleciona o competidor com maior fitness
                melhor = max(competidores, key=lambda i: fitness[i])
                pais.append(populacao[melhor])

            # garante que o melhor caminho da geração anterior participa
            if melhor_caminho and melhor_caminho not in pais:
                pais.append(melhor_caminho)

            return pais
                
        
        def crossover_pmx(pai1, pai2):
            a = pai1.split(' ')
            b = pai2.split(' ')
            n = len(a)

            # copia as bordas fixas 0 ... 0
            filho = ['0'] + [None] * (n-2) + ['0']

            # dois cortes aleatórios entre 1 e n-2
            p1, p2 = sorted(random.sample(range(1, n-1), 2))

            # copia o segmento do pai1
            for i in range(p1, p2 + 1):
                filho[i] = a[i]

            # aplica mapeamento PMX para preencher o restante com base no pai2
            for i in range(p1, p2 + 1):
                if b[i] not in filho:
                    pos = i
                    val = a[i]
                    while True:
                        pos = b.index(val)
                        if filho[pos] is None:
                            filho[pos] = b[i]
                            break
                        val = a[pos]

            # preenche os espaços vazios com os elementos restantes do pai2
            for i in range(1, n-1):
                if filho[i] is None:
                    filho[i] = b[i]

            return " ".join(filho)


        def crossover_populacao(pais, taxa_crossover):
            filhos = []
            custos_filhos = []
            indice = 0
            
            while len(filhos) < taxa_crossover:
                pai1 = pais[indice % len(pais)]
                pai2 = pais[(indice + 1) % len(pais)]
                filho = crossover_pmx(pai1, pai2)
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

                
        def mutacao(taxa_mutacao, caminhos, filhos_cross, custos_filhos_cross):
            prop_inversao_cross = 0.60
            prop_inversao_pop = 0.30
            prop_insert_pop = 0.10

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

            filhos_totais = filhos_cross + mutacoes if filhos_cross else mutacoes
            custos_totais = custos_filhos_cross + novos_custos if filhos_cross else novos_custos
            return filhos_totais, custos_totais
  
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

        
        def atualizarPopulacao(populacao, filhos, custos_pais, custos_filhos, tamanho_populacao):
            """
            Seleciona a nova população combinando diversidade e pressão seletiva.
            A seleção é por torneio k=3 entre todos os pais + filhos.
            Mantém exatamente `tamanho_populacao` indivíduos, sem elitismo obrigatório.
            """
            

            # junta todos os candidatos
            todos = populacao + filhos
            todos_custos = custos_pais + custos_filhos
            n_total = len(todos)

            # índice de referência
            indices = list(range(n_total))

            nova_pop = []
            nova_custos = []

            k = 3  # tamanho do torneio — bom equilíbrio (3 ou 4 recomendado)

            for _ in range(tamanho_populacao):
                # seleciona k candidatos
                competidores = random.sample(indices, k)
                # pega aquele com menor custo entre eles
                melhor_idx = min(competidores, key=lambda i: todos_custos[i])

                nova_pop.append(todos[melhor_idx])
                nova_custos.append(todos_custos[melhor_idx])

            return nova_pop, nova_custos

            
        # Execução das funções
        if caminho_do_arquivo.endswith('.txt'):
            global tamanho_populacao

            populacao = []

            tsp, dicDistancias, dicCasas = tornarTSPLIB() 
            print(dicCasas)
            #print(*tsp, sep='')
            qtdeCidades = len(dicCasas)
            
            nivel_de_geracoes = 1
            max_geracoes = 80
            tamanho_populacao = 300
            populacao = inicializaPopulacao(tamanho_populacao, qtdeCidades)
            custos, melhor_caminho, melhor_custo = (calculaAptidao(populacao, dicDistancias))
            dic_caminhos = dict(zip(populacao, custos)) # Adiciona todos os caminhos num dicionário
            #print(len(populacao),f'população inicial:\n{populacao}')
            filhos_cross = None
            melhores_das_geracoes = []
            melhores_custos_geracoes = []
            while (nivel_de_geracoes <= max_geracoes):                
            
                #taxa_mutacao = int(tamanho_populacao * (1 - (nivel_de_geracoes / max_geracoes)))
                #taxa_crossover = tamanho_populacao  *  (nivel_de_geracoes / max_geracoes)
                taxa_mutacao = int(tamanho_populacao * (random.randint(2, 10)*0.01))
                taxa_crossover = int(tamanho_populacao * 0.90)
                nivel_de_geracoes += 1  # Aumenta o nivel da geração
                
                if taxa_crossover != 0:
                    pais = torneioPais(populacao, custos, taxa_crossover, melhor_caminho)           # Seleciona num torneio binário
                    filhos_cross, custos_filhos_cross = crossover_populacao(pais, taxa_crossover)  # Ajuste: passar a quantidade
                    #print(f"{len(filhos_cross)} filhos gerados por crossover: \n{filhos_cross}")

                    #for i, filho in enumerate(filhos_cross):
                    #    print(f"  Filho {i+1}: {filho}, Custo: {custos_filhos_cross[i]}")

                if taxa_mutacao != 0:
                    filhos, novos_custos = mutacao(taxa_mutacao, populacao, filhos_cross, custos_filhos_cross)
                populacao, custos = atualizarPopulacao(populacao, filhos, custos, novos_custos, tamanho_populacao)
                melhor_caminho, melhor_custo = melhorDaGeracao(populacao, custos)
                #print(len(populacao))
                melhores_das_geracoes.append(melhor_caminho)
                melhores_custos_geracoes.append(melhor_custo)
                #print("→ filhos crossover:", len(filhos_cross))
                print(len(filhos))
            print(melhores_custos_geracoes)
            melhor_camino, melhor_custo = melhorDaGeracao(melhores_das_geracoes, melhores_custos_geracoes)
            caminho_numerado = melhor_caminho.split(' ')
            caminho_letrado = [letraCasas[int(cidade)] for cidade in caminho_numerado]
            caminho_formatado = " -> ".join(caminho_letrado)

            
            
        elif caminho_do_arquivo.endswith('.tsp'):
            linhas_tsp, dicDistancias, dicCasas = lerTSP(caminho_do_arquivo)
            # AQUI
            print('tsp')
            qtdeCidades = len(dicCasas)
            
            nivel_de_geracoes = 1
            max_geracoes = 80
            tamanho_populacao = 300
            populacao = inicializaPopulacao(tamanho_populacao, qtdeCidades)
            custos, melhor_caminho, melhor_custo = (calculaAptidao(populacao, dicDistancias))
            dic_caminhos = dict(zip(populacao, custos)) # Adiciona todos os caminhos num dicionário
            #print(len(populacao),f'população inicial:\n{populacao}')
            filhos_cross = None
            melhores_das_geracoes = []
            melhores_custos_geracoes = []
            while (nivel_de_geracoes <= max_geracoes):                
            
                #taxa_mutacao = int(tamanho_populacao * (1 - (nivel_de_geracoes / max_geracoes)))
                #taxa_crossover = tamanho_populacao  *  (nivel_de_geracoes / max_geracoes)
                taxa_mutacao = int(tamanho_populacao * (random.randint(2, 10)*0.01))
                taxa_crossover = int(tamanho_populacao * 0.90)
                nivel_de_geracoes += 1  # Aumenta o nivel da geração
                
                if taxa_crossover != 0:
                    pais = torneioPais(populacao, custos, taxa_crossover, melhor_caminho)           # Seleciona num torneio binário
                    filhos_cross, custos_filhos_cross = crossover_populacao(pais, taxa_crossover)  # Ajuste: passar a quantidade
                    #print(f"{len(filhos_cross)} filhos gerados por crossover: \n{filhos_cross}")

                    #for i, filho in enumerate(filhos_cross):
                    #    print(f"  Filho {i+1}: {filho}, Custo: {custos_filhos_cross[i]}")

                if taxa_mutacao != 0:
                    filhos, novos_custos = mutacao(taxa_mutacao, populacao, filhos_cross, custos_filhos_cross)
                populacao, custos = atualizarPopulacao(populacao, filhos, custos, novos_custos, tamanho_populacao)
                melhor_caminho, melhor_custo = melhorDaGeracao(populacao, custos)
                #print(len(populacao))
                melhores_das_geracoes.append(melhor_caminho)
                melhores_custos_geracoes.append(melhor_custo)
                #print("→ filhos crossover:", len(filhos_cross))
                print(len(filhos))
            print(melhores_custos_geracoes)
            melhor_camino, melhor_custo = melhorDaGeracao(melhores_das_geracoes, melhores_custos_geracoes)
            caminho_numerado = list(map(int, melhor_caminho.split(' ')))
            caminho_formatado = " -> ".join(map(str, caminho_numerado))

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

