from tkinter import *
import game2048

colours = {
	'background': '#FAF8EF',
	'button_new_game_bg': '#8F7A66',
	'button_new_game_text': 'white'
}


root = Tk()
root.title("2048")

# Frames
top_frame = Frame(root, highlightbackground="black", highlightcolor="black",highlightthickness=1)
top_frame.grid(row=0, column=0)

title_frame = Frame(top_frame, height=100, width=30)
title_frame.grid(row=0, column=0)

score_frame = Frame(top_frame)
score_frame.grid(row=0, column=1)

board_frame = Frame(root)
board_frame.grid(row=1, column=0)

# Simple text
title = Label(top_frame, text='2048', bg=colours['background'])
title.grid(row=0, column=0)

score_label_text = Label(score_frame, text='Score')
score_label_text.grid(row=0, column=0)
score_label_value = Label(score_frame, text='0')
score_label_value.grid(row=1, column=0)
# Simple button
button_new_game = Button(top_frame, text="New game", 
	bg=colours['button_new_game_bg'],
	fg=colours['button_new_game_text'])
button_new_game.grid(row=1, column=1)

root.configure(background=colours['background'])



root.mainloop()