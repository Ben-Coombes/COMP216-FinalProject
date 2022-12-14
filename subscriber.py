import matplotlib
import paho.mqtt.client as mqtt
import json
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.animation import FuncAnimation
from tkinter import messagebox


# this function is called when the subscriber receives a message
# we are simply display some data items on screen, normally this
# data is sent to another system to be cleansed, stored and processed
# and then some action can be taken
class Subscriber:
    def __init__(self):
        self.client = mqtt.Client()

        self.window = Tk()

        self.output = None

        self.plot1 = None

        self.x_vals = []
        self.y_vals = []

        # setting the title
        self.window.title('Subscriber')

        # dimensions of the main window
        self.window.geometry("700x700")

        self.canvas = Canvas(self.window, width=500, height=500, bg='white')
        self.canvas.pack()

        # button that displays the plot
        self.plot_button = Button(master=self.window, command=self.start_clicked, height=2, width=10, text="Start")

        self.clear_button = Button(master=self.window, command=self.stop_clicked, height=2, width=10, text="Stop",
                                   background="yellow")

        self.fig = Figure(figsize=(5, 5), dpi=100)
        # place the button
        self.plot_button.pack()
        self.clear_button.pack()

        # run the gui
        self.window.mainloop()


    def on_message(self, client, userdata, message):
        data = message.payload.decode('utf-8')
        obj = json.loads(data)
        print(f'Blood Pressure @ Time: {obj["Time"]}')
        self.update_graph(obj["Stock Price"])

    def start_clicked(self, *args):
        self.client.on_message = self.on_message
        self.client.connect('localhost', 1883)
        self.client.subscribe('STOCKS/Tesla')
        self.client.loop_start()

        # graph stuff
        y = [i ** 2 for i in range(101)]
        # adding the subplot
        self.plot1 = self.fig.add_subplot(111)

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        self.output = FigureCanvasTkAgg(self.fig, master=self.canvas)
        self.output.draw()

        # placing the canvas on the Tkinter window
        self.output.get_tk_widget().pack()

    def animate(self):
        print("animate")
        self.plot1.clear()
        self.plot1.plot(self.x_vals, self.y_vals)
        self.output.draw()


    def update_graph(self, new_value):
        print(new_value)
        self.y_vals.append(new_value)
        x = len(self.x_vals)
        self.x_vals.append(x)
        self.animate()

    def stop_clicked(self, *args):
        self.client.loop_stop()

        # graph stuff

        if self.output:
            for child in self.canvas.winfo_children():
                child.destroy()
            # or just use canvas.winfo_children()[0].destroy()

        self.output = None
        self.x_vals = []
        self.y_vals = []
        self.fig.clear()


sub = Subscriber()
