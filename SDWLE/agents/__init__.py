from SDWLE.agents.agent_registry import AgentRegistry as __ar__
from SDWLE.agents.basic_agents import RandomAgent, DoNothingAgent
from SDWLE.agents.trade_agent import TradeAgent

registry = __ar__()

registry.register("Nothing", DoNothingAgent)
registry.register("Random", RandomAgent)
registry.register("Trade", TradeAgent)