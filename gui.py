import PySimpleGUI as gui
import subprocess

def ExecuteCommandSubprocess(command, *args):
    try:
        sp = subprocess.Popen([command, *args], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = sp.communicate()
        if out:
            print(out.decode("utf-8"))
        if err:
            print(err.decode("utf_8"))
    except:
        pass

layout = [
    [gui.Text('Simulator output...', size=(40,1))],
    [gui.Output(size=(88,20), font='Courier 10')],
    [gui.ReadButton('Run'), gui.Button('Exit')]
]

window = gui.Window('Dojo Simulator').Layout(layout)

while True:
    (button, value) = window.Read()
    if button == 'Run':
        ExecuteCommandSubprocess('python', './main.py')
    if button == 'Exit' or button is None:
        break
