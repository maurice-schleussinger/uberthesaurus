import json, csv
from Tkinter import *
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString
from descriptor import Descriptor
from main import MyApp
dsetdict = {}
class descriptorset(object):
	"""docstring for descriptorset"""
	def __init__(self, arg):
		super(descriptorset, self).__init__()
		self.arg = arg


def create_dset(setname,appname):
	"""This creates a new descriptorset which is added to the list dsetdict """
	if setname not in dsetdict.keys():
		dsetdict[setname] = Descriptorset(setname)
	else:
		print "Deskriptorset " + setname + " gibt es schon"
	appname.update_dlist(dsetdict)

def edit_dset(setname, newname):
	"""Edits the name of a descriptorset."""
	dsetdict[setname].set_name(newname)
	#TODO edit setname in dsetdict

def add(name, term, rel,appname):
	"""This forwards its variables to add_term and also checks whether a new term has been created successfully. If so, it will create a set for the new term."""
	if dsetdict[name].add_term(term, rel):
		create_dset(term,appname)

def export_dsets(format, filename):
	"""This exports all elements of the list dsetdict to JSON, CSV or XML"""
	# make a dict tempdict with str from objectdict dsetdict
	tempdict = {}
	for  elem in dsetdict:
		tempdict[elem] = dsetdict[elem].get_terms()
	# handle the export
	if format == "JSON":
		with open("%s.json"%filename,"w") as json_output:
			json.dump(tempdict,json_output)
	elif format == "CSV":
			with open('%s.csv'%filename, 'w') as csv_output:
				writer = csv.writer(csv_output, delimiter=";")
				writer.writerow(tempdict.keys())
				writer.writerow(tempdict.values())
	elif format == "XML":
		xmldsetdict = Element( "Deskriptorsets")
		for name, terms in tempdict.iteritems():
			xmldset = SubElement(xmldsetdict, name)
			for elem in terms:
				xmlelem = SubElement(xmldset, elem)
				xmlelem.text=""
				for elm in terms[elem]:
					xmlelem.text +=elm+", "
		## print xml
		xml = tostring(xmldsetdict)
		dom = parseString(xml)
		print dom.toprettyxml('    ')
	else:
		print "Fehler! Unbekanntes Format!"


def import_dsets(format, filename):
	"""This imports descriptorsets from JSON, CSV or XML and returns a dict"""
	if format == "JSON":
		with open("%s.json"%filename,"r") as json_input:
			data = json.load(json_input)
			#print "JSON: ", data
	elif format == "CSV":
		data = {}
		with open('%s.csv'%filename, 'r') as csv_input:
			reader = csv.reader(csv_input, delimiter=";")
			for row in reader:
				keys = row
				values= reader.next()
				for elem in range(len(keys)):
					data[keys[elem]]=values[elem]
	elif format == "XML":
		pass
	else:
		print "Fehler! Unbekanntes Format!"

if __name__ == '__main__':
	# GUI TESTS
	root = Tk()
	myapp = MyApp(root)
	myapp.update_dlist(dsetdict)

	# DSET TESTS
	create_dset("Auto", myapp)
	create_dset("Esel", myapp)
	create_dset("Fahrrad", myapp)
	dsetdict["Fahrrad"]. add_term("Klingel", "VB")
	dsetdict["Fahrrad"].add_term("Fahrzeuge", "UB")
	dsetdict["Fahrrad"].add_term("Mofa", "VB")
	#print dsetdict["Fahrrad"].add_term("Yes", "OB")
	add("Fahrrad", "Fortbewegungsmittel", "UB", myapp)
	add("Esel", "Fortbewegungsmittel", "OB", myapp)
	root.mainloop()



	# IMPORT/EXPORT
	# export_dsets("JSON", "lol")
	# export_dsets("CSV", "lol")
	# export_dsets("XML", "lol")
	# import_dsets("JSON", "lol")
	# import_dsets("CSV", "lol")
	# import_dsets("XML", "lol")