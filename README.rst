IOSSHy provides an easy to use desktop tool to quickly create and destory SSH tunnels and launch commands based on a preconfigured setup.

============
Installation
============
------------
Dependencies
------------
IOSSHy depends upon the following external libraries:

* PyKDE4 (Optional for better KDE4 integration)
* PyQt4
* Paramiko

------------------
Build instructions
------------------
Before using this applications the Qt forms and icon resources must be compiled.
There is a unix shell script in the root of the distribution package named *build.sh* that takes care of this process::

	cd [SOURCE FOLDER]
	sh build.sh
	chmod 755 bin/iosshy
	bin/iosshy

=============
Example usage
=============
Create a SSH tunnel to a remote host on the MySQL port and launch a program locally that uses the tunnel to manipulate the database.
When the program terminates the tunnel is automatically closed.
