jankens
=======

jankens is, as its name tells, a script which plays the jankens (rock - paper -
scissors) game with an end-user.

The game is playable through netcat or telnet. Launch the script on your
local machine (using python 3.6) then launch a game using:

.. code:: raw

    nc localhost 8888

or

.. code:: raw

    telnet localhost 8888

Example of game:


.. code:: raw

    1: Guu (Rock)
    2: Choki (Scissors)
    3: Paa (Paper)

    Your move? 1
    Draw!
    Me 0 - 0 You
    Your move? 3
    Good catch!
    Me 0 - 1 You
    Your move? 2
    Draw!
    Me 0 - 1 You
    Your move? 1
    Good catch!
    Me 0 - 2 You
    End of the game!
    You won! Congratulations!
    See you next time for another game.
