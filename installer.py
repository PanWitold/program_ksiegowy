import subprocess
import os

extended = ".py"
path_to_main_dir = r"C:\Users\PC\Desktop\serwer\!serwer"
path_to_output = rf"C:\Users\PC\Desktop\\"

path_to_zamowienia = path_to_main_dir + r"\zamowienia" + extended
path_to_dostawy = path_to_main_dir + r"\dostawy" + extended
path_to_uzytkownicy = path_to_main_dir + r"\uzytkownicy" + extended

files = [path_to_zamowienia, path_to_dostawy, path_to_uzytkownicy]


def execute_installer(path_file):
    if del_exists(path_file):
        print(f"Nazwa pliku: {path_file}")
        name = f"python -m pyinstaller --onefile --distpath {path_to_output} {path_file}"
        subprocess.call(name, shell=True)
    else:
        print("Nie można wykonać operacji ze względu na błąd\nNajprawdopodobniej jest to brak uprawnień")


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
