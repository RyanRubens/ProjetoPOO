from abc import ABC, abstractmethod


class EstadoDesenho(ABC):

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


class EstadoOcioso(EstadoDesenho):

    def ao_pressionar(self, contexto, event):
        tipo = contexto.janela.obter_tipo_figura()
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
