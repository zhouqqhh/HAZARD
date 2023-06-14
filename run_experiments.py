from challenge import Challenge, init_logs
from policy.llm import LLM, SamplingParameters
from policy.change_reasoner import LLMChangeReasoner
from policy.random import RandomAgent
from policy.fire_flood_heuristic import HAgent, HAgentWind_FROM_MCTS
from policy.human import HumanAgent
from policy.mcts import MCTS
from policy.record_agent import RecordAgent
from policy.rl import RLAgent
import argparse
import os

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api_key", type=str)
    parser.add_argument("--api_key_file", type=str, default="")
    parser.add_argument("--output_dir", type=str, default="outputs")
    parser.add_argument("--env_name", type=str, choices=["fire", "flood", "wind"], default="flood")
    parser.add_argument("--agent_name", type=str, choices=["random", "llm", "mcts", "llm+change", "h_agent", "human",
                                                           "record", "rl"], default="llm")
    parser.add_argument("--data_dir", type=str, default="data/room_setup_fire/mm_craftroom_2a-1")
    parser.add_argument("--port", type=int, default=1071)
    parser.add_argument("--max_tokens", type=int, default=64)
    parser.add_argument("--prompt_path", type=str, default="llm/prompt.csv")
    parser.add_argument("--lm_id", type=str, default="gpt-3.5-turbo")
    parser.add_argument("--debug", action='store_true', default=False)
    return parser.parse_args()

def get_agent(args):
    if args.agent_name == "llm":
        sampling_parameters = SamplingParameters(debug=args.debug, max_tokens=args.max_tokens)
        if args.api_key_file != "":
            api_key_file = open(args.api_key_file)
            api_key_list = api_key_file.readlines()
            api_key_list = [api_key.strip() for api_key in api_key_list]
            return LLM(source="openai", lm_id=args.lm_id, prompt_template_path=args.prompt_path, cot=True,
                       sampling_parameters=sampling_parameters, task=args.env_name, api_key=api_key_list)
        else:
            return LLM(source="openai", lm_id=args.lm_id, prompt_template_path=args.prompt_path, cot=True,
                       sampling_parameters=sampling_parameters, task=args.env_name, api_key=args.api_key)
    elif args.agent_name == "llm+change":
        sampling_parameters = SamplingParameters(debug=args.debug)
        if args.api_key_file != "":
            api_key_file = open(args.api_key_file)
            api_key_list = api_key_file.readlines()
            api_key_list = [api_key.strip() for api_key in api_key_list]
            return LLMChangeReasoner(source="openai", lm_id=args.lm_id, prompt_template_path=args.prompt_path,
                                     cot=True, sampling_parameters=sampling_parameters, task=args.env_name,
                                     api_key=api_key_list)
        else:
            return LLMChangeReasoner(source="openai", lm_id=args.lm_id, prompt_template_path=args.prompt_path,
                                     cot=True, sampling_parameters=sampling_parameters, task=args.env_name,
                                     api_key=args.api_key)
    elif args.agent_name == 'mcts':
        return MCTS(task=args.env_name)
    elif args.agent_name == 'random':
        return RandomAgent(task=args.env_name)
    elif args.agent_name == 'human':
        return HumanAgent(task=args.env_name, prompt_template_path=args.prompt_path)
    elif args.agent_name == "h_agent":
        if args.env_name in ["fire", "flood"]:
            return HAgent(task=args.env_name)
        else:
            return HAgentWind_FROM_MCTS(task=args.env_name)
    elif args.agent_name == "record":
        return RecordAgent(task=args.env_name)
    elif args.agent_name == "rl":
        return RLAgent(task=args.env_name)
    else:
        assert False

if __name__ == "__main__":
    args = get_args()
    print(args.data_dir)
    print(args.output_dir)
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    logger = init_logs(output_dir=args.output_dir, name=f"{args.env_name}_{args.agent_name}")
    if args.agent_name == "rl":
        challenge = Challenge(env_name=args.env_name, data_dir=args.data_dir, output_dir=args.output_dir, logger=logger,
                            launch_build=not args.debug, debug=args.debug, port=args.port, screen_size=1024, map_size_h=256, map_size_v=256)
    else:
        challenge = Challenge(env_name=args.env_name, data_dir=args.data_dir, output_dir=args.output_dir, logger=logger,
                            launch_build=not args.debug, debug=args.debug, port=args.port, screen_size=1024)
    agent = get_agent(args)
    if os.path.exists(os.path.join(args.data_dir, "log.txt")): # single episode
        challenge.submit(agent=agent, logger=logger, eval_episodes=1)
    else:
        challenge_list = os.listdir(args.data_dir)
        challenge_list = sorted(challenge_list)
        count = 0
        for task in challenge_list:
            if 'craftroom' not in task and 'kitchen' not in task and 'suburb' not in task:
                continue
            count += 1
            if count > 10: break
            now_data_dir = os.path.join(args.data_dir, task)
            now_output_dir = os.path.join(args.output_dir, task)
            if not os.path.exists(now_output_dir):
                os.makedirs(now_output_dir)
            eval_result_path = os.path.join(args.output_dir, task, 'eval_result.json')
            if os.path.exists(eval_result_path):
                print(f"{eval_result_path} exists")
                continue # already evaluated
            challenge.output_dir = now_output_dir
            challenge.data_dir = now_data_dir
            print(now_output_dir)
            challenge.submit(agent=agent, logger=logger, eval_episodes=1)
    challenge.env.controller.communicate({"$type": "terminate"})
    challenge.env.controller.socket.close()
