import subprocess
import os

<<<<<<< HEAD
=======

>>>>>>> 99858378a62303818c8829e8a2e7dbe4ac37969d
def run_flask():
    os.chdir('app')
    subprocess.run(['python', 'app.py'])

def run_etl():
    os.chdir('etl')
    subprocess.run(['python', 'etl.py'])

<<<<<<< HEAD
def main():
    print("Que deseas ejecutar?")
=======

def main():
    print("¿Qué deseas ejecutar?")
>>>>>>> 99858378a62303818c8829e8a2e7dbe4ac37969d
    print("1. Flask (app web)")
    print("2. ETL (proceso de datos)")
    op = input("Elige (1/2): ")
    if op == "1":
        run_flask()
    elif op == "2":
        run_etl()
    else:
<<<<<<< HEAD
        print("Opcion no valida.")

if __name__ == "__main__":
    main()
=======
        print("Opción no válida.")

if __name__ == "__main__":
    main() 
>>>>>>> 99858378a62303818c8829e8a2e7dbe4ac37969d
