from projeto_poo.modelo import Desenho
from projeto_poo.visao import JanelaDesenho
from projeto_poo.controlador import ControladorDesenho


def main():
    desenho = Desenho()          # Model
    janela = JanelaDesenho()     # View
    ControladorDesenho(desenho, janela)  # Controller liga Model <-> View
    janela.iniciar()


if __name__ == '__main__':
    main()
