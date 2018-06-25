#!/usr/bin/env python3
import asyncio
import random


class JankenServerProtocol(asyncio.Protocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.my_score = self.your_score = 0
        self.moves = 0

    def _send_your_move(self):
        self.transport.write(b"Your move? ")

    def connection_made(self, transport):
        print("New connection.")
        self.transport = transport

        message = ("1: Guu (Rock)\n"
                   "2: Choki (Scissors)\n"
                   "3: Paa (Paper)\n\n")
        self.transport.write(message.encode())
        self._send_your_move()

    def _send_score(self):
        self.transport.write("Me {} - {} You\n".format(
                            self.my_score, self.your_score).encode())

    def _next_move(self):
        if self.my_score == 2 or self.your_score == 2:
            self.transport.write(b"End of the game!\n")
            if self.my_score > self.your_score:
                self.transport.write(b"I won!\n")
            elif self.my_score == self.your_score:
                self.transport.write(b"It's a draw!\n")
            else:
                self.transport.write(b"You won! Congratulations!\n")
            self.transport.write(b"See you next time for another game.\n")
            self.transport.close()
        else:
            self._send_your_move()

    def data_received(self, data):
        try:
            your_move = int(data.decode())

            if your_move < 1 or your_move > 3:
                raise ValueError()
        except ValueError:
            self.transport.write("Invalid choice: {!r}\n".format(
                data).encode())
            self.send_your_move()
        else:
            my_move = random.randint(1, 3)
            you_won = my_move == 1 and your_move == 3 or \
                my_move == 2 and your_move == 1 or \
                my_move == 3 and your_move == 2
            draw = my_move == your_move
            if you_won:
                self.transport.write(b"Good catch!\n")
                self.your_score += 1
            elif draw:
                self.transport.write(b"Draw!\n")
            else:
                self.transport.write(b"Shame! :-)\n")
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
