import json
import subprocess
import sys
from datetime import datetime


# funcao para realizar a instalacao de um pacote (networkx)
def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Pacote '{package}' instalado com sucesso.")
        import networkx as nx
    except subprocess.CalledProcessError as e:
        print(f"Erro ao tentar instalar o pacote '{package}'.")
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


try:
    import networkx as nx

except ModuleNotFoundError:
    install_package("networkx")

try:
    import matplotlib.pyplot as plt

except ModuleNotFoundError:
    install_package("matplotlib")


#cria a conexao entre cada usuario baseado nas amizades do dataset e retorna uma lista com peso de cada aresta (Pode ser extraido outros metodos apartir desse)
def connect_friends_in_graph():
    # lista que vai conter os nodos e o peso entre eles
    lista = []

    dataset_amizades = dataset["amizades"]


    for node in grafo.nodes():
        for i in range(len(dataset_amizades)):
            if grafo.nodes[node]["id"] == dataset_amizades[i]["usuario1_id"]:
                # calcula o tempo de amizade em dias e com base no numero de dias calcula um peso
                tempo = datetime.now() - datetime.strptime(dataset_amizades[i]["data_inicio"], "%Y-%m-%d")
                peso = calculate_friendship_time(tempo.days)

                # adiciona uma aresta que conecta os dois nodos
                grafo.add_edge(node, dataset_amizades[i]["usuario2_id"])

                # prints de teste
                # printa o nome do usuario da iteracao e o id dos dois usuarios que possuem uma amizade
                print("\nNome do usuario: ", grafo.nodes[node]["nome"])
                print("Id usuario 1: ", dataset_amizades[i]["usuario1_id"])
                print("Id Usuario 2: ", dataset_amizades[i]["usuario2_id"])
                print("Peso da amizade: ", peso)

                # adiciona na lista os dados de user 1 e 2, e o peso da realacao deles
                lista.append((dataset_amizades[i]["usuario1_id"], dataset_amizades[i]["usuario2_id"], peso))


    return lista

#faz a apresentacao do grafico
def present(grafo, lista):

    # converte a lista para um dicionario
    edge_labels = {(source, target): count for source, target, count in lista}

    # posicao das arestas
    pos = nx.spring_layout(grafo)

    # desenha o grafo
    nx.draw(grafo, pos, with_labels=True)

    # peso das arestas
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=edge_labels)

    plt.show()

#calcula o peso com base no tempo (Em dias) de amizade
def calculate_friendship_time(days):
    contador = 0

    while days > 200:
        contador += 1
        days -= 200

    return contador


if __name__ == '__main__':
    # Leitura do dataset
    dataset_path = 'dataset_rede_social_ficticia.json'
    with open(dataset_path, 'r') as dataset_file:
        dataset = json.load(dataset_file)

    # Criacao do grado
    grafo = nx.Graph()

    # Iterando sobre o dataset para adicionar um nodo para cada usuario e os atributos do nodo (ID e Nome)
    for i in range(len(dataset["usuarios"])):
        grafo.add_node(dataset["usuarios"][i]["id"])
        attrs = {i + 1: {"id": dataset["usuarios"][i]["id"], "nome": dataset["usuarios"][i]["nome"]}}
        nx.set_node_attributes(grafo, attrs)

    # Printa do atributo de nome de casa nodo
    for i in grafo.nodes():
        print("Nome do usuario: ", grafo.nodes[i]["nome"])

    # recebe a lista retornada
    lista = connect_friends_in_graph()
    
    present(grafo, lista)
