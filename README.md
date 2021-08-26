# IC-7300-time-sync
Python3 script to sync the ICOM IC-7300 radio's clock (date and time) with your computer via CAT commands.

The latest script is Set_IC7300_date_time.py as modified by AD0YO
The original script is Set_IC7300_time.py as written by loughkb

At the top of the script are a few variables you'll have to set.
The serial device name your 7300 is at and the baudrate.
Whether to use local or gmt.
you can set the verbose to True to get a little output.
The rest of the script is commented and should be self-explainatory.  

You can run it manually from the terminal, or set it up as a cron job to automatically update the radio clock at an interval.  

After downloading the script, you'll need to mark it as executable.  From the terminal, you can do this with the following command.
chown +x {script name}
From most desktops, you can right-click on the script and select properties.  Under the permissions tab, there should be a check box to "allow executing as a program".

To make the script accessible system wide, you can copy it,  as the root user, to the /usr/bin directory.
sudo cp ./{script name} /usr/bin

When run, the script will get the current time of your computer, wait for the top of the minute at 00 seconds, and set the radio's time.

There is a demo video on my you tube channel.  Search you tube for KB9RLW python to find it, or copy the video link below.
