# Fly Food 🚁 - Otimização de Rotas de Entrega 🗺️

<p align="center">
  

<p align="center">
  <img src="https://i.ibb.co/TxftJ0c5/Fly-food-logo.png" alt="Fly-food-logo" border="0">
</p>

</p>

<p align="center">
  <strong>Uma ferramenta de desktop para otimização de rotas de entrega, que calcula o caminho mais curto para visitar múltiplos pontos, oferecendo suporte a mapas de grade personalizados e formatos TSPLIB padrão.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/GUI-Tkinter-orange?style=for-the-badge" alt="Tkinter">
  <img src="https://img.shields.io/badge/Status-Funcional-green?style=for-the-badge" alt="Status: Funcional">
</p>

---

## 📜 Índice

1.  [Sobre o Projeto](#-sobre-o-projeto)
2.  [Preview da Aplicação](#-preview-da-aplicação)
3.  [Funcionalidades Principais](#-funcionalidades-principais)
4.  [Tecnologias Utilizadas](#-tecnologias-utilizadas)
5.  [Algoritmo de Otimização](#-algoritmo-de-otimização)
6.  [Suporte a Arquivos TSPLIB](#-suporte-a-arquivos-tsplib)
7.  [Como Executar](#-como-executar)
8.  [Formato do Arquivo de Entrada (Mapa de Grade)](#-formato-do-arquivo-de-entrada-mapa-de-grade)
9.  [Artigo cientifico](#-artigo-cientifico)
---

## 🎯 Sobre o Projeto

O **Fly Food** foi desenvolvido como uma solução avançada para o **Problema do Caixeiro Viajante (PCV)**. O objetivo é encontrar a rota mais eficiente para um drone de entrega que precisa partir de um ponto de origem, visitar uma série de destinos e retornar à base, minimizando a distância total percorrida.

A aplicação evoluiu para suportar duas abordagens de entrada de dados:

1.  **Mapas de Grade Personalizados:** Lidos a partir de arquivos de texto simples, onde a distância é calculada usando a **Métrica de Distância Manhattan**.
2.  **Arquivos TSPLIB:** Suporte a formatos padrão de PCV, permitindo a análise de grandes *benchmarks* como o **brasil58**, onde a distância é calculada com base nas coordenadas fornecidas.

Para lidar com a complexidade do PCV, o Fly Food utiliza um poderoso **Algoritmo Genético**, que busca encontrar soluções ótimas ou quase ótimas de forma eficiente, superando a limitação da força bruta em problemas de grande escala.

---

## ✨ Preview da Aplicação

A interface gráfica foi projetada para ser simples e direta, focando na usabilidade.

| Tela Principal | Resultado do Cálculo |
| :---: | :---: |
| *<center><img src="https://i.ibb.co/0yKr4HhP/unnamed.png" alt="unnamed" border="0"></center>* | *<center><img src="https://i.ibb.co/rR36mR0m/unnamed.png" alt="unnamed" border="0"></center>* |

---

## 🚀 Funcionalidades Principais

* **Interface Gráfica Intuitiva:** Uma janela simples construída com Tkinter para facilitar a interação.
* **Múltiplos Formatos de Entrada:** Suporte para **Mapas de Grade** personalizados e arquivos padrão **TSPLIB**.
* **Resolução de Problemas de Grande Escala:** Utiliza o **Algoritmo Genético** para encontrar rotas ótimas em instâncias complexas (e.g., brasil58).
* **Métricas de Distância Flexíveis:**
    * **Distância Manhattan:** Usada para mapas de grade.
    * **Distância Euclidiana/Coordenada:** Usada para arquivos TSPLIB (dependendo da especificação do arquivo).
* **Exibição Clara de Resultados:** Apresenta a menor distância encontrada, a sequência do caminho ideal e o tempo de processamento.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Propósito |
| :--- | :--- |
| **Python** | Linguagem principal do projeto. |
| **tkinter** | Biblioteca nativa para a construção da interface gráfica (GUI). |
| **numpy** | Utilizada para criar e gerenciar matrizes de distâncias de forma eficiente. |
| **time** | Para medir o desempenho e o tempo de execução do Algoritmo Genético. |
| **os** | Para operações do sistema operacional e manipulação de arquivos. |
| **random** | Essencial para as operações aleatórias do Algoritmo Genético (população inicial, mutações, etc.). |

---

## 🧬 Algoritmo de Otimização

O projeto utiliza um **Algoritmo Genético** para solucionar o Problema do Caixeiro Viajante (PCV).

### Componentes Chave

* **Crossover (Recombinação):**
    * **PMX (Partially Mapped Crossover):** Utilizado para gerar descendentes a partir de dois pais, garantindo a validade da rota (que todos os pontos sejam visitados exatamente uma vez).
* **Mutações:** Para introduzir diversidade na população e evitar mínimos locais.
    * **Swap (Troca):** Troca a posição de dois pontos aleatórios na rota.
    * **Insert (Inserção):** Move um ponto para uma posição diferente na rota.

---

## 📄 Suporte a Arquivos TSPLIB

A aplicação possui a capacidade de carregar e processar arquivos de *benchmark* do Problema do Caixeiro Viajante (PCV) no formato **TSPLIB**.

* **Objetivo:** Permitir a execução do Algoritmo Genético em instâncias clássicas e complexas, como a **brasil58**, utilizando as coordenadas e especificações de distância contidas no arquivo.

---

## ⚙️ Como Executar

Siga os passos abaixo para executar o Fly Food em seu ambiente local.

### Pré-requisitos
-   Python 3.10 ou superior
-   Git

### Passos

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Breno-Jansen/Flyfood---PISI-II---BDLP.git](https://github.com/Breno-Jansen/Flyfood---PISI-II---BDLP.git)
    ```

2.  **Crie e ative um ambiente virtual (Recomendado):**
    ```bash
    # Cria o ambiente
    python -m venv venv

    # Ativa o ambiente
    # No Windows:
    venv\Scripts\activate
    # No macOS/Linux:
    source venv/bin/activate
    ```
    
3.  **Instale as bibliotecas:**
    
    ```bash
    pip install numpy
    pip install pillow
    ```

4.  **Execute a aplicação:**
    O ponto de entrada da interface gráfica é o arquivo `main.py`.
    ```bash
    python main.py
    ```

---

## 📄 Formato do Arquivo de Entrada (Mapa de Grade)

Para que o cálculo do mapa de grade funcione corretamente, o arquivo `.txt` deve seguir uma estrutura específica:

1.  A **primeira linha** deve conter as dimensões da grade: `Linhas Colunas` (separadas por um espaço).
2.  As **linhas seguintes** devem representar a grade, onde:
    -   `0` representa um espaço vazio.
    -   `R` representa o ponto de partida e de chegada (origem).
    -   Qualquer outra letra (ex: `A`, `B`, `C`) representa um ponto de entrega.

**Exemplo de um arquivo `mapa.txt` válido:**

4 4<br> 
R 0 A 0<br>
0 0 0 B<br>
0 C 0 0<br>
0 0 0 0

---

## 📜 Artigo Científico

O desenvolvimento do **Fly Food** e a aplicação do **Algoritmo Genético** para a solução do PCV foram detalhados em um artigo científico. Este artigo descreve a metodologia, a implementação do *crossover* PMX e das mutações (*Swap* e *Insert*), além de apresentar os resultados comparativos de desempenho em relação a outras abordagens.

Para acesso completo ao material e à análise de dados, o PDF está disponível abaixo:

* **🔗 Link para o Artigo Completo (PDF):**
    [Clique aqui para visualizar o PDF do Artigo Científico](https://drive.google.com/file/d/1xAJZ3yPG_-6kCIsO4jt7Iox3XkFw8eRz/view?usp=sharing)

* **📝 Projeto FlyFood:** *Otimização de Rotas de Entrega utilizando Algoritmo Genético em Ambientes de Grade e TSPLIB*

