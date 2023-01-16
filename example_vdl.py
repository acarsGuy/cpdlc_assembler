#!/usr/bin/python
# -*- coding: utf-8 -*-
import cpdlc_parse_vdl
import json


def test(json_str):
	cpdlc = json.loads(json_str)
	out = cpdlc_parse_vdl.parse(cpdlc)

	print(out)



test('{"atc_downlink_message": {"header": {"msg_id": 7, "timestamp": {"date": {"year": 2023, "month": 1, "day": 11}, "time": {"hour": 9, "min": 11, "sec": 49}}, "logical_ack": "required"}, "msg_data": {"msg_elements": [{"msg_element": {"choice_label": "REQUEST DIRECT TO [position]", "choice": "dM22Position", "data": {"position": {"choice": "fixName", "data": {"fix_name": {"fix": "DEVRU"}}}}}}]}}}')