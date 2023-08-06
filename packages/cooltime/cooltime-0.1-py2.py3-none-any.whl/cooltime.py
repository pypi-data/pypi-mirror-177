
from datetime import datetime as datetimeSon
from random import randint


nowTime = lambda : str(datetimeSon.now())[:19]  # -> '2021-10-24 20:19:10'

nowDate = lambda : str(datetimeSon.now())[:10]  # -> '2021-10-24'

prettyTime = lambda : f"[{nowTime()}]"      # -> '[2021-10-24 20:18:57]'

randomTime = lambda: str(datetimeSon.fromtimestamp(
            randint(63043200, 2114352000)
            ))[:19]  # -> '2021-10-24 20:19:10'
