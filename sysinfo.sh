#!/bin/sh

upSeconds="$(/usr/bin/cut -d. -f1 /proc/uptime)"
secs=$((${upSeconds}%60))
mins=$((${upSeconds}/60%60))
hours=$((${upSeconds}/3600%24))
days=$((${upSeconds}/86400))
UPTIME=`printf "%d days, %02dh%02dm%02ds" "$days" "$hours" "$mins" "$secs"`

# get the load averages
read one five fifteen rest < /proc/loadavg

echo "$(tput setaf 2)
                  `date +"%A, %e %B %Y, %r"`
   .~~.   .~~.    `uname -srmo`
  '. \ ' ' / .'   `lsb_release -d | sed "s/Description:\t//"`$(tput setaf 1)
   .~ .~~~..~.
  : .~.'~'.~. :   Uptime.............: ${UPTIME}
 ~ (   ) (   ) ~  Memory.............: `cat /proc/meminfo | grep MemFree | awk {'print $2'}`kB (Free) / `cat /proc/meminfo | grep MemTotal | awk {'print $2'}`kB (Total)
( : '~'.~.'~' : ) Load Averages......: ${one}, ${five}, ${fifteen} (1, 5, 15 min)
 ~ .~ (   ) ~. ~  Running Processes..: `ps ax | wc -l | tr -d " "`
  (  : '~' :  )   IP Addresses.......: `ip a | grep glo | awk '{print $2}' | head -1 | cut -f1 -d/` and `wget -q -O - http://icanhazip.com/ | tail`
   '~ .~~~. ~'    CPU Temprature.....: `vcgencmd measure_temp | sed 's/temp=//'`
       '~'
$(tput sgr0)"
