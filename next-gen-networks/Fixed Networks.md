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

### Dynamic Bandwidth Assignment
DBA is the process by which the OLT decides how to assign upstream transmission opportunities (e.g., bandwidth) to the ONUs.
### Ranging Operations
### Split ratio
point-to-point
ONU: home unit
OLT: network unit
examine a 1:32 system, one OLT to 32 ONUs, with max 10km fibre length we obtain an ideal loss of: 15dB for the splitter + 3dB for the fiber loss = 18dB
GPON standard includes split ratios of 1:16 and 1:64, and max ONU-OLT distance of 20km
newer standards allow for higher split ratios

PON is a power split architecture (passive splits), and at each split the power is divided and some noise is added
3dB loss -> half the power
with 32 splits: 32 = $2^5$ -> 3dB $\times$ 5 = 15dB loss due to splits
with 64 splits: 64 = $2^6$ -> 3dB $\times$ 6 = 18dB loss due to splits

XGS-PON designed to allow for tunable lasers in the ONU later but not necessitating it

DOCSIS Data Over Cable Service Interface Specification

Which operator is best positioned in Ireland?
- Eir because it's the incumbent and own all infrastructure? No, because they have to share their capacity.
- Virgin media because it owns cable TV infrastructure? Maybe, because they own the most coaxial networks and there's not much fibre in Dublin, but fibre is being brought to the home in Dublin now.

- Broadband is a commodity in our information age.
- Digital divide is a big social issue for all governments.
- This means that governments are under pressure to make sure their country will meet these expectations.
- In addition, a broadband infrastructure is essential for our information-based economy
	- hard to attract foreign investment if your overall infrastructure is poor
	- studies have shown that doubling broadband ...
#### Local Loop Unbundling
- local loop is the distance from the house to the network central office
#### Sub Loop Unbundling
deals with sharing of the copper from the cabinet to the user, but it's expensive
need equipment in each central office,
about 1000 central offices in Ireland

### Next Generation Access (NGA) Bitstream
#### PON Unbundling
- point-to-point fibre is easy as it allows for LLU
	- for this reason a number of countries
- US said forget about unbundling, whoever owns the network can use it how they want
- Japan told incumbent operator you have to share it but we'll make sure you get proportional benefit from it, Japan had highest penetration
- EU, no decision for a long time, no decision ultimately made, not much clarity, EU said one thing, individual country said another thing

- trend is to convert central offices into small data centres, switching processing, same jobs at different scales


### 27th November 2023, 14:00, LB04
- fronthaul capacity issue
- need higher capacity depending on where you put your split
- can't treat fixed network and mobile network as separate anymore
- OpenRAN means opening interfaces, latest thing happening in the field
	- standardise interfaces
	- O-RU is hardware
	- O-DU is software (but in principle closed source)
	- Can mix and match open source and closed source systems, because the interfaces are open standards
Why is OpenRAN interesting?
- near-real time RAN intelligent controllor (RIC)
- Machine Learning based handover prediction, when will the user move to the next cell?
- Handover is typically decided by the signal received at a particular moment, so the boundaries of a cell are fuzzy.
- Prediction Horizon is the time window for which we make a classification: handover, (HO) no-handover (NO HO). With a prediction horizon of 2.5s and a prediction of handover (HO), we are saying there will be a handover within the next 2.5s. If the prediction horizon is longer, e.g. 20s then our prediction is more ambiguous, we are not saying *when* in the 20s period the handover will occur, so it's easier to correctly guess when the prediction horizon is longer.
- ML-based early attack detection:
	- dataset collector
	- ml model training
	- online ml classifier
	- feature extractor
	- messaging broker
- BBU sends slot scheduling through OLT, ONU, remote site to user equipment.
- The OLT can intercept the slot scheduling to calculate and distribute Dynamic Bandwidth Allocation (DBA) Bandwidth Map (BWMap) early to the ONU. This is called cooperative DBA. Now called cooperative transport interface (CTA). This reduces the latency considerably compared to sending the BWMap lazily.
- Google developed OpenFlow to essentially design their own switches.
- Today even the optical layer is being opened up, allowing people to write their own software for optical networks.
**transfer learning of EDFA modeling for Digital Twin:**
- different WDM channels undergo different amplification and noise figure, causing:
	- different power levels
	- different noise levels
	- QoT degradation when adding and dropping signals dynamically
- would be great if we could use 'transfer learning' to apply a learned model for a particular amplifier to different amplifiers in different scenarios
- if we can do transfer learning we might only need a small number of samples to retrain, which means we can potentially do online learning in the network
- compare: booster amplifier (beginning of link), preamp (end of link), have different purposes and properties
#### exercises

A Wavelength Division Multiplexing (WDM) transmission system with 40 channels needs to operate over a 1000 km distance. Amplifiers have 15 dBm of power and noise figure of 6 dB, while the fibre has a nominal attenuation of 0.2 dB/km. The distance between amplifiers is 50 km. The signals all transmit at 33 Gbaud (occupying a 37GHz bandwidth). Also consider that a margin of at least 4 dB is required.

(a) What is the maximum useful data rate of your system, considering all channels, if the reqired OSNR for 16QAM, 32 QAM and 64 QAM are respectively 18, 23, 28. Notice that these rates can only be achieved using error correction codes, which have an overhead of 9% (i.e. they use 9% of the channel capacity).


Data rate (b/s) is the baud rate (sym/s) times the number of bits per symbol (b/sym).
Baud rate is 33 Gbaud = $33\times 10^6$.
16 QAM = 4 bits, 18 dB
32 QAM = 5 bits, 23 dB
64 QAM = 6 bits, 28 dB

Next step: calculate the OSNR for the amplified system, and choose the maximum modulation you can use at that OSNR, then calculate the data rate of the system with that modulation.


This is as far as we got on the exercise, he asked us to attempt to finish it for tomorrow.

$\text{OSNR}=P_{\text{TOT}} - NF - G - 10\log_{10}{N_{Ch}} -10\log_{10}{N_{amps}} + 58 - M$
$G=0.2\text{dB/km}*50\text{km}=10\text{dB}$
$M=4dB$
$P_{\text{TOT}}=15$
$N_{Ch}=40$
$N_{amps}=1000km/50km=20$

$\text{OSNR} = 15 - 6 - 10 -13 -10 - 58 - 4 = 24dB$
We should choose the 32 QAM modulation, giving us 5 bits per symbol.
Therefore the channel rate is:
$R_{Ch}=33\cdot5Gbaud$
But after error correction we get:
$R_{Ch}=33\cdot 5\cdot 0.91=150.15$
And with 40 channels we get about $6Tbit/s$.

Chromatic dispersion is a time value.

$\delta T_{[ps]}=D_{[\frac{ps}{nm.km}]}\cdot L_{[km]}\cdot \delta \lambda_{[nm]}$
With a 37GHz channel we can get $\delta \lambda$ by $\frac{0.8\cdot 37}{100}=0.296$.
$D=17_{[\frac{ps}{nm\cdot km}]}$.
$D_{DCF}=-150_{[\frac{ps}{nm\cdot km}]}$.
$\delta T=17\cdot50\cdot0.296=251.6$
$L_{DCF}=\frac{\delta T}{D_{DCF}\cdot \delta \lambda}\approx 5km$. Amount of DCF per span.

$L_{DCF}=\frac{\delta T}{D_{DCF}\cdot \delta\lambda}=\frac{251.6}{-150\cdot0.296}=-5.666km$


![[q5.png]]

#### QoS tools
A QoS tool is some sort of functionality that makes decisions about packets.
- **Policer:** discards packets when they go above a pre-established threshold
- **Shaper:** delay packets so that the bandwidth threshold is not exceeded at any given time
- **Classifier:** inspects incoming packet and assigns to it a class of service (COS)
- **Metering and coloring:** check the rate at which packets are coming in against pre-defined thresholds and subsequently marks packets with different "colors"
- **Queue Differentiation:** Use multiple FIFO mode queues, different COS packets can be assigned to different queues.
- **Scheduler:** decides in which order to get packets from different queues
- **Rewrite:** can modify a packet COS marking






