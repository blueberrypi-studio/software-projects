import tkinter as tk


def draw_calender(root):
    """draws calender"""
    day_list = []
    row = 0
    column = 0
    for day in range(31):
        day = tk.Frame(root, bg='red', width=100, height=100, padx=5, pady=5)
        day.grid(row=row, column=column)
        
        column += 1
        if column >= 6:
            row += 1
            column = 0
        


    # # Create the frames
    # frame1 = tk.Frame(root, bg='red', width=100, height=100)
    # frame2 = tk.Frame(root, bg='green', width=100, height=100)
    # frame3 = tk.Frame(root, bg='blue', width=100, height=100)
    # frame4 = tk.Frame(root, bg='yellow', width=100, height=100)

    # # Use the grid layout manager to place the frames in a 2x2 grid
    # frame1.grid(row=0, column=0)
    # frame2.grid(row=0, column=1)
    # frame3.grid(row=1, column=0)
    # frame4.grid(row=1, column=1)

def setup():
    """Setup Tkinter"""
    # Create the main window
    root = tk.Tk()
    root.geometry("1920x1080")

    return root

def main():
    """main function of the program"""
    root = setup()
    draw_calender(root)

    # Start the event loop
    root.mainloop()


main()
