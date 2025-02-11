import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import subprocess
import threading
import os
from pathlib import Path
import re

class UniversalExtractor:
    def __init__(self, root):
        self.root = root
        self.root.title("7z and RAR, Zip not work")
        self.root.geometry("800x600")
        
        # Variables para almacenar las rutas
        self.archivo_comprimido = tk.StringVar()
        self.archivo_diccionario = tk.StringVar()
        self.directorio_salida = tk.StringVar()
        
        # Variable para controlar la búsqueda
        self.busqueda_activa = False
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Sección archivo comprimido
        ttk.Label(main_frame, text="Archivo comprimido:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.archivo_comprimido, width=60).grid(row=0, column=1, padx=5)
        ttk.Button(main_frame, text="Buscar", command=self.buscar_archivo).grid(row=0, column=2)
        
        # Sección archivo diccionario
        ttk.Label(main_frame, text="Diccionario:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.archivo_diccionario, width=60).grid(row=1, column=1, padx=5)
        ttk.Button(main_frame, text="Buscar", command=self.buscar_diccionario).grid(row=1, column=2)
        
        # Sección directorio de salida
        ttk.Label(main_frame, text="Directorio de salida:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.directorio_salida, width=60).grid(row=2, column=1, padx=5)
        ttk.Button(main_frame, text="Buscar", command=self.buscar_directorio).grid(row=2, column=2)
        
        # Frame para opciones
        options_frame = ttk.LabelFrame(main_frame, text="Opciones", padding="5")
        options_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Timeout
        self.timeout_var = tk.IntVar(value=10)
        ttk.Label(options_frame, text="Timeout (segundos):").grid(row=0, column=0, padx=5)
        ttk.Entry(options_frame, textvariable=self.timeout_var, width=5).grid(row=0, column=1)
        
        # Barra de progreso
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(main_frame, length=600, mode='determinate', variable=self.progress_var)
        self.progress.grid(row=4, column=0, columnspan=3, pady=10)
        
        # Área de texto para el log
        self.log_area = scrolledtext.ScrolledText(main_frame, height=15, width=90)
        self.log_area.grid(row=5, column=0, columnspan=3, pady=5)
        
        # Frame para botones de control
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=10)
        
        # Botones de inicio y parada
        self.start_button = ttk.Button(button_frame, text="Iniciar búsqueda", command=self.iniciar_busqueda)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Detener", command=self.detener_busqueda, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
    def buscar_archivo(self):
        filename = filedialog.askopenfilename(
            filetypes=[
                ("Archivos comprimidos", "*.rar;*.zip;*.7z;*.001;*.part1.rar;*.zip.001"),
                ("Archivos RAR", "*.rar;*.part1.rar"),
                ("Archivos ZIP", "*.zip;*.zip.001"),
                ("Archivos 7Z", "*.7z;*.7z.001"),
                ("Todos los archivos", "*.*")
            ]
        )
        if filename:
            self.archivo_comprimido.set(filename)
            # Autocompletar directorio de salida
            self.directorio_salida.set(str(Path(filename).parent / "extracted"))
            
    def buscar_diccionario(self):
        filename = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if filename:
            self.archivo_diccionario.set(filename)
            
    def buscar_directorio(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directorio_salida.set(directory)
            
    def log(self, mensaje):
        self.log_area.insert(tk.END, mensaje + "\n")
        self.log_area.see(tk.END)
        
    def detectar_formato(self, archivo):
        """Detecta el formato y tipo (normal/volumen) del archivo"""
        nombre = archivo.lower()
        
        # Patrones para detectar archivos por volumen
        patrones = {
            'rar_vol': r'\.part\d+\.rar$',
            'zip_vol': r'\.z\d+$|\.zip\.\d+$',
            '7z_vol': r'\.7z\.\d+$'
        }
        
        # Detectar tipo de archivo y si es volumen
        if re.search(patrones['rar_vol'], nombre) or nombre.endswith('.rar'):
            return 'rar', bool(re.search(patrones['rar_vol'], nombre))
        elif re.search(patrones['zip_vol'], nombre) or nombre.endswith('.zip'):
            return 'zip', bool(re.search(patrones['zip_vol'], nombre))
        elif re.search(patrones['7z_vol'], nombre) or nombre.endswith('.7z'):
            return '7z', bool(re.search(patrones['7z_vol'], nombre))
        else:
            return None, False
            
    def verificar_herramientas(self):
        """Verifica que las herramientas necesarias estén instaladas"""
        herramientas = {
            '7z': False,
            'unrar': False
        }
        
        try:
            subprocess.run(['7z'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            herramientas['7z'] = True
        except FileNotFoundError:
            pass
            
        try:
            subprocess.run(['unrar'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            herramientas['unrar'] = True
        except FileNotFoundError:
            pass
            
        return herramientas
        
    def probar_password(self, archivo, password, formato):
        """Intenta extraer el archivo con la contraseña dada"""
        try:
            if formato == 'rar':
                cmd = ['unrar', 'x', f'-p{password}', archivo, self.directorio_salida.get(), '-y']
            else:  # zip y 7z
                cmd = ['7z', 'x', f'-p{password}', archivo, f'-o{self.directorio_salida.get()}', '-y']
                
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=self.timeout_var.get()
            )
            
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            self.log(f"Timeout al probar: {password}")
            return False
        except Exception as e:
            self.log(f"Error al probar {password}: {str(e)}")
            return False
            
    def iniciar_busqueda(self):
        # Verificaciones básicas
        if not all([self.archivo_comprimido.get(), self.archivo_diccionario.get(), self.directorio_salida.get()]):
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return
            
        # Verificar herramientas instaladas
        herramientas = self.verificar_herramientas()
        if not herramientas['7z'] and not herramientas['unrar']:
            messagebox.showerror("Error", "Necesita tener instalado 7-Zip o UnRAR")
            return
            
        # Detectar formato
        formato, es_volumen = self.detectar_formato(self.archivo_comprimido.get())
        if not formato:
            messagebox.showerror("Error", "Formato de archivo no soportado")
            return
            
        if formato == 'rar' and not herramientas['unrar']:
            messagebox.showerror("Error", "Necesita tener instalado UnRAR para archivos RAR")
            return
            
        if (formato in ['zip', '7z']) and not herramientas['7z']:
            messagebox.showerror("Error", "Necesita tener instalado 7-Zip para archivos ZIP/7Z")
            return
            
        # Crear directorio de salida
        os.makedirs(self.directorio_salida.get(), exist_ok=True)
        
        # Iniciar la búsqueda en un hilo separado
        self.busqueda_activa = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        self.log(f"Iniciando búsqueda para archivo {formato.upper()}" + (" (multivolumen)" if es_volumen else ""))
        threading.Thread(target=self.proceso_busqueda, args=(formato,), daemon=True).start()
        
    def detener_busqueda(self):
        self.busqueda_activa = False
        self.stop_button.config(state=tk.DISABLED)
        self.log("Deteniendo búsqueda...")
        
    def proceso_busqueda(self, formato):
        try:
            # Leer el diccionario
            with open(self.archivo_diccionario.get(), "r", encoding='utf-8') as f:
                contraseñas = [line.strip() for line in f]
            
            total_passwords = len(contraseñas)
            self.progress_var.set(0)
            self.log(f"Iniciando búsqueda con {total_passwords} contraseñas...")
            
            for idx, contraseña in enumerate(contraseñas, 1):
                if not self.busqueda_activa:
                    break
                    
                # Actualizar progreso
                self.progress_var.set(idx / total_passwords * 100)
                self.log(f"Probando: {contraseña}")
                
                if self.probar_password(self.archivo_comprimido.get(), contraseña, formato):
                    self.log(f"\n¡CONTRASEÑA ENCONTRADA! ✅: {contraseña}")
                    messagebox.showinfo("Éxito", f"¡Contraseña encontrada!: {contraseña}")
                    return
            
            if self.busqueda_activa:
                self.log("\nBúsqueda completada sin éxito ❌")
                messagebox.showinfo("Fin", "No se encontró la contraseña en la lista")
            else:
                self.log("\nBúsqueda detenida por el usuario")
                
        except Exception as e:
            self.log(f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))
            
        finally:
            self.busqueda_activa = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = UniversalExtractor(root)
    root.mainloop()