import random
from collections import namedtuple

Row = namedtuple('StateAction', ('state_start', 'action', 'state_end', 'reward'))

class ReplayMemory(object):

    def __init__(self):
        self.memory = []
        self.position = 0

    def push(self, *args):
        """Saves a row."""
        self.memory.append(None)
        self.memory[self.position] = Row(*args)
        self.position = self.position + 1 

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

    def merge(self, memories):
        for m in memories:
            for row in m:
                self.push(*row)
