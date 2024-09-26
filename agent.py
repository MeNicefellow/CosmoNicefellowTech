from utils import *
from agent_literal import *
class Agent:
    def __init__(self, role):
        self.role = role
        self.literal = agents_literals[role]

