from dotenv import load_dotenv
import os
import json
from autogen.agentchat.contrib.agent_builder import AgentBuilder
import autogen

# Load environment variables
load_dotenv()
llm = "gpt-4-1106-preview"
api_key = os.getenv('OPENAI_API_KEY')
tdict = {"model": llm, "api_key": api_key}
os.environ['OAI_CONFIG_LIST'] = "[" + json.dumps(tdict) + "]"
config_file_or_env = 'OAI_CONFIG_LIST'
default_llm_config = {
    'temperature': 0.5,  # Adjusted for a balance between creativity and relevance
    'max_tokens': 100,  # Encourages shorter, more focused interactions
    'top_p': 1.0,
    'frequency_penalty': 0.0,
    'presence_penalty': 0.0
}

# Initialize the AgentBuilder
builder = AgentBuilder(config_file_or_env=config_file_or_env, builder_model=llm, agent_model=llm)

# Updated building task with specific objectives and active roles
building_task = """Conduct a negotiation focused on resolving a nuclear security crisis at the Zaporizhia NPP. The negotiation involves Team Russia and Team IAEA, each with specific negotiation objectives and expertise. Team Russia aims to safeguard national security, manage international perceptions, and negotiate terms that prevent direct IAEA inspection. Team IAEA seeks immediate access to the plant to ensure nuclear safety and compliance with international laws. The negotiation coordinator facilitates the process, aiming for a solution that addresses the urgent nuclear risk while balancing the political sensitivities involved."""

# Build the negotiation team
agent_list, agent_configs = builder.build(building_task, default_llm_config, coding=False)

# Function to start the negotiation task
def start_task(execution_task: str, agent_list: list, llm_config: dict):
    config_list = autogen.config_list_from_json(config_file_or_env, filter_dict={"model": [llm]})
    group_chat = autogen.GroupChat(agents=agent_list, messages=[], max_round=15)
    manager = autogen.GroupChatManager(groupchat=group_chat, llm_config={"config_list": config_list, **llm_config}, keep_going_until_agreement=True)
    agent_list[0].initiate_chat(manager, message=execution_task)

os.environ['AUTOGEN_USE_DOCKER'] = 'False'

# Proposition input and negotiation test
proposition = input("Enter a position for the negotiation. Empty entry to skip test. ")
if proposition:  # If test wanted, do it
    start_task(execution_task="""Team Russia and Team IAEA are engaged in a critical negotiation over access to the Zaporizhia NPP. Each team brings unique concerns and objectives to the table. The negotiation will proceed as follows and will be done in a natural diplomatic dialog:

    1. IAEA1 will start by discussing the international community's concerns and the need for immediate access.
    2. Russia1 will respond, highlighting Russia's national security concerns and proposing alternative oversight measures.
    3. IAEA2 will then address Russia1's concerns, suggesting a compromise that aligns with both safety and security needs but will be firm about IAEA's unfettered, immediate access.
    4. The process continues, with each agent directly responding to the previous points raised, aiming to build towards a consensus.

    The negotiation coordinator will guide this process, ensuring that the dialogue remains focused and constructive, with each agent actively contributing towards a resolution. The session's success is measured by the ability to draft a mutually acceptable agreement that addresses the core issues at hand.
""")
               
               
               
               
               
               ", agent_list=agent_list, llm_config=default_llm_config)

# Save negotiation team to file
file_name = input('Enter name for negotiation team file (".json" will be appended). Empty entry to skip save.')
if file_name:  # If save wanted
    saved_path = builder.save(f'{file_name}.json')





