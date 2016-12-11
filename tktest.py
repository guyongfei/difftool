from Tkinter import *
import tkFileDialog

file_opt = {
	'defaultextension':'.zip',
	'filetypes':[('all files','.*'),('zip files', '.zip')],
	'initialdir':'/Users/gutianzi/code/python/guisample/',
	'title':'this is a title'
}

def sel():
	selection = "you selected the option " + str(radiovar.get())
	print selection

def chkbtn1_sel():
	print 'chkbtn1 changed '+ str(chkvar1.get())

def chkbtn2_sel():
	print 'chkbtn2 changed '+ str(chkvar2.get())

def doquit():
	exit()

def doit():
	print 'doit'
	cmdstrvar.set('adbcccc')
	cmdentry.config(textvariable = cmdstrvar)

def askopensrcfilename():
	filename = tkFileDialog.askopenfilename(**file_opt)
	srcstrvar.set(filename)
	srcentry.config(textvariable=srcstrvar)

def askopendestfilename():
	filename = tkFileDialog.askopenfilename(**file_opt)
	deststrvar.set(filename)
	destentry.config(textvariable=deststrvar)




top = Tk()
srcframe = Frame(top)
srcframe.pack()
destframe = Frame(top)
destframe.pack()
radioframe = Frame(top)
radioframe.pack()
checkframe = Frame(top)
checkframe.pack()
cmdframe = Frame(top)
cmdframe.pack()
btnframe = Frame(top)
btnframe.pack()

srclabel = Label(srcframe, text='src: ')
srclabel.pack(side=LEFT)
srcstrvar = StringVar()
srcentry = Entry(srcframe, bd=5, textvariable=srcstrvar)
srcentry.pack(side=LEFT)
srcbtn = Button(srcframe, text='select', command = askopensrcfilename)
srcbtn.pack(side=RIGHT)


destlabel = Label(destframe, text='dest:')
destlabel.pack(side=LEFT)
deststrvar = StringVar()
destentry = Entry(destframe, bd=5, textvariable=deststrvar)
destentry.pack(side=LEFT)
destbtn = Button(destframe, text='select', command = askopendestfilename)
destbtn.pack(side=RIGHT)

radiovar = IntVar()
rqualcom = Radiobutton(radioframe, text="Qualcom", variable=radiovar, value=1, command=sel)
rqualcom.pack(side=LEFT)
rmtkcom = Radiobutton(radioframe, text="Mtk", variable=radiovar, value=2, command=sel)
rmtkcom.pack(side=LEFT)
rothercom = Radiobutton(radioframe, text="Other", variable=radiovar, value=3, command=sel)
rothercom.pack(side=RIGHT)

chkvar1 = IntVar()
chkvar2 = IntVar()
chkbtn1 = Checkbutton(checkframe, text='checkbox1', variable=chkvar1, onvalue=1, \
	offvalue=0, command=chkbtn1_sel)
chkbtn1.pack()
chkbtn2 = Checkbutton(checkframe, text='checkbox2', variable=chkvar2, onvalue=1, \
	offvalue=0, command=chkbtn2_sel)
chkbtn2.pack()

cmdlabel = Label(cmdframe, text='cmd:')
cmdlabel.pack(side=LEFT)
cmdstrvar = StringVar()
cmdentry = Entry(cmdframe, bd=5, textvariable= cmdstrvar)
cmdentry.pack(side=RIGHT)


btn1 = Button(btnframe, text='cancel', command=doquit)
btn1.pack(side=LEFT)
btn2 = Button(btnframe, text='ok', command=doit)
btn2.pack(side=RIGHT)

top.mainloop()