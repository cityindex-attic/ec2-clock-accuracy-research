maintainer       "David Laing"
maintainer_email "david.laing@cityindex.com"
license          "Apache v2"
description      "Base install for Windows 2008R2 and Ubuntu machines (configures users etc)"
long_description IO.read(File.join(File.dirname(__FILE__), 'README.md'))
version          "0.0.23"

supports "ubuntu"
supports "windows"

depends  "sudo"
depends  "windows_ntpd"
	