import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo,showerror
import os
from tkinter import HORIZONTAL
from tkinter import font as tkFont
from tkinter import filedialog
import time
import cv2
import threading
from urllib.parse import urlparse

from urllib.parse import urlparse
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('Image resize App')
        self.geometry('800x900')
        self.save_file= None
        self.read_file=None
        self.helv24 = tkFont.Font(family='Arial', size=24, weight='bold')
        self.helv12 = tkFont.Font(family='Arial', size=12, weight='bold')
        self.value_progress=0
        self.gray_check = IntVar()
        self.rgb_to_bgr = IntVar()
        self.heightValue=StringVar(self, value="0")
        self.withtValue=StringVar(self, value="0")
		

        # label
        self.label = ttk.Label(self, text='Image size change App!',  font=self.helv24)
        self.label.grid(row=1,column=1, pady=30, padx=50,columnspan = 2)
        self.progress=ttk.Progressbar(self,orient=HORIZONTAL,length=100,mode='determinate')
        self.progress.grid(row=9,column=1,ipady=10, ipadx=300,pady=50,padx=50,columnspan = 2)

        # button
        self.read_entry = tk.Entry(self,state=DISABLED)
        self.read_entry.grid(row=2,column=1,ipadx=70,ipady=15, pady=20)
        self.button_read = tk.Button(self, text='Choose  image directory',fg="white", bg="green", font=self.helv12)
        self.button_read['command'] = self.button_clicked

        self.button_read.grid(row=3,column=1,ipady=15,padx=90,ipadx=20)
        self.write_entry = tk.Entry(self,state=DISABLED)
        self.write_entry.grid(row=2,column=2,ipadx=70,ipady=15, pady=20)

      
        
        self.button_write = tk.Button(self, text='Choose  save directory',fg="white", bg="red",font=self.helv12)
        self.button_write['command'] = self.write_button
        #self.button_write['font']=self.helv24
        self.button_write.grid(row=3,column=2, ipady=15,ipadx=20)


        #Entry Width row=4
        self.label_width = ttk.Label(self, text='Enter Image width',  font=self.helv12)
        self.label_width .grid(row=4, column=1, pady=30, padx=20)
        self.entry_with = tk.Entry(self,textvariable = self.withtValue)
        self.entry_with.grid(row=4,column=2,ipadx=70,ipady=15, pady=20)

		#Entry Width row=5
        self.label_height = ttk.Label(self, text='Enter Image height',  font=self.helv12)
        self.label_height.grid(row=5, column=1, pady=30, padx=20)
        self.entry_height = tk.Entry(self,textvariable=self.heightValue)
        self.entry_height.grid(row=5,column=2,ipadx=70,ipady=15, pady=20)


        C1 = Checkbutton(self, text = "Convert Gray", variable = self.gray_check, onvalue = 1, offvalue = 0, height=5, width = 20)
        C1.grid(row=7,column=1)

        C2 = Checkbutton(self, text = "RGB_to_BGR", variable = self.rgb_to_bgr, onvalue = 1, offvalue = 0, height=5, width = 20)
        C2.grid(row=7,column=2)

        self.button_run = tk.Button(self, text='Run',font=self.helv12,fg="white", bg="blue")
        self.button_run['command'] = self.run_resizing
        self.button_run.grid(row=8,column=1,ipady=15, ipadx=200,pady=30,padx=50,columnspan = 2)

        self.heightValue.trace('w', self.limitHeight)
        self.withtValue.trace('w', self.limitWeight)
        self.gray_check.trace('w', self.checkBoxControl)
        self.rgb_to_bgr.trace('w', self.checkBoxControlGray)

    def checkBoxControlGray(self,*args):
    	if(self.gray_check.get()==1):
    		self.gray_check.set(0)

    def checkBoxControl(self,*args):
    	if(self.rgb_to_bgr.get()==1):
    		self.rgb_to_bgr.set(0)
    	# if(self.rgb_to_bgr.get()==1 and self.gray_check.get()==1):
    	# 	self.gray_check.set(0)
    		


    def limitHeight(self,*args):
    	try: 
    		int(self.entry_height.get())
    	except ValueError as value:

    		return showerror(title="Entry value  is invalid", message="Only Integer values are accepted")

    	if(int(self.entry_height.get())>1000):
    		showinfo(title="Max height value exceeded", message="Max Value for height 1000px")
    		self.entry_height.focus()

    def limitWeight(self,*args):
    	try: 
    		int(self.entry_with.get())
    	except ValueError as value:

    		return showerror(title="Entry value  is invalid", message="Only Integer values are accepted")

    	if(int(self.entry_with.get())>1000):
    	 showinfo(title="Save directory", message="Max Value for height 1000px")
    	 self.entry_with.focus()

    def change_image_size(self, url):
    	with open(url, 'rb') as f:
    		check_chars = f.read()[-2:]
    	if check_chars != b'\xff\xd9':
    		print('Not complete image')
    	else:
    		src = cv2.imread(url, cv2.IMREAD_UNCHANGED)
	    	# scale_percent = 50
	    	# width = int(src.shape[1] *2)
	    	# height = int(src.shape[0] *2)
	  
	    	dsize = (int(self.entry_with.get()), int(self.entry_height.get()))
	    	
	    	if self.gray_check.get()==1:
	    		("gray check true")
	    		src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
	    	if self.rgb_to_bgr.get()==1:
	    		src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
	    	output = cv2.resize(src, dsize)
	    	path_parse=urlparse(url)
	    	file_name=os.path.basename(path_parse.path)
	    	saving_path=os.path.join(self.save_file,file_name)
	    	


	    	cv2.imwrite(saving_path,output) 


    def write_button(self):
    	currdir = os.getcwd()
    	self.save_file=filedialog.askdirectory(parent=self, initialdir=currdir, title='Please select a directory to save the resized images')#
    	self.write_entry.config(state='normal')
    	self.write_entry.insert(0,self.save_file)
    	self.write_entry.config(state='disabled')
    	

    def button_clicked(self):
    	currdir = os.getcwd()
    	self.read_file = filedialog.askdirectory(parent=self, initialdir=currdir, title='Please select a directory to scan images')
    	print("temodir ::", self.read_file)
    	self.read_entry.config(state='normal')
    	self.read_entry.insert(0,self.read_file)
    	self.read_entry.config(state='disabled')
    	
    def run_resizing(self):
    	if self.save_file is None:
    		return showinfo(title="File Upload", message="Your file has been uploaded successfully!")

    	if(int(self.entry_height.get())>1000):
    		return showinfo(title="Save directory", message="Max Value for height 1000px")
    	else:
    		print(" self.save_file", self.save_file)
    	length_of_file=len(os.listdir(self.read_file))
    	for index,item in enumerate(os.listdir(self.read_file)):
    		thrd_1 = threading.Thread(target= self.change_image_size, args=('{}/{}'.format(self.read_file,item),))
    		thrd_1.daemon = True
    		
    		thrd_1.start()
    		self.change_image_size('{}/{}'.format(self.read_file,item))
    		time.sleep(0.4)
    		self.progress['value']=round(((index+1)/length_of_file),2)*100
    		self.update_idletasks()
    	showinfo(title="Save directory", message="Resizing completed succesfully")
    	
        


if __name__ == "__main__":
    app = App()
    app.mainloop()