from aip import AipSpeech
from ffmpy3 import FFmpeg
from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
import random
import os
import time
import json
import traceback

class Translate():
	def __init__(self):
	
		self.APP_ID = '百度语音api APP_ID'
		self.API_KEY = '百度语音api API_KEY'
		self.SECRET_KEY = '百度语音api SECRET_KEY'
		
		self.root = tkinter.Tk()
		self.root.title("语音识别")
		self.root.minsize = (600, 400)
		self.frame = tkinter.Frame(self.root)
		self.frame.pack()
		
		self.start_button = tkinter.Button(self.frame, command=self.chose, text="选择文件").grid(row=1, column=0,pady=5)
		self.speech_text = tkinter.Text()
		self.speech_text.pack()
		tkinter.mainloop()

	def chose(self):
		selectFileName = tkinter.filedialog.askopenfilename(title='选择文件')
		speech_type = ['.wav' ,'.pcm']
		video_type = ['.mp4', '.rmvb', '.avi']
		type = os.path.splitext(selectFileName)[1]
		
		if(type in speech_type):
			self.to_screen("正在识别...")
			self.speech_to_text(selectFileName)
		elif(type in video_type):
			speech_path = self.video_to_speech(selectFileName)
			self.to_screen("转换成功，正在识别...")
			self.speech_to_text(speech_path)
		else:
			self.to_screen("错误的文件格式")
		
		
	def video_to_speech(self, filepath):
		try:
			self.to_screen("正在转换文件...")
			file_location = "%s/video_output" % os.path.dirname(os.path.realpath(__file__))
			if not os.path.exists(file_location):os.makedirs(file_location)
			outputfile = "%s/%s.wav" % (file_location, ''.join(random.sample('zyxwvutsrqponmlkjihgfedcbaABCDEFGHIJKLMNOPQRSTUVWXYZ',10)))
			ff = FFmpeg(
				inputs={filepath: None},
				outputs={outputfile: '-vn -ar 8000 -ac 2 -ab 8000 -f wav'}
				)
			ff.cmd
			ff.run()
		except:
			tkinter.messagebox.showerror('错误',traceback.format_exc())
		return outputfile

	def get_file_content(self, filePath):
		with open(filePath, 'rb') as fp:
			return fp.read()

	def speech_to_text(self, filePath):
		client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)
		res = client.asr(self.get_file_content(filePath), 'wav', 16000, {
			'dev_pid': 1537,
		})
		if(res['err_no'] == 0):
			self.to_screen(res['result'][0])
		else:
			self.to_screen(res['err_msg'])
		
	def to_screen(self, text):
		self.speech_text.insert(INSERT, '%s\n' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		self.speech_text.insert(END, '%s\n' % text)

def main():
	text = Translate()
	pass


if __name__ == "__main__":
	main()