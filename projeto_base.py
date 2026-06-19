from tkinter import *
from tkinter import ttk

#dicionario de cores
cores = {
    "Preto": "black",
    "Branco": "white",
    "Vermelho": "red",
    "Verde": "green",
    "Azul": "blue"
}

# Quando mouse é pressionado
def iniciar_figura_nova(event): 
    global figura_nova
    cor_contorno = cores[contorno_figura_var.get()]
    cor_preenchimento = cores[dentro_figura_var.get()]
    match tipo_figura_var.get():
        case 'Linha':
            figura_nova = ("linha", (event.x, event.y, event.x, event.y), cor_contorno, "")
        case 'Oval':
            figura_nova = ('oval', (event.x, event.y, event.x, event.y), cor_contorno, cor_preenchimento)
        case 'Circulo':
            global cx, cy
            cx = event.x
            cy = event.y
            figura_nova = ('circulo', (event.x, event.y, event.x, event.y), cor_contorno, cor_preenchimento)
        case 'Rabisco':
            figura_nova = ("rabisco", [(event.x, event.y)], cor_contorno, "")

# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    global figura_nova
    match figura_nova[0]:
        case "rabisco":
            figura_nova[1].append((event.x, event.y))
        case "linha":
            figura_nova = ("linha", (figura_nova[1][0], figura_nova[1][1], event.x, event.y), figura_nova[2], figura_nova[3])
        case 'circulo':
            global cx, cy
            raio = ((event.x - cx)**2 + (event.y - cy)**2) ** 0.5
            figura_nova = ("circulo", (cx - raio, cy - raio, cx + raio, cy + raio), figura_nova[2], figura_nova[3])
        case 'oval':
            figura_nova = ("oval", (figura_nova[1][0], figura_nova[1][1], event.x, event.y), figura_nova[2], figura_nova[3])   
    desenhar_figuras()
    desenhar_figura_nova()

# Quando mouse é solto
def incluir_figura_nova(event): 
    if not incompleta(figura_nova): # para evitar incluir figuras incompletas, como uma linha sem comprimento ou um rabisco com um único ponto
        figuras.append(figura_nova) 
    desenhar_figuras()

def desenhar_figuras():
    canvas.delete("all")
    for fig, values, cor_borda, cor_dentro in figuras:
     match fig:
        case "linha":
            canvas.create_line(values[0], values[1], values[2], values[3], fill=cor_borda)
        case "rabisco":
            canvas.create_line(values, fill=cor_borda)
        case "oval" | "circulo":
            canvas.create_oval(values[0], values[1], values[2], values[3], outline=cor_borda, fill=cor_dentro)

def desenhar_figura_nova():
    fig, values, cor_borda, cor_dentro = figura_nova
    match fig:
        case "linha":
            canvas.create_line(values[0], values[1], values[2], values[3], fill=cor_borda, dash=(4, 2))
        case "circulo" | "oval":
            canvas.create_oval(values[0], values[1], values[2], values[3],outline=cor_borda, fill=cor_dentro, dash=(4, 2))
        case "rabisco":
            canvas.create_line(values, fill=cor_borda, dash=(4, 2))

def incompleta(figura):
    fig, values = figura[0], figura[1]

    if fig in ("linha", "oval", "circulo"):
        return (values[0], values[1]) == (values[2], values[3])

    elif fig == "rabisco":
        return len(values) <= 1

def resetar_tela():
    global figuras
    figuras = []
    canvas.delete("all")


#******* MAIN *******#

figuras = []       # Todas as figuras desenhadas
figura_nova = None # Figura que está sendo desenhada, mas ainda não foi incluída em figuras

root = Tk()
frame = Frame(root)

# Widgets arranjados com Layout grid dentro de frame
paddings = {'padx': 5, 'pady': 5} 

# label (texto indicatico)
label = ttk.Label(frame,  text='Figuras:')
label.grid(column=0, row=0, sticky=W, **paddings)
ttk.Label(frame, text='Cor Contorno:').grid(column=1, row=0, sticky=W, **paddings)
ttk.Label(frame, text= 'Cor Interna:').grid(column=2, row=0, sticky=W, **paddings)
# option menu
tipo_figura_var = StringVar(root) # Guarda o tipo de figura selecionado no option menu (linha ou rabisco)
option_menu = ttk.OptionMenu(frame, tipo_figura_var,
                             'Linha', 'Linha', 'Rabisco', 'Circulo', 'Oval')
option_menu.grid(column=0, row=0, sticky=N, **paddings)



#Selecao de cor
contorno_figura_var = StringVar(root)
color_menu_out = ttk.OptionMenu(frame, contorno_figura_var, 
                            'Preto', 'Preto', 'Vermelho', 'Verde', 'Azul')
color_menu_out.grid(column=1, row=0, sticky=N, **paddings)
dentro_figura_var = StringVar(root)
color_menu_in = ttk.OptionMenu(frame, dentro_figura_var,
                               'Branco', 'Branco', 'Vermelho', 'Verde', 'Azul')
color_menu_in.grid(column=2, row=0, sticky=N, **paddings)



# Área de desenho
canvas = Canvas(frame, bg='white', width=1080, height=920)
canvas.grid(column=0, row=1, columnspan=4, sticky=W, **paddings)
frame.pack()
bnt_limpar = Button(frame, text='Limpar Tela', command=resetar_tela)
bnt_limpar.grid(column=3, row=0, sticky=N)


# Eventos de mouse associados ao canvas - com seus callbacks
canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)
root.mainloop()