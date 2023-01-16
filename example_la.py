#!/usr/bin/python
# -*- coding: utf-8 -*-
import cpdlc_parse_la
import json


def test(json_str):
	d = json.loads(json_str)
	cpdlc = d['arinc622']['cpdlc']

	out = cpdlc_parse_la.parse(cpdlc)

	print(out)


test('{"arinc622": {"msg_type": "fans1a_cpdlc_msg", "crc_ok": true, "gs_addr": "RECOEYA", "air_addr": "..OEIIS", "cpdlc": {"err": false, "atc_uplink_msg": {"header": {"msg_id": 1, "timestamp": {"hour": 23, "min": 38, "sec": 31}}, "atc_uplink_msg_element_id": {"choice_label": "MAINTAIN [altitude]", "choice": "uM19Altitude", "data": {"alt": {"choice": "altitudeFlightLevel", "data": {"flight_level": 410}}}}, "atc_uplink_msg_element_id_seq": [{"atc_uplink_msg_element_id": {"choice_label": "MONITOR [icaounitname] [frequency]", "choice": "uM120ICAOunitnameFrequency", "data": {"icao_unit_name_freq": {"icao_unit_name": {"icao_facility_id": {"choice": "iCAOfacilitydesignation", "data": {"icao_facility_designation": "SBAO"}}, "icao_facility_function": "center"}, "freq": {"choice": "frequencyhf", "data": {"hf": {"val": 6649.0, "unit": "kHz"}}}}}}}, {"atc_uplink_msg_element_id": {"choice_label": "AT [position] MONITOR [icaounitname] [frequency]", "choice": "uM121PositionICAOunitnameFrequency", "data": {"pos_icao_unit_name_freq": {"pos": {"choice": "fixName", "data": {"fix": "DEKON"}}, "icao_unit_name": {"icao_facility_id": {"choice": "iCAOfacilitydesignation", "data": {"icao_facility_designation": "GOOO"}}, "icao_facility_function": "center"}, "freq": {"choice": "frequencyhf", "data": {"hf": {"val": 8861.0, "unit": "kHz"}}}}}}}, {"atc_uplink_msg_element_id": {"choice_label": "[freetext]", "choice": "uM169FreeText", "data": {"free_text": "SECONDARY 6535"}}}]}}}}')
