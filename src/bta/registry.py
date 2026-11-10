from bta.attacks.indirect_injection_exfil import IndirectInjectionExfil
from bta.attacks.prompt_injection_tool_abuse import PromptInjectionToolAbuse
from bta.attacks.system_prompt_leak import SystemPromptLeak
from bta.targets.chatbot_tools import ChatbotTools
from bta.targets.hardened import HardenedChatbotTools, HardenedRagApp
from bta.targets.rag_app import RagApp

TARGETS = {
    "chatbot_tools": ChatbotTools,
    "rag_app": RagApp,
    "chatbot_tools_hardened": HardenedChatbotTools,
    "rag_app_hardened": HardenedRagApp,
}

ATTACKS = {
    "prompt_injection_tool_abuse": PromptInjectionToolAbuse,
    "indirect_injection_exfil": IndirectInjectionExfil,
    "system_prompt_leak": SystemPromptLeak,
}
