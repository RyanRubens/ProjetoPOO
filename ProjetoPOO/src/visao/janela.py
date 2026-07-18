from tkinter import Tk, Frame, Canvas, Button, StringVar, W, N
from tkinter import ttk


class JanelaDesenho:
    """View: monta a interface gráfica e expõe métodos para ler o estado
    selecionado pelo usuário e para (re)desenhar o canvas."""

    CORES = {
        "Preto": "black",
        "Branco": "white",
        "Vermelho": "red",
        "Verde": "green",
        "Azul": "blue",
    }

    def __init__(self):
        self.root = Tk()
        self.root.title("Editor de Desenhos")
        self.frame = Frame(self.root)
        paddings = {'padx': 5, 'pady': 5}

        ttk.Label(self.frame, text='Figuras:').grid(column=0, row=0, sticky=W, **paddings)
        ttk.Label(self.frame, text='Cor Contorno:').grid(column=1, row=0, sticky=W, **paddings)
        ttk.Label(self.frame, text='Cor Interna:').grid(column=2, row=0, sticky=W, **paddings)

        self.tipo_figura_var = StringVar(self.root)
        self.option_menu = ttk.OptionMenu(
            self.frame, self.tipo_figura_var, 'Linha', 'Linha', 'Rabisco', 'Circulo', 'Oval', 'Poligono',
            'PoligonoRegular', 'Selecionar'
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

    def redesenhar(self, figuras, selecionada=None):
        selecionada = selecionada or []
        self.limpar_canvas()
        for figura in figuras:
            figura.desenhar(self.canvas, selecionado=(figura in selecionada))

    def desenhar_temporaria(self, figura):
        """Desenha (tracejada) a figura que ainda está sendo criada pelo usuário."""
        figura.desenhar(self.canvas, tracejado=True)
    
    def desenhar_retangulo_selecao(self, x1, y1, x2, y2):
        """feedback visual apenas -não faz parte do model. 
        Deve ser chamado depois de `redesenhar`,
        para ficar por cima das figuras."""
        self.canvas.create_rectangle(x1, y1, x2, y2, outline='gray50', dash=(4, 2))

    # ---- Vinculação de eventos: quem faz o quê é decidido pelo controlador ----
    def vincular_eventos(self, ao_pressionar, ao_mover, ao_soltar, ao_finalizar, ao_limpar):
        def ao_pressionar_com_foco(event):
            self.canvas.focus_set()
            ao_pressionar(event)

        self.canvas.bind('<ButtonPress-1>', ao_pressionar_com_foco)
        self.canvas.bind('<B1-Motion>', ao_mover)
        self.canvas.bind('<ButtonRelease-1>', ao_soltar)
        self.canvas.bind('<ButtonPress-3>', ao_finalizar)  #Botão direito finalizando o Poligono comum/regular.
        self.botao_limpar.config(command=ao_limpar)

    def vincular_teclado(self, ao_apagar, ao_mover_frente, ao_mover_tras, ao_mover_topo, ao_mover_fundo,
                          ao_copiar, ao_colar, ao_desfazer, ao_refazer):
        """Liga as teclas que atuam sobre a(s) figura(s) selecionada(s)."""
        self.canvas.bind('<Delete>', ao_apagar)
        self.canvas.bind('<Right>', ao_mover_frente)
        self.canvas.bind('<Left>', ao_mover_tras)
        self.canvas.bind('<Up>', ao_mover_topo)
        self.canvas.bind('<Down>', ao_mover_fundo)
        self.canvas.bind('<Control-c>', ao_copiar)
        self.canvas.bind('<Control-v>', ao_colar)
        self.canvas.bind('<Control-z>', ao_desfazer)
        self.canvas.bind('<Control-y>', ao_refazer)

    def vincular_mudanca_cor(self, ao_mudar_cor):
        """Chama ao_mudar_cor sempre que o usuário troca a cor de contorno ou
        de preenchimento no respectivo menu (usado para recolorir a seleção)."""
        self.contorno_figura_var.trace_add('write', lambda *_args: ao_mudar_cor())
        self.dentro_figura_var.trace_add('write', lambda *_args: ao_mudar_cor())

    def iniciar(self):
        self.root.mainloop()
