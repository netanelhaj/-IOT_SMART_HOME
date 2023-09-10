import threading
import paho.mqtt.client as mqtt
import random
from tkinter import *

# MQTT client setup
client = mqtt.Client()
client.connect("broker.hivemq.com", 1883)

# GUI setup for monitor
def lock_gui():
    root = Tk()
    root.title("Lock Sensor")
    root.geometry("250x250")

    # Label to display sensor status
    monitor_status = StringVar()
    monitor_status.set("")
    monitor_label = Label(root, textvariable=monitor_status, font=("Helvetica", 16))
    # Place the text label in the center of the window
    monitor_label.place(relx=0.5, rely=0.5, anchor=CENTER)
    # monitor_label.pack()

    # MQTT callback function
    def on_message(client, userdata, message):
        monitor_status.set("Door status: " + message.payload.decode())

    client.on_message = on_message
    client.subscribe("lock/status")

    # start the loop to process received messages
    client.loop_start()

    # Create a quit button
    quit_button = Button(root, text="Quit", command=root.destroy, font=("Helvetica", 12))
    quit_button.place(relx=1, rely=1, x=-10, y=-10, anchor=SE)

    root.mainloop()


# Function to simulate lock sensor
def lock_sensor():
    return random.choice(['Unlocked', 'Locked'])

# GUI setup for lock sensor
def monitor_gui():
    monitor = Tk()
    monitor.title("Smart Lock Application")
    monitor.geometry("375x579")

    # Label to display sensor status
    sensor_status = StringVar()
    sensor_status.set(lock_sensor())
    status_label = Label(monitor, textvariable=sensor_status)
    status_label.pack(pady=10)

    # Label to display current action
    action_label = Label(monitor, text="")
    action_label.pack(pady=10)

    # Label for password prompt
    password_label = Label(monitor, text="Enter password:")
    password_label.pack(pady=10)

    # StringVar to store the password
    password = StringVar()
    password.set("password")

    # Entry widget for password input
    password_entry = Entry(monitor, show="*", width=20)
    password_entry.pack(pady=10)

    def check_password():
        entered_password = password_entry.get()
        if entered_password == password.get():
            action_label.config(text="Correct Password", font=("Helvetica", 12))
            lock_button.config(state=NORMAL)
        else:
            action_label.config(text="Incorrect Password", font=("Helvetica", 12))

    def lock_unlock():
        if sensor_status.get() == "open":
            sensor_status.set("closed")
            client.publish("lock/status", "Locked")
            action_label.config(text="Locked door: True", font=("Helvetica", 12))
            print("Published message: Lock")
            lock_button.config(state=DISABLED)
        else:
            sensor_status.set("open")
            client.publish("lock/status", "Unlocked")
            action_label.config(text="Locked door: False", font=("Helvetica", 12))
            print("Published message: Unlock")
            lock_button.config(state=DISABLED)

    # Button to check the password
    submit_button = Button(monitor, text="Enter", command=check_password)
    submit_button.pack(pady=10)

    # Button to lock or unlock the sensor
    lock_button = Button(monitor, text="Lock/Unlock", command=lock_unlock,state=DISABLED)
    lock_button.pack(pady=10)

    def change_password():
        change_password_window = Toplevel(monitor)
        change_password_window.title("Change Password")
        change_password_window.geometry("300x150")

        # Label for new password
        new_password_label = Label(change_password_window, text="New password:")
        new_password_label.pack(pady=10)

        # Entry widget for new password
        new_password_entry = Entry(change_password_window, show="*", width=20)
        new_password_entry.pack(pady=10)

        # Function to save the new password
        def save_password():
            new_password = new_password_entry.get()
            password.set(new_password)
            change_password_window.destroy()

        # Save password button
        save_password_button = Button(change_password_window, text="Save", command=save_password)
        save_password_button.pack(pady=10)

    # Password change button
    change_password_button = Button(monitor, text="Change password", command=change_password)
    change_password_button.pack(pady=10)

    # Create a quit button
    quit_button = Button(monitor, text="Quit", command=monitor.destroy, font=("Helvetica", 12))
    quit_button.place(relx=1, rely=1, x=-10, y=-10, anchor=SE)

    client.publish("lock/status",sensor_status.get())
    monitor.mainloop()

# create threads for both gui
monitor_thread = threading.Thread(target=lock_gui)
lock_thread = threading.Thread(target=monitor_gui)

# start the threads
monitor_thread.start()
lock_thread.start()


