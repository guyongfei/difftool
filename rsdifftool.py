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
import time

current_dir = os.path.split(os.path.realpath(__file__))[0]
tmp_dir = os.path.join(current_dir, 'tmp')
tmp_src_dir = str(tmp_dir)+"/src"
tmp_dest_dir = str(tmp_dir)+"/dest"
status = 0 # 0:inial; 1:unzipping; 2:unzip over; 3:diffing; 4:done
is_src_dest_unzipped = False

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
	srcfilename = srcstrvar.get()
	destfilename = deststrvar.get()
	global status
	print status
	print isbusy()
	if isbusy():
		tkMessageBox.showinfo('信息', '程序正在运行，请耐心等待')
	elif not os.path.exists(srcfilename) or not os.path.exists(destfilename):
		tkMessageBox.showerror('错误', '文件不存在')
	else:
		if os.path.exists(tmp_dir):
			shutil.rmtree(tmp_dir)
		os.mkdir(tmp_dir)
		
		unzipsrccmd = r'unzip -o '+srcfilename+' -d '+tmp_src_dir
		unzipdestcmd = r'unzip -o '+destfilename+' -d '+tmp_dest_dir
		status = 1
		thread.start_new_thread( unzipfiles, (unzipsrccmd,unzipdestcmd,) )


def doit():
	cmdstr = cmdentry.get(0.0, END)
	global status
	print status
	if isbusy():
		tkMessageBox.showinfo('信息', '程序正在运行，请耐心等待')
	elif 'ota_from_target_files' not in cmdstr:
		tkMessageBox.showerror('error','cmd is incorrect!')
	else:
		status = 3
		thread.start_new_thread( diffing, (cmdstr,) )


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

def unzipfiles(cmdstrsrc, cmdstrdest):
	global status
	cmdentry.delete(0.0, END)
	cmdentry.insert(INSERT, "正在解压和解析文件，请耐心等待...")
	cmdentry.config()

	os.system(cmdstrsrc)
	os.system(cmdstrdest)
	time.sleep(10)

	# srcxmlfile = tmp_src_dir+'/redstone_fota_info.xml'
	# print parsexml(srcxmlfile)
	# destxmlfile = tmp_dest_dir+'/redstone_fota_info.xml'
	# print parsexml(destxmlfile)

	srcimagezipfile = tmp_src_dir+'/redstone_target_files.zip'
	destimagezipfile = tmp_dest_dir+'/redstone_target_files.zip'
	outfile = str(current_dir)+'/update.zip'

	cmdstr = tmp_src_dir+'/'+'build/tools/releasetools/ota_from_target_files '+'-v -i '+srcimagezipfile+' '+destimagezipfile+' '+outfile
	cmdentry.delete(0.0, END)
	cmdentry.insert(INSERT, cmdstr)
	cmdentry.config()
	status = 2

	tkMessageBox.showinfo('信息', '解压完成，请点击差分按钮')

def diffing(cmdstrdiff):
	global status
	cmdentry.delete(0.0, END)
	cmdentry.insert(INSERT, "正在生成差分包，请耐心等待...")
	cmdentry.config()

	os.chdir(tmp_src_dir)
	os.system(cmdstrdiff)

	cmdentry.delete(0.0, END)
	cmdentry.insert(INSERT, '差分包生成完成。')
	cmdentry.config()

	status = 4
	tkMessageBox.showinfo('信息', '差分包已完成。')


def isbusy():
	global status
	if status == 1 or status==3:
		return True
	else:
		return False


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