import matplotlib.pyplot as plt
import networkx as nx

class No:
    def __init__(self, v):
        self.v = v
        self.e = None
        self.d = None
        self.h = 1

def altura(n):
    if not n:
        return 0
    return n.h

def fator(n):
    return altura(n.e) - altura(n.d)

def rotacao_direita(y):
    x = y.e
    t = x.d
    x.d = y
    y.e = t
    y.h = 1 + max(altura(y.e), altura(y.d))
    x.h = 1 + max(altura(x.e), altura(x.d))
    return x

def rotacao_esquerda(x):
    y = x.d
    t = y.e
    y.e = x
    x.d = t
    x.h = 1 + max(altura(x.e), altura(x.d))
    y.h = 1 + max(altura(y.e), altura(y.d))
    return y

def inserir(r, v):
    if not r:
        return No(v)
    if v < r.v:
        r.e = inserir(r.e, v)
    elif v > r.v:
        r.d = inserir(r.d, v)
    else:
        return r
    r.h = 1 + max(altura(r.e), altura(r.d))
    f = fator(r)
    if f > 1 and v < r.e.v:
        return rotacao_direita(r)
    if f < -1 and v > r.d.v:
        return rotacao_esquerda(r)
    if f > 1 and v > r.e.v:
        r.e = rotacao_esquerda(r.e)
        return rotacao_direita(r)
    if f < -1 and v < r.d.v:
        r.d = rotacao_direita(r.d)
        return rotacao_esquerda(r)
    return r

def menor(n):
    atual = n
    while atual.e:
        atual = atual.e
    return atual

def remover(r, v):
    if not r:
        return r
    if v < r.v:
        r.e = remover(r.e, v)
    elif v > r.v:
        r.d = remover(r.d, v)
    else:
        if not r.e:
            return r.d
        elif not r.d:
            return r.e
        t = menor(r.d)
        r.v = t.v
        r.d = remover(r.d, t.v)
    r.h = 1 + max(altura(r.e), altura(r.d))
    f = fator(r)
    if f > 1 and fator(r.e) >= 0:
        return rotacao_direita(r)
    if f > 1 and fator(r.e) < 0:
        r.e = rotacao_esquerda(r.e)
        return rotacao_direita(r)
    if f < -1 and fator(r.d) <= 0:
        return rotacao_esquerda(r)
    if f < -1 and fator(r.d) > 0:
        r.d = rotacao_direita(r.d)
        return rotacao_esquerda(r)
    return r

def busca(r, v):
    if not r:
        return None
    if v == r.v:
        return r
    if v < r.v:
        return busca(r.e, v)
    return busca(r.d, v)

def montar_grafo(r, g, p=None):
    if not r:
        return
    g.add_node(r.v)
    if p is not None:
        g.add_edge(p, r.v)
    if r.e:
        montar_grafo(r.e, g, r.v)
    if r.d:
        montar_grafo(r.d, g, r.v)

def plotar(r):
    g = nx.DiGraph()
    montar_grafo(r, g)
    pos = hierarchy_pos(g, raiz(r))
    plt.figure(figsize=(10,6))
    nx.draw(g, pos, with_labels=True, node_size=800)
    plt.show()

def raiz(r):
    return r.v if r else None

def hierarchy_pos(g, r, width=1, vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None):
    if pos is None:
        pos = {}
    pos[r] = (xcenter, vert_loc)
    filhos = list(g.successors(r))
    if filhos:
        dx = width/2
        for i, f in enumerate(filhos):
            pos = hierarchy_pos(g, f, width=dx, vert_gap=vert_gap,
                                vert_loc=vert_loc-vert_gap,
                                xcenter=xcenter + (i-0.5)*dx,
                                pos=pos, parent=r)
    return pos

nums = [15, 10, 20, 8, 12, 17, 25, 6, 11, 13]
raiz_arvore = None
for n in nums:
    raiz_arvore = inserir(raiz_arvore, n)

while True:
    op = input('i inserir  r remover  p procurar  s sair: ')
    if op == 'i':
        v = int(input('valor: '))
        raiz_arvore = inserir(raiz_arvore, v)
        plotar(raiz_arvore)
    elif op == 'r':
        v = int(input('valor: '))
        raiz_arvore = remover(raiz_arvore, v)
        plotar(raiz_arvore)
    elif op == 'p':
        v = int(input('valor: '))
        x = busca(raiz_arvore, v)
        if x:
            raiz_arvore = remover(raiz_arvore, v)
        plotar(raiz_arvore)
    elif op == 's':
        break
