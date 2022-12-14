import json
from tkinter import *
import paho.mqtt.client as mqtt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure


# this function is called when the subscriber receives a message
# we are simply display some data items on screen, normally this
# data is sent to another system to be cleansed, stored and processed
# and then some action can be taken
class Subscriber:
    def __init__(self, name, topic):
        self.topic = topic
        self.graph_name = variable.get()
        self.client = mqtt.Client()

        self.window = Toplevel(master)

        self.output = None

        self.plot1 = None

        self.x_vals = []
        self.y_vals = []

        # setting the title
        self.window.title(name)

        # dimensions of the main window
        self.window.geometry("700x630")

        self.canvas = Canvas(self.window, width=500, height=500, bg='white')
        self.canvas.pack()

        # button that displays the plot
        self.plot_button = Button(master=self.window, command=self.start_clicked, height=2, width=10, text="Start")

        self.clear_button = Button(master=self.window, command=self.stop_clicked, height=2, width=10, text="Stop",
                                   background="yellow")

        self.fig = Figure(figsize=(5, 5), dpi=100, constrained_layout=True)
        # place the button
        self.plot_button.pack()
        self.clear_button.pack()

        # run the gui

    def on_message(self, client, userdata, message):
        data = message.payload.decode('utf-8')
        obj = json.loads(data)
        self.update_graph(obj["Stock Price"])
        print(obj["Time"] + ': $' + str(obj['Stock Price']))

    def start_clicked(self, *args):
        self.client.on_message = self.on_message
        self.client.connect('localhost', 1883)
        self.client.subscribe('STOCKS/' + self.topic)
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
        self.plot1.clear()
        self.plot1.set_title(self.graph_name)
        self.plot1.set_xlabel("Weeks")
        self.plot1.set_ylabel("Price")

        self.plot1.plot(self.x_vals, self.y_vals)
        self.output.draw()

    def update_graph(self, new_value):
        if self.isfloat(new_value):
            self.y_vals.append(new_value)
            x = len(self.x_vals)
            self.x_vals.append(x)
            self.animate()

    def stop_clicked(self, *args):
        self.client.unsubscribe('STOCKS/' + self.topic)
        self.client.loop_stop()

        # graph stuff

        if self.output:
            for child in self.canvas.winfo_children():
                child.destroy()

        self.output = None
        self.x_vals = []
        self.y_vals = []
        self.fig.clear()

    def isfloat(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False


def subscribe():
    name = t.get("1.0", "end-1c")
    sub = Subscriber(name, variable.get())


master = Tk()
master.title("Master")
master.geometry("250x250")

fig_master = Figure(figsize=(5, 5), dpi=100)
l = Label(text="Enter Name of Subscriber:")
t = Text(master=master, height=2, width=20, bg="light yellow")
sub_button = Button(master=master, command=subscribe, height=2, width=10, text="Subscribe", background="yellow")

OPTIONS = ["TSLA", "NVDA", "AAPL"]  # etc

variable = StringVar(master)
variable.set(OPTIONS[0])  # default value
options = OptionMenu(master, variable, *OPTIONS)

l.pack()
t.pack()
options.pack()
sub_button.pack()
mainloop()
