import tkinter as tk
from tkinter import messagebox
from functions.reader import Reader
from functions.nfa import NFA

class AFNGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de AFNs")  # Título de la ventana
        self.regex_entry = None
        self.create_widgets()

    def create_widgets(self):
        # Crear los widgets de la interfaz
        program_title_label = tk.Label(self.root, text=program_title, font=("Arial", 14))
        program_title_label.pack(pady=10)

        regex_label = tk.Label(self.root, text="Expresión regular:")
        regex_label.pack(pady=5)

        self.regex_entry = tk.Entry(self.root, width=50)
        self.regex_entry.pack(pady=5)

        create_afn_button = tk.Button(self.root, text="Crear AFN", command=self.create_afn)
        create_afn_button.pack(pady=10)

        exit_button = tk.Button(self.root, text="Salir", command=self.root.quit)
        exit_button.pack(pady=10)

    def create_afn(self):
        # Método para crear el AFN y mostrar el resultado
        regex = self.regex_entry.get()

        if not regex:
            messagebox.showerror("Error", "Por favor ingrese una expresión regular.")
            return

        try:
            reader = Reader(regex)
            tree = reader.Reader()

            nfa = NFA(tree, regex)
            nfa.WriteNFADiagram()

            messagebox.showinfo("AFN Creado", "Se ha creado el AFN correctamente.")

        except AttributeError as e:
            messagebox.showerror("Error", f"Expresión no válida: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

# Definir las constantes y mensajes del programa
program_title = '''
        AUTOMATAS FINITOS        

Genera AFNs basados en una expresión regular.
'''

# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = AFNGeneratorApp(root)
    root.mainloop()
