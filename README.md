# PItanga_software

## Notes
On vk16k33 key pres is not detected on low duty cycles 
```

The keyscanning circuit utilises the COM1/KS0 to COM3/KS2 outputs high as the keyscan output drivers.
The outputs COM0 to COM7 pulse low sequentially as the displays are multiplexed. The actual low time
varies from 64μs to 1024μs due to pulse width modulation from 1/16th to 16/16th for dimming control. The
LED drive mode waveforms and scanning shows the typical situation when all eight LED cathode drivers are
used.

```
