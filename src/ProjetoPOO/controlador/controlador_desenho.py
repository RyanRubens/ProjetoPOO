from ..modelo import Linha, Oval, Circulo, Rabisco


class ControladorDesenho:
    """Controlador: reage aos eventos de mouse vindos da view, cria/atualiza
    figuras e as guarda no modelo, e pede à view para redesenhar.
    """

    # Mapeia o texto do menu de tipos para a classe de figura correspondente.
    # Adicionar uma nova figura ao combo da view + uma entrada aqui é o
    # suficiente para o app passar a suportá-la.
    CRIADORES = {
        'Linha': lambda x, y, cor_cont, cor_pren: Linha(x, y, x, y, cor_cont),
        'Oval': lambda x, y, cor_cont, cor_pren: Oval(x, y, x, y, cor_cont, cor_pren),
        'Circulo': lambda x, y, cor_cont, cor_pren: Circulo(x, y, 0, cor_cont, cor_pren),
        'Rabisco': lambda x, y, cor_cont, cor_pren: Rabisco(x, y, cor_cont),
    }

    def __init__(self, desenho, janela):
        self.desenho = desenho
        self.janela = janela
        self.figura_atual = None

        self.janela.vincular_eventos(
            ao_pressionar=self.iniciar_figura,
            ao_mover=self.atualizar_figura,
            ao_soltar=self.concluir_figura,
            ao_limpar=self.limpar_tela,
        )

    def iniciar_figura(self, event):
        """Chamado quando o botão do mouse é pressionado no canvas."""
        cor_contorno = self.janela.obter_cor_contorno()
        cor_preenchimento = self.janela.obter_cor_preenchimento()
        tipo = self.janela.obter_tipo_figura()

        criador = self.CRIADORES.get(tipo)
        if criador is not None:
            self.figura_atual = criador(event.x, event.y, cor_contorno, cor_preenchimento)

    def atualizar_figura(self, event):
        """Chamado quando o mouse se move com o botão pressionado."""
        if self.figura_atual is None:
            return
        self.figura_atual.atualizar(event.x, event.y)
        self.janela.redesenhar(self.desenho.obter_figuras())
        self.janela.desenhar_temporaria(self.figura_atual)

    def concluir_figura(self, event):
        """Chamado quando o botão do mouse é solto."""
        if self.figura_atual is not None:
            self.desenho.adicionar_figura(self.figura_atual)
            self.figura_atual = None
        self.janela.redesenhar(self.desenho.obter_figuras())

    def limpar_tela(self):
        self.desenho.limpar()
        self.janela.limpar_canvas()
