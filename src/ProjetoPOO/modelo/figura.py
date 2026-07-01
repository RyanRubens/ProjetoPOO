from abc import ABC, abstractmethod


class Figura(ABC):
    """Classe base abstrata para qualquer figura que pode ser desenhada no canvas."""

    def __init__(self, cor_cont, cor_pren=None):
        self.cor_cont = cor_cont
        self.cor_pren = cor_pren

    @abstractmethod
    def desenhar(self, canvas, tracejado=False):
        """Desenha a figura no canvas do Tkinter."""
        pass

    @abstractmethod
    def incompleto(self):
        """Indica se a figura ainda não tem forma/tamanho válido (ex.: linha sem comprimento)."""
        pass

    @abstractmethod
    def atualizar(self, x, y):
        """Atualiza a figura enquanto ela está sendo arrastada/desenhada com o mouse."""
        pass


class Linha(Figura):
    def __init__(self, x1, y1, x2, y2, cor_cont):
        super().__init__(cor_cont, cor_pren=None)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def atualizar(self, x, y):
        self.x2, self.y2 = x, y

    def desenhar(self, canvas, tracejado=False):
        borda = (4, 2) if tracejado else None
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor_cont, dash=borda)

    def incompleto(self):
        return (self.x1, self.y1) == (self.x2, self.y2)


class Oval(Figura):
    def __init__(self, x1, y1, x2, y2, cor_cont, cor_pren):
        super().__init__(cor_cont, cor_pren)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def atualizar(self, x, y):
        self.x2, self.y2 = x, y

    def desenhar(self, canvas, tracejado=False):
        borda = (4, 2) if tracejado else None
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2, outline=self.cor_cont, fill=self.cor_pren, dash=borda)

    def incompleto(self):
        return (self.x1, self.y1) == (self.x2, self.y2)


class Circulo(Oval):
    def __init__(self, cx, cy, raio, cor_cont, cor_pren):
        super().__init__(cx - raio, cy - raio, cx + raio, cy + raio, cor_cont, cor_pren)
        self.cx, self.cy = cx, cy
        self.raio = raio

    def atualizar(self, x, y):
        self.raio = ((x - self.cx) ** 2 + (y - self.cy) ** 2) ** 0.5
        self.x1, self.y1 = self.cx - self.raio, self.cy - self.raio
        self.x2, self.y2 = self.cx + self.raio, self.cy + self.raio

    def incompleto(self):
        return self.raio == 0


class Rabisco(Figura):
    def __init__(self, x, y, cor_cont):
        super().__init__(cor_cont)
        self.pontos = [(x, y)]

    def atualizar(self, x, y):
        self.pontos.append((x, y))

    def desenhar(self, canvas, tracejado=False):
        if len(self.pontos) > 1:
            borda = (4, 2) if tracejado else None
            canvas.create_line(self.pontos, fill=self.cor_cont, dash=borda)

    def incompleto(self):
        return len(self.pontos) <= 1


class Poligono(Figura):
    def __init__(self, x, y, cor_cont, cor_pren):
        super().__init__(cor_cont, cor_pren)
        self.vertices = [(x, y)]

    def atualizar(self, x, y):
        self.vertices.append((x, y))

    def desenhar(self, canvas, tracejado=False):
        if len(self.vertices) > 1:
            borda = (4, 2) if tracejado else None
            canvas.create_polygon(self.vertices, outline=self.cor_cont, fill=self.cor_pren, dash=borda)

    def incompleto(self):
        return len(self.vertices) < 3
