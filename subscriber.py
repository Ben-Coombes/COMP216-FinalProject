import matplotlib
import paho.mqtt.client as mqtt
import json
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import messagebox


# this function is called when the subscriber receives a message
# we are simply display some data items on screen, normally this
# data is sent to another system to be cleansed, stored and processed
# and then some action can be taken
def on_message(client, userdata, message):
    data = message.payload.decode('utf-8')
    obj = json.loads(data)
    print(f'Blood Pressure @ Time: {obj["Time"]}')


def start_clicked(*args):
    client.on_message = on_message
    client.connect('localhost', 1883)
    client.subscribe('COMP216/test')
    client.loop_start()

    # graph stuff
    global output, fig
    fig = Figure(figsize=(5, 5), dpi=100)
    y = [i ** 2 for i in range(101)]
    # adding the subplot
    plot1 = fig.add_subplot(111)

    # plotting the graph
    plot1.plot(y)

    # creating the Tkinter canvas
    # containing the Matplotlib figure
    output = FigureCanvasTkAgg(fig, master=canvas)
    output.draw()

    # placing the canvas on the Tkinter window
    output.get_tk_widget().pack()


def stop_clicked(*args):
    client.loop_stop()

    # graph stuff
    global output
    if output:
        for child in canvas.winfo_children():
            child.destroy()
        # or just use canvas.winfo_children()[0].destroy()

    output = None



client = mqtt.Client()

window = Tk()

output = None
fig = None

# setting the title
window.title('Plotting in Tkinter')

# dimensions of the main window
window.geometry("700x700")

canvas = Canvas(window, width=500, height=500, bg='white')
canvas.pack()

# button that displays the plot
plot_button = Button(master = window, command = start_clicked, height = 2, width = 10, text = "Start")

clear_button = Button(master = window, command = stop_clicked, height = 2, width = 10, text = "Stop", background = "yellow")

# place the button
plot_button.pack()
clear_button.pack()

# run the gui
window.mainloop()