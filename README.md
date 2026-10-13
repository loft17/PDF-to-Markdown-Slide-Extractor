# PDF to Markdown Slide Extractor

Un script en Python diseñado específicamente para procesar documentos PDF con formato de diapositivas o presentaciones. Permite realizar un recorte visual interactivo de la zona de la diapositiva, extraer automáticamente las capturas página por página, filtrar el texto redundante de la imagen y empaquetarlo todo en un archivo Markdown (`.md`) limpio y estructurado.

---

## Características Principales

* **Selección Visual Interactiva**: Abre una ventana gráfica en la primera página para que puedas dibujar con el ratón el rectángulo exacto que deseas recortar (aplicándose de forma idéntica a todo el PDF).
* **Filtrado de Texto Inteligente**: Extrae únicamente el texto situado *fuera* de la zona recortada (por ejemplo, los apuntes o descripciones al pie de página), evitando duplicar el texto que ya aparece dentro de la diapositiva.
* **Organización Dinámica**: Permite definir una carpeta personalizada para almacenar las capturas (con valor por defecto `_recursos`), actualizando automáticamente las rutas dentro del archivo Markdown generado.
* **Compatibilidad Multiplataforma**: Utiliza **PyMuPDF** (`pymupdf`), ofreciendo un rendimiento rápido y alta resolución (150 DPI) en las capturas.

---

## Requisitos Previos

Asegúrate de tener instalado **Python 3** en tu sistema. Luego, instala las librerías necesarias ejecutando el siguiente comando en tu terminal:

```bash
pip install pymupdf Pillow
```

---

## Uso del Script

Puedes ejecutar el script directamente desde la terminal pasando el archivo PDF como argumento.

### 1. Uso básico (Carpeta de imágenes por defecto: `_recursos`)
```bash
py pdf_a_markdown.py tu_documento.pdf
```

### 2. Uso avanzado (Personalizando la carpeta de imágenes)
Puedes utilizar la opción `-d` o `--dir` para indicar el nombre de la carpeta donde se guardarán las capturas (las rutas del archivo Markdown se adaptarán automáticamente):
```bash
py pdf_a_markdown.py tu_documento.pdf -d imagenes_personalizadas
```

---

## ¿Cómo funciona el flujo?

1. **Lectura del PDF**: El script carga el documento utilizando PyMuPDF.
2. **Interfaz de Recorte**: Se abre una ventana emergente donde haces clic y arrastras para enmarcar la diapositiva.
3. **Procesamiento**: Al soltar el ratón, calcula las proporciones y recorre cada página del PDF generando:
   * La captura recortada de la diapositiva dentro de la carpeta seleccionada.
   * El texto inferior limpio de cada página.
4. **Generación del Markdown**: Crea un archivo `resultado.md` ordenado con la estructura visual de imagen arriba y texto abajo.

---

## Licencia
Este proyecto es de código libre y adaptable para tus flujos de trabajo de apuntes y documentación.