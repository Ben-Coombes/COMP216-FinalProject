import time
from tkinter import messagebox
import paho.mqtt.client as mqtt
import json
import random
from group_1_data_generator import Generator
from tkinter import *
import threading


class Publisher(threading.Thread):
    def __init__(self, start_price, volatility, trend, stock_name, pub_name):
        threading.Thread.__init__(self)
        self.running = True
        self.window = None
        self.pub_name = pub_name
        self.text = None
        self.stock_data = {
            'Time': time.asctime(),
            'Stock Price': start_price,
            'Stock Name': stock_name
        }
        self.volatility = volatility
        self.trend = trend
        self.generator = Generator(trend, volatility)
        self.client = mqtt.Client()
        self.create_window()

    def send_data(self):
        if self.running:
            self.stock_data['Time'] = time.asctime()
            self.client.connect('localhost', 1883)
            self.client.publish('STOCKS/' + self.stock_data['Stock Name'], json.dumps(self.stock_data))
            self.print_text(self.stock_data['Time'] + ' - ' + str(self.stock_data['Stock Name']) + ': $' + str(
                self.stock_data['Stock Price']))
            print(self.stock_data['Time'] + ' - ' + str(self.stock_data['Stock Name']) + ': $' + str(
                self.stock_data['Stock Price']))
            self.client.disconnect()

    def run(self):
        while self.running:
            if self.isfloat(self.stock_data['Stock Price']):
                current_price = self.stock_data['Stock Price']
            self.stock_data['Stock Price'] = self.generator.generate_stock_price(current_price)
            time.sleep(0.5)
            if random.randint(0, 100) == 1:
                print('FAILED - Publisher error no data sent to Broker')
                continue
            if random.randint(0, 200) == 1:
                self.stock_data['Stock Price'] = '######'
            self.send_data()

    def print_text(self, msg):
        self.text.insert("end", msg + "\n")
        self.text.see("end")

    def create_window(self):
        self.window = Toplevel(master)
        self.window.geometry('500x300')
        self.window.title(self.pub_name)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.text = Text(self.window, height=6, width=40)
        vsb = Scrollbar(self.window, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.running = False
            self.window.destroy()

    def isfloat(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False


def create_pub():
    name = t.get("1.0", "end-1c")
    start = float(t1.get("1.0", "end-1c"))
    vol = float(t2.get("1.0", "end-1c"))
    trend = float(t3.get("1.0", "end-1c"))
    pub = Publisher(start, vol, trend, variable.get(), name)
    pub.start()
    print('test')


if __name__ == '__main__':
    master = Tk()
    master.geometry("400x400")

    l = Label(text="Enter Name of Publisher:")
    t = Text(master=master, height=2, width=20, bg="light yellow")

    l1 = Label(text="Enter Start Price:")
    t1 = Text(master=master, height=2, width=20, bg="light yellow")

    l2 = Label(text="Enter Volatility:")
    t2 = Text(master=master, height=2, width=20, bg="light yellow")

    l3 = Label(text="Enter Trend:")
    t3 = Text(master=master, height=2, width=20, bg="light yellow")

    l4 = Label(text="Select Stock:")

    sub_button = Button(master=master, command=create_pub, height=2, width=15, text="Create Publisher",
                        background="yellow")

    OPTIONS = ["TSLA", "NVDA", "AAPL"]  # etc

    variable = StringVar(master)
    variable.set(OPTIONS[0])  # default value
    options = OptionMenu(master, variable, *OPTIONS)

    l.pack()
    t.pack()
    l1.pack()
    t1.pack()
    l2.pack()
    t2.pack()
    l3.pack()
    t3.pack()
    l4.pack()
    options.pack()
    sub_button.pack()
    master.mainloop()
