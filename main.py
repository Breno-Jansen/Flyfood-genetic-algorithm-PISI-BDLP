from pathlib import Path
from tkinter import Tk, Canvas, Text, Button, PhotoImage
import heuristica


def relative_to_assets(path: str) -> Path:
    output_path = Path(__file__).parent
    assets_path = output_path / 'build' / "assets" / "frame0"
    return assets_path / Path(path)

window = Tk()
window.geometry("1221x672")
window.configure(bg = "#409AE4")


canvas = Canvas(
    window,
    bg = "#409AE4",
    height = 672,
    width = 1221,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    610.0,
    336.0,
    image=image_image_1
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: heuristica.executar_calculo(entry_1),
    relief="flat",
    activebackground="#409AE4"
    
)

button_1.place(
    x=196.0,
    y=477.0,
    width=356.0,
    height=116.0
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    379.5,
    352.5,
    image=entry_image_1
)
entry_1 = Text(
    bd=0,
    bg="#EDEDED",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=205.0,
    y=240.0,
    width=349.0,
    height=223.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: heuristica.selecionar_arquivo(entry_1),
    relief="flat",
    activebackground="#409AE4"
)
button_2.place(
    x=696.0,
    y=493.0,
    width=356.0,
    height=116.0
)

window.resizable(False, False)
window.mainloop()
