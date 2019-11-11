# FVCBot
[![FVCBot - Wikimedia Commons](https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Mini-Robot.png/211px-Mini-Robot.png)](https://commons.wikimedia.org/wiki/User:FVCBot)

Hi, I’m Featured video candidates bot. My job includes counting of votes, closing nomination, notifying the nominator if the nomination gets featured and marking the featured nominations with featured video tag. I work in 3 shifts a day (5:00, 13:00, 21:00 UTC). I live in the servers of Toollabs (Eqiad cluster), Virginia, Ashburn, United States of America. 


From Eatcha:
This script is derived from the source code of fpcBot https://github.com/Zitrax/fpcBot  which was originally written by 
Daniel78 at commons.wikimedia.org or Zitrax on GitHub. 

Its user page is at https://commons.wikimedia.org/wiki/User:FVCBot


Bot's recent edits can be found at https://commons.wikimedia.org/wiki/Special:Contributions/FVCBot

This bot runs in 3 shifts 5:00, 13:00, 21:00 UTC  , the cronjob looks like the following. 
0 5,13,21 * * * jsub -once python3 fvc.py -park -close -auto




### Emergency bot shutoff button, can be used by wikimedia commons Administrators only

[![FVCBot - Wikimedia Commons](https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Shutdown_button_red_wikimedia.svg/120px-Shutdown_button_red_wikimedia.svg.png)](https://commons.wikimedia.org/w/index.php?title=Special:Blockip&wpTarget=FVCBot&wpExpiry=indefinite&wpAnonOnly=0&wpHardBlock=1&wpAutoBlock=0&wpCreateAccount=0&wpReason=other&wpReason-other=Bot%20malfunctioning:%20)


[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![GPL 3 license](https://img.shields.io/badge/GPL-3-green.svg)](https://github.com/eatcha-wikimedia/FVCBot/blob/master/LICENSE)
![Open Source Love png1](https://badges.frapsoft.com/os/v1/open-source.png?v=103)

