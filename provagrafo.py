import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:

    def insert(self, root, key):
        if not root:
            return Node(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        balance = self.getBalance(root)

        if balance > 1 and key < root.left.key:
            return self.rightRotate(root)
        if balance < -1 and key > root.right.key:
            return self.leftRotate(root)
        if balance > 1 and key > root.left.key:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
        if balance < -1 and key < root.right.key:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def delete(self, root, key):

        if not root:
            return root
        elif key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            
            if not root.left:
                return root.right
            elif not root.right:
                return root.left

            temp = self.getMinValue(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)

        if not root:
            return root

        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        balance = self.getBalance(root)

        if balance > 1 and self.getBalance(root.left) >= 0:
            return self.rightRotate(root)
        if balance > 1 and self.getBalance(root.left) < 0:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
        if balance < -1 and self.getBalance(root.right) <= 0:
            return self.leftRotate(root)
        if balance < -1 and self.getBalance(root.right) > 0:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def getMinValue(self, node):
        while node.left:
            node = node.left
        return node

    def leftRotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        return y

    def rightRotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        return y

    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

def add_edges(G, node, pos={}, x=0, y=0, layer=1):
    if not node:
        return

    pos[node.key] = (x, y)

    dx = 1 / (2 ** layer)

    if node.left:
        G.add_edge(node.key, node.left.key)
        add_edges(G, node.left, pos, x - dx, y - 1, layer + 1)

    if node.right:
        G.add_edge(node.key, node.right.key)
        add_edges(G, node.right, pos, x + dx, y - 1, layer + 1)

    return pos


def plot_tree(root):
    G = nx.DiGraph()
    pos = add_edges(G, root)

    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True,
            node_size=2500, node_color="#4DA8DA",
            font_size=12, font_weight="bold",
            arrows=False)

    plt.title("Árvore Binária (AVL) Balanceada")
    plt.show()

if __name__ == "__main__":
    tree = AVLTree()
    root = None

    valores = [3, 5, 8, 12, 15, 18, 25, 27, 30, 32, 35, 37, 40, 41, 45, 48, 50, 53, 55, 58, 60, 62, 70, 75]
    # valores = [1,2,3,4,5,6,7,8,9,10]

    for v in valores:
        root = tree.insert(root, v)

    plot_tree(root)

    while True:
        print("\nO que deseja fazer?")
        print("1 - Inserir elemento")
        print("2 - Remover elemento")
        print("3 - Procurar elemento")
        print("4 - Sair")

        op = input("Escolha: ")

        if op == "1":
            n = int(input("Valor para inserir: "))
            root = tree.insert(root, n)
            plot_tree(root)

        elif op == "2":
            n = int(input("Valor para remover: "))
            root = tree.delete(root, n)
            plot_tree(root)

        elif op == "3":
            n = int(input("Valor para procurar: "))
            def busca(root, v):
                if not root: return False
                if root.key == v: return True
                if v < root.key: return busca(root.left, v)
                return busca(root.right, v)

            if busca(root, n):
                print("➡ Valor encontrado! Removendo da árvore...")
                root = tree.delete(root, n)
                plot_tree(root)
            else:
                print("Valor não encontrado!")

        elif op == "4":
            break
        else:
            print("Opção inválida!")
