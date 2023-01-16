#!/usr/bin/python
# -*- coding: utf-8 -*-

# #Comment means not implemented
# #Comment? means implemeted but not tested

#OK
def la_time(d):
	h = d['time']['hour']
	m = d['time']['min']

	if h < 10:
		h = "0"+str(h)
	else:
		h = str(h)

	if m < 10:
		m = "0"+str(m)
	else:
		m = str(m)
		
	return f"{h}:{m}"

#OK
def la_freetext(d):
	return d['free_text']

#?
def la_altitude(d):
	if d['alt']['choice'] == 'altitudeFlightLevel':
		fl = d['alt']['data']['flight_level']
		return f'F{fl}'

	if d['alt']['choice'] == 'altitudeQNH':
		val  = d['alt']['data']['alt_qnh']['val']
		unit = d['alt']['data']['alt_qnh']['unit']

		return f'{val}{unit} (QNH)'

	if d['alt']['choice'] == 'altitudeQNHMeters':
		val  = d['alt']['data']['alt_qnh_meters']['val']
		unit = d['alt']['data']['alt_qnh_meters']['unit']

		return f'{val}{unit} (QNH)'

	if d['alt']['choice'] == 'altitudeQFE':
		val  = d['alt']['data']['alt_qfe']['val']
		unit = d['alt']['data']['alt_qfe']['unit']

		return f'{val}{unit} (QFE)'

	if d['alt']['choice'] == 'altitudeQFEMeters':
		val  = d['alt']['data']['alt_qfe_meters']['val']
		unit = d['alt']['data']['alt_qfe_meters']['unit']

		return f'{val}{unit} (QFE)'

	if d['alt']['choice'] == 'altitudeGNSSFeet':
		val  = d['alt']['data']['alt_gnss']['val']
		unit = d['alt']['data']['alt_gnss']['unit']

		return f'{val}{unit} (GNSS)'

	if d['alt']['choice'] == 'altitudeGNSSMeters':
		val  = d['alt']['data']['alt_gnss_meters']['val']
		unit = d['alt']['data']['alt_gnss_meters']['unit']

		return f'{val}{unit} (GNSS)'


	return '[_altitude]'
	#altitudeQNHMeters?
	#altitudeQFE?
	#altitudeQFEMeters?
	#altitudeGNSSFeet?
	#altitudeGNSSMeters?
	#altitudeFlightLevelMetric

#?
def la_frequency(d):
	if d['freq']['choice'] == 'frequencyhf':
		val  = d['freq']['data']['hf']['val']
		unit = d['freq']['data']['hf']['unit']

		return f'{val}{unit}'

	if d['freq']['choice'] == 'frequencyvhf':
		val  = d['freq']['data']['vhf']['val']
		unit = d['freq']['data']['vhf']['unit']

		return f'{val}{unit}'

	if d['freq']['choice'] == 'frequencyuhf':
		val  = d['freq']['data']['uhf']['val']
		unit = d['freq']['data']['uhf']['unit']

		return f'{val}{unit}'

	return '[_frequency]'
	#satchannel

#OK?
def la_distance(d):
	if d['dist']['choice'] == 'distanceNm':
		val  = d['dist']['data']['dist_nm']['val']
		unit = d['dist']['data']['dist_nm']['unit']

		return f'{val}{unit}'

	if d['dist']['choice'] == 'distanceKm':
		val  = d['dist']['data']['dist_km']['val']
		unit = d['dist']['data']['dist_km']['unit']

		return f'{val}{unit}'

	return '[_distance]'

	#distanceNm?
	#distanceKm?

#OK
def la_icaounitname(d):
	if d['icao_unit_name']['icao_facility_id']['choice'] == 'iCAOfacilitydesignation':
		name = d['icao_unit_name']['icao_facility_id']['data']['icao_facility_designation']
		fkt  = d['icao_unit_name']['icao_facility_function'].upper()

		return f"{name} {fkt}"

	if d['icao_unit_name']['icao_facility_id']['choice'] == 'iCAOfacilityname':
		name = d['icao_unit_name']['icao_facility_id']['data']['icao_facility_name']
		fkt  = d['icao_unit_name']['icao_facility_function'].upper()

		return f"{name} {fkt}"

	return "[icaounitname]"

