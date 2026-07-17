import copy
from abc import ABC, abstractmethod
from ..modelo import FiguraComposta

DESLOCAMENTO_COLAR = 15
MASCARA_SHIFT = 0x0001  # bit de Shift em event.state (Tkinter)

CTRL = 0x0004


def _selecionar_com_modificador(contexto, figura, event):
    """Leva em conta o CTRL aticado, se estiver adciona a figura ás selecionadas,
    se nçao roda como ao_pressionar normal (nçao muda pra estadoOcioso).
    Caso já esteja selecionada remove"""
    if event.state & CTRL:
        if figura in contexto.figuras_selecionadas:
            contexto.figuras_selecionadas.remove(figura)
        else:
            contexto.figuras_selecionadas.append(figura)
    elif figura not in contexto.figuras_selecionadas:
        contexto.figuras_selecionadas = [figura]


class EstadoDesenho(ABC):
    """Interface do padrão State."""

    @abstractmethod
    def ao_pressionar(self, contexto, event):
        """Botão do mouse pressionado no canvas."""
        raise NotImplementedError

    @abstractmethod
    def ao_mover(self, contexto, event):
        """Mouse movido com o botão pressionado."""
        raise NotImplementedError

    @abstractmethod
    def ao_soltar(self, contexto, event):
        """Botão do mouse solto."""
        raise NotImplementedError

    @abstractmethod
    def ao_finalizar(self, contexto, event):
        """Botão direito do mouse: finaliza figuras de múltiplos cliques
        (ex.: o Polígono), que não têm um evento natural de 'soltar'."""
        raise NotImplementedError

    #Ações seleção
    def ao_apagar(self, contexto):
        pass

    def ao_mover_frente(self, contexto):
        pass

    def ao_mover_tras(self, contexto):
        pass

    def ao_mover_topo(self, contexto):
        pass

    def ao_mover_fundo(self, contexto):
        pass

    def ao_copiar(self, contexto):
        pass

    def ao_colar(self, contexto):
        pass

    def ao_mudar_cor(self, contexto):
        pass

    def ao_agrupar(self, contexto):
        pass

    def ao_desagrupar(self, contexto):
        pass


class EstadoOcioso(EstadoDesenho):

    def ao_pressionar(self, contexto, event):
        tipo = contexto.janela.obter_tipo_figura()

        if tipo == 'Selecionar':
            figura = contexto.desenho.figura_no_ponto(event.x, event.y)
            if figura is None:
                return  # clique em área vazia: nada a selecionar, continua ocioso

            _selecionar_com_modificador(contexto, figura, event)
            contexto.ultimo_x, contexto.ultimo_y = event.x, event.y
            contexto.redesenhar_com_selecao()
            if contexto.figuras_selecionadas:
                contexto.mudar_estado(EstadoArrastandoSelecao())
            return

        cor_cont = contexto.janela.obter_cor_contorno()
        cor_pren = contexto.janela.obter_cor_preenchimento()

        figura = contexto.criar_figura(tipo, event.x, event.y, cor_cont, cor_pren)
        if figura is None:
            contexto.retangulo_inicio = (event.x, event.y)
            contexto.mudar_estado(EstadoSelecionandoRetangulo())
            return

        contexto.figura_atual = figura
        if tipo == 'Poligono':
            contexto.mudar_estado(EstadoDesenhandoPoligono())
        elif tipo == 'PoligonoRegular':
            contexto.mudar_estado(EstadoDesenhandoPoligonoRegular())
        else:
            contexto.mudar_estado(EstadoArrastando())

    def ao_mover(self, contexto, event):
        pass  # sem figura em construção: nada a atualizar

    def ao_soltar(self, contexto, event):
        pass

    def ao_finalizar(self, contexto, event):
        pass


class EstadoArrastando(EstadoDesenho):

    def ao_pressionar(self, contexto, event):
        pass  # já existe uma figura em andamento; ignora novo clique

    def ao_mover(self, contexto, event):
        contexto.figura_atual.atualizar(event.x, event.y)
        contexto.redesenhar_com_temporaria()

    def ao_soltar(self, contexto, event):
        contexto.confirmar_figura_atual()
        contexto.mudar_estado(EstadoOcioso())

    def ao_finalizar(self, contexto, event):
        pass


