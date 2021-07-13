import subprocess

extended = ".py"
path_to_main_dir = r"C:\Users\Lenovo\PycharmProjects\program_ksiegowy"
path_to_output = rf"C:\Users\Lenovo\Desktop\\"

path_to_zamowienia = path_to_main_dir + r"\zamowienia" + extended
path_to_dostawy = path_to_main_dir + r"\dostawy" + extended
path_to_uzytkownicy = path_to_main_dir + r"\uzytkownicy" + extended

#print(path_to_zamowienia, path_to_dostawy, path_to_output, sep="\n")


def execute_installer(path_file):
    print(f"Nazwa pliku: {path_file}")
    name = f"pyinstaller --onefile --distpath {path_to_output} {path_file}"
    subprocess.call(name, shell=True)


if __name__ == '__main__':
    execute_installer(path_to_zamowienia)
