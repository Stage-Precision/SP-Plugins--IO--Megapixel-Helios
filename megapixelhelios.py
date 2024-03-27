import sys
import os
import sp
import requests
import json

class MegapixelModule(sp.BaseModule):

	pluginInfo = {
		"name" : "Megapixel",
		"description" : "Communicate with Megapixel LED Processor",
		"author" : "SP",
		"version" : (1, 0),
		"spVersion" : (1, 2, 0),
		"helpPath" : os.path.join(os.path.dirname(os.path.abspath(__file__)),"help.md")
	}

	def __init__(self):
		sp.BaseModule.__init__(self)
		
	def afterInit(self):
		self.hostip = self.moduleContainer.addIPParameter("Ip", False)
		self.pluginData = self.moduleContainer.addDataParameter("Device")
		
		self.addAction("Read System", "", self.getProcessorInfoAC)
		self.addAction("Read Processor Info", "", self.getProcessorFullInfoAC)
		self.addAction("Read Alert", "", self.getProcessorAlertAC)
		self.addAction("Read Preset List", "", self.getPresetListAC)

		actionProcessorName = self.addAction("Set Processor Name", "", self.setProcessorNameAC)
		actionProcessorName.addStringParameter("Name", "")

		actionProcessorBlackout = self.addAction("Blackout", "", self.setProcessorBlackoutAC)
		actionProcessorBlackout.addBoolParameter("Blackout", True)
		
		actionProcessorFreeze = self.addAction("Freeze", "", self.setProcessorFreezeAC)
		actionProcessorFreeze.addBoolParameter("Freeze", True)
		
		actionProcessorBrightness = self.addAction("Set Brightness and Gamma", "", self.setProcessorBrightnesAC)
		actionProcessorBrightness.addIntParameter("Brightness", 100,0,100)
		actionProcessorBrightness.addFloatParameter("Gamma", 3.1,1,4)


	def post_request_with_json(self, url, json_data):
		try:
			headers = {'Content-Type': 'application/json'}
			response = requests.post(url, headers=headers, data=json.dumps(json_data))
			response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
			return response.json()
		except requests.exceptions.RequestException as e:
			print(f"Error during POST request: {e}")
			return None
	
	def get_request_to_json(self, url):
			try:
				response = requests.get(url)
				response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
				return response.json()
			except requests.exceptions.RequestException as e:
				print(f"Error during GET request: {e}")
				return None
			
	def getProcessorInfoAC(self):
		url = "http://" + self.hostip.value + "/api/v1/public?sys.info="
		json_result = self.get_request_to_json(url)
		if json_result:
			self.pluginData.setTreeValueWithJson("", str(json.dumps(json_result)))
	
	def getPresetListAC(self):
		url = "http://" + self.hostip.value + "/api/v1/presets/list"
		json_result = self.get_request_to_json(url)
		if json_result:
			self.pluginData.setTreeValueWithJson("Presets", str(json.dumps(json_result)))
	
	def getProcessorFullInfoAC(self):
		url = "http://" + self.hostip.value + "/api/v1/public"
		json_result = self.get_request_to_json(url)
		if json_result:
			self.pluginData.setTreeValueWithJson("", str(json.dumps(json_result)))
	
	def getProcessorAlertAC(self):
		url = "http://" + self.hostip.value + "api/v1/public?dev.ingest.alerts="
		json_result = self.get_request_to_json(url)
		if json_result:
			self.pluginData.setTreeValueWithJson("", str(json.dumps(json_result)))

	def setProcessorNameAC(self, name):
		url = "http://" + self.hostip.value + "/api/v1/public?sys.description="
		data = {"sys": {"description": name}}
		json_result = self.post_request_with_json(url, data)

	def setProcessorBlackoutAC(self, state):
		url = "http://" + self.hostip.value + "/api/v1/public?dev.display.blackout="
		data = {"dev": {"display": { "blackout": state}}}
		json_result = self.post_request_with_json(url, data)

	def setProcessorFreezeAC(self, state):
		url = "http://" + self.hostip.value + "/api/v1/public?dev.display.freeze="
		data = {"dev": {"display": { "freeze": state}}}
		json_result = self.post_request_with_json(url, data)

	def setProcessorBrightnesAC(self, brightness, gamma):
		url = "http://" + self.hostip.value + "/api/v1/public?dev.display="
		data = {"dev":{ "display":{ "brightness":brightness, "gamma": gamma}}}
		json_result = self.post_request_with_json(url, data)

if __name__ == "__main__":
	sp.registerPlugin(MegapixelModule)