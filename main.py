import tkinter as tk
from tkinter import filedialog
from pybtex.plugin import find_plugin
from pybtex.database import parse_file
import pyperclip

def convertir_bib_a_apa7():
    root = tk.Tk()
    root.withdraw()

    bib_file = filedialog.askopenfilename(
        title="Selecciona tu archivo .bib",
        filetypes=[("Archivos BibTeX", "*.bib")]
    )

    if not bib_file:
        print("No se seleccionó ningún archivo.")
        return
    try:
        estilo = find_plugin('pybtex.style.formatting', 'apa7')()
        backend = find_plugin('pybtex.backends', 'plaintext')()
        bib_data = parse_file(bib_file)

        referencias = []

        for entry in bib_data.entries.values():
            try:
                authors = entry.persons.get('author', [])
                if authors:
                    primer_autor = str(authors[0].last_names[0])
                else:
                    primer_autor = "AutorDesconocido"
                year = entry.fields.get('year', 's.f.')
                formatted_entry = list(estilo.format_entries([entry]))[0]
                referencia_completa = formatted_entry.text.render(backend)
                referencia_final = f"({primer_autor}, {year}) {referencia_completa}"
                referencias.append(referencia_final)

            except Exception:
                author = ", ".join(str(a) for a in entry.persons.get('author', []))
                title = entry.fields.get('title', 'Sin título')
                year = entry.fields.get('year', 's.f.')
                referencias.append(f"({author}, {year}) {title}.")

        texto_final = "\n\n".join(referencias)
        pyperclip.copy(texto_final)
        print("Referencias copiadas al portapapeles.")
        print(texto_final)

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
    finally:
        root.destroy()
        input("Presiona Enter para salir... \n")
if __name__ == "__main__":
    convertir_bib_a_apa7()
