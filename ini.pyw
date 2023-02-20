import os
import subprocess


def main():
    
    git_2 = 'git pull'
    completed = subprocess.run(git_2 , shell=True)
    #completed.returncode
    print(completed.returncode)
    #print(os.system(git_2))
    print('Todo OK, se iniciará el programa')
    librerias = 'pip install -r requirements.txt'
    pip_librerias = subprocess.run(librerias, shell=True)
    print(pip_librerias.returncode)
    inicio = "py ini/inicio.py"
    iniciar = subprocess.run(inicio, shell=True)
    print(iniciar.returncode)
    
    

if __name__ == '__main__':
    main()
    