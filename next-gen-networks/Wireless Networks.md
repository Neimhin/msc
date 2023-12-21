# Summary
### Wireless Channel Impairments and Mitigation Techniques 
### Overview of Wireless Networks
### Mobile Architectures: LTE, LTE-A, LTE-A-PRO
### Wireless Local Area Networks
### Wirless LAN: HetNet and small cell deployments, mmWave
### Internet of Things
- (Industrial) Internet of Things
- Machine-to-Machine (M2M)
- Machine-Type Communications (MTC)
	- massive MTC
		- very large number of devices, usually sensors and actuators
		- low cost devices
		- long battery life
		- capillar networks may bridge connections to devices
		- short range access vi Wi-Fi, Bluetooth
		- gateway nodes
	- critical IoT/MTC
		- e.g. traffic safety/control
		- control of critical infrastructure
		- industrial processes
		- automotive, energy utilities, Industrie 4.0
		- requires very high reliability and availability
		- automation of energy distribution in a smart gride exemplifies critical MTC/IoT
	- 5G promises:
		- very high uptime (> 9.999%)
		- ultra low-latency (<5ms round trip)
#### Low Power Wide Area Networks (LPWAN)
- small messages with specific duty cycles
- low power end nodes and long battery life
- access in awkard locations, in building, rural up to 30km
- public networks that server multiple use-cases and users
##### aims:
- low bill of material (BOM) for long lasting devices to be deployed at scale
- minimum cost and power usage
- minimal handshaking which impacts achievable QoS levels
- MAC is difficult here because we're talking about thousands of devices with small messages, rather than the normal small number of devices with large messages (e.g. media streaming)
- immature application space
	- not much known about traffic profiles
## Notes
### Coherence (ChatGPT)
### Coherence Time
**Coherence Time in Mobile Telecommunications**: In mobile telecommunications, coherence time represents the time period during which the wireless channel conditions (e.g., channel gains, delays, phase shifts) remain relatively constant or predictable as a mobile device moves. It is influenced by factors such as the velocity of the mobile device, the carrier frequency, and the environment (e.g., urban or rural).
Relative motion of the transmitter and receiver can introduce Doppler shifts in the received signal. Doppler shifts cause frequency and phase changes.
The environment influences how much multi-path interference occurs, which can affect coherence time. If the environment is changing constantly (moving vehicle, trains, elevators, people) then the channel will change and coherence may be lost.

#### Coherence examp
Given that the user in a certain mobile communication system is moving with a velocity of 1,000 km/h, which of the following downlink power allocation strategies makes more sense, assuming multiple antennas at the base station?

(i) The transmit power budget is divided evenly among the base station's antennas.
(ii) The transmit power budget is divided among the base station's antennas, according to the channel state information feedback provided by the mobile phone to the base station.
(iii) No transmit power is assigned to the user if it experiences a bad channel condition.


****
**answer:**
(i) The transmit power budget is divided evenly among the base station's antennas.
- No up-to-date channel state information can be fed back to the transmitter if users are moving very fast, as channel coherence time is shorter than feedback+transmission time.