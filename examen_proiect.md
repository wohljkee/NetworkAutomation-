# Requirements:
 - (1p) Docstrings (sort) and type-hints wherever possible 
 - (1p) Pylint run with a score of 10. You can use modified rc file or inline disable 
 - (1p) At least 5 unittests with at least 1 Mocked object, preferable MagicMock
 - (1p) Ubuntu Server interface and route configuration with subprocess
 - (1p) Single testbed with all devices and correct topology and connections (telnet port update allowed)
 - (1p) IOU/CSR/IOSv/FTD initial configuration + interface configuration (interface not via telnet)
 - (1p) DHCP server configured on one device and one endpoint to receive IP from DHCP
 - (1p) IOU/CSR/IOSv/FTD Static route configuration (use different connectors/methods)
 - (1p) FTD access rule to allow ICMP protocol or network or security zone 
 - (1p) Ubuntu server can ping all endpoints - verification part of pyATS test

Extra points:
 - (2P) OSPF configured on 2 devices - functional 
 - (2p) Executing any device configuration in parallel 