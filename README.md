Amazon EC2 clock accuracy research
==================================

## Vision

Millisecond clock accuracy is important for many applications, and especially for financial applications.

Accuracy (especially in Windows and older Linux kernels) can be poor on virtualized hardware due to the 
[necessary] CPU interruptions experienced by VM Guest OSes.  
[This VMware whitepaper](http://www.vmware.com/files/pdf/Timekeeping-In-VirtualMachines.pdf) discusses the underlying
technical reasons for this.

This repository contains the results of research into how accurate EC2 instance clocks can be made when
using NTP, and a description of the tools & research methodology used so that this research an be reproduced.

### Status

Currently available are respective infrastructure automation scripts to operate a cross region cluster of of Amazon EC2 machines 
of differing sizes and OS, see the following links for further details:

* [Infrastructure setup instructions](https://github.com/cityindex/ec2-clock-accuracy-research/tree/master/infrastructure#infrastructure-setup-instructions)
* [Botocross - A (dedicated) Python package for operating cross region AWS resources](https://github.com/sopel/botocross)

## Challenges

### Steal Time

It should be possible to gain more insight into the accuracy of virtualized hardware by measuring the *CPU steal time* 
and correlating it with NTP data (see IBM's presentation 
[CPU time accounting](http://public.dhe.ibm.com/software/dw/linux390/perf/CPU_time_accounting.pdf) for for a technical explanation 
and illustrations of the concept). However, while most Unix/Linux monitoring tools nowadays expose this metric, it doesn't seem to be 
(readily) available on Windows via respective 
[Windows Performance Counters](http://technet.microsoft.com/en-us/library/cc774901%28v=ws.10%29.aspx) yet 
for example (see [Is there a Windows equivalent of Unix 'CPU steal time'?](http://serverfault.com/q/392216/10305) for details).
