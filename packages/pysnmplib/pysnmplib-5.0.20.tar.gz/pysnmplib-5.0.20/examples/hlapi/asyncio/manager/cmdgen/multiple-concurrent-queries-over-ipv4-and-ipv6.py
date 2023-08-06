"""
Concurrent queries
++++++++++++++++++

Send multiple SNMP GET requests at once using the following options:

* with SNMPv2c, community 'public'
* over IPv4/UDP
* to multiple Agents at localhost
* for instance of SNMPv2-MIB::sysDescr.0 MIB object
* based on asyncio I/O framework

Functionally similar to:

| $ snmpget -v2c -c public localhost:161 SNMPv2-MIB::sysDescr.0
| $ snmpget -v2c -c public localhost:162 SNMPv2-MIB::sysDescr.0
| $ snmpget -v2c -c public localhost:163 SNMPv2-MIB::sysDescr.0

"""  #
import asyncio
from pysnmp.hlapi.asyncio import *


async def getone(snmpEngine, hostname):
    get_result = await getCmd(
        snmpEngine,
        CommunityData("public"),
        UdpTransportTarget(hostname),
        ContextData(),
        ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
    )

    errorIndication, errorStatus, errorIndex, varBinds = await get_result
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print(
            "{} at {}".format(
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
            )
        )
    else:
        for varBind in varBinds:
            print(" = ".join([x.prettyPrint() for x in varBind]))


snmpEngine = SnmpEngine()

asyncio.run(
    asyncio.wait(
        [
            getone(snmpEngine, ("localhost", 161)),
            getone(snmpEngine, ("localhost", 162)),
            getone(snmpEngine, ("localhost", 163)),
        ]
    )
)
