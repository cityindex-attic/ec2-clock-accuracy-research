Amazon EC2 clock accuracy research
==================================

### Vision

Millisecond clock accuracy is important for many applications, and especially for financial applications.

Accuracy (especially in Windows and older Linux kernels) can be poor on virtualized hardware due to the 
[necessary] CPU interruptions experienced by VM Guest OSes.  
[This VMWare whitepaper](http://www.vmware.com/files/pdf/Timekeeping-In-VirtualMachines.pdf) discusses the underlying
technical reasons for this.

This repository contains the results of research into how accurate EC2 instance clocks can be made when
using NTP, and a description of the tools & research methodology used so that this research an be reproduced.

