#!/usr/bin/python
# -*- coding: utf-8 -*-
from Tkinter import *
import tkFileDialog
import tkMessageBox
import Zfile
import os
import sys
import shutil
from xml.dom.minidom import parse
import xml.dom.minidom

current_dir = os.path.split(os.path.realpath(__file__))[0]

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

def askopensrcfilename():
	filename = tkFileDialog.askopenfilename(**file_opt)
	srcstrvar.set(filename)
	srcentry.config(textvariable=srcstrvar)

def askopendestfilename():
	filename = tkFileDialog.askopenfilename(**file_opt)
	deststrvar.set(filename)
	destentry.config(textvariable=deststrvar)

def doquit():
	exit()

def domakecmd():
	cmdstr = makecmdstr('./makecmd')
	print cmdstr

def doit():
	srcfilename = srcstrvar.get()
	destfilename = deststrvar.get()

	if not os.path.exists(srcfilename) or not os.path.exists(destfilename):
		tkMessageBox.showerror('错误', '文件不存在')
	else:
		tmp_dir = os.path.join(current_dir, 'tmp')
		if os.path.exists(tmp_dir):
			shutil.rmtree(tmp_dir)
		os.mkdir(tmp_dir)
		tmp_src_dir = str(tmp_dir)+"/src"
		tmp_dest_dir = str(tmp_dir)+"/dest"
		Zfile.extract(srcfilename, tmp_src_dir)
		Zfile.extract(destfilename, tmp_dest_dir)
		srcxmlfile = tmp_src_dir+'/test.xml'
		parsexml(srcxmlfile)
		destxmlfile = tmp_dest_dir+'/test.xml'
		parsexml(destxmlfile)

		cmdstr = makecmdstr(tmp_src_dir+'/bin/diff.bat')
		print cmdstr
		print 'x' + str(os.system(cmdstr))

def makecmdstr(cmdstr0):
	cmdstr = cmdstr0
	if chkvar1.get() == 1:
		cmdstr += ' -chkvar1 '
	if chkvar2.get() == 1:
		cmdstr += ' -chkvar2 '
	if radiovar.get() == 1:
		cmdstr += ' -mode=qc '
	elif radiovar.get() == 2:
		cmdstr += ' -mode=mtk '
	else:
		cmdstr += ' -mode=other '

	srcfilename = srcstrvar.get()
	destfilename = deststrvar.get()

	cmdstr += str(srcfilename+' '+destfilename)
	return cmdstr


def parsexml(xmlfile):
	DOMTree = xml.dom.minidom.parse(xmlfile)
	rootnode = DOMTree.documentElement
	tonode = rootnode.getElementsByTagName('to')[0]
	tovalue = tonode.childNodes[0].data
	print tovalue

EPAD = 3

top = Tk()
srclabel = Label(top, text='src: ')
srcstrvar = StringVar()
srcentry = Entry(top, bd=5, textvariable=srcstrvar)
srcbtn = Button(top, text='select', command = askopensrcfilename)
top.rowconfigure(0,weight=1)
top.columnconfigure(1,weight=1)
srclabel.grid(column=0,row=0, padx=EPAD)
srcentry.grid(column=1,columnspan=15,row=0, sticky=E+W, padx=EPAD)
srcbtn.grid(column=16, row =0, padx=EPAD)

destlabel = Label(top, text='dest:')
deststrvar = StringVar()
destentry = Entry(top, bd=5, textvariable=deststrvar)
destbtn = Button(top, text='select', command = askopendestfilename)
destlabel.grid(column=0, row=1, padx=EPAD)
destentry.grid(column=1,columnspan=15,row=1, sticky=E+W, padx=EPAD)
destbtn.grid(column=16, row =1, padx=EPAD)

radiovar = IntVar()
rqualcom = Radiobutton(top, text="Qualcom", variable=radiovar, value=1, command=sel)
rmtkcom = Radiobutton(top, text="Mtk", variable=radiovar, value=2, command=sel)
rothercom = Radiobutton(top, text="Other", variable=radiovar, value=3, command=sel)

chkvar1 = IntVar()
chkvar2 = IntVar()
chkbtn1 = Checkbutton(top, text='checkbox1', variable=chkvar1, onvalue=1, \
	offvalue=0, command=chkbtn1_sel)
chkbtn2 = Checkbutton(top, text='checkbox2', variable=chkvar2, onvalue=1, \
	offvalue=0, command=chkbtn2_sel)

cmdlabel = Label(top, text='cmd:')
cmdstrvar = StringVar()
cmdentry = Entry(top, bd=5, textvariable= cmdstrvar)


btncancel = Button(top, text='cancel', command=doquit)
btnmakecmd = Button(top, text='makeCmd', command=domakecmd)
btnok = Button(top, text='ok', command=doit)



# srcframe = Frame(top)
# srcframe.pack()
# destframe = Frame(top)
# destframe.pack()
# radioframe = Frame(top)
# radioframe.pack()
# checkframe = Frame(top)
# checkframe.pack()
# cmdframe = Frame(top)
# cmdframe.pack()
# btnframe = Frame(top)
# btnframe.pack()

# srclabel = Label(srcframe, text='src: ')
# srclabel.pack(side=LEFT)
# srcstrvar = StringVar()
# srcentry = Entry(srcframe, bd=5, textvariable=srcstrvar)
# srcentry.pack(side=LEFT)
# srcbtn = Button(srcframe, text='select', command = askopensrcfilename)
# srcbtn.pack(side=RIGHT)


# destlabel = Label(destframe, text='dest:')
# destlabel.pack(side=LEFT)
# deststrvar = StringVar()
# destentry = Entry(destframe, bd=5, textvariable=deststrvar)
# destentry.pack(side=LEFT)
# destbtn = Button(destframe, text='select', command = askopendestfilename)
# destbtn.pack(side=RIGHT)

# radiovar = IntVar()
# rqualcom = Radiobutton(radioframe, text="Qualcom", variable=radiovar, value=1, command=sel)
# rqualcom.pack(side=LEFT)
# rmtkcom = Radiobutton(radioframe, text="Mtk", variable=radiovar, value=2, command=sel)
# rmtkcom.pack(side=LEFT)
# rothercom = Radiobutton(radioframe, text="Other", variable=radiovar, value=3, command=sel)
# rothercom.pack(side=RIGHT)

# chkvar1 = IntVar()
# chkvar2 = IntVar()
# chkbtn1 = Checkbutton(checkframe, text='checkbox1', variable=chkvar1, onvalue=1, \
# 	offvalue=0, command=chkbtn1_sel)
# chkbtn1.pack()
# chkbtn2 = Checkbutton(checkframe, text='checkbox2', variable=chkvar2, onvalue=1, \
# 	offvalue=0, command=chkbtn2_sel)
# chkbtn2.pack()

# cmdlabel = Label(cmdframe, text='cmd:')
# cmdlabel.pack(side=LEFT)
# cmdstrvar = StringVar()
# cmdentry = Entry(cmdframe, bd=5, textvariable= cmdstrvar)
# cmdentry.pack(side=RIGHT)


# btn1 = Button(btnframe, text='cancel', command=doquit)
# btn1.pack(side=LEFT)
# btn2 = Button(btnframe, text='ok', command=doit)
# btn2.pack(side=RIGHT)
top.geometry('500x80+20+20')

top.mainloop()