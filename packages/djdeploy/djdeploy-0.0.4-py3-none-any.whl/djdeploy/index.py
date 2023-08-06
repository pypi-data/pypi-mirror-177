from tkinter import *
from tkinter import filedialog
import paramiko
import os
import webbrowser
import time
from threading import Thread
import pyautogui
import sys


def openFile():
    filepath = filedialog.askopenfilename(
        initialdir="C:\\Users",
        title="Navigate to pem file",
        filetypes=(("Pem Files","*.pem"),))
    return filepath


def is_git_repo(repository):
    try:
        branches = os.system(f'git ls-remote --exit-code -h -q {repository}')
        if branches == 0: return True
        raise Exception
    except Exception as err:
        print('Git Error: ', err.__class__.__name__)
        return False


def showPrint(stdout, stderr):
    for line in stdout.readlines(): print(line.strip())
    for line in stderr: print(line.strip())


def pemDeployment():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        host = input('Please enter your server host name ( Public IPV4 Address)\n> ')
        username = input('Please enter your server username: ')
        key_file = str(openFile())
        print('Connecting...')
        ssh.connect(host, username=username, key_filename=key_file)
        print('Connected!')

        repo = input('Git Repo Link: ')
        token = input('Git Token: ')
        repository = repo.replace('https://', f'https://{token}@')
        repo = is_git_repo(repository)
        if repo == True:
            branch = input('Please also specify branch name: ')
        else:
            print('Invalid git details!')
            exit()
        folder_name = repository.split('/')[-1].replace('.git', '')

        print('Cloning git repo\'s on server!')
        stdin, stdout, stderr = ssh.exec_command(f'git clone -b {branch} {repository} && mv {folder_name}/ project && git clone https://{token}@github.com/ardevpk/setup.git ')
        showPrint(stdout, stderr)
        print('Cloning completed!')

        print('Executing scripts on server!')
        print('It takes a little bit of time, So you can a grab a cup of coffee!')
        stdin, stdout, stderr = ssh.exec_command(f'sudo python3 ./setup/main.py')
        showPrint(stdout, stderr)
        print('Execution completed!')

        print('Restarting...')
        stdin, stdout, stderr = ssh.exec_command(f'./restart.sh')
        showPrint(stdout, stderr)
        print('Restarted!')
        ssh.close()
        print('Opening...')
        time.sleep(2)
        if input('Wants to open host in browser?\n(Y/n): ').lower()=='y':
            webbrowser.open(f'http://{host}')

        if input('Wants to connect to server?\n(Y/n): ').lower()=='y':
            os.system(f'ssh -i {key_file} {username}@{host}')
        else:
            print('Thanks for using the djdeploy!')
            exit()

    except Exception as err:
        print('Error: ', err.__class__.__name__)


def passwordDeployment():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        host = input('Please enter your server host name ( Public IPV4 Address)\n> ')
        username = input('Please enter your server username: ')
        password = input('Please enter your server password: ')
        print('Connecting...')
        ssh.connect(host, username=username, password=password)
        print('Connected!')

        repo = input('Git Repo Link: ')
        token = input('Git Token: ')
        repository = repo.replace('https://', f'https://{token}@')
        repo = is_git_repo(repository)
        if repo == True:
            branch = input('Please also specify branch name: ')
        else: raise Exception

        folder_name = repository.split('/')[-1].replace('.git', '')
        
        print('Cloning git repo\'s on server!')
        stdin, stdout, stderr = ssh.exec_command(f'git clone -b {branch} {repository} && mv {folder_name}/ project && git clone https://{token}@github.com/ardevpk/setup.git ')
        showPrint(stdout, stderr)
        print('Cloning completed!')

        print('Executing scripts on server!')
        ssh.close()


        def openSystem():
            os.system(f'ssh {username}@{host} sudo python3 setup/main.py')

        thread = Thread(target=openSystem, args=())
        thread.start()
        time.sleep(3)
        pyautogui.write(str(password))
        pyautogui.press('enter')

        while True:
            if not thread.is_alive():
                print('Execution completed!')
                if input('Wants to open host in browser?\n(Y/n): ').lower()=='y':
                    webbrowser.open(f'http://{host}')
                    break
        
        print('Thanks for using the djdeploy!')
        exit()

    except Exception as err:
        print('Error: ', err.__class__.__name__)


def main():
    helpp = ['\tArgument, Description.', '\t--pem, Aws deployment with pem.', '\t--passwd, DigitalOcrean deployment with username and password login.']
    if len(sys.argv) > 1:
        argv = sys.argv[1]
        if argv == '--pem': pemDeployment()
        elif argv == '--passwd': passwordDeployment()
        elif argv == '--help': print("\n".join(helpp))
        else:
            print('Please pass any valid argument to execute!')
            exit()
    else:
        print('Please pass any argument to execute!')
        exit()


if __name__ == '__main__':
    main()
