import subprocess
import os

extended = ".py"
path_to_main_dir = r"C:\Users\PC\Desktop\serwer\!serwer"
path_to_output = r"C:\Users\PC\Desktop\serwer\!serwer\dist"
# absolute path for all of files
path_to_zamowienia = path_to_main_dir + r"\zamowienia" + extended
path_to_dostawy = path_to_main_dir + r"\dostawy" + extended
path_to_uzytkownicy = path_to_main_dir + r"\uzytkownicy" + extended
# list with path files
files = [path_to_zamowienia, path_to_dostawy, path_to_uzytkownicy]

def execute_installer(path_file):
    output_file = path_to_output + path_file.split("/")[-1].split(".")[0]
    if del_exists(output_file+".exe"):
        name = fr"C:\Users\PC\AppData\Roaming\Python\Python38\Scripts\pyinstaller.exe --onefile --windowed --noconsole --icon=icon.ico --distpath {path_to_output} {path_file}"
        subprocess.call(name, shell=True)
        print(f"Pomyslnie wygenerowano plik exe do {path_file}")
    else:
        print(f"Nie można wykonac konwersji pliku {path_file}\nNajprawdopodobniej wina jest brak uprawnień")


def del_exists(path_file):
    if os.path.isfile(path_file):
        try:
            name = "rm " + path_file
            subprocess.call(name, shell=True)
        except:
            return False
    return True


for i in files:
    execute_installer(i)
