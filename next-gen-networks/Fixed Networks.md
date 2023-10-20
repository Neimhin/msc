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
