from abc import ABC, abstractmethod

class Figura(ABC):
    def _init_(self, cor_cont, cor_pren = None):
        self.cor_cont = cor_cont
        self.cor_pren = cor_pren

    @abstractmethod
    def desenhar(self, canvas, tracejado=False):
        pass

    @abstractmethod
    def incompleto(self):
        pass

class Linha(Figura):
    def _init_(self,x1,y1,x2,y2, cor_cont):
        super()._init_(cor_cont, cor_pren= None)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2


    def desenhar(self, canvas, tracejado = False):
        borda =(4, 2) if tracejado else None
        canvas.create_line(self.x1, self.y1, self.x2,self.y2, fill=self.cor_cont, dash=borda)


    def incompleto(self):
        return (self.x1, self.y1)==(self.x2, self.y2)
          
          

class Oval(Figura):
    def _init_(self, x1, y1,x2,y2,cor_cont, cor_pren):
        super()._init_(cor_cont, cor_pren)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def desenhar(self, canvas, tracejado = False):
        borda =(4,2) if tracejado else None
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2, outline=self.cor_cont, fill=self.cor_pren, dash=borda)

    def incompleto(self):
        return (self.x1, self.y1)==(self.x2, self.y2)
        
class Circulo(Oval):
    def  _init_(self, cx,cy, raio, cor_cont,cor_pren):
        super()._init_(cx - raio, cy - raio, cx + raio, cy + raio, cor_cont, cor_pren)
        self.raio = raio

    def incompleto(self):
         return self.raio == 0
           
class Rabisco(Figura):
    def _init_(self,pontos, cor_cont):
        super()._init_(cor_cont)
        self.pontos = pontos

    def desenhar(self, canvas, tracejado = False):
        if len(self.pontos)> 1:
         borda =(4, 2) if tracejado else None
         canvas.create_line(self.pontos, fill= self.cor_cont, dash=borda)

    def incompleto(self):
        return len(self.pontos)<= 1


class Poligono(Figura):
    def _init_(self, vertices, cor_cont, cor_pren):
        super()._init_(cor_cont,cor_pren)
        self.vertices = vertices

    def desenhar(self, canvas, tracejado = False):
        if len(self.vertices)> 1:
            borda= (4, 2) if tracejado else None
            canvas.create_polygon(self.vertices, outline=self.cor_cont, fill=self.cor_pren, dash= borda)

    def incompleto(self):
        return len(self.vertices)< 3