# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 17:38:40 2024

@author: tevslin
debate management modules
"""
# Define paths for your images directly as specified
logo_image_path = 'logo_image.jpg'  # Path to your logo image
russia_flag_path = 'russia_flag.jpg'  # Path to Russia flag image
iaea_flag_path = 'iaea_logo.png'  # Path to IAEA logo image
chat_manager_flag_path = 'judge.png'  # Path to Chat Manager image

class debate:    
    def __init__(self, api_key, llm="gpt-4-1106-preview",
                 saved_team='debateteam.json'):  # Default to local file
        import os
        import json
        
        self.llm = llm
        tdict = {"model": llm, "api_key": api_key}
        os.environ['OAI_CONFIG_LIST'] = "[" + json.dumps(tdict) + "]"
        self.config_file_or_env = 'OAI_CONFIG_LIST'
        self.saved_team = saved_team  # Now points to a local file by default
        self.llm_config = {'temperature': 0}
        os.environ['AUTOGEN_USE_DOCKER'] = 'False'
        
    def load_team(self):
        import requests
        import tempfile
        import os
        from urllib.parse import urlparse
        from autogen.agentchat.contrib.agent_builder import AgentBuilder
        
        parsed = urlparse(self.saved_team)
        if parsed.scheme and parsed.netloc:
            response = requests.get(self.saved_team)
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(response.content)
            file_name = tmp_file.name
        else:
            file_name = self.saved_team
        builder = AgentBuilder(config_file_or_env=self.config_file_or_env)
        self.agent_list, self.agent_config = builder.load(file_name)
        if not self.saved_team == file_name:
            os.remove(file_name)
        

    def do_debate(self,proposition):
        import autogen
        
        config_list = autogen.config_list_from_json(self.config_file_or_env,
                                                    filter_dict={"model": [self.llm]})
        group_chat = autogen.GroupChat(agents=self.agent_list, messages=[], max_round=15)
        manager = autogen.GroupChatManager(
            groupchat=group_chat, llm_config={"config_list": config_list, **self.llm_config}
        )
        self.agent_list[0].initiate_chat(manager, message=proposition)


if __name__ == '__main__':
    from dotenv import load_dotenv
    import os

    load_dotenv()       
    dm=debate(os.getenv('OPENAI_API_KEY'))
    dm.load_team()
    proposition=" "
    while len(proposition)>0:  #loop unitl user terminates
        proposition=input("what position would you like to negotiate? hit enter to terminate. ")
        if len(proposition)>0: #if not terminating
            dm.do_debate(f'Please continue to negotiate your position {proposition}')
        
        
        

