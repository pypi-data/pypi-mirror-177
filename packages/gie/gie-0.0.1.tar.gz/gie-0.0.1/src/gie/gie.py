
import random
def moo():

    msgs = [
        "Hello, gie!",
        "Mooo!",
        "How bis ya?",                                                                                                                                                                                                                                                                                                                 "Bis tired!", "Warkentje!", "Coffebrodje?","MOOOOO!", "Where is poodle?", "Bis Moona? Hello!", "Shepoo? Bis you?", "Indeed, indeed!", "I miss japan!", "time to go to sleep?",
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
