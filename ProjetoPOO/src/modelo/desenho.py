class Desenho:
    """Modelo que mantém a lista de figuras já confirmadas no desenho.

    A ordem da lista define a ordem de desenho (z-order): o índice 0 é
    desenhado primeiro (fica no fundo) e o último índice é desenhado por
    último (fica no topo, por cima das demais).
    """

    def __init__(self):
        self._figuras = []

    def adicionar_figura(self, figura):
        """Adiciona a figura à coleção, ignorando figuras incompletas
        (ex.: uma linha sem comprimento ou um rabisco com um único ponto)."""
        if not figura.incompleto():
            self._figuras.append(figura)
    
    def remover_figura(self, figura):
        if figura in self._figuras:
            self._figuras.remove(figura)

    def figura_no_ponto(self, x, y):
        for figura in reversed(self._figuras):
            if figura.contem_ponto(x, y):
                return figura
        return None

    #Metodos seleção#
    def mover_para_frente(self, figura):
        if figura not in self._figuras:
            return
        i = self._figuras.index(figura)
        if i < len(self._figuras) - 1:
            self._figuras[i], self._figuras[i + 1] = self._figuras[i + 1], self._figuras[i]

    def mover_para_tras(self, figura):
        if figura not in self._figuras:
            return
        i = self._figuras.index(figura)
        if i > 0:
            self._figuras[i], self._figuras[i - 1] = self._figuras[i - 1], self._figuras[i]

    def mover_para_topo(self, figura):
        if figura in self._figuras:
            self._figuras.remove(figura)
            self._figuras.append(figura)

    def mover_para_fundo(self, figura):
        if figura in self._figuras:
            self._figuras.remove(figura)
            self._figuras.insert(0, figura)
            
    def limpar(self):
        self._figuras = []

    def obter_figuras(self):
        return self._figuras
