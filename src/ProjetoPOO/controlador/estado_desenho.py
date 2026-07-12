import copy
from abc import ABC, abstractmethod

DESLOCAMENTO_COLAR = 15

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

class EstadoOcioso(EstadoDesenho):

    def ao_pressionar(self, contexto, event):
        tipo = contexto.janela.obter_tipo_figura()

        if tipo == 'Selecionar':
            figura = contexto.desenho.figura_no_ponto(event.x, event.y)
            if figura is None:
                return  # clique em área vazia: nada a selecionar, continua ocioso

            contexto.figuras_selecionadas = [figura]
            contexto.ultimo_x, contexto.ultimo_y = event.x, event.y
            contexto.redesenhar_com_selecao()
            contexto.mudar_estado(EstadoArrastandoSelecao())
            return

        cor_cont = contexto.janela.obter_cor_contorno()
        cor_pren = contexto.janela.obter_cor_preenchimento()

        figura = contexto.criar_figura(tipo, event.x, event.y, cor_cont, cor_pren)
        if figura is None:
            return

        contexto.figura_atual = figura
        if tipo == 'Poligono':
            contexto.mudar_estado(EstadoDesenhandoPoligono())
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
            # Usuário trocou o tipo de figura no menu: encerra a seleção e
            # deixa o EstadoOcioso tratar este mesmo clique como o início de
            # uma nova figura, em vez de "gastar" o clique só desmarcando.
            contexto.figuras_selecionadas = []
            contexto.redesenhar_com_selecao()
            contexto.mudar_estado(EstadoOcioso())
            contexto.estado.ao_pressionar(contexto, event)
            return

        figura = contexto.desenho.figura_no_ponto(event.x, event.y)

        if figura is None:
            contexto.figuras_selecionadas = []
            contexto.redesenhar_com_selecao()
            contexto.mudar_estado(EstadoOcioso())
            return

        if figura not in contexto.figuras_selecionadas:
            contexto.figuras_selecionadas = [figura]
            contexto.redesenhar_com_selecao()

        contexto.ultimo_x, contexto.ultimo_y = event.x, event.y
        contexto.mudar_estado(EstadoArrastandoSelecao())

    def ao_mover(self, contexto, event):
        pass  # botão não está pressionado: nada a arrastar

    def ao_soltar(self, contexto, event):
        pass

    def ao_finalizar(self, contexto, event):
        pass

    def ao_apagar(self, contexto):
        for figura in contexto.figuras_selecionadas:
            contexto.desenho.remover_figura(figura)
        contexto.figuras_selecionadas = []
        contexto.mudar_estado(EstadoOcioso())
        contexto.redesenhar_com_selecao()

    def ao_mover_frente(self, contexto):
        for figura in contexto.figuras_selecionadas:
            contexto.desenho.mover_para_frente(figura)
        contexto.redesenhar_com_selecao()

    def ao_mover_tras(self, contexto):
        for figura in contexto.figuras_selecionadas:
            contexto.desenho.mover_para_tras(figura)
        contexto.redesenhar_com_selecao()

    def ao_mover_topo(self, contexto):
        for figura in contexto.figuras_selecionadas:
            contexto.desenho.mover_para_topo(figura)
        contexto.redesenhar_com_selecao()

    def ao_mover_fundo(self, contexto):
        for figura in contexto.figuras_selecionadas:
            contexto.desenho.mover_para_fundo(figura)
        contexto.redesenhar_com_selecao()

    def ao_copiar(self, contexto):
        contexto.buffer_copia = [copy.deepcopy(figura) for figura in contexto.figuras_selecionadas]

    def ao_colar(self, contexto):
        if not contexto.buffer_copia:
            return

        novas = []
        for figura in contexto.buffer_copia:
            copia = copy.deepcopy(figura)
            copia.mover(DESLOCAMENTO_COLAR, DESLOCAMENTO_COLAR)
            contexto.desenho.adicionar_figura(copia)
            novas.append(copia)

        # A colagem seguinte parte da posição recém-colada, criando um
        # efeito de cascata a cada Ctrl+V repetido.
        contexto.buffer_copia = novas
        contexto.figuras_selecionadas = novas
        contexto.mudar_estado(EstadoSelecaoAtiva())
        contexto.redesenhar_com_selecao()

    def ao_mudar_cor(self, contexto):
        cor_cont = contexto.janela.obter_cor_contorno()
        cor_pren = contexto.janela.obter_cor_preenchimento()
        for figura in contexto.figuras_selecionadas:
            figura.cor_cont = cor_cont
            if figura.cor_pren is not None:  # Linha e Rabisco não têm preenchimento
                figura.cor_pren = cor_pren
        contexto.redesenhar_com_selecao()
