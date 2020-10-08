from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep
import base64
import random
from playsound import playsound
import os
import sys
#import chromedriver_autoinstaller

import threading


from datetime import datetime

import tkinter as tk
from tkinter import font
from getpass import getpass

class Google:

	

	def __init__(self,username,password,meet_link):

		# SET PREFERENCES AND STARTUP ARGUMENTS
		chrome_options = Options()
		chrome_options.add_experimental_option("prefs", { "profile.default_content_setting_values.notifications": 1})
		chrome_options.add_argument("--use-fake-device-for-media-stream") 
		chrome_options.add_argument("--use-fake-ui-for-media-stream") 
		chrome_options.add_argument("--mute-audio")
		desired_cap = chrome_options.to_capabilities()
		desired_cap.update({
			'browser_version': '84.0',
			'os': 'Windows',
			'os_version': '10'
		})
		
		dirname = os.path.dirname(os.path.abspath(__file__))
		soundpath = os.path.join(dirname, 'juntos.mp3')

		# CREATE DRIVER FOR BROWSER
		self.driver=webdriver.Chrome('chromedriver.exe', desired_capabilities = desired_cap)

		# MOVE BROWSER OFF SCREEN
		self.driver.set_window_position(-1500,-1500)

		# NAVIGATE TO GOOGLE LOGIN AND INPUT USERNAME/PASSWORD
		self.driver.get("https://developers.google.com/oauthplayground")
		sleep(3)
		self.driver.find_element_by_xpath('//*[@id="api-AI-Platform-Training-&-Prediction-API-v1"]').click()
		self.driver.find_element_by_xpath('//*[@id="scopesContainer"]/li[2]').click()
		self.driver.find_element_by_xpath('//*[@id="authorizeApisButton"]').click()
		sleep(1)
		self.driver.find_element_by_xpath('//input[@type="email"]').send_keys(username)
		print('로그인 중...')
		self.driver.find_element_by_xpath('//*[@id="identifierNext"]').click()
		# print('click')
		sleep(6)
		# print('now')
		self.driver.find_element_by_xpath('//input[@type="password"]').send_keys(password)
		self.driver.find_element_by_xpath('//*[@id="passwordNext"]').click()
		print('로그인 완료.')

		# NAVIGATE TO GOOGLE MEET CALL, MUTE AUDIO AND VIDEO, AND JOIN
		# self.driver.get('https://meet.google.com/' + code)
		self.driver.get(meet_link)
		print('인증 정보 수집 중...')
		sleep(1)
		self.driver.get(meet_link)
		sleep(3)
		self.driver.get(meet_link)
		sleep(3)
		self.driver.get(meet_link)
		print('인증 정보 수집 완료')
		self.driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[5]/div[3]/div/div/div[2]/div/div/div[1]/div/div[4]/div[1]/div/div/div').click()
		self.driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[5]/div[3]/div/div/div[2]/div/div/div[1]/div/div[4]/div[2]/div/div').click()
		sleep(1)
		self.driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[5]/div[3]/div/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[1]').click()
		print('출석 준비 완료!')
		# WAIT FOR PERMISSION TO JOIN AND OPEN THE CHAT WINDOW
		while True:
			try:
				self.driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[5]/div[3]/div[6]/div[3]/div/div[2]/div[3]/span/span/div/div').click()
				break
			except NoSuchElementException:
				continue

		# READ LATEST CHAT MESSAGE, OUTPUT TO CONSOLE, AND HIGHLIGHT QUESTIONS
		

		def read_chat(block_len, msg_len):
			try:
				info = ["", "", "", False, block_len, msg_len, False, ""]
				# print("hello")
				chat = self.driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[5]/div[3]/div[3]/div/div[2]/div[2]/div[2]/span[2]/div/div[1]')
				blocks = chat.find_elements_by_class_name("GDhqjd")
				if len(blocks) != 0:
					try:
						messages = blocks[-1].find_elements_by_class_name("oIy2qc")
						
					except StaleElementReferenceException:
						print("Stale Reference")
					# print("blocks: " + str(len(blocks)))
					if len(blocks) != block_len or len(messages) != msg_len:
						block_len = len(blocks)
						msg_len = len(messages)

						name = blocks[-1].find_element_by_class_name("YTbUzc")
						time = blocks[-1].find_element_by_class_name("MuzmKe")
						send_id = blocks[-1].get_attribute("data-sender-id")

						if name.text != "나":

							info[0] = messages[-1].text
							info[1] = name.text
							info[2] = time.text
							info[4] = block_len
							info[5] = msg_len
							info[7] = send_id

						
							if "!출석" in messages[-1].text:
								print(name.text+" 출석 로그 확인")
								info[3] = True
								info[6] = True
								return info
							if "!종료" in messages[-1].text:
								sys.exit()
								return info
							else:
								info[3] = False
								info[6] = False
								return info
						else:
							return info
					else:
						return info
				else:
					return info

						
			except NoSuchElementException:
				print("NoSuchElement")

		root = tk.Tk()
		root.title("출석 로그")

		block_len = 0
		msg_len = 0
		users = []
		msg_num = 1
		def task(block_len,msg_len,users,COLORS, msg_num):
			# info = [0: message, 1: name, 2: time, 3: presence bool (Is it a presence?), 4: # of blocks, 
			# 5: # of messages in last block, 6: message bool (Is there a message?), 7: data_sender_id (unique id for each user)]
			f = open(datetime.now().strftime("%Y-%m-%d %H시")+"출석 명단.txt", 'a')
			rtn_info = read_chat(block_len, msg_len)
			user_recorded = 0
			if rtn_info[6]:
				block_len = rtn_info[4]
				msg_len = rtn_info[5]
				if len(users) != 0:
					for i in range(len(users)):
						if (rtn_info[7] == users[i][0]) == False:
							if user_recorded != 1:
								user_recorded = 0
						else:
							user_recorded = 1
							user_index = i
				else:
					rand_color = random.choice(COLORS)
					users.append([rtn_info[7], rand_color])
					user_recorded = 1
					user_index = 0
				if user_recorded == 0:
					rand_color = random.choice(COLORS)
					user_index = len(users)
					users.append([rtn_info[7], rand_color])
				text.insert(tk.END, ("{" + datetime.now().strftime("%H:%M:%S") + "} " + rtn_info[1] + ": " + rtn_info[0] + "\n"))
				f.write(("[출석][" + datetime.now().strftime("%H:%M:%S") + "]" + rtn_info[1]+"\n"));
				f.close();
				text.see("end")
				text.tag_add(str(msg_num), str(msg_num) + ".11", str(msg_num)+"."+str(len(rtn_info[1])+12))
				text.tag_config(str(msg_num), foreground=users[user_index][1])
				if rtn_info[3]:
					#playsound(soundpath, False)
					text.tag_add(str(msg_num)+".1", str(msg_num)+"."+str(len(rtn_info[1])+13), str(msg_num)+"."+str(len(rtn_info[1])+13+len(rtn_info[0])))
					text.tag_config(str(msg_num)+".1", background="blue", foreground="white")
				msg_num = msg_num + 1
			root.after(250, task, block_len, msg_len, users, COLORS, msg_num)

		canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
		canvas.pack()
		frame = tk.Frame(root, bd=5)
		frame.place(relwidth=1, relheight=1)
		scrollbar = tk.Scrollbar(frame)
		scrollbar.place(relwidth=0.025,relheight=1,relx=0.975,rely=0)

		text = tk.Text(frame, font=("Malgun Gothic", 12),spacing1=0.25, wrap=tk.WORD,yscrollcommand=scrollbar.set)
		text.place(relwidth=0.975, relheight=1,rely=0,relx=0)
		scrollbar.config( command = text.yview )
		root.after(2000, task, block_len, msg_len, users, COLORS, msg_num)
		root.mainloop()
		

HEIGHT = 500
WIDTH = 500

COLORS = ["#0000FF", "#006400", "#6B8E23", "#008B8B", "#B8860B", "#C71585", "#4682B4", "#2E8B57", "#8B4513", "#9400D3", "#8B0000", "#BDB76B", "#663399", "#663399", "#808000", "#008080", "#800000", "#2F4F4F", "#708090"]

if len(sys.argv) != 4:
	username = input("회의에 참여할 구글 아이디: ")
	password = getpass("비밀번호(보안입력): ")
	meet_link = input("구글Meet 회의 참여 링크를 입력 해 주세요: ")
else:
	username = sys.argv[1]
	password = sys.argv[2]
	meet_link = sys.argv[3]

mylike = Google(username,password,meet_link)