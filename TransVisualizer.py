from tkinter import ttk
from tkinter import *
import matplotlib.pyplot as plt

root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
gears_value = StringVar()
max_rpm_value = StringVar()
tire_width = StringVar()
tire_ratio = StringVar()
tire_wheel_diameter = StringVar()
mainframe = ttk.Frame(root, padding="5 5 8 8")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

def gear_calculate(*args):
    try:
        frame = ttk.Frame(mainframe, padding="8 8 8 8")
        frame.grid(column=0, row=20, sticky=(N, W, E, S))
        frame['borderwidth'] = 2
        frame['relief'] = 'sunken'
        global gears
        global max_rpm
        gears = int(gears_value.get())
        max_rpm = int(max_rpm_value.get())
        ttk.Label(frame, text="\nExample transmission: Getrag 282\nGear 1: 3.50\nGear 2: 2.05\nGear 3: 1.38\nGear 4: 0.94\nGear 5: 0.72\nFinal drive: 3.61").grid(column=0, row=20, sticky=W)
        entries = []
        
        for i in range(gears+1):
            if i >= gears:
                ttk.Label(frame, text=f"Final drive ratio: ").grid(column=0, row=i, sticky=W)
            else:
                ttk.Label(frame, text=f"Gear {i+1} ratio: ").grid(column=0, row=i, sticky=W)
            (entry := ttk.Entry(frame)).grid(column=1, row=i, sticky=W)
            entries.append(entry)
        
        ttk.Button(frame, text="Submit", command=lambda: submit_variables(entries)).grid(column=1, row=i+1, sticky=(S, W))

         
    except ValueError:
        pass


def submit_variables(entries):
    gear_ratios = []

    for entry in entries:
        user_input = entry.get()
        gear_ratios.append(user_input)
    
    tire_diameter = calculate_tire_size()
    per_gear_speed_vs_rpm = calculate_speed(tire_diameter, gear_ratios)
    graph(per_gear_speed_vs_rpm)



def calculate_tire_size():
    tire_diameter = (round((((int(tire_width.get())*(int(tire_ratio.get()))/2540*2)+(int(tire_wheel_diameter.get())))), 2))
    
    print(tire_diameter)
    return tire_diameter

def calculate_speed(tire_diameter, gear_ratios):
    per_gear_speed_vs_rpm = {}
    for i in range(gears):
        rpm = 0
        speed_per_rpm = {}
        while rpm <= max_rpm:
            speed = 0
            ratio = float(gear_ratios[i])
            final = float(gear_ratios[-1])
            speed = round(((rpm*tire_diameter)/((ratio*final)*336)), 2)
            speed_per_rpm[rpm] = speed
            rpm += 100
        per_gear_speed_vs_rpm[f"Gear {i+1}"] = speed_per_rpm

    print(per_gear_speed_vs_rpm)
    return per_gear_speed_vs_rpm

def graph(per_gear_speed_vs_rpm):
    c = 0.0
    for i in range(gears):
        rpm_vs_speed = per_gear_speed_vs_rpm[f"Gear {i+1}"]
        list_values = list(rpm_vs_speed.values())
        list_keys = list(rpm_vs_speed.keys())
        c = list_values[-1]
    
        if i == gears-1:
            list_values_new = list_values[index:]
            list_keys_new = list_keys[index:]
            
        else:
            next_list_values = list((per_gear_speed_vs_rpm[f"Gear {i+2}"]).values())
            if i == 0:
                list_values_new = list_values
                list_keys_new = list_keys

            else:
                list_values_new = list_values[index:]
                list_keys_new = list_keys[index:]
        
            closest = closest_value(next_list_values, c)
            index = next_list_values.index(closest)
        plt.plot(list_values_new, list_keys_new)
    
    plt.show()

def closest_value(next_list_values, c):
  return next_list_values[min(range(len(next_list_values)), key=lambda i: abs(next_list_values[i]-c))]

def main():
    ttk.Label(mainframe, text='Welcome to the Transmission Gear Ratio visualizer. \nThis is used to see how wheel speed compares to engine rpm for each gear.').grid(column=0, row=0, sticky=(W, E))
    ttk.Label(mainframe, text='How many gears does your tansmission have?\nExample: 5').grid(column=0, row=1, sticky=(W, E))
    ttk.Entry(mainframe, textvariable=gears_value).grid(column=0, row=2, sticky=(W, E))
    ttk.Label(mainframe, text="What is your max RPM? \nExample: 6000").grid(column=0, row=3, sticky=W)
    ttk.Entry(mainframe, textvariable=max_rpm_value).grid(column=0, row=4, sticky=W)
    ttk.Label(mainframe, text="What is your tire size of the driven axle? \nExample: 215/60R15 is, box 1=215, box 2=60, box 3=15").grid(column=0, row=5, sticky=W)
    ttk.Entry(mainframe, textvariable=tire_width).grid(column=0, row=6, sticky=W)
    ttk.Entry(mainframe, textvariable=tire_ratio).grid(column=0, row=7, sticky=W)
    ttk.Entry(mainframe, textvariable=tire_wheel_diameter).grid(column=0, row=8, sticky=W)
    
    entries=[]
    ttk.Button(mainframe, text="Submit", command=lambda: gear_calculate(entries)).grid(column=0, row=9, sticky=(W, E)) 
        
    root.mainloop()

main()