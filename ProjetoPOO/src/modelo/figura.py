import math
from abc import ABC, abstractmethod

TOLERANCIA_CLIQUE = 6
LARGURA_NORMAL = 1
LARGURA_SELECIONADA = 3

def _distancia_ponto_segmento(x1, y1, x2, y2, px, py):
    """Distância entre o segmento ((x1,y1), (x2,y2)) e o ponto (px, py)."""
    dx = x2 - x1
    dy = y2 - y1

    ab_len_sq = dx ** 2 + dy ** 2

    if ab_len_sq == 0:
        return math.sqrt((px - x1) ** 2 + (py - y1) ** 2)

    ap_x = px - x1
    ap_y = py - y1

    t = (ap_x * dx + ap_y * dy) / ab_len_sq
    t = max(0.0, min(1.0, t))

    ponto_proximo_x = x1 + t * dx
    ponto_proximo_y = y1 + t * dy

    return math.sqrt((px - ponto_proximo_x) ** 2 + (py - ponto_proximo_y) ** 2)

class Figura(ABC):
    """Classe base abstrata para qualquer figura que pode ser desenhada no canvas."""

    def __init__(self, cor_cont, cor_pren=None):
        self.cor_cont = cor_cont
        self.cor_pren = cor_pren

    @abstractmethod
    def desenhar(self, canvas, tracejado=False, selecionado=False):
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

    @abstractmethod
    def contem_ponto(self, x, y):
        pass
    
    @abstractmethod
    def mover(self, dx, dy):
        pass


class Linha(Figura):
    def __init__(self, x1, y1, x2, y2, cor_cont):
        super().__init__(cor_cont, cor_pren=None)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def atualizar(self, x, y):
        self.x2, self.y2 = x, y

    def desenhar(self, canvas, tracejado=False, selecionado=False):
        borda = (4, 2) if tracejado else None
        largura = LARGURA_SELECIONADA if selecionado else LARGURA_NORMAL
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor_cont, dash=borda, width=largura)

    def incompleto(self):
        return (self.x1, self.y1) == (self.x2, self.y2)

    def contem_ponto(self, x, y):
        return _distancia_ponto_segmento(self.x1, self.y1, self.x2, self.y2, x, y) <= TOLERANCIA_CLIQUE

    def mover(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

class Oval(Figura):
    def __init__(self, x1, y1, x2, y2, cor_cont, cor_pren):
        super().__init__(cor_cont, cor_pren)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def atualizar(self, x, y):
        self.x2, self.y2 = x, y

    def desenhar(self, canvas, tracejado=False, selecionado=False):
        borda = (4, 2) if tracejado else None
        largura = LARGURA_SELECIONADA if selecionado else LARGURA_NORMAL
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2, outline=self.cor_cont, fill=self.cor_pren,
                            dash=borda, width=largura)

    def incompleto(self):
        return (self.x1, self.y1) == (self.x2, self.y2)

    def contem_ponto(self, x, y):
        rx = abs(self.x2 - self.x1) / 2
        ry = abs(self.y2 - self.y1) / 2
        if rx == 0 or ry == 0:
            return False
        cx = (self.x1 + self.x2) / 2
        cy = (self.y1 + self.y2) / 2
        return ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1

    def mover(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy


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

    def contem_ponto(self, x, y):
        if self.raio == 0:
            return False
        return math.hypot(x - self.cx, y - self.cy) <= self.raio

    def mover(self, dx, dy):
        super().mover(dx, dy)  # desloca x1,y1,x2,y2 (herdado de Oval)
        self.cx += dx
        self.cy += dy


class Rabisco(Figura):
    def __init__(self, x, y, cor_cont):
        super().__init__(cor_cont)
        self.pontos = [(x, y)]

    def atualizar(self, x, y):
        self.pontos.append((x, y))

    def desenhar(self, canvas, tracejado=False, selecionado=False):
        if len(self.pontos) > 1:
            borda = (4, 2) if tracejado else None
            largura = LARGURA_SELECIONADA if selecionado else LARGURA_NORMAL
            canvas.create_line(self.pontos, fill=self.cor_cont, dash=borda, width=largura)

    def incompleto(self):
        return len(self.pontos) <= 1

    def contem_ponto(self, x, y):
        if len(self.pontos) < 2:
            return False
        for i in range(len(self.pontos) - 1):
            x1, y1 = self.pontos[i]
            x2, y2 = self.pontos[i + 1]
            if _distancia_ponto_segmento(x1, y1, x2, y2, x, y) <= TOLERANCIA_CLIQUE:
                return True
        return False

    def mover(self, dx, dy):
        self.pontos = [(px + dx, py + dy) for px, py in self.pontos]


class Poligono(Figura):
    def __init__(self, x, y, cor_cont, cor_pren):
        super().__init__(cor_cont, cor_pren)
        self.vertices = [(x, y)]

    def atualizar(self, x, y):
        self.vertices.append((x, y))

    def desenhar(self, canvas, tracejado=False, selecionado=False):
        if len(self.vertices) > 1:
            borda = (4, 2) if tracejado else None
            largura = LARGURA_SELECIONADA if selecionado else LARGURA_NORMAL
            canvas.create_polygon(self.vertices, outline=self.cor_cont, fill=self.cor_pren,
                                   dash=borda, width=largura)

    def incompleto(self):
        return len(self.vertices) < 3

    def contem_ponto(self, x, y):
        """Ray casting: conta quantas arestas do polígono um raio horizontal
        partindo de (x, y) atravessa. Ímpar = dentro, par = fora."""
        n = len(self.vertices)
        if n < 3:
            return False

        dentro = False
        p1x, p1y = self.vertices[0]

        for i in range(n + 1):
            p2x, p2y = self.vertices[i % n]

            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            x_interceptado = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= x_interceptado:
                            dentro = not dentro

            p1x, p1y = p2x, p2y

        return dentro

    def mover(self, dx, dy):
        self.vertices = [(vx + dx, vy + dy) for vx, vy in self.vertices]
