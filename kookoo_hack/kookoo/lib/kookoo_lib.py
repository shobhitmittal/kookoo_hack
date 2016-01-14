from lxml import etree

def first_response(message,is_text,format_lan=None,lang="EN"):
	root = etree.Element('Response')
	#root.append(etree.Element('playtext'))
	# another child with text
	if is_text is True:
		child = etree.Element('playtext')
		child.text = str(message)
		root.append(child)
	else:
		child = etree.Element('say-as',format=format_lan,lang="EN")
		child.text = str(message)
		root.append(child)
	data_to_return=etree.tostring(root, xml_declaration=True,encoding='utf-8')
	#print(etree.tostring(root, xml_declaration=True))
	return data_to_return

#<?xml version="1.0" encoding="UTF-8"?>
# <response>     
# <say-as  format="501" lang="EN">123ABC</say-as>     
# </response>
#
