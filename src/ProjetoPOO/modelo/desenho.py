class Desenho:
    """Modelo que mantém a lista de figuras já confirmadas no desenho.

    Não sabe nada sobre Tkinter nem sobre a interface: é pura lógica/estado.
    """

    def __init__(self):
        self._figuras = []

    def adicionar_figura(self, figura):
        """Adiciona a figura à coleção, ignorando figuras incompletas
        (ex.: uma linha sem comprimento ou um rabisco com um único ponto)."""
        if not figura.incompleto():
            self._figuras.append(figura)

    def limpar(self):
        self._figuras = []

    def obter_figuras(self):
        return self._figuras
