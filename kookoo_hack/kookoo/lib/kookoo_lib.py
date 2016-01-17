from lxml import etree

def first_response(message,is_text,sid=None,collectdtmf=False,format_lan=None,lang="EN",character_limit='8',terminal_character='#',timeout_time='5000'):
	#root.append(etree.Element('playtext'))
	# another child with text
	if is_text is True and collectdtmf is False:
		root = etree.Element('Response')
		child = etree.Element('playtext')
		child.text = str(message)
		root.append(child)
	elif is_text is False and collectdtmf is False:
		root = etree.Element('Response')
		child = etree.Element('say-as',format=format_lan,lang="EN")
		child.text = str(message)
		root.append(child)
	elif is_text is True and collectdtmf is True:
		if sid is None:
			raise Exception('Value of sid paramter is Invalid.Value is Null.' +str(sid))
		root = etree.Element('Response',sid=sid)
		child_dtmf = etree.Element('collectdtmf',l=character_limit,t=terminal_character,o=timeout_time)
		child = etree.Element('playtext')
		child.text = str(message)
		child_dtmf.append(child)
		root.append(child_dtmf)
	data_to_return=etree.tostring(root, xml_declaration=True,encoding='utf-8')
	print data_to_return
	return data_to_return

def venue_explain(value,place):
	talk=str(value)+' '+str(place)+' '
	return talk

#<?xml version="1.0" encoding="UTF-8"?>
# <response>     
# <say-as  format="501" lang="EN">123ABC</say-as>     
# </response>
#

#<?xml version="1.0" encoding="UTF-8"?>     
# <response sid="12345">     
# <collectdtmf l="4" t="#" o="5000">     
# <playtext>Please enter your pin number
# </playtext>     
# </collectdtmf>     
# </response>  