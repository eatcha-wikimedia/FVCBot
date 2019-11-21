# FVCBot : Featured video candidates bot
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f6844b0fbc5146b7a44413795aada49b)](https://www.codacy.com/manual/eatcha-wikimedia/FVCBot?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=eatcha-wikimedia/FVCBot&amp;utm_campaign=Badge_Grade)[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)[![GPL 3 license](https://img.shields.io/badge/GPL-3-green.svg)](https://github.com/eatcha-wikimedia/FVCBot/blob/master/LICENSE)


[![FVCBot - Wikimedia Commons](https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Mini-Robot.png/211px-Mini-Robot.png)](https://commons.wikimedia.org/wiki/User:FVCBot)

Hi, I’m [Featured video](https://commons.wikimedia.org/wiki/Commons:Featured_videos) [candidates](https://commons.wikimedia.org/wiki/Commons:Featured_video_candidates) [bot](https://commons.wikimedia.org/wiki/User:FVCBot). My job includes counting of votes, closing nomination, notifying the nominator if the nomination gets featured and marking the featured nominations with featured video tag. I work in 3 shifts a day (5:00, 13:00, 21:00 UTC). I live in the servers of Toollabs (Eqiad cluster), Virginia, Ashburn, United States of America. 

From Eatcha: This script is derived from the source code of [fpcBot](https://github.com/Zitrax/fpcBot) which was originally written by Daniel78 at commons.wikimedia.org / Zitrax on GitHub. Bot's recent edits can be found at [Special:Contributions/FVCBot](https://commons.wikimedia.org/wiki/Special:Contributions/FVCBot)

This bot runs in 3 shifts 5:00, 13:00, 21:00 UTC  , the cronjob looks like the following. 
0 5,13,21 * * * jsub -once python3 fvc.py -park -close -auto

## Emergency bot shutoff button, can be used by wikimedia commons Administrators only

[![FVCBot - Wikimedia Commons](https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Shutdown_button_red_wikimedia.svg/120px-Shutdown_button_red_wikimedia.svg.png)](https://commons.wikimedia.org/w/index.php?title=Special:Blockip&wpTarget=FVCBot&wpExpiry=indefinite&wpAnonOnly=0&wpHardBlock=1&wpAutoBlock=0&wpCreateAccount=0&wpReason=other&wpReason-other=Bot%20malfunctioning:%20)
