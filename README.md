# Descompresor de Archivos 7z y RAR

Este es un programa para descomprimir archivos en formato **7z** y **RAR**. **No es compatible con archivos ZIP.**

## Dependencias
Antes de ejecutar el programa, instala las siguientes dependencias con `pip`:

```sh
pip install rarfile py7zr pyzipper rarfile tqdm unrar patool chardet
```

## Requisitos Adicionales
### Windows
Si usas Windows, asegúrate de tener instalados:
- [7-Zip](https://www.7-zip.org/download.html)
- [UnRar](https://www.rarlab.com/rar_add.htm)

Estos programas son necesarios para manejar archivos RAR y 7z correctamente.

## Uso
Ejecuta el script desde la terminal o línea de comandos para descomprimir archivos compatibles(Recomiendo usar desde VsCode. Si quieres crear un archivo .exe haz lo siguiente
##
instalar **pyinstaller**

```sh
pip install pyinstaller
```

##
Luego ejecuta 
```sh
pyinstaller --onefile --noconsole descompress.py
```

##
**NOTA** Una vez creado el archivo .exe debes tener UnRar.exe en la misma carpeta.
