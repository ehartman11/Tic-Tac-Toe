import tkinter as tk
import tic_tac_toe_logic as g
import records

btnDict = {}
userName = ""
oppoName = ""

# Create the main window
mainWindow = tk.Tk()
mainWindow.title('Tic Tac Toe')
mainWindow.geometry("200x200+800+300")

vBar = tk.IntVar(value=1)
buttonFrame = tk.Frame(mainWindow, relief="sunken")

entryLabel = tk.Label(mainWindow)
entryLabel.config(text="Enter user's name: ")
entryLabel.place(x='50', y='55')

userEntry = tk.Entry(mainWindow, relief='sunken')
userEntry.place(x='50', y='75', width=100)

buttonEntry = tk.Button(mainWindow, relief='raised')
buttonEntry.configure(text='Enter', command=lambda: set_play_screen())
buttonEntry.place(x='155', y='75', height='19')


def set_oppo():
    global oppoName, userEntry, entryLabel, buttonEntry

    oppoName = ""
    entryLabel = tk.Label(mainWindow)
    entryLabel.config(text="Enter opponent's name: ")
    entryLabel.place(x='50', y='55')

    userEntry = tk.Entry(mainWindow, relief='sunken')
    userEntry.place(x='50', y='75', width=100)

    buttonEntry = tk.Button(mainWindow, relief='raised')
    buttonEntry.configure(text='Enter', command=lambda: [update_oppo(), entryLabel.destroy(),
                                                         userEntry.destroy(), buttonEntry.destroy()])
    buttonEntry.place(x='155', y='75', width='19')


def update_oppo():
    global oppoName
    oppoName = userEntry.get()
    reset_buttonFrame()
    reset_board()
    g.start_game(1)


def set_play_screen():
    global userName
    userName = userEntry.get()
    g.set_user()

    entryLabel.destroy()
    userEntry.destroy()
    buttonEntry.destroy()

    buttonPlayCPU = tk.Button(mainWindow, relief='raised')
    buttonPlayCPU.grid(row=0, column=0, columnspan=2, sticky='e')
    buttonPlayCPU.configure(text='Play CPU', command=lambda: [reset_buttonFrame(), reset_board(), g.start_game(0)])

    buttonPlay1v1 = tk.Button(mainWindow, relief='raised')
    buttonPlay1v1.grid(row=0, column=2, columnspan=2, sticky='w')
    buttonPlay1v1.configure(text='Play 1v1', command=lambda: [set_oppo()])

    buttonStats = tk.Button(mainWindow, relief='raised', command=lambda: [set_stat_window(), buttonStats.destroy()])
    buttonStats.grid(row=0, column=4, sticky='w')
    buttonStats.configure(text='Stats')

    easyRadio = tk.Radiobutton(mainWindow, variable=vBar, value=1, text='Easy')
    easyRadio.grid(row=1, column=0, sticky='ws')
    medRadio = tk.Radiobutton(mainWindow, variable=vBar, value=2, text='Medium')
    medRadio.grid(row=2, column=0, sticky='w')
    hardRadio = tk.Radiobutton(mainWindow, variable=vBar, value=3, text='Hard')
    hardRadio.grid(row=3, column=0, sticky='nw')


def reset_buttonFrame():
    global buttonFrame
    buttonFrame.destroy()
    buttonFrame = tk.Frame(mainWindow, relief='sunken')
    buttonFrame.place(x=85, y=75)


def set_stat_window():
    def replace_statButton():
        buttonStats = tk.Button(mainWindow, relief='raised', command=lambda: set_stat_window())
        buttonStats.grid(row=0, column=4, sticky='w')
        buttonStats.configure(text='Stats')

    g.P1.reset_stats()

    buttonStats = tk.Button(mainWindow, relief='raised', command=lambda: set_stat_window())
    buttonStats.grid(row=0, column=4, sticky='w')
    buttonStats.configure(text='Stats')

    statsFrame = tk.LabelFrame(mainWindow, relief='raised')
    statsFrame.place(x='10', y='10', height='150', width='180')
    header = ['Opponent', 'Wins', 'Losses', 'Ties']
    for i in range(4):
        label = tk.Label(statsFrame, text=header[i], underline=0)
        label.grid(row=0, column=i)
    exitButton = tk.Button(statsFrame, text='x', relief='ridge', command=lambda: [statsFrame.destroy(), buttonStats.destroy(),
                                                                                  replace_statButton()])
    exitButton.grid(row=0, column=4, sticky='nw')
    records.playerStats.download_stats(g.P1)
    rw = 1
    cl = 0
    for k in g.P1.stats:
        label = tk.Label(statsFrame, text=k)
        label.grid(row=rw, column=cl)
        cl += 1
        for v in g.P1.stats[k]:
            label = tk.Label(statsFrame, text=v)
            label.grid(row=rw, column=cl)
            cl += 1
        cl = 0
        rw += 1


def replace_button(b):
    rw = b[2]
    cl = b[3]
    b[0].destroy()
    if g.game.win_state is False:
        b = tk.Button(buttonFrame, relief='sunken')
        b.grid_configure(row=rw, column=cl)
        b.configure(text=f' {g.game.current_player.sym} ')
    else:
        b = tk.Button(buttonFrame, relief='raised')
        b.grid_configure(row=rw, column=cl)
        b.configure(text='     ')


def reset_board():
    for i in range(9):
        btnDict[f'btn{str(i + 1)}'] = [tk.Button(buttonFrame, relief='raised'), i + 1]
    btn = 1
    for r in range(3):
        for c in range(3):
            btnDict[f'btn{btn}'].append(r)
            btnDict[f'btn{btn}'].append(c)
            place_button(btnDict[f'btn{btn}'])
            btn += 1


def place_button(b):
    b[0].grid(row=b[2], column=b[3], sticky='news')
    b[0].configure(text='    ', command=lambda: [replace_button(b), g.game.update(b[1])])


def start_game():
    mainWindow.mainloop()

