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
outfile = '' #the output file path


file_opt = {
	'defaultextension':'.zip',
	'filetypes':[('all files','.*'),('zip files', '.zip')],
	'initialdir':'/home/fay/code/difftool/zipfiles',
	'title':'this is a title'
}

def sel():
	selection = "you selected the option " + str(radiovar.get())
	print selection

def chkverbose_sel():
	print 'chkverbose changed '+ str(chkverbosevar.get())

def chkblock_sel():
	print 'chkblock changed '+ str(chkblockvar.get())

def askopensrcfilename():
	filename = tkFileDialog.askopenfilename(**file_opt)
	srcstrvar.set(filename)
	srcentry.config(textvariable=srcstrvar)

def askopendestfilename():
	filename = tkFileDialog.askopenfilename(**file_opt)
	deststrvar.set(filename)
	destentry.config(textvariable=deststrvar)

def doquit():
	global status
	if status ==1 or status ==3:
		if tkMessageBox.askyesno('注意', '后台脚本正在运行中，程序退出后，脚本仍会运行完成，是否退出？', default='no'):
			exit()
	else:
		exit()

def domakecmd():
	global status
	srcfilename = srcstrvar.get()
	destfilename = deststrvar.get()
	platvalue = radiovar.get()
	if isbusy():
		tkMessageBox.showinfo('信息', '程序正在运行，请耐心等待')
	elif not os.path.exists(srcfilename) or not os.path.exists(destfilename):
		tkMessageBox.showerror('错误', '原包或目标包不存在')
	elif platvalue == 0:
		tkMessageBox.showerror('错误', '请选择目标平台')
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
	if isbusy():
		tkMessageBox.showinfo('信息', '程序正在运行，请耐心等待')
	elif 'ota_from_target_files' not in cmdstr or status !=2:
		tkMessageBox.showerror('错误','指令不正确，请生成差分指令')
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
	global outfile
	cmdentry.delete(0.0, END)
	cmdentry.insert(INSERT, "正在解压和解析文件，请耐心等待...")
	cmdentry.config()

	if os.system(cmdstrsrc) != 0 or os.system(cmdstrdest) != 0:
		cmdentry.delete(0.0, END)
		cmdentry.insert(INSERT, '解压失败，请重试！')
		cmdentry.config()
		status = 0
		tkMessageBox.showerror('错误', '解压失败，请重试！')
	else :

		# srcxmlfile = tmp_src_dir+'/redstone_fota_info.xml'
		# print parsexml(srcxmlfile)
		# destxmlfile = tmp_dest_dir+'/redstone_fota_info.xml'
		# print parsexml(destxmlfile)

		cmdstr = generatecmdstr()
		cmdentry.delete(0.0, END)
		cmdentry.insert(INSERT, cmdstr)
		cmdentry.config()
		status = 2

		tkMessageBox.showinfo('信息', '解压完成，请点击开始差分按钮')

def generatecmdstr():
	cmdstr = tmp_src_dir+'/'+'build/tools/releasetools/ota_from_target_files'
	if chkverbosevar.get() == 1:
		cmdstr += ' -v'
	if chkblockvar.get() == 1:
		cmdstr += ' --block'
	platvalue = radiovar.get()
	if platvalue == 2:
		cmdstr += ' -s ' + tmp_src_dir + '/device/mediate/build/releasetools/mt_ota_from_target_files.py'

	srcimagezipfile = tmp_src_dir+'/redstone_target_files.zip'
	destimagezipfile = tmp_dest_dir+'/redstone_target_files.zip'
	outfile = str(current_dir)+'/update.zip'

	cmdstr += ' -i '+srcimagezipfile+' '+destimagezipfile+' '+outfile
	return cmdstr

def diffing(cmdstrdiff):
	global status
	global outfile
	cmdentry.delete(0.0, END)
	cmdentry.insert(INSERT, "正在生成差分包，请耐心等待...")
	cmdentry.config()

	os.chdir(tmp_src_dir)
	if os.system(cmdstrdiff) != 0:
		cmdentry.delete(0.0, END)
		cmdentry.insert(INSERT, '差分包生成失败。')
		cmdentry.config()

		status = 2
		tkMessageBox.showerror('错误', '差分包生成失败。')
	else:
		cmdentry.delete(0.0, END)
		cmdentry.insert(INSERT, '差分包生成完成: '+ outfile)
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
srclabel = Label(top, text='原包：')
srcstrvar = StringVar()
srcentry = Entry(top, bd=5, textvariable=srcstrvar)
srcbtn = Button(top, text='选择', command = askopensrcfilename)
top.rowconfigure(4,weight=1)
top.columnconfigure(1,weight=1)
srclabel.grid(column=0,row=0, padx=EPAD)
srcentry.grid(column=1,columnspan=15,row=0, sticky=E+W, padx=EPAD)
srcbtn.grid(column=16, row =0, padx=EPAD)

destlabel = Label(top, text='目标包：')
deststrvar = StringVar()
destentry = Entry(top, bd=5, textvariable=deststrvar)
destbtn = Button(top, text='选择', command = askopendestfilename)
destlabel.grid(column=0, row=1, padx=EPAD)
destentry.grid(column=1,columnspan=15,row=1, sticky=E+W, padx=EPAD)
destbtn.grid(column=16, row =1, padx=EPAD)

radiovar = IntVar()
rqualcom = Radiobutton(top, text="高通", variable=radiovar, value=1, command=sel)
rmtk = Radiobutton(top, text="联发科", variable=radiovar, value=2, command=sel)
rzx = Radiobutton(top, text="展讯", variable=radiovar, value=3, command=sel)
rother = Radiobutton(top, text="其他", variable=radiovar, value=4, command=sel)
rqualcom.grid(column=12,row=2, padx=EPAD)
rmtk.grid(column=13, row=2, padx=EPAD)
rzx.grid(column=14, row=2, padx=EPAD)
rother.grid(column=15, row=2, padx=EPAD)

chkverbosevar = IntVar()
chkblockvar = IntVar()
chkverbose = Checkbutton(top, text='输出详情', variable=chkverbosevar, onvalue=1, \
	offvalue=0, command=chkverbose_sel)
chkblock = Checkbutton(top, text='block模式', variable=chkblockvar, onvalue=1, \
	offvalue=0, command=chkblock_sel)
chkverbose.grid(column=14, row = 3, padx=EPAD)
chkblock.grid(column=15, row =3, padx=EPAD)

cmdstrvar = StringVar()
cmdentry = Text(top, bd=5)
cmdentry.grid(column=0, row=4, columnspan=17, sticky=E+W+S+N, padx=EPAD)

btncancel = Button(top, text='退出', command=doquit)
btnmakecmd = Button(top, text='生成差分指令', command=domakecmd)
btnok = Button(top, text='开始差分', command=doit)
btnmakecmd.grid(column=14, row=5, padx=EPAD)
btnok.grid(column=15, row=5, padx=EPAD)
btncancel.grid(column=16, row=5,  padx=EPAD)

top.geometry('800x250+20+20')

top.mainloop()