#OK~
def la_position(d):
	if d['pos']['choice'] == 'fixName':
		return d['pos']['data']['fix']

	if d['pos']['choice'] == 'navaid':
		return d['pos']['data']['navaid']

	if d['pos']['choice'] == 'latitudeLongitude':
		ll = d['pos']['data']['lat_lon']
		ret = ""

		if 'deg' in ll['lat']:
			lat_deg = ll['lat']['deg']
			ret += f'{lat_deg}°'

		if 'min' in ll['lat']:
			lat_min = ll['lat']['min']
			ret += f"{lat_min}'"

		if 'sec' in ll['lat']:
			lat_sec = ll['lat']['sec']
			ret += f"{lat_sec}''"

		if 'dir' in ll['lat']:
			lat_dir = ll['lat']['dir']
			if lat_dir == 'north':
				lat_dir = 'N'
			if lat_dir == 'south':
				lat_dir = 'S'
			ret += lat_dir

		ret += " "
		if 'deg' in ll['lon']:
			lon_deg = ll['lon']['deg']
			ret += f'{lon_deg}°'

		if 'min' in ll['lon']:
			lon_min = ll['lon']['min']
			ret += f"{lon_min}'"

		if 'sec' in ll['lon']:
			lon_sec = ll['lon']['sec']
			ret += f"{lon_sec}''"

		if 'dir' in ll['lon']:
			lon_dir = ll['lon']['dir']
			if lon_dir == 'west':
				lon_dir = 'W'
			if lon_dir == 'east':
				lon_dir = 'E'
			ret += lon_dir

		return ret
	
	if d['pos']['choice'] == 'airport':
		return d['pos']['data']['airport']

	if d['pos']['choice'] == 'placeBearingDistance':
		bear = la_degrees(d['pos']['data']['place_bearing_dist'])
		dist = la_distance(d['pos']['data']['place_bearing_dist'])

		if 'fix' in d['pos']['data']['place_bearing_dist']:
			place = d['pos']['data']['place_bearing_dist']['fix']
		else:
			place = '[_place]'

		return f"{bear} RADIAL {dist} OF {place}"

	return "[_position]"

#OK?
def la_speed(d):
	if d['speed']['choice'] == 'speedMach':
		mach = d['speed']['data']['speed_mach']['val']
		return f"MACH {mach}"

	if d['speed']['choice'] == 'speedIndicated':
		val  = d['speed']['data']['speed_indicated']['val']
		unit = d['speed']['data']['speed_indicated']['unit']
		return f"{val}{unit} (IAS)"

	if d['speed']['choice'] == 'speedTrue':
		val  = d['speed']['data']['speed_true']['val']
		unit = d['speed']['data']['speed_true']['unit']
		return f"{val}{unit} (TAS)"

	if d['speed']['choice'] == 'speedGround':
		val  = d['speed']['data']['speed_gnd']['val']
		unit = d['speed']['data']['speed_gnd']['unit']
		return f"{val}{unit} (TAS)"

	if d['speed']['choice'] == 'speedIndicatedMetric':
		val  = d['speed']['data']['speed_indicated_metric']['val']
		unit = d['speed']['data']['speed_indicated_metric']['unit']
		return f"{val}{unit} (IAS)"

	if d['speed']['choice'] == 'speedTrueMetric':
		val  = d['speed']['data']['speed_true_metric']['val']
		unit = d['speed']['data']['speed_true_metric']['unit']
		return f"{val}{unit} (TAS)"

	if d['speed']['choice'] == 'speedGroundMetric':
		val  = d['speed']['data']['speed_gnd_metric']['val']
		unit = d['speed']['data']['speed_gnd_metric']['unit']
		return f"{val}{unit} (TAS)"

	if d['speed']['choice'] == 'speedMachLarge':
		mach = d['speed']['data']['speed_mach_large']['val']
		return f"MACH {mach}"

	return '[_speed]'
	#speedMachLarge?
	#speedGroundMetric?
	#speedGround?
	#speedTrueMetric?
	#speedIndicatedMetric?

#OK
def la_beaconcode(d):
	return d['beacon_code']

#OK
def la_tofrom(d):
	return d['to_from'].upper()

#OK?
def la_degrees(d):
	if d['deg']['choice'] == 'degreesMagnetic':
		val  = d['deg']['data']['deg_mag']['val']
		unit = d['deg']['data']['deg_mag']['unit']
		if unit == 'deg':
			unit = '°'

		return f"{val}{unit} (magnetic)"
	
	if d['deg']['choice'] == 'degreesTrue':
		val  = d['deg']['data']['deg_true']['val']
		unit = d['deg']['data']['deg_true']['unit']
		if unit == 'deg':
			unit = '°'

		return f"{val}{unit} (true)"

	return '[_degrees]'
	#deg_true?

#OK
def la_direction(d):
	return d['dir'].upper()

#OK?
def la_distanceoffset(d):
	if d['dist_offset']['choice'] == 'distanceOffsetNm':
		val  = d['dist_offset']['data']['dist_offset_nm']['val']
		unit = d['dist_offset']['data']['dist_offset_nm']['unit']

		return f"{val}{unit}"

	if d['dist_offset']['choice'] == 'distanceOffsetKm':
		val  = d['dist_offset']['data']['dist_offset_km']['val']
		unit = d['dist_offset']['data']['dist_offset_km']['unit']

		return f"{val}{unit}"

	return '[_distanceoffset]'
	#distanceOffsetKm?

#OK
def la_icaofacilitydesignation(d):
	return d['icao_facility_designation']

#OK
def la_tp4table(d):
	tab = d['tp4table']
	if tab == 'labelA':
		return 'LABEL A'
	if tab == 'labelB':
		return 'LABEL B'
	return tab

#OK
def la_errorinformation(d):
	ei = d['err_info']

	types = {
		"applicationError": 'Application Error',
		"duplicateMsgIdentificationNumber": 'Duplicate Msg Identification Number',
		"unrecognizedMsgReferenceNumber": 'Unrecognized Msg Reference Number',
		"endServiceWithPendingMsgs": 'End Service With Pending Msgs',
		"endServiceWithNoValidResponse": 'End Service With No Valid Response',
		"insufficientMsgStorageCapacity": 'Insufficient Msg Storage Capacity',
		"noAvailableMsgIdentificationNumber": 'No Available Msg Identification Number',
		"commandedTermination": 'Commanded Termination',
		"insufficientData": 'Insufficient Data',
		"unexpectedData": 'Unexpected Data',
		"invalidData": 'Invalid Data',
		"reservedErrorMsg1": 'reserved Error Msg 1',
		"reservedErrorMsg2": 'reserved Error Msg 2',
		"reservedErrorMsg3": 'reserved Error Msg 3',
		"reservedErrorMsg4": 'reserved Error Msg 4',
		"reservedErrorMsg5": 'reserved Error Msg 5',
		"reservedErrorMsg6": 'reserved Error Msg 6',
	}

	if ei in types:
		ei = types[ei].upper()

	return f"ERROR: {ei}"

#OK~
def la_routeclearance(d):
	ret = ""

	if 'airport_dst' in d['rte_clearance']:
		ap = d['rte_clearance']['airport_dst']
		ret += f"{ap} VIA "

	if 'rte_info_seq' in d['rte_clearance']:
		points = []
		for p in d['rte_clearance']['rte_info_seq']:
			points.append(la_rte_info(p['rte_info']))
	else:
		points = ""
	ret += ";".join(points)

	return ret

#?
def la_rte_info(d):
	if d['choice'] == 'publishedIdentifier':
		return d['data']['published_identifier']['fix']

	if d['choice'] == 'latitudeLongitude':
		ll = d['data']['lat_lon']
		ret = ""

		if 'deg' in ll['lat']:
			lat_deg = ll['lat']['deg']
			ret += f'{lat_deg}°'

		if 'min' in ll['lat']:
			lat_min = ll['lat']['min']
			ret += f"{lat_min}'"

		if 'sec' in ll['lat']:
			lat_sec = ll['lat']['sec']
			ret += f"{lat_sec}''"

		if 'dir' in ll['lat']:
			lat_dir = ll['lat']['dir']
			if lat_dir == 'north':
				lat_dir = 'N'
			if lat_dir == 'south':
				lat_dir = 'S'
			ret += lat_dir

		ret += " "
		if 'deg' in ll['lon']:
			lon_deg = ll['lon']['deg']
			ret += f'{lon_deg}°'

		if 'min' in ll['lon']:
			lon_min = ll['lon']['min']
			ret += f"{lon_min}'"

		if 'sec' in ll['lon']:
			lon_sec = ll['lon']['sec']
			ret += f"{lon_sec}''"

		if 'dir' in ll['lon']:
			lon_dir = ll['lon']['dir']
			if lon_dir == 'west':
				lon_dir = 'W'
			if lon_dir == 'east':
				lon_dir = 'E'
			ret += lon_dir
		return ret

	if d['choice'] == 'airwayIdentifier':
		awid = d['data']['airway_id']
		return f"AIRWAY {awid}"

	return '[_routeinfopoint]'
	#"placeBearingPlaceBearing"
	#"placeBearingDistance"
	#"trackDetail"


