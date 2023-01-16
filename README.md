# cpdlc_parser
A parser for CPDLC messages from dumpvdl2 / libacars. Assembles CPDLC messages decoded by dumpvdl2 or libacars.

See example files...


## Short "API-Doc"
- ´cpdlc_parse_la.py´: assembles CPDLC Msgs from libacars
- ´cpdlc_parse_vdl.py´: assembles CPDLC Msgs from dumpvdl2

Each contains a ´parse´ function, returning dict. Keys:
- ´msgs´: list of contained and assembled messages
- ´dir´: 'DOWNLINK/UPLINK/DOWNLINK PDUS/UPLINK PDUS',
- 'msg_id': message id,
-  'logical_ack': 'required/notRequired',   **VDL2 ONLY**
-  'timestamp': CPDLC timestamp


## Message support
Should work with most common types CPDLCs.
Only few dumpvdl2 CPDLC types supported!

Many msg types still not supported, if you receive such a msg please open Issue and post JSON dump of CPDLC data.
