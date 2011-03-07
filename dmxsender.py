#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       dmxsender.py
#       
#       Copyright 2011 J.A.Nache <nache.nache@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

from scapy.all import *
import pygtk, gtk, thread
import threading
import os, sys, time
import artdmx #scapy no tiene soporte para artnet ni artdmx, así que
			  #he tenido que crear la capa. La referencia del protocolo
			  #está en: http://www.artisticlicence.com/WebSiteMaster/User%20Guides/art-net.pdf

WORKPATH=os.path.abspath(os.path.dirname(sys.argv[0])).replace(" ","\ ")
RAWWORKPATH=os.path.abspath(os.path.dirname(sys.argv[0]))

class DMXSendGUI:
	
	def __init__(self):
		self.ip_destino=None
		self.puerto_destino=None
		self.ip_origen=None
		self.puerto_origen=None
		self.universo=None
		self.subred=None
		#self.canales=None
		self.intervalo=None
		self.onoff=False
		self.status=False
		
		builder = gtk.Builder()
		builder.add_from_file(RAWWORKPATH + "/gui/gui.glade")
		builder.connect_signals({ "on_window_destroy" : self.stop })
		
		#la ventana principal
		self.win = builder.get_object("window1")
		self.win.show()
		self.win.set_title("ArtDMX Sender by J.A. NachE <nache.nache@gmail.com>")
		self.win.connect("destroy", self.stop, "WM destroy")

		#los widgets
		self.entry_destino=builder.get_object("entry_destino")
		self.entry_origen=builder.get_object("entry_origen")
		self.entry_universo=builder.get_object("entry_universo")
		self.entry_subred=builder.get_object("entry_subred")
		self.entry_intervalo=builder.get_object("entry_intervalo")
		#self.textview_canal=builder.get_object("textview_canal")
		self.button_onoff=builder.get_object("button_onoff")
		self.vbox_principal=builder.get_object("vbox_principal")
		self.box_control=builder.get_object("box_control")
		
		#vamos a liarla parda
		CVbox=gtk.HBox()
		self.scales={}
		for i in range(0,512):
			self.scales[i]=gtk.VScale()
			self.scales[i].set_digits(0)
			self.scales[i].set_range(0, 255)
			self.scales[i].set_inverted(True)
			self.scales[i].show()
			if i < 10:
				vboz=gtk.VBox()
				lab=gtk.Label("Canal "+str(i))
				lab.set_angle(-45)
				vboz.pack_start(lab, False)
				vboz.pack_start(self.scales[i], True)
				CVbox.pack_start(vboz, True, True, 0)
			
			
		self.box_control.add(CVbox)
		
		
		#los eventos (conexiones)
		self.button_onoff.connect("toggled", self.on, "onoff")

		gtk.gdk.threads_init()
		self.win.show_all()
	def set_scale_value(self, num, value):
		self.scales[num].set_value(value)
		
	def get_scale_value(self, num):
		return self.scales[num].get_value()

	def get_scale_value_hex(self, num):
		return chr(int(hex(self.scales[i].get_value()),16))

	def get_intervalo(self):
		return self.intervalo
		
	def start(self):
		self.status=True
		gtk.main()
		
	def stop(self, widget=None, data=None):
		self.status=False
		self.onoff=False
		gtk.main_quit()
	

	def on(self,widget=None, data=None):
		if widget.get_active() == True:
			try:
				self.ip_destino=self.entry_destino.get_text().split(":")[0]
				self.puerto_destino=self.entry_destino.get_text().split(":")[1]
			
				self.ip_origen=self.entry_origen.get_text().split(":")[0]
				self.puerto_origen=self.entry_origen.get_text().split(":")[1]
			
				self.universo=self.entry_universo.get_text()
				self.subred=self.entry_subred.get_text()
				self.intervalo=self.entry_intervalo.get_text()
			
				#buff=self.textview_canal.get_buffer()
				#inicio=buff.get_start_iter()
				#fin=buff.get_end_iter()
			
				#self.canales=buff.get_text(inicio,fin,False)
				#print self.canales
				self.vbox_principal.set_sensitive(False)
				self.onoff=True
			except:
				self.off()
		else:
			self.off()

	def off(self):
		self.button_onoff.set_active(False)
		self.vbox_principal.set_sensitive(True)
		self.onoff=False
		
		
class threadGui(threading.Thread):  
	def __init__(self):  
		threading.Thread.__init__(self)  
		self.gui=DMXSendGUI() 
	
	def run(self):  
		self.gui.start()

	def gui_quit(self):
		self.gui.stop()

	def get_gui(self):
		return self.gui
	
	def status_gui(self):
		return self.gui.status
		
	def onoff(self):
		return self.gui.onoff
		
	def get_dst(self):
		return self.gui.ip_destino
		
	def get_src(self):
		return self.gui.ip_origen
		
	def get_sport(self):
		return int(self.gui.puerto_origen)
		
	def get_dport(self):
		return int(self.gui.puerto_destino)
		
	def get_universo(self):
		return int(self.gui.universo)
		
	def get_subred(self):
		return int(self.gui.subred)
		
	def get_canales(self):
		return self.gui.canales
	
	def set_scale_value(self, num, value):
		return self.gui.scales[num].set_value(value)
		
	def get_scale_value(self, num):
		return self.gui.scales[num].get_value()

	def get_scale_value_hex(self, num):
		return chr(int(hex(self.gui.scales[i].get_value()),16))

	def get_intervalo(self):
		return float(self.gui.intervalo)
		

	def off(self):
		self.gui.off()


class dmsparser:
	gui=None
	def __init__(self,thegui):
		self.dmxarray=[]
		gui=thegui
		self.reset()
		
	def reset(self):
		self.dmxarray=[]
		for i in range(512):
			self.dmxarray.append(chr(int(hex(0),16)))
			
	def get_values(self):
		#self.reset()

		for i in range(512):
			#canal=canal_valor.split(":")[0]
			#valor=chr(int(hex(int(canal_valor.split(":")[1])), 16))
			valor=int(gui.get_scale_value(i))
			
			self.dmxarray[int(i)]=chr(int(hex(valor),16))
		return ''.join(self.dmxarray)
		
	
if __name__ == "__main__":
	gui=threadGui()
	gui.start()
	
	artnet=artdmx.ArtNet()
	artdmx=artdmx.ArtDMX()
	dms=dmsparser(gui)
	while True:
		if gui.status_gui() and gui.onoff():
			try:
				print "Start sending"
				ip=IP(dst=gui.get_dst(),src=gui.get_src())
				udp=UDP(sport=gui.get_sport(),dport=gui.get_dport())
				artdmx.setfieldval("universe", gui.get_universo())
				artdmx.setfieldval("subnet", gui.get_subred())
				while gui.onoff():
					try:
						payload=dms.get_values()
						paquete=ip/udp/artnet/artdmx/payload
						paquete.display()
						send(paquete)
						time.sleep(gui.get_intervalo())
					except:
						gui.off()
				print "Terminado envio"
			except:
				print "Algo ha fallado"
				gui.off()
				raise
		else:
			if gui.status_gui() == False and gui.onoff() == False:
				break
			time.sleep(1)
			print "-->", gui.status_gui()
			print "-->", gui.onoff()
