from tkinter import *
import random
from sentences import *
import keyboard

time = 0
counter = 1

# Colors
title_color_white = "#ffffff"
accuracy_label_color_purple = "#e64df7"
all_frame_bg_color_grayish = "#1d1f1e"
sentence_text_color_neon_blue = "#00d5ff"
timer_color_yellow = "#f7f24d"
typing_text_color_green = "#22ff00"
wrong_typing_color_neon_red = "#ff0000"

# /////////////////////// Error Checking Method \\\\\\\\\\\\\\\\\\\
def checking_error():
    if type_text.get(1.0, "end-1c") not in sent_dict[index_of_sentence]:
        type_text['fg'] = wrong_typing_color_neon_red
    else:
        type_text['fg'] = typing_text_color_green
    
    if type_text['state']==NORMAL:
        Mainwindow.after(1, checking_error)

# /////////////////// Calculate Accuracy and Speed \\\\\\\\\\\\\\\\\
def calculate_acc_speed():
    type_text['state'] = DISABLED

    global accuracy
    global gross_speed
    global net_speed
    global minutes

    total_letters = 0
    accurate_letters = 0
    
    typed = type_text.get(1.0, "end-1c")
    text = sent_dict[index_of_sentence]

    # Count the accurate letters and total letters
    for i in range(len(text)):
        if text[i]==typed[i]:
            accurate_letters+=1
        total_letters+=1
    
    # Calculate time, accuracy, gross speed and net speed
    minutes = time/60
    accuracy = round((accurate_letters/total_letters)*100)
    gross_speed = round((total_letters/5)/minutes)
    net_speed = round((accurate_letters/5)/minutes)

# //////////////////// Show the Speed Test Result \\\\\\\\\\\\\\\\
def result():
    global line_graph_label
    calculate_acc_speed()

    label_acc = Label(time_Frame, text = "Accuracy", font=("arial",14), width = 10, bg = all_frame_bg_color_grayish, fg = accuracy_label_color_purple)
    label_acc.grid(row=1, column=0)

    label_acc = Label(time_Frame, text = str(accuracy) +" %",font=("arial",28, "bold"), bg = all_frame_bg_color_grayish, fg = accuracy_label_color_purple)
    label_acc.grid(row=2, column=0)

    Label(time_Frame, font = ("arial", 50), bg = all_frame_bg_color_grayish, fg = accuracy_label_color_purple).grid(row = 3, column = 0)

    label_net = Label(time_Frame, text = "Net Speed",font=("arial",14), bg = all_frame_bg_color_grayish, fg = accuracy_label_color_purple)
    label_net.grid(row=4, column=0)

    label_net = Label(time_Frame, text = net_speed,font=("arial",45,"bold"),height=1, width = 3, bg = accuracy_label_color_purple, fg = all_frame_bg_color_grayish, justify = RIGHT)
    label_net.grid(row=5, column=0, padx = 10)

    label_per = Label(time_Frame, text = "wpm",font=("arial",12), bg = accuracy_label_color_purple, fg = all_frame_bg_color_grayish, width = 4, justify = LEFT)
    label_per.grid(row=6, column=0)

    Label(time_Frame, font = ("arial", 50), bg = all_frame_bg_color_grayish, fg = accuracy_label_color_purple).grid(row = 7, column = 0)

    label_gross = Label(time_Frame, text = "Gross Speed\n"+str(gross_speed)+" wpm",font=("arial",12), bg = all_frame_bg_color_grayish, fg = accuracy_label_color_purple)
    label_gross.grid(row=8, column=0)

# ///////////////// Start the Timer when the typer start typing \\\\\\\\\\\
def time_starts():
    global time
    global speed_data
    global total_key_pressed
    global counter
    time = time + 0.05
    time = round(time, 2)

    # Update the timer
    if time==counter:
        counter+=1
        time_label["text"] = int(time)
    
    # Stops the typing and Call the result method
    if len(type_text.get(1.0, "end-1c"))>=len(sent_dict[index_of_sentence]):
        result()
    else:
        Mainwindow.after(47,time_starts)


# ////////////////// Time starts on Key Press \\\\\\\\\\\\\\\\\
def start_typing():
    if len(type_text.get(1.0, "end-1c"))!=0:
        time_starts()
    else:
        time_label.after(100,start_typing)

