import time
import threading
import tkinter as tk
from tkinter import ttk, font

# Ref: https://github.com/rdbende/Sun-Valley-ttk-theme
# Install: pip install sv-ttk
import sv_ttk

from wifi_communicator import WiFiCommunicator, OutMessage


class GUI(tk.Tk):
	'''
	'''
	
	ON_BUTTON_STR = 'ON'
	OFF_BUTTON_STR = 'OFF'
	ON_COLOR = 'green'
	OFF_COLOR = 'red'
	
	def __init__(self, communicator: WiFiCommunicator, *, title: str = 'Test GUI',
							 min_size: 'tuple[int, int]' = (400,400)) -> None:
		'''
		'''
		super().__init__()
		
		# The wifi communicator object
		self._communicator = communicator
		
		# Initialize the application
		self.__set_style_and_configure_font(dark=True)
		self.__initialise_window(title, min_size)
		self.__create_widgets()
		
		# Bind the click on (X) button event to the __on_closing_cb
		self.protocol("WM_DELETE_WINDOW", self.__on_closing_cb)
		
		# Incoming messages handler
		self._end_signal = False
		self._msgs_thread_handle = threading.Thread(target=self.__messages_receiving_thread, daemon=True)
		self._msgs_thread_handle.start()
		
		# Keep alive the GUI and do whatever periodic update to the screen
		self.after(1, self.__update)
	
	def __set_style_and_configure_font(self, dark: bool = True):
		'''
		sets the app style and font size
		'''
		sv_ttk.set_theme("dark" if dark else 'light')
		font.nametofont('TkDefaultFont').configure(size=9)
		ttk.Style().configure('.', font=(None, 10))
	
	def __initialise_window(self, title, min_size):
		self.title(title)
		self.minsize(*min_size)
	
	def __create_widgets(self):
		'''
		Create all graphical elements
		'''
		self.__create_received_msg_label()
		self.__create_message_frequency_current_selector()
	
	def __create_message_frequency_current_selector(self):
		self.selected_channel = tk.IntVar()
		self.selected_frequency = tk.IntVar()
		self.selected_current = tk.IntVar()
		self._channels_select_0 = tk.Radiobutton(self, text = "channel 0", variable=self.selected_channel, value=0)
		self._channels_select_0.grid(row=0,column=0)
		self._channels_select_1 = tk.Radiobutton(self, text = "channel 1", variable=self.selected_channel, value=1)
		self._channels_select_1.grid(row=1,column=0)
		self._channels_select_2 = tk.Radiobutton(self, text = "channel 2", variable=self.selected_channel, value=2)
		self._channels_select_2.grid(row=2,column=0)
		self._channels_select_3 = tk.Radiobutton(self, text = "channel 3", variable=self.selected_channel, value=3)
		self._channels_select_3.grid(row=3,column=0)
		self._channels_select_4 = tk.Radiobutton(self, text = "channel 4", variable=self.selected_channel, value=4)
		self._channels_select_4.grid(row=4,column=0)
		self._channels_select_5 = tk.Radiobutton(self, text = "channel 5", variable=self.selected_channel, value=5)
		self._channels_select_5.grid(row=5,column=0)
		self._channels_select_6 = tk.Radiobutton(self, text = "channel 6", variable=self.selected_channel, value=6)
		self._channels_select_6.grid(row=6,column=0)
		self._channels_select_7 = tk.Radiobutton(self, text = "channel 7", variable=self.selected_channel, value=7)
		self._channels_select_7.grid(row=7,column=0)
		self._frequency_label = tk.Label(text=" select Frequency")
		self._frequency_label.grid(row=0,column=1,rowspan=2,columnspan=2)
		self._current_label = tk.Label(text=" select current mA")
		self._current_label.grid(row=0,column=3,rowspan=2,columnspan=2)
		self._frequncy_select = tk.Scale(self,variable=self.selected_frequency,from_=500,to=100,orient=tk.VERTICAL)
		self._frequncy_select.grid(row=2,column=1,columnspan=2,rowspan=7)
		self._current_select = tk.Scale(self,variable=self.selected_current,from_=10,to=0,orient=tk.VERTICAL)
		self._current_select.grid(row=2,column=3,columnspan=2,rowspan=7)
		self._send_message_button = tk.Button(text="set tactile pad")
		self._send_message_button.grid(column=5,row=3, rowspan=2, columnspan=3)
	
	

	
	

	def __create_received_msg_label(self):
		self._received_msg_label = tk.StringVar(value='No messages!')
		tk.Label(self, textvariable=self._received_msg_label).place(relx=0.01, rely=0.7, relwidth=0.98)
	
	# -------------------- #
	#  On events callbacks #
	# -------------------- #
	
	def on_close_cb(self, *args):
		quit(0)
	
	def _send_message_button_click_cb(self, *args):
		'''
		'''
		compose_message = f"A{self.selected_channel}B{self.selected_frequency}C{self.selected_current}"
		
	# ------------------------------- #
	#  Update the screen periodically #
	# ------------------------------- #
	
	def __messages_receiving_thread(self):
		'''
		'''
		while not self._end_signal:
			message = self._communicator.get_message()
			
			if message.require_acknowledgment:
				msg = OutMessage(data='A')
				self._communicator.send_message(msg)
			
			self._received_msg_label.set(message.data)
			
			time.sleep(0.001)
	
	def __update(self):
		'''
		This is called each 1ms to update the GUI elements and do periodic actions
		'''
		return