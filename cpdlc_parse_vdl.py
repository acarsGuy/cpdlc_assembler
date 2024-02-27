#!/usr/bin/python
# -*- coding: utf-8 -*-

def vdl_offset(d):
	if 'distance_specified' in d and d['distance_specified']['choice'] == 'distanceSpecifiedNm':
		val  = int(d['distance_specified']['data']['offset']['val'])
		unit = d['distance_specified']['data']['offset']['unit']
		return f"{val}{unit}"

	return "[_offset]"	

def vdl_direction(d):
	return d['direction'].upper()

def vdl_unitname(d):
	if 'facility_name' in d['unit_name']:
		return d['unit_name']['facility_name']

	if 'facility_designation' in d['unit_name']:
		return d['unit_name']['facility_designation']

	return '[_unitname]'

def vdl_frequency(d):
	if d['frequency']['choice'] == 'frequencyhf':
		val  = d['frequency']['data']['hf']['val']
		unit = d['frequency']['data']['hf']['unit']

		return f'{val}{unit}'

	if d['frequency']['choice'] == 'frequencyvhf':
		val  = d['frequency']['data']['vhf']['val']
		unit = d['frequency']['data']['vhf']['unit']

		return f'{val}{unit}'

	if d['frequency']['choice'] == 'frequencyuhf':
		val  = d['frequency']['data']['uhf']['val']
		unit = d['frequency']['data']['uhf']['unit']

		return f'{val}{unit}'

	return '[_frequency]'

def vdl_facility(d):
	if d['facility']['choice'] == 'facilityDesignation':
		return d['facility']['data']['facility_designation']

	return '[_facility]'

def vdl_speed(d):
	if d['speed']['choice'] == 'speedMach':
		mach = d['speed']['data']['mach']['val']
		return f"MACH {mach}"

	if d['speed']['choice'] == 'speedIndicated':
		val  = int(d['speed']['data']['indicated_airspeed']['val'])
		unit = d['speed']['data']['indicated_airspeed']['unit']
		return f"{val}{unit}"

	
	return '[_speed]'

def vdl_level(d):
	if d['level']['choice'] == 'singleLevel':
		return vdl_level2(d['level']['data'])

	if d['level']['choice'] == 'blockLevel':
		levels_conv = []
		for level in d['level']['data']['block_level']:
			levels_conv.append(vdl_level2(level))

		return " - ".join(levels_conv)


	return '[_level]'

def vdl_level2(d):
	if d['level_type']['choice'] == 'levelFlightLevel':
		fl = d['level_type']['data']['flight_level']
		return f'FL{fl}'

	if d['level_type']['choice'] == 'levelFeet':
		val  = int(d['level_type']['data']['flight_level']['val'])
		unit = d['level_type']['data']['flight_level']['unit']
		return f"{val}{unit}"

	return '[_level2]'

def vdl_position(d):
	if d['position']['choice'] == 'fixName':
		return d['position']['data']['fix_name']['fix']

	if d['position']['choice'] == 'navaid':
		return d['position']['data']['navaid']['navaid_name']

	return '[_position]'

def vdl_freetext(d):
	return d['free_text']

def vdl_error(d):
	ei = d['error_info']

	types = {
		"unrecognizedMsgReferenceNumber": "unrecognized Msg Reference Number",
		"logicalAcknowledgementNotAccepted": "logical Ack Not Accepted",
		"insufficientResources": "insufficient Resources",
		"invalidMessageElementCombination": "invalid Msg Element Combination",
		"invalidMessageElement": "invalid Msg Element"
	}

	if ei in types:
		ei = types[ei].upper()

	return f"ERROR: {ei}"

