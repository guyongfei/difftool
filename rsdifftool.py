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
import thread

current_dir = os.path.split(os.path.realpath(__file__))[0]
tmp_dir = os.path.join(current_dir, 'tmp')
tmp_src_dir = str(tmp_dir)+"/src"
tmp_dest_dir = str(tmp_dir)+"/dest"

file_opt = {
	'defaultextension':'.zip',
	'filetypes':[('all files','.*'),('zip files', '.zip')],
	'initialdir':'/home/fay/code/difftool/zipfiles',
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
	cmdstr = makecmdstr()
	cmdentry.delete(0.0, END)
	cmdentry.insert(INSERT, cmdstr)
	cmdentry.config()


def doit():
	cmdstr = cmdentry.get(0.0, END)
	print cmdstr
	if 'ota_from_target_files' not in cmdstr:
		tkMessageBox.showerror('error','cmd is incorrect!')
	else:
		os.chdir(tmp_src_dir)
		os.system(cmdstr)

def makecmdstr():
	srcfilename = srcstrvar.get()
	destfilename = deststrvar.get()

	if not os.path.exists(srcfilename) or not os.path.exists(destfilename):
		tkMessageBox.showerror('错误', '文件不存在')
		return ''
	else:
		if os.path.exists(tmp_dir):
			shutil.rmtree(tmp_dir)
		os.mkdir(tmp_dir)
		
		unzipsrccmd = r'unzip -o '+srcfilename+' -d '+tmp_src_dir
		unzipdestcmd = r'unzip -o '+destfilename+' -d '+tmp_dest_dir
		# try:
		thread.start_new_thread( runcmd, (unzipsrccmd,) )
		thread.start_new_thread( runcmd, (unzipdestcmd,) )
		# except:
		# 	print "Error: unable to start thread"

		print 'xxxxxxxxx'
		return 'xxx'
   
		# os.system(unzipsrccmd)
		# os.system(unzipdestcmd)

		# srcxmlfile = tmp_src_dir+'/redstone_fota_info.xml'
		# print parsexml(srcxmlfile)
		# destxmlfile = tmp_dest_dir+'/redstone_fota_info.xml'
		# print parsexml(destxmlfile)

		# srcimagezipfile = tmp_src_dir+'/redstone_target_files.zip'
		# destimagezipfile = tmp_dest_dir+'/redstone_target_files.zip'
		# outfile = str(current_dir)+'/update.zip'

	return tmp_src_dir+'/'+'build/tools/releasetools/ota_from_target_files '+'-v -i '+srcimagezipfile+' '+destimagezipfile+' '+outfile


def parsexml(xmlfile):
	DOMTree = xml.dom.minidom.parse(xmlfile)
	rootnode = DOMTree.documentElement
	items = rootnode.getElementsByTagName('Item')
	for item in items:
		if item.getAttribute('name') == 'ro.redstone.model':
			modelvalue = item.getAttribute('value')
		elif item.getAttribute('name') == 'ro.redstone.version':
			versionvalue = item.getAttribute('value')
	return (modelvalue, versionvalue)

def runcmd(cmdstr):
	os.system(cmdstr)

EPAD = 3

top = Tk()
srclabel = Label(top, text='src: ')
srcstrvar = StringVar()
srcentry = Entry(top, bd=5, textvariable=srcstrvar)
srcbtn = Button(top, text='select', command = askopensrcfilename)
top.rowconfigure(3,weight=1)
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
rmtk = Radiobutton(top, text="Mtk", variable=radiovar, value=2, command=sel)
rzx = Radiobutton(top, text="zhanxun", variable=radiovar, value=3, command=sel)
rother = Radiobutton(top, text="Other", variable=radiovar, value=4, command=sel)
rqualcom.grid(column=12,row=2, padx=EPAD)
rmtk.grid(column=13, row=2, padx=EPAD)
rzx.grid(column=14, row=2, padx=EPAD)
rother.grid(column=15, row=2, padx=EPAD)


# chkvar1 = IntVar()
# chkvar2 = IntVar()
# chkbtn1 = Checkbutton(top, text='checkbox1', variable=chkvar1, onvalue=1, \
# 	offvalue=0, command=chkbtn1_sel)
# chkbtn2 = Checkbutton(top, text='checkbox2', variable=chkvar2, onvalue=1, \
# 	offvalue=0, command=chkbtn2_sel)
# chkbtn1.grid(column=0, row = 3, padx=EPAD)
# chkbtn2.grid(column=1, row =3, padx=EPAD)


cmdstrvar = StringVar()
cmdentry = Text(top, bd=5)
cmdentry.grid(column=0, row=3, columnspan=17, sticky=E+W+S+N, padx=EPAD)


btncancel = Button(top, text='cancel', command=doquit)
btnmakecmd = Button(top, text='makeCmd', command=domakecmd)
btnok = Button(top, text='ok', command=doit)
btncancel.grid(column=14, row=4,  padx=EPAD)
btnmakecmd.grid(column=15, row=4, padx=EPAD)
btnok.grid(column=16, row=4, padx=EPAD)


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
# rmtk = Radiobutton(radioframe, text="Mtk", variable=radiovar, value=2, command=sel)
# rmtk.pack(side=LEFT)
# rother = Radiobutton(radioframe, text="Other", variable=radiovar, value=3, command=sel)
# rother.pack(side=RIGHT)

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
top.geometry('800x180+20+20')

top.mainloop()