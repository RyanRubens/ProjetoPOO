from ..modelo import *
from .estado_desenho import EstadoOcioso

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
        'Poligono': lambda x, y, cor_cont, cor_pren: Poligono(x, y, cor_cont, cor_pren),
        'PoligonoRegular': lambda x, y, cor_cont, cor_pren: PoligonoRegular(x, y, 0, cor_cont, cor_pren),
    }

    def __init__(self, desenho, janela):
        self.desenho = desenho
        self.janela = janela
        self.figura_atual = None
        self.estado = EstadoOcioso()
        self.pilha_desfazer = []
        self.pilha_refazer = []

        self.figuras_selecionadas = []
        self.buffer_copia = []
        self.ultimo_x = None
        self.ultimo_y =None
        self.retangulo_inicio = None

        self.janela.vincular_eventos(
            ao_pressionar=self.ao_pressionar,
            ao_mover=self.ao_mover,
            ao_soltar=self.ao_soltar,
            ao_finalizar=self.ao_finalizar,
            ao_limpar=self.limpar_tela,
        )
        
        self.janela.vincular_teclado(
            ao_apagar=self.ao_apagar,
            ao_mover_frente=self.ao_mover_frente,
            ao_mover_tras=self.ao_mover_tras,
            ao_mover_topo=self.ao_mover_topo,
            ao_mover_fundo=self.ao_mover_fundo,
            ao_copiar=self.ao_copiar,
            ao_colar=self.ao_colar,
            ao_desfazer=self.desfazer,
            ao_refazer=self.refazer,
        )
        self.janela.vincular_mudanca_cor(self.ao_mudar_cor)

    #------Delegação dos eventos do estado do mouse----
    def ao_pressionar(self, event):
        self.estado.ao_pressionar(self, event)

    def ao_mover(self, event):
        self.estado.ao_mover(self, event)

    def ao_soltar(self, event):
        self.estado.ao_soltar(self, event)

    def ao_finalizar(self, event):
        self.estado.ao_finalizar(self, event)

    #-----Delegação de eventos selecao-----#
    def ao_apagar(self, event=None):
        self.estado.ao_apagar(self)

    def ao_mover_frente(self, event=None):
        self.estado.ao_mover_frente(self)

    def ao_mover_tras(self, event=None):
        self.estado.ao_mover_tras(self)

    def ao_mover_topo(self, event=None):
        self.estado.ao_mover_topo(self)

    def ao_mover_fundo(self, event=None):
        self.estado.ao_mover_fundo(self)

    def ao_copiar(self, event=None):
        self.estado.ao_copiar(self)

    def ao_colar(self, event=None):
        self.estado.ao_colar(self)

    def ao_mudar_cor(self, *_args):
        self.estado.ao_mudar_cor(self)

    def ao_agrupar(self, event=None):
        self.estado.ao_agrupar(self)

    def ao_desagrupar(self, event=None):
        self.estado.ao_desagrupar(self)

    #___________________#
    def mudar_estado(self, novo_estado):
        self.estado = novo_estado

    def criar_figura(self, tipo, x, y, cor_cont, cor_pren):
        criador = self.CRIADORES.get(tipo)
        if criador is None:
            return None
        return criador(x, y, cor_cont, cor_pren)

    def redesenhar_com_temporaria(self):
        self.janela.redesenhar(self.desenho.obter_figuras())
        self.janela.desenhar_temporaria(self.figura_atual)

    def redesenhar_com_selecao(self):
        self.janela.redesenhar(self.desenho.obter_figuras(), self.figuras_selecionadas)

    def redesenhar_com_retangulo(self, x1, y1, x2, y2):
        self.janela.redesenhar(self.desenho.obter_figuras(), self.figuras_selecionadas)
        self.janela.desenhar_retangulo_selecao(x1, y1, x2, y2)
        
    def confirmar_figura_atual(self):
        if self.figura_atual is not None:
            self.salvar_estado()
            self.desenho.adicionar_figura(self.figura_atual)
            self.figura_atual = None
        self.janela.redesenhar(self.desenho.obter_figuras(), self.figuras_selecionadas)

    def salvar_estado(self):
        """Chamado ANTES de qualquer ação que modifique o desenho."""
        self.pilha_desfazer.append(self.desenho.obter_estado())
        self.pilha_refazer.clear()

    def desfazer(self, event=None):
        if not self.pilha_desfazer:
            return
        self.pilha_refazer.append(self.desenho.obter_estado())
        estado_anterior = self.pilha_desfazer.pop()
        self.desenho.restaurar_estado(estado_anterior)
        self.figuras_selecionadas = []
        self.mudar_estado(EstadoOcioso())
        self.redesenhar_com_selecao()

    def refazer(self, event=None):
        if not self.pilha_refazer:
            return
        self.pilha_desfazer.append(self.desenho.obter_estado())
        proximo_estado = self.pilha_refazer.pop()
        self.desenho.restaurar_estado(proximo_estado)
        self.figuras_selecionadas = []
        self.mudar_estado(EstadoOcioso())
        self.redesenhar_com_selecao()

    def limpar_tela(self):
        self.desenho.limpar()
        self.figuras_selecionadas = []
        self.mudar_estado(EstadoOcioso())
        self.janela.limpar_canvas()