def la_assemble(msg,data):

	placeholder_count = msg.count('[')
	if placeholder_count == 0:
		return msg
	if placeholder_count == 1:
		dataroot = data
	if placeholder_count > 1:
		firstkey = list(data.keys())[0]
		dataroot = data[firstkey]

	if type(dataroot) == list:
		#Two equal placeholders
		if firstkey == 'pos_pos':
			for (i,di) in enumerate(dataroot):
				rep = la_position(di)
				msg = msg.replace('[position]',rep,1)
		if firstkey == 'alt_alt':
			for (i,di) in enumerate(dataroot):
				rep = la_altitude(di)
				msg = msg.replace('[altitude]',rep,1)
		if firstkey == 'speed_speed':
			for (i,di) in enumerate(dataroot):
				rep = la_speed(di)
				msg = msg.replace('[speed]',rep,1)


	#Assemble
	if '[time]' in msg:
		rep = la_time(dataroot)
		msg = msg.replace('[time]', rep)

	if '[freetext]' in msg:
		rep = la_freetext(dataroot)
		msg = msg.replace('[freetext]', rep)

	if '[altitude]' in msg:
		rep = la_altitude(dataroot)
		msg = msg.replace('[altitude]',rep)

	if '[frequency]' in msg:
		rep = la_frequency(dataroot)
		msg = msg.replace('[frequency]',rep)

	if '[icaounitname]' in msg:
		rep = la_icaounitname(dataroot)
		msg = msg.replace('[icaounitname]',rep)

	if '[position]' in msg:
		rep = la_position(dataroot)
		msg = msg.replace('[position]',rep)

	if '[speed]' in msg:
		rep = la_speed(dataroot)
		msg = msg.replace('[speed]',rep)

	if '[tofrom]' in msg:
		rep = la_tofrom(dataroot)
		msg = msg.replace('[tofrom]',rep)

	if '[beaconcode]' in msg:
		rep = la_beaconcode(dataroot)
		msg = msg.replace('[beaconcode]',rep)

	if '[degrees]' in msg:
		rep = la_degrees(dataroot)
		msg = msg.replace('[degrees]',rep)

	if '[direction]' in msg:
		rep = la_direction(dataroot)
		msg = msg.replace('[direction]',rep)

	if '[distanceoffset]' in msg:
		rep = la_distanceoffset(dataroot)
		msg = msg.replace('[distanceoffset]',rep)

	if '[icaofacilitydesignation]' in msg:
		rep = la_icaofacilitydesignation(dataroot)
		msg = msg.replace('[icaofacilitydesignation]',rep)

	if '[tp4table]' in msg:
		rep = la_tp4table(dataroot)
		msg = msg.replace('[tp4table]',rep)

	if '[errorinformation]' in msg:
		rep = la_errorinformation(dataroot)
		msg = msg.replace('[errorinformation]',rep)

	if '[routeclearance]' in msg:
		rep = la_routeclearance(dataroot)
		msg = msg.replace('[routeclearance]',rep)


	return msg.replace('\00', '')




def parse(cpdlcroot):
	if 'err' in cpdlcroot and cpdlcroot['err']:
		return False

	ret  = {}
	ret['msgs'] = []
	if 'atc_uplink_msg' in cpdlcroot:
		pkey = 'atc_uplink_msg'
		ret['dir'] = 'UPLINK'
	elif 'atc_downlink_msg' in cpdlcroot:
		pkey = 'atc_downlink_msg'
		ret['dir'] = 'DOWNLINK'
	else:
		return False


	if 'msg_id' in cpdlcroot[pkey]['header']:
		ret['msg_id'] = cpdlcroot[pkey]['header']['msg_id']
	else:
		ret['msg_id'] = None
	if 'timestamp' in cpdlcroot[pkey]['header']:
		ts_h = cpdlcroot[pkey]['header']['timestamp']['hour']
		ts_m = cpdlcroot[pkey]['header']['timestamp']['min']
		ts_s = cpdlcroot[pkey]['header']['timestamp']['sec']
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
		ret['timestamp'] = f"{h}:{m}:{s}"
	else:
		ret['timestamp'] = None

	if pkey+'_element_id' in cpdlcroot[pkey]:
		msg = cpdlcroot[pkey][pkey+'_element_id']['choice_label']
		dat = cpdlcroot[pkey][pkey+'_element_id']['data']
		ret['msgs'].append(la_assemble(msg,dat))

	if pkey+'_element_id_seq' in cpdlcroot[pkey]:
		for el in cpdlcroot[pkey][pkey+'_element_id_seq']:
			msg = el[pkey+'_element_id']['choice_label']
			dat = el[pkey+'_element_id']['data']
			ret['msgs'].append(la_assemble(msg,dat))
	

	return ret




"""
TODO
---------------------------------------

#predepartureclearance
#legtype
#procedurename
#altimeter
#verticalrate
#remainingfuel
#remainingsouls
#atiscode

#MSGS with three placeholdes two equal
"""