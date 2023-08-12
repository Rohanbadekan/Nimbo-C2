import os
from jsonc_parser.parser import JsoncParser

nimbo_root = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
config_file = os.path.join(nimbo_root, "config.jsonc")
config_agent_file = os.path.join(nimbo_root, "agent", "config.nim")
config = JsoncParser.parse_file(os.path.join(nimbo_root, "config.jsonc"))

config_agent = f"""
import nimprotect

############################ CONFIG ############################
# C2
let c2_scheme* = protectString("{config["listener"]["scheme"]}")
let c2_address* = protectString("{config["listener"]["address"]}")
let c2_port* = {config["listener"]["port"]}
# Agent
let is_exe* = IS_EXE
let sleep_on_execution* = {config["agent"]["sleep_on_execution"]}
let agent_execution_path_windows* = protectString("{config["agent"]["exe"]["execution_path"]}")
let agent_execution_path_linux* = protectString("{config["agent"]["elf"]["execution_path"]}")
var call_home_timeframe* = {config["agent"]["call_home_timeframe"]}
var call_home_jitter_percent* = {config["agent"]["call_home_jitter_percent"]}
var memsleep_technique* = {config["agent"]["sleep_obfuscation_technique"]}
var nekko_rc4_key* = protectString("{config["agent"]["nekko_rc4_key"]}")
# Communication
let communication_aes_key* = protectString("{config["communication"]["aes_key"]}")
let communication_aes_iv* = protectString("{config["communication"]["aes_iv"]}")
# Tasks
let could_not_retrieve* = "-"
############################ CONFIG ############################
"""


def create_config(is_exe: bool):
    global config_agent
    config_agent = config_agent.replace("IS_EXE", str(is_exe).lower())
    with open(config_agent_file, "wt") as f:
        f.write(config_agent)
