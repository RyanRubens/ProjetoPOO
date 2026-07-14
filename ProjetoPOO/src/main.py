from .modelo import Desenho
from .visao import JanelaDesenho
from .controlador import ControladorDesenho


def main():
    desenho = Desenho()          # Model
    janela = JanelaDesenho()     # View
    ControladorDesenho(desenho, janela)  # Controller liga Model <-> View
    janela.iniciar()


if __name__ == '__main__':
    main()
