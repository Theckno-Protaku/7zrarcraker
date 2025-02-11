# 7z and RAR File Extractor with password dictionary

This is a program to extract files in **7z** and **RAR** format. **It is not compatible with ZIP files.**

## Dependencies
Before running the program, install the following dependencies using `pip`:

```sh
pip install rarfile py7zr pyzipper rarfile tqdm unrar patool chardet
```

## Additional Requirements
### Windows
If you are using Windows, make sure you have installed:
- [7-Zip](https://www.7-zip.org/download.html)
- [UnRar](https://www.rarlab.com/rar_add.htm)

These programs are necessary to handle RAR and 7z files correctly.

## Usage
Run the script from the terminal or command line to extract supported files. **It is recommended to use it from VSCode.**

Additionally, the program requires a **password dictionary** to attempt extraction of protected files.

### Creating an Executable File
If you want to create an `.exe` file, follow these steps:

#### Install **pyinstaller**
```sh
pip install pyinstaller
```

#### Generate the Executable
```sh
pyinstaller --onefile --noconsole descompress.py
```

### Important Note
Once the `.exe` file is created, you must have `UnRar.exe` in the same folder for it to work correctly.

