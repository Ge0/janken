#!/usr/bin/env python3
import asyncio
import random


class JankenServerProtocol(asyncio.Protocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.my_score = self.your_score = 0
        self.moves = 0

    def _send_line(self, line):
        self.transport.write(f"{line}\r\n".encode())

    def _send_your_move(self):
        self.transport.write(b"\nYour move? ")

    def connection_made(self, transport):
        print("New connection.")
        self.transport = transport

        self._send_line("1: Guu (Rock)")
        self._send_line("2: Choki (Scissors)")
        self._send_line("3: Paa (Paper)")
        self._send_your_move()

    def _send_score(self):
        self._send_line("Me {} - {} You".format(
                        self.my_score, self.your_score))

    def _next_move(self):
        if self.my_score == 2 or self.your_score == 2:
            self._send_line("End of the game!")
            if self.my_score > self.your_score:
                self._send_line("I won!")
            elif self.my_score == self.your_score:
                self._send_line("It's a draw!")
            else:
                self._send_line("You won! Congratulations!")
            self._send_line("See you next time for another game.")
            self.transport.close()
        else:
            self._send_your_move()

    def data_received(self, data):
        try:
            your_move = int(data.decode())

            if your_move < 1 or your_move > 3:
                raise ValueError()
        except ValueError:
            self._send_line("Invalid choice: {!r}".format(data))
            self._send_your_move()
        else:
            my_move = random.randint(1, 3)
            you_won = my_move == 1 and your_move == 3 or \
                my_move == 2 and your_move == 1 or \
                my_move == 3 and your_move == 2
            draw = my_move == your_move
            if you_won:
                self._send_line("Good catch!")
                self.your_score += 1
            elif draw:
                self._send_line("Draw!")
            else:
                self._send_line("Shame! :-)")
                self.my_score += 1
            self._send_score()
            self._next_move()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    coro = loop.create_server(JankenServerProtocol, '0.0.0.0', 8888)
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Caught ^C. Exit.")
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
