
import random
def moo():

    msgs = [
        "Hello, gie!",
        "Mooo!",
        "How bis ya?",                                                                                                                                                                                                                                                                                                                 "Bis tired!", "Warkentje!", "Coffebrodje?","MOOOOO!", "Where is poodle?", "Bis Moona? Hello!", "Sheepoo? Bis you?", "Indeed, indeed!", "I miss japan!", "time to go to sleep?", "Where bis Sheepoo?", "Amsterdam misses ya!", "Smile more!", "Remember to smile!", "Enjoy the day!", "Take it easy, you work too hard!", "When will my hair grow back?", "Bis poodle with ya?", "Yayaya!", "YAYAYA!",
        "Gie bis sleeeeepyyyy!",
    ]

    msg = random.choice(msgs)

    gie = f"""

    o        O
     \  v   /
     /^^^^^^\\
    /        \\
   |  O    O  |
   | .      . |  {msg}
   |  \____/  |
    \        /
     \      /
      |    |
      |    |
      |    |
      |    |
      |    |
       \__/
    """
    print(gie)
