import os
import sys
import argparse
import pymupdf
import tkinter as tk
from PIL import Image, ImageTk

class CropSelector:
    """Ventana interactiva para seleccionar visualmente el área de recorte."""
    def __init__(self, page):
        self.page = page
        self.rect = None
        
        self.root = tk.Tk()
        self.root.title("Selecciona el área de la diapositiva (Click y arrastra)")
        
        pix = page.get_pixmap(dpi=100)
        img_path = "_temp_preview.png"
        pix.save(img_path)
        
        self.pil_img = Image.open(img_path)
        self.img_width, self.img_height = self.pil_img.size
        
        self.canvas = tk.Canvas(self.root, width=self.img_width, height=self.img_height)
        self.canvas.pack()
        
        self.tk_img = ImageTk.PhotoImage(self.pil_img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)
        
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        
        self.start_x = None
        self.start_y = None
        self.rect_id = None
        
        lbl = tk.Label(self.root, text="Haz clic y arrastra para seleccionar el área de la diapositiva.", fg="blue")
        lbl.pack(pady=5)
        
        self.root.mainloop()
        
        if os.path.exists(img_path):
            os.remove(img_path)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_move_press(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect_id, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x, end_y = (event.x, event.y)
        
        pdf_w, pdf_h = self.page.rect.width, self.page.rect.height
        
        x0 = min(self.start_x, end_x) * (pdf_w / self.img_width)
        y0 = min(self.start_y, end_y) * (pdf_h / self.img_height)
        x1 = max(self.start_x, end_x) * (pdf_w / self.img_width)
        y1 = max(self.start_y, end_y) * (pdf_h / self.img_height)
        
        self.rect = pymupdf.Rect(x0, y0, x1, y1)
        self.root.destroy()

def extraer_texto_fuera_de_recorte(page, crop_rect):
    """Extrae únicamente el texto que se encuentra fuera del rectángulo de la diapositiva."""
    text_blocks = page.get_text("blocks")
    texto_filtrado = []
    
    for b in text_blocks:
        b_rect = pymupdf.Rect(b[:4])
        if b_rect.y0 >= crop_rect.y1 - 10:  
            texto_filtrado.append(b[4])
            
    return "".join(texto_filtrado).strip()

def pdf_a_markdown_visual(pdf_path, output_md_path="resultado.md", images_dir="_recursos"):
    if not os.path.exists(pdf_path):
        print(f"Error: No se encuentra el archivo PDF en la ruta: '{pdf_path}'")
        return

    os.makedirs(images_dir, exist_ok=True)
    doc = pymupdf.open(pdf_path)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    if len(doc) == 0:
        print("El PDF está vacío.")
        return

    print("Abriendo ventana visual para seleccionar el recorte...")
    selector = CropSelector(doc[0])
    
    if not selector.rect:
        print("No se seleccionó ningún área. Cancelado.")
        return
        
    crop_rect = selector.rect
    print(f"Área seleccionada correctamente. Procesando {len(doc)} páginas...")
    
    markdown_lines = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # 1. Generar la imagen recortada
        pix = page.get_pixmap(dpi=150, clip=crop_rect)
        image_filename = f"{base_name}_pagina_{page_num + 1}.png"
        image_path = os.path.join(images_dir, image_filename)
        pix.save(image_path)
        
        # 2. Extraer el texto fuera del área de recorte
        text = extraer_texto_fuera_de_recorte(page, crop_rect)
        
        # 3. Formatear en Markdown usando dinámicamente la carpeta configurada
        markdown_lines.append(f"## Página {page_num + 1}\n\n")
        markdown_lines.append(f"![]({images_dir}/{image_filename})\n\n")
        if text:
            markdown_lines.append(f"{text}\n\n")
        markdown_lines.append("---\n\n")
        
    with open(output_md_path, "w", encoding="utf-8") as f:
        f.writelines(markdown_lines)
        
    print(f"¡Proceso completado! Archivo Markdown generado en: {output_md_path}")
    print(f"Las imágenes se han guardado en la carpeta: {images_dir}/")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convierte un PDF a Markdown extrayendo diapositivas recortadas y texto.")
    parser.add_argument("pdf", nargs="?", default="SophosEndpointAccessandNavigationEP0520v7.0.pdf", help="Ruta del archivo PDF")
    parser.add_argument("-d", "--dir", default="_recursos", help="Carpeta personalizada para las imágenes (por defecto: _recursos)")
    
    args = parser.parse_args()
    
    salida_md = "resultado.md"
    pdf_a_markdown_visual(args.pdf, salida_md, images_dir=args.dir)