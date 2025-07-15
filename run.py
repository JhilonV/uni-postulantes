import subprocess
import os

def run_flask():
    os.chdir('app')
    subprocess.run(['python', 'app.py'])

def run_etl():
    os.chdir('etl')
    subprocess.run(['python', 'etl.py'])

def main():
    print("Que deseas ejecutar?")
    print("1. Flask (app web)")
    print("2. ETL (proceso de datos)")
    op = input("Elige (1/2): ")
    if op == "1":
        run_flask()
    elif op == "2":
        run_etl()
    else:
        print("Opcion no valida.")

if __name__ == "__main__":
    main()
