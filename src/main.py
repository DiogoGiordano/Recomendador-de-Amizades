import json
import subprocess
import sys

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


# Cria a conexao entre cada usuario baseado nas amizades do dataset (Sem peso de tempo ainda)
def connect_friends_in_graph():
    for node in grafo.nodes():
        for i in range(len(dataset["amizades"])):
            if grafo.nodes[node]["id"] == dataset["amizades"][i]["usuario1_id"]:
                grafo.add_edge(node, dataset["amizades"][i]["usuario2_id"])
                print("Nome do usuario: ", grafo.nodes[node]["nome"])
                print("Id usuario 1: ", dataset["amizades"][i]["usuario1_id"])
                print("Id Usuario 2: ", dataset["amizades"][i]["usuario2_id"])


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

    connect_friends_in_graph()

    nx.draw(grafo, with_labels=True, node_color='skyblue', node_size=700, edge_color='black', linewidths=1,
            font_size=15)
    plt.show()