# Display the reseted window
def reload():
    Mainwindow.destroy()
    main()

# /////////////////////////// ShortCuts \\\\\\\\\\\\\\\\\\\\\\\\\\
def key_pressed(event):
    if keyboard.is_pressed("ctrl+r"):
        reload()

# <<<<<<<<<<<<<<<<<<<<<<<<<< Main Window >>>>>>>>>>>>>>>>>>>>>>>>
def main():
    global time
    global total_key_pressed
    global counter
    global Mainwindow
    global time_label
    global type_text
    global sentence
    global text_frame
    global time_Frame
    global sentence_Frame
    global type_Frame
    global index_of_sentence
    
    time = 0
    total_key_pressed = 0
    counter = 1
    
    Mainwindow = Tk()
    width = Mainwindow.winfo_screenwidth()
    height = Mainwindow.winfo_screenheight()
    Mainwindow.state("zoomed")


    Mainwindow.bind('<Key>', key_pressed)

    # Fetching the sentence from the sentences module
    index_of_sentence = random.randint(0,len(sent_dict)-1)
    sentence = sentences[index_of_sentence]

    # _____________________ Title Frame ____________________
    title_frame = Frame(Mainwindow, width = width, height = height*0.1, bg = all_frame_bg_color_grayish)
    title_frame.pack()
    title_frame.pack_propagate(0)
    
    # Label - Speed Typing Test

    title_label = Label(title_frame, text="Speed Typing Test", bg = all_frame_bg_color_grayish, fg = title_color_white, font=("arial", 30, "bold"))
    title_label.pack(ipadx=10, ipady=10, side=LEFT)

    # _____________________ Text Frame ______________________
    text_frame = Frame(Mainwindow, width = width, height = height*0.89, bg = '#ffffff')
    text_frame.pack()
    text_frame.pack_propagate(0)


    # ------------ Time Frame ------------
    time_Frame = Frame(text_frame, bg = all_frame_bg_color_grayish, bd = 0, relief=SOLID, width=width*0.1, height = height*0.845)
    time_Frame.grid(row = 0, column = 0, rowspan=3, padx = 1, pady = 1)
    time_Frame.grid_propagate(0)

    # Label - Timer
    time_label = Label(time_Frame, font=("arial", 36, "bold"), fg = timer_color_yellow, bg = all_frame_bg_color_grayish)
    time_label.grid(columnspan=2, padx = 50, pady = 50)
    time_label["text"] = time


    # ---------- Sentences Frame ---------
    sentence_Frame = Frame(text_frame, bg = all_frame_bg_color_grayish, bd = 0, relief=SOLID, width=width*0.9, height = height*0.42)
    sentence_Frame.grid(row = 0, column = 1, pady = 1)
    sentence_Frame.pack_propagate(0)

    # Label - Sentence to type
    text_Label = Label(sentence_Frame, text = sentence, font=("consolas", 24), justify=LEFT, bg = all_frame_bg_color_grayish, fg = sentence_text_color_neon_blue)
    text_Label.pack(padx=60,pady=30, anchor="nw")

    
    # ----------- Typing Frame ------------
    type_Frame = Frame(text_frame, bg = all_frame_bg_color_grayish, bd = 0, relief=SOLID, width=width*0.9, height = height*0.42)
    type_Frame.grid(row = 2, column = 1)
    type_Frame.pack_propagate(0)

    # TextBox - Typing here
    type_text = Text(type_Frame, width=60, height=7, font=("consolas",24), bg = all_frame_bg_color_grayish, fg = typing_text_color_green)
    type_text.pack(pady=20, side=LEFT, padx=60)
    type_text['state'] = NORMAL


    # ________________________ Info Frame _____________________________
    info_frame = Frame(Mainwindow, width = width, height = height*0.1, bg = 'lightgray')
    info_frame.pack()
    info_frame.pack_propagate(0)

    title_label = Label(info_frame, text="Made By: Ashish Kumar Patel", bg = "lightgray", fg = "black", font=("arial", 10))
    title_label.pack()

    type_text.focus()

    start_typing()
    checking_error()
    Mainwindow.mainloop()

main()