def vdl_assemble(msg,data):
	placeholder_count = msg.count('[') + msg.count('FREE TEXT') + msg.count('ERROR')
	if placeholder_count == 0:
		return msg
	if placeholder_count == 1:
		dataroot = data
	if placeholder_count > 1:
		firstkey = list(data.keys())[0]
		dataroot = data[firstkey]

	if '[offset]' in msg:
		rep = vdl_offset(dataroot)
		msg = msg.replace('[offset]',rep)

	if '[direction]' in msg:
		rep = vdl_direction(dataroot)
		msg = msg.replace('[direction]',rep)

	if '[frequency]' in msg:
		rep = vdl_frequency(dataroot)
		msg = msg.replace('[frequency]',rep)

	if '[unitname]' in msg:
		rep = vdl_unitname(dataroot)
		msg = msg.replace('[unitname]',rep)

	if '[facility]' in msg:
		rep = vdl_facility(dataroot)
		msg = msg.replace('[facility]',rep)

	if '[speed]' in msg:
		rep = vdl_speed(dataroot)
		msg = msg.replace('[speed]',rep)

	if '[level]' in msg:
		rep = vdl_level(dataroot)
		msg = msg.replace('[level]', rep)

	if '[position]' in msg:
		rep = vdl_position(dataroot)
		msg = msg.replace('[position]', rep)

	if msg == 'FREE TEXT':
		rep = vdl_freetext(dataroot)
		msg = msg.replace('FREE TEXT', rep)

	if msg == 'ERROR':
		rep = vdl_error(dataroot)
		msg = msg.replace('ERROR',rep)

	return msg.replace('\00', '')

def handle_pdus(pdu,ret):
	if pdu['choice'] == 'abortUser':
		reason = pdu['data']['cpdlc_user_abort_reason'].upper()
		
		ret['msgs'].append(f"USER ABORT: {reason}")
		ret['msg_id'] = None
		ret['logical_ack'] = None
		ret['timestamp'] = None

		return ret
	if pdu['choice'] == 'abortProvider':
		reason = pdu['data']['cpdlc_provider_abort_reason'].upper()
		
		ret['msgs'].append(f"PROVIDER ABORT: {reason}")
		ret['msg_id'] = None
		ret['logical_ack'] = None
		ret['timestamp'] = None

		return ret

	#startdown
	#startup
	#send
	#forward
	#forwardresponse


	return pdu['choice']

def parse(cpdlcroot):
	ret  = {}
	ret['msgs'] = []
	if 'atc_uplink_message' in cpdlcroot:
		pkey = 'atc_uplink_message'
		ret['dir'] = 'UPLINK'
	elif 'atc_downlink_message' in cpdlcroot:
		pkey = 'atc_downlink_message'
		ret['dir'] = 'DOWNLINK'
	elif 'protected_aircraft_pdus' in cpdlcroot:
		pkey = 'protected_aircraft_pdus'
		ret['dir'] = 'DOWNLINK PDUS'
		return handle_pdus(cpdlcroot[pkey],ret)
	elif 'protected_ground_pdus' in cpdlcroot:
		pkey = 'protected_ground_pdus'
		ret['dir'] = 'UPLINK PDUS'
		return handle_pdus(cpdlcroot[pkey],ret)
	else:
		return False


	if 'msg_id' in cpdlcroot[pkey]['header']:
		ret['msg_id'] = cpdlcroot[pkey]['header']['msg_id']
	else:
		ret['msg_id'] = None

	if 'logical_ack' in cpdlcroot[pkey]['header']:
		ret['logical_ack'] = cpdlcroot[pkey]['header']['logical_ack']
	else:
		ret['logical_ack'] = None

	if 'timestamp' in cpdlcroot[pkey]['header']:
		ts_h = cpdlcroot[pkey]['header']['timestamp']['time']['hour']
		ts_m = cpdlcroot[pkey]['header']['timestamp']['time']['min']
		ts_s = cpdlcroot[pkey]['header']['timestamp']['time']['sec']
		ts_d = cpdlcroot[pkey]['header']['timestamp']['date']['day']
		ts_o = cpdlcroot[pkey]['header']['timestamp']['date']['month']
		ts_y = cpdlcroot[pkey]['header']['timestamp']['date']['year']

		if ts_h < 10:
			h = "0"+str(ts_h)
		else:
			h = str(ts_h)
		if ts_m < 10:
			m = "0"+str(ts_m)
		else:
			m = str(ts_m)
		if ts_s < 10:
			s = "0"+str(ts_s)
		else:
			s = str(ts_s)
		if ts_d < 10:
			d = "0"+str(ts_d)
		else:
			d = str(ts_d)
		if ts_o < 10:
			o = "0"+str(ts_o)
		else:
			o = str(ts_o)
		ret['timestamp'] = f"{ts_y}-{o}-{d} {h}:{m}:{s}"
	else:
		ret['timestamp'] = None

	if 'msg_data' in cpdlcroot[pkey] and 'msg_elements' in cpdlcroot[pkey]['msg_data']:
		for el in cpdlcroot[pkey]['msg_data']['msg_elements']:
			ret['msgs'].append(vdl_assemble(el['msg_element']['choice_label'],el['msg_element']['data']))

	return ret
