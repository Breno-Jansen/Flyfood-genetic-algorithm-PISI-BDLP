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
    filetypes = (('All Files', '*.*'), ('tsp files', '*.tsp'))
    fpath = filedialog.askopenfilename(title="Selecione o arquivo de matriz", filetypes=filetypes,)
    if fpath:
        caminho_do_arquivo = fpath
        entry_widget.delete("1.0", "end")
        entry_widget.insert("1.0", f"Arquivo carregado:\n{os.path.basename(caminho_do_arquivo)}")

letraCasas = []
def executar_calculo(entry_widget):
    contador_de_tempo = time.perf_counter()    
    global caminho_do_arquivo, letraCasas
    letraCasas.clear()  # limpa sempre
    # Verifica se um arquivo foi selecionado primeiro
    if not caminho_do_arquivo:
        entry_widget.delete("1.0", "end")
        entry_widget.insert("1.0", "Erro: Por favor, carregue um arquivo .txt primeiro.")
        return

    try:
            
        entry_widget.delete("1.0", "end")
        entry_widget.insert("1.0", f"Calculando.")
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

            with open (f'created_file{int(time.time())}.tsp', "w", encoding="utf-8") as tsp:
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
                    if a == b:  # não deveria acontecer
                        continue
                    try:
                        soma_individual += dicDistancias[(min(a, b), max(a, b))]
                    except KeyError:
                        print(f"Par {(a,b)} não encontrado no dicionário")
                        
                return soma_individual


        def inicializaPopulacao(tamanho, qtdeCidades):
            populacao = []
            lista_iniciar = list(range(qtdeCidades))  # todas as cidades
            #print(lista_iniciar)
            for _ in range(tamanho):
                # escolhe ponto inicial aleatório
                ponto_inicial = random.choice(lista_iniciar)

                # cria lista de cidades sem o ponto inicial
                restantes = [c for c in lista_iniciar if c != ponto_inicial]
                random.shuffle(restantes)

                # monta indivíduo: começa e termina no ponto inicial
                individuo_base = str(ponto_inicial) + " " + " ".join(map(str, restantes)) + " " + str(ponto_inicial)

                populacao.append(individuo_base)
                #print(individuo_base)
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
            
        def torneioPais(populacao, custos, taxa_crossover, melhor_caminho=None, k=4,):
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

            # bordas dos pais devem ser iguais (ciclo fechado), mas o start pode ser diferente entre pais
            assert a[0] == a[-1], "Pai1 inválido: não fecha ciclo"
            assert b[0] == b[-1], "Pai2 inválido: não fecha ciclo"

            s = a[0]  # start do filho será o start do pai1

            # miolos (sem as bordas)
            miolo_a = a[1:n-1]
            miolo_b = b[1:n-1]

            # se o start dos pais for diferente, precisamos garantir que nenhum miolo contém 's'
            # e que ambos os miolos têm o mesmo universo de cidades exceto 's'
            # remove 's' do miolo_b se por algum motivo entrou
            miolo_b = [x for x in miolo_b if x != s]
            # também garanta que miolo_a não tenha 's'
            miolo_a = [x for x in miolo_a if x != s]

            # universo esperado: todas as cidades exceto s
            universo = set(a) - {s}
            # garante comprimento correto
            if len(miolo_a) != n-2 or len(miolo_b) != n-2:
                # se algum estiver com tamanho errado, tente reparar completando faltantes pela ordem de b
                faltantes = [x for x in b[1:n-1] if x != s and x not in miolo_a]
                miolo_a = miolo_a + faltantes
                faltantes = [x for x in a[1:n-1] if x != s and x not in miolo_b]
                miolo_b = miolo_b + faltantes
                miolo_a = miolo_a[:n-2]
                miolo_b = miolo_b[:n-2]

            # PMX sobre miolos
            filho_miolo = [None] * (n-2)
            p1, p2 = sorted(random.sample(range(0, n-2), 2))

            # copia segmento de miolo_a
            for i in range(p1, p2+1):
                filho_miolo[i] = miolo_a[i]

            # mapeamento PMX usando miolo_b
            for i in range(p1, p2+1):
                val_b = miolo_b[i]
                if val_b not in filho_miolo:
                    pos = i
                    val = miolo_a[i]
                    while True:
                        try:
                            pos = miolo_b.index(val)
                        except ValueError:
                            # se não achar (pais estranhos), sai e deixa completar depois
                            break
                        if filho_miolo[pos] is None:
                            filho_miolo[pos] = val_b
                            break
                        val = miolo_a[pos]

            # completa posições vazias com elementos de miolo_b
            for i in range(0, n-2):
                if filho_miolo[i] is None:
                    candidato = miolo_b[i]
                    if candidato in filho_miolo or candidato == s:
                        # pega primeiro faltante na ordem de miolo_b
                        faltantes = [x for x in miolo_b if x not in filho_miolo and x != s]
                        candidato = faltantes[0] if faltantes else candidato
                    filho_miolo[i] = candidato

            # reconstrói filho com bordas s ... s
            filho = [s] + filho_miolo + [s]
            return " ".join(filho)


        def crossover_populacao(pais, taxa_crossover):
            filhos = []
            custos_filhos = []
            indice = 0
            
            while len(filhos) < taxa_crossover:
                pai1 = pais[indice % len(pais)]
                pai2 = pais[(indice + 1) % len(pais)]
                filho = crossover_pmx(pai1, pai2)
                # valida antes de aceitar
                if validar_individuo(filho, qtdeCidades):
                    filhos.append(filho)
                    custos_filhos.append(custoCaminho(filho, dicDistancias))
                indice += 1

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
                        # só índices do miolo: 1 .. n_cidades-2
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

                        # força bordas iguais ao pai
                        filho[0] = individuo[0]
                        filho[-1] = individuo[-1]

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

            # inversão população
            inversao(caminhos, mutacoes, novos_custos, inversao_pop)

            # inversão filhos crossover
            if filhos_cross:
                inversao(filhos_cross, mutacoes, novos_custos, inversao_cross)

            # inserção
            max_inserts = min(insert_pop, len(caminhos))
            try:
                for l in range(max_inserts):
                    individuo_insert = caminhos[l].split(' ')
                    n_cidades = len(individuo_insert)

                    erro = True
                    tentativas = 0
                    while erro and tentativas < 30:
                        tentativas += 1
                        # só índices do miolo
                        pos_origem = random.randint(1, n_cidades - 2)
                        pos_destino = random.randint(1, n_cidades - 2)
                        if pos_origem == pos_destino:
                            continue

                        filho = individuo_insert[:]
                        cidade = filho.pop(pos_origem)
                        filho.insert(pos_destino, cidade)

                        # força bordas iguais ao pai
                        filho[0] = individuo_insert[0]
                        filho[-1] = individuo_insert[-1]

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

        def validar_individuo(ind_str, qtdeCidades):
            genes = list(map(int, ind_str.split()))
            if genes[0] != genes[-1]:
                return False
            s = genes[0]
            miolo = genes[1:-1]
            esperado = set(range(qtdeCidades)) - {s}
            return set(miolo) == esperado and len(miolo) == len(esperado)

        def mensagens(entry_widget, mensagem):
            entry_widget.insert("1.0", mensagem)
            entry_widget.update_idletasks()

        # Execução das funções
        if caminho_do_arquivo.endswith('.txt'):
            global tamanho_populacao

            populacao = []

            tsp, dicDistancias, dicCasas = tornarTSPLIB() 
            print(len(dicCasas))
            #print(*tsp, sep='')
            qtdeCidades = len(dicCasas)
            
            nivel_de_geracoes = 1
            max_geracoes = 70
            tamanho_populacao = 400
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
                taxa_mutacao = int(tamanho_populacao * (random.randint(2, 6)*0.01))
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
                #print(len(filhos))
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
            max_geracoes = 2000
            tamanho_populacao = 1000
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
                taxa_mutacao = int(tamanho_populacao * (random.randint(2, 6)*0.01))
                taxa_crossover = int(tamanho_populacao * 0.85)
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
                #print(len(filhos))
                if nivel_de_geracoes == max_geracoes//5:
                    mensagem = (
                        f"👶 gerando individuos..\n\n"
                    )
                    mensagens(entry_widget, mensagem)
                if nivel_de_geracoes == 2*(max_geracoes//5):
                    mensagem = (
                        f"🏆 fazendo torneios...\n\n"
                    )
                    mensagens(entry_widget, mensagem)
                if nivel_de_geracoes == 3*(max_geracoes//5):
                    mensagem = (
                        f"❤️ pais cruzando....\n\n"
                    )
                    mensagens(entry_widget, mensagem)
                if nivel_de_geracoes == 4*(max_geracoes//5):
                    mensagem = (
                        f"🧬 mutantes aparecendo.....\n\n"
                    )
                    mensagens(entry_widget, mensagem)
            print(melhores_custos_geracoes)
            melhor_camino, melhor_custo = melhorDaGeracao(melhores_das_geracoes, melhores_custos_geracoes)
            caminho_numerado = list(map(int, melhor_caminho.split(' ')))
            caminho_formatado = " -> ".join(map(str, caminho_numerado)) 
                         

        else:
            mensagem_erro = (
                f"Ocorreu um erro:\nTecnicamente: {e}\n\nVerifique se o formato do arquivo .txt está na forma certa:\n"
                "EX:\n"
                "33\n"
                "C00\n00B\nR0A\n")
            entry_widget.delete("1.0", "end")
            entry_widget.insert("1.0", mensagem_erro)
            entry_widget.update_idletasks()
           

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
        
        mensagem_erro = (
            f"Ocorreu um erro:\nTecnicamente: {e}\n\nVerifique se o formato do arquivo .txt está na forma certa:\n"
            "EX:\n"
            "33\n"
            "C00\n00B\nR0A\n")
        entry_widget.delete("1.0", "end")
        entry_widget.insert("1.0", mensagem_erro)
        entry_widget.update_idletasks()