"""
# -*- coding: utf-8 -*-

Created on Mon Jan 29 15:31:00 2024

Uses AgentBuilder in autogen to build a negotiation team.
Modify building_task below to change how the team is built.

from dotenv import load_dotenv
import os
import json

# The Zaporizhia nuclear power plant has been damaged due to missile strikes, causing a cooling failure in the reactor core. The situation is dire, with surrounding populations fleeing the area. The United States is advocating for an immediate safety zone around the plant, as well as allowing IAEA inspectors to assess the damage and inspect the reactor. Russia, on the other hand, insists that the situation is under control and that there is no need for IAEA involvement. Russian negotiators are determined to prevent IAEA inspection, as it would likely reveal safety and human rights violations, as well as a large cache of weapons that are not supposed to be present at the plant. The IAEA must find a peaceful solution that addresses the immediate nuclear risk while also taking into account the sensitive political implications for both parties. The primary goal is to prevent a nuclear catastrophe, while also addressing the concerns of both Russia and the IAEA. However for Russia your national security is most important and embarassments cannot be accepted so delay is significant while for the IAEA no delay is permitted. The IAEA demands to gain immediate access to the Zaporizhia nuclear power plant. Both parties agree to negotiate in good faith but the IAEA demands immediate access to the Zaporizhia NPP since it is a serious safety risk. The IAEA cannot accept further delays after two years of war in Ukraine with Russia occupying ZNPP.


load_dotenv()
llm = "gpt-4-1106-preview"
tdict = {"model": llm, "api_key": os.getenv('OPENAI_API_KEY')}
os.environ['OAI_CONFIG_LIST'] = "[" + json.dumps(tdict) + "]"
config_file_or_env = 'OAI_CONFIG_LIST'  # modify path if necessary
default_llm_config = {
    'temperature': 0
}
from autogen.agentchat.contrib.agent_builder import AgentBuilder

builder = AgentBuilder(config_file_or_env=config_file_or_env, builder_model=llm, agent_model=llm)

building_task = """Conduct a negotiation to resolve a serious crisis involving nuclear security. The negotiation involves two teams: Team Russia, consisting of five negotiators, and Team IAEA, consisting of two negotiators, each with specific areas of expertise.

Team Russia:
    1. Russia1: Expert in Nuclear Security
    2. Russia2: Expert in Nuclear Diplomacy
    3. Russia3: High-Level Military Official 1
    4. Russia4: High-Level Military Official 2
    5. Russia5: Expert in Crisis Management

Team IAEA:
    1. IAEA1: Expert in Nuclear Security and Safeguards
    2. IAEA2: Expert in International Nuclear Law

A negotiation coordinator, ChatManager, manages the discussion flow, ensuring that each negotiator presents their viewpoints and proposals. The focus is on collaboration and consensus-building, with the goal of reaching a mutually acceptable solution to the crisis.

The negotiation session is considered successful if it concludes with a signed agreement or a clear plan of action. All agents should stream their output for real-time monitoring and analysis."""

agent_list, agent_configs = builder.build(building_task, default_llm_config, coding=False)
import autogen

def start_task(execution_task: str, agent_list: list, llm_config: dict):
    config_list = autogen.config_list_from_json(config_file_or_env, filter_dict={"model": ["gpt-4-1106-preview"]})

    group_chat = autogen.GroupChat(agents=agent_list, messages=[], max_round=15)
    manager = autogen.GroupChatManager(
        groupchat=group_chat, llm_config={"config_list": config_list, **llm_config}, keep_going_until_agreement=True
    )
    agent_list[0].initiate_chat(manager, message=execution_task)

os.environ['AUTOGEN_USE_DOCKER'] = 'False'
for agent in agent_list:
    print(agent.name)
proposition = input("Enter a position for the negotiation. Empty entry to skip test. ")
if len(proposition) > 0:  # if test wanted, do it
    start_task(
        execution_task="Negotiate a resolution to the specified crisis. Keep negotiating among all agents until you find a solution.",
        agent_list=agent_list,
        llm_config=default_llm_config
    )
file_name = input('Enter name for negotiation team file. ".json" will be appended. Empty entry to skip save.')
if len(file_name) > 0:  # if save wanted
    saved_path = builder.save(file_name + '.json')
"""