class EstadoDesenhandoPoligono(EstadoDesenho):

    def ao_pressionar(self, contexto, event):
        contexto.figura_atual.atualizar(event.x, event.y)
        contexto.redesenhar_com_temporaria()

    def ao_mover(self, contexto, event):
        pass  # cada vértice é definido por um clique, não por arraste

    def ao_soltar(self, contexto, event):
        pass  # soltar o botão não tem efeito para o polígono

    def ao_finalizar(self, contexto, event):
        contexto.confirmar_figura_atual()
        contexto.mudar_estado(EstadoOcioso())


class EstadoArrastandoSelecao(EstadoDesenho):


    def ao_pressionar(self, contexto, event):
        pass  # já estamos arrastando a partir do clique que iniciou a seleção

    def ao_mover(self, contexto, event):
        dx = event.x - contexto.ultimo_x
        dy = event.y - contexto.ultimo_y
        for figura in contexto.figuras_selecionadas:
            figura.mover(dx, dy)
        contexto.ultimo_x, contexto.ultimo_y = event.x, event.y
        contexto.redesenhar_com_selecao()

    def ao_soltar(self, contexto, event):
        contexto.mudar_estado(EstadoSelecaoAtiva())

    def ao_finalizar(self, contexto, event):
        pass


class EstadoSelecaoAtiva(EstadoDesenho):

    def ao_pressionar(self, contexto, event):
        tipo = contexto.janela.obter_tipo_figura()

        if tipo != 'Selecionar':
            contexto.figuras_selecionadas = [figura]
            contexto.ultimo_x, contexto.ultimo_y = event.x, event.y
            contexto.salvar_estado()
            contexto.redesenhar_com_selecao()
            contexto.mudar_estado(EstadoArrastandoSelecao())
            return
            

        figura = contexto.desenho.figura_no_ponto(event.x, event.y)

        if figura not in contexto.figuras_selecionadas:
            contexto.figuras_selecionadas = [figura]
            contexto.redesenhar_com_selecao()

        contexto.ultimo_x, contexto.ultimo_y = event.x, event.y
        contexto.salvar_estado()
        contexto.mudar_estado(EstadoArrastandoSelecao())

        _selecionar_com_modificador(contexto, figura, event)
        contexto.ultimo_x, contexto.ultimo_y = event.x, event.y
        contexto.redesenhar_com_selecao()

        if contexto.figuras_selecionadas:
            contexto.mudar_estado(EstadoArrastandoSelecao())
        else:
            contexto.mudar_estado(EstadoOcioso())


    def ao_mover(self, contexto, event):
        pass  # botão não está pressionado: nada a arrastar

    def ao_soltar(self, contexto, event):
        pass

    def ao_finalizar(self, contexto, event):
        pass

    def ao_apagar(self, contexto):
        contexto.salvar_estado()
        for figura in contexto.figuras_selecionadas:
            contexto.desenho.remover_figura(figura)
        contexto.figuras_selecionadas = []
        contexto.mudar_estado(EstadoOcioso())
        contexto.redesenhar_com_selecao()

    def ao_mover_frente(self, contexto):
        contexto.salvar_estado()
        for figura in contexto.figuras_selecionadas:
            contexto.desenho.mover_para_frente(figura)
        contexto.redesenhar_com_selecao()

    def ao_mover_tras(self, contexto):
        contexto.salvar_estado()
        for figura in contexto.figuras_selecionadas:
            contexto.desenho.mover_para_tras(figura)
        contexto.redesenhar_com_selecao()

    def ao_mover_topo(self, contexto):
        contexto.salvar_estado()
        for figura in contexto.figuras_selecionadas:
            contexto.desenho.mover_para_topo(figura)
        contexto.redesenhar_com_selecao()

    def ao_mover_fundo(self, contexto):
        contexto.salvar_estado()
        for figura in contexto.figuras_selecionadas:
            contexto.desenho.mover_para_fundo(figura)
        contexto.redesenhar_com_selecao()

    def ao_copiar(self, contexto):
        contexto.buffer_copia = [copy.deepcopy(figura) for figura in contexto.figuras_selecionadas]

    def ao_colar(self, contexto):
        if not contexto.buffer_copia:
            return
        contexto.salvar_estado()
        novas = []
        for figura in contexto.buffer_copia:
            copia = copy.deepcopy(figura)
            copia.mover(DESLOCAMENTO_COLAR, DESLOCAMENTO_COLAR)
            contexto.desenho.adicionar_figura(copia)
            novas.append(copia)

        # A colagem seguinte parte da posição recém-colada, criando tipo
        # uma reação em cadeia a cada Ctrl+V repetido.
        contexto.buffer_copia = novas
        contexto.figuras_selecionadas = novas
        contexto.mudar_estado(EstadoSelecaoAtiva())
        contexto.redesenhar_com_selecao()

    def ao_mudar_cor(self, contexto):
        contexto.salvar_estado()
        cor_cont = contexto.janela.obter_cor_contorno()
        cor_pren = contexto.janela.obter_cor_preenchimento()
        for figura in contexto.figuras_selecionadas:
            figura.cor_cont = cor_cont
            if figura.cor_pren is not None:
                figura.cor_pren = cor_pren
        contexto.redesenhar_com_selecao()


    def ao_agrupar(self, contexto):
        """Ctrl+G: agrupa as figuras selecionadas em uma única FiguraComposta.
        """
        selecionadas = contexto.figuras_selecionadas
        if len(selecionadas) < 2:
            return

        for figura in selecionadas:
            contexto.desenho.remover_figura(figura)

        composta = FiguraComposta(list(selecionadas))
        contexto.desenho.adicionar_figura(composta)
        contexto.figuras_selecionadas = [composta]
        contexto.redesenhar_com_selecao()

    def ao_desagrupar(self, contexto):
        """Ctrl+Shift+G: desfaz a composição de qualquer FiguraComposta que
        esteja selecionada."""
        nova_selecao = []
        desagrupou_alguma = False

        for figura in contexto.figuras_selecionadas:
            if isinstance(figura, FiguraComposta):
                contexto.desenho.remover_figura(figura)
                for filha in figura.figuras_compostas:
                    contexto.desenho.adicionar_figura(filha)
                    nova_selecao.append(filha)
                desagrupou_alguma = True
            else:
                nova_selecao.append(figura)

        if desagrupou_alguma:
            contexto.figuras_selecionadas = nova_selecao
            contexto.redesenhar_com_selecao()


class EstadoDesenhandoPoligonoRegular(EstadoDesenho):
    """PoligonoRegular já foi criado (triângulo, raio 0) no clique inicial.
    Enquanto este estado estiver ativo:
      - mover o mouse (arrastando) ajusta o raio;
      - cada novo clique esquerdo soma um lado (Shift: subtrai), mínimo 3 e máximo 20;
      - duplo clique esquerdo finaliza
    """

    def ao_pressionar(self, contexto, event):
        shift_pressionado = bool(event.state & MASCARA_SHIFT)
        variacao = -1 if shift_pressionado else 1
        contexto.figura_atual.mudar_num_lados(variacao)
        contexto.redesenhar_com_temporaria()

    def ao_mover(self, contexto, event):
        contexto.figura_atual.atualizar(event.x, event.y)
        contexto.redesenhar_com_temporaria()

    def ao_soltar(self, contexto, event):
        pass  # figura só é confirmada no duplo clique (ao_finalizar)

    def ao_finalizar(self, contexto, event):
        contexto.confirmar_figura_atual()
        contexto.mudar_estado(EstadoOcioso())

class EstadoSelecionandoRetangulo(EstadoDesenho):
    """O usuário clicou em área vazia (no modo 'Selecionar') e está
    arrastando o mouse, desenhando um retângulo elástico.
    """

    def ao_pressionar(self, contexto, event):
        pass  # já estamos arrastando a partir do clique que iniciou o retângulo

    def ao_mover(self, contexto, event):
        x0, y0 = contexto.retangulo_inicio
        contexto.redesenhar_com_retangulo(x0, y0, event.x, event.y)

    def ao_soltar(self, contexto, event):
        x0, y0 = contexto.retangulo_inicio
        contexto.figuras_selecionadas = [
            figura for figura in contexto.desenho.obter_figuras()
            if figura.selecionado_por_retangulo(x0, y0, event.x, event.y)
        ]
        contexto.retangulo_inicio = None
        contexto.redesenhar_com_selecao()
        if contexto.figuras_selecionadas:
            contexto.mudar_estado(EstadoSelecaoAtiva())
        else:
            contexto.mudar_estado(EstadoOcioso())

    def ao_finalizar(self, contexto, event):
        pass