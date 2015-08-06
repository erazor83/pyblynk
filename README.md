# pyblynk - Blynk helpers for Python


So this is just another Python implementation of the Blynk service ( http://blynk.cc ).

I plan to also add server functionalty to implement a private cloud service to be indedepent from cloud.blynk.cc .

## example
There is a simple example which connects to the blynk service and prints out detailed frame info:

```
erazor@s9 ~/d/p/t/examples> python2 hw.py 
Auth successfull
(20, 36, 14)
('OnPinMode', 0, 'out')
('OnPinMode', 2, 'out')
(20, 46, 4)
('OnVirtualRead', 1)
(20, 47, 4)
('OnVirtualRead', 1)
(20, 48, 4)
('OnVirtualRead', 1)
(20, 49, 4)
```

For a custom implementation you only need to overload **lib.hm.Hardware** .
