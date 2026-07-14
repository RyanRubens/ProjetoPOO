from tkinter import Tk, Frame, Canvas, Button, StringVar, W, N
from tkinter import ttk


class JanelaDesenho:
    """View: monta a interface gráfica e expõe métodos para ler o estado
    selecionado pelo usuário e para (re)desenhar o canvas.

    Não conhece regras de negócio (quando uma figura está completa, etc.) -
    isso é responsabilidade do modelo/controlador.
    """

    CORES = {
        "Preto": "black",
        "Branco": "white",
        "Vermelho": "red",
        "Verde": "green",
        "Azul": "blue",
    }

    def __init__(self):
        self.root = Tk()
        self.root.title("Editor de Desenhos - MVC")
        self.frame = Frame(self.root)
        paddings = {'padx': 5, 'pady': 5}

        ttk.Label(self.frame, text='Figuras:').grid(column=0, row=0, sticky=W, **paddings)
        ttk.Label(self.frame, text='Cor Contorno:').grid(column=1, row=0, sticky=W, **paddings)
        ttk.Label(self.frame, text='Cor Interna:').grid(column=2, row=0, sticky=W, **paddings)

        self.tipo_figura_var = StringVar(self.root)
        self.option_menu = ttk.OptionMenu(
            self.frame, self.tipo_figura_var, 'Linha', 'Linha', 'Rabisco', 'Circulo', 'Oval'
        )
        self.option_menu.grid(column=0, row=0, sticky=N, **paddings)

        self.contorno_figura_var = StringVar(self.root)
        self.color_menu_out = ttk.OptionMenu(
            self.frame, self.contorno_figura_var, 'Preto', 'Preto', 'Vermelho', 'Verde', 'Azul'
        )
        self.color_menu_out.grid(column=1, row=0, sticky=N, **paddings)

        self.dentro_figura_var = StringVar(self.root)
        self.color_menu_in = ttk.OptionMenu(
            self.frame, self.dentro_figura_var, 'Branco', 'Branco', 'Vermelho', 'Verde', 'Azul'
        )
        self.color_menu_in.grid(column=2, row=0, sticky=N, **paddings)

        self.canvas = Canvas(self.frame, bg='white', width=1080, height=920)
        self.canvas.grid(column=0, row=1, columnspan=4, sticky=W, **paddings)
        self.frame.pack()

        self.botao_limpar = Button(self.frame, text='Limpar Tela')
        self.botao_limpar.grid(column=3, row=0, sticky=N)

    # ---- Leitura do estado selecionado na UI (usado pelo controlador) ----
    def obter_tipo_figura(self):
        return self.tipo_figura_var.get()

    def obter_cor_contorno(self):
        return self.CORES[self.contorno_figura_var.get()]

    def obter_cor_preenchimento(self):
        return self.CORES[self.dentro_figura_var.get()]

    # ---- Desenho no canvas ----
    def limpar_canvas(self):
        self.canvas.delete("all")

    def redesenhar(self, figuras):
        self.limpar_canvas()
        for figura in figuras:
            figura.desenhar(self.canvas)

    def desenhar_temporaria(self, figura):
        """Desenha (tracejada) a figura que ainda está sendo criada pelo usuário."""
        figura.desenhar(self.canvas, tracejado=True)

    # ---- Vinculação de eventos: quem faz o quê é decidido pelo controlador ----
    def vincular_eventos(self, ao_pressionar, ao_mover, ao_soltar, ao_limpar):
        self.canvas.bind('<ButtonPress-1>', ao_pressionar)
        self.canvas.bind('<B1-Motion>', ao_mover)
        self.canvas.bind('<ButtonRelease-1>', ao_soltar)
        self.botao_limpar.config(command=ao_limpar)

    def iniciar(self):
        self.root.mainloop()
