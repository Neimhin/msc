> A PON (passive optical network) refers to a fiber-optic network utilizing a point-to-multipoint topology and fiber optical splitters to deliver data from a single transmission point to multiple user endpoints. In contrast to AON, multiple customers are connected to a single transceiver by means of a branching tree of fibers and passive splitter/combiner units, operating entirely in the optical domain and without power in a PON architecture. There are two major current PON standards: Gigabit Passive Optical Network (GPON) and Ethernet Passive Optical Network (EPON).
> -- https://community.fs.com/article/abc-of-pon-understanding-olt-onu-ont-and-odn.html
## Introduction
Connecting each access ISP to every other access ISP doesn't scale; $O(n^2)$. Solution: hierarchy of providers at different scales.

Content provider networks (e.g. Google, Microsoft, Azure) are at similar scales to Tier 1 ISPs, and so have great leverage.

**Rates:**

| Term       | Definition                                                                                       | Example                                        |
|------------|--------------------------------------------------------------------------------------------------|------------------------------------------------|
| Baud Rate  | The number of symbols transmitted per second.                                                    | A system transmitting 1000 symbols/s has a baud rate of 1000 Baud. |
| Frequency  | The number of cycles of a periodic wave occurring per second.                                    | An FM radio station broadcasting at 100.7 MHz operates at a frequency of 100.7 million cycles per second.  |
| Bit Rate   | The number of bits transmitted per second.                                                       | A system transmitting data at 1 Mbps has a bit rate of 1 million bits per second. |
| Data Rate  | Often used interchangeably with bit rate, but can refer to the effective amount of data transmitted per second, considering factors like error correction. | In a system with error correction, a 1 Mbps transmission might have an effective data rate less than 1 Mbps due to overhead. |



## Optical Propagation
- total internal reflection
- path loss: ~0.2 dB/km\
- up to 150km without amplification

### Optical Transmitters and Receivers
- LASER: Light Amplification by Stimulated Emission of Radiation
	- generate **coherent light**

**Direct Detection:**

### ROADMs
OADM = Optical Add/Drop Multiplexer, a type of Wave Division Multiplexing
ROADM = Reconfigurable OADM

### Passive Optical Network (PON)
> 
- expensive to deploy fibre solutions to the access as the cost of each connection is not shared among users
- PtP fibre doesn't help much as:
	- it requires one individual fibre per user
	- at the network end it requires one termination port per user
- PONs were invented to reduce the cost for Capital (CAPEX) and Operational (OPEX) expenditures:
	- the idea is to share the optical fibre into a tree structure using PON
#### point-to-point fibre
Non-FTTP customers, big business customer, FTTP
very expensive, not implemented by many companies
and a lot of capacity in the fibre, not needed by a single customer

#### time-division multiplexing passive optical network TDM-PON
OLT: Optical Line Terminal
ONU: Optical Network Unit
how do we avoid collision when transmission from OLT is multicast to all the ONUs?
OLT schedules the transmissions telling ONUs when to start and stop transmission, so everything is highly synchronised.
Frequency of schedule updates are implementation dependent.

## GPON vs EPON
Gigabit PON and Ethernet PON.
GPON more for telecomms people. EPON more for ethernet, less strict.

### duplex scheme
the most economically convenient duplex scheme is wavelength division duplex over single fibre, although two-fibre systems are allowed by the standard

XG-PON1 1 channel
NG-PON2 4 channels
