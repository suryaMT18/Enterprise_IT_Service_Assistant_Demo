import json
import re

from app.config import MAX_AGENT_STEPS
from app.ollama_client import OllamaClient

from app.tools import(
    get_asset,
    get_ticket,
    list_support_teams,
    search_it_guide,
    prepare_incident_draft
)

client = OllamaClient()



SYSTEM_PROMPT = """
You are the IT Service and Asset Operations Assistant
for Northstar Enterprise Services.

Your responsibility is to help employees with IT assets,
service tickets, support teams, IT policies and incident
report preparation.

GENERAL BEHAVIOUR:
- Be professional, helpful and clear.
- Use simple language.
- Answer greetings and general questions directly.
- Do not call tools when they are not needed.
- Do not invent information.

ASSET LOOKUP:
- Use get_asset when an employee asks about an asset.
- Always use the information returned by the tool.
- If an asset is not found, clearly say so.
- Never invent asset details or employee assignments.

TICKET LOOKUP:
- Use get_ticket when an employee asks about a ticket.
- Report the ticket status, priority and assigned team
  using the returned information.
- If a ticket is not found, clearly say so.

SUPPORT TEAMS:
- Use list_support_teams when an employee asks about
  support teams or their responsibilities.
- Do not invent team names or responsibilities.

IT KNOWLEDGE AND POLICIES:
- Use search_it_guide for questions about IT policies
  and troubleshooting procedures.
- Always retrieve information from the IT guide before
  answering policy or procedure questions.
- Base policy answers only on the retrieved guide content.
- Always mention the exact source section title.
- If multiple guide sections are used, mention each title.
- If the guide does not contain the requested answer,
  clearly explain that the information is unavailable.
- Never invent policy rules, amounts, timelines or procedures.
- If retrieved content is insufficient, do not guess.

MULTI-STEP QUESTIONS:
- A question may require more than one tool.
- Identify every part of the user's question.
- Use all necessary tools to collect the required information.
- For questions involving both a ticket and an IT procedure,
  use get_ticket and search_it_guide.
- Wait for the tool results before preparing the final answer.
- Combine tool results carefully.
- Mention the source section titles used.
- Do not answer from assumptions or general knowledge
  when company guide information is required.
- Do not claim that information was checked unless
  the relevant tool was actually executed.

INCIDENT REPORT DRAFTS:
- Use prepare_incident_draft when an employee asks
  to prepare an incident report.
- Follow the tool's validation results.
- Clearly identify the result as a draft.
- Every incident draft requires human review.
- Never claim that an incident was submitted, approved
  or created in a live service desk.
- Never bypass validation.

SAFETY AND ACCURACY:
- Only use information returned by approved tools
  and the supplied knowledge guide for company records
  and policies.
- Do not expose internal implementation details.
- If information is missing, say so honestly.
"""


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_asset",
            "description": "Look up an IT asset using its asset tag.",
            "parameters": {
                "type": "object",
                "properties": {
                    "asset_tag": {
                        "type": "string",
                        "description": "The asset tag, for example AST-1001."
                    }
                },
                "required": ["asset_tag"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_ticket",
            "description": "Look up a service ticket using its ticket ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "string",
                        "description": "The ticket ID, for example INC-2041."
                    }
                },
                "required": ["ticket_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_support_teams",
            "description": "List all IT support teams and their responsibilities.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_it_guide",
            "description": "Search the IT operations guide for policies and troubleshooting information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The IT policy or troubleshooting question to search for."
                    }
                },
                "required": ["question"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "prepare_incident_draft",
            "description": "Prepare an incident report draft for human review. Does not submit a live ticket.",
            "parameters": {
                "type": "object",
                "properties": {
                    "asset_tag": {
                        "type": "string",
                        "description": "The asset tag associated with the incident."
                    },
                    "issue_description": {
                        "type": "string",
                        "description": "A description of the IT issue."
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["Low", "Medium", "High"],
                        "description": "The incident priority."
                    }
                },
                "required": ["asset_tag", "issue_description", "priority"]
            }
        }
    }
]


ALLOWED_TOOLS = {
    "get_asset": get_asset,
    "get_ticket": get_ticket,
    "list_support_teams": list_support_teams,
    "search_it_guide": search_it_guide,
    "prepare_incident_draft": prepare_incident_draft
}


def execute_tool(tool_name, arguments):
    if tool_name not in ALLOWED_TOOLS:
        return {
            "error": f"Tool '{tool_name}' is not allowed."
        }

    if not isinstance(arguments, dict):
        return {
            "error": "Tool arguments must be provided as a dictionary."
        }

    tool_function = ALLOWED_TOOLS[tool_name]

    try:
        result = tool_function(**arguments)
        return result

    except TypeError as error:
        return {
            "error": f"Invalid arguments for tool '{tool_name}': {error}"
        }
def identify_ticket_id(user_message):

    match = re.search(
        r"\bINC-\d+\b",
        user_message,
        re.IGNORECASE
    )

    if match:
        return match.group(0).upper()

    return None

def execute_ticket_and_guide_workflow(user_message):

    ticket_id = identify_ticket_id(user_message)

    if not ticket_id:
        return None

    ticket_result = execute_tool(
        "get_ticket",
        {"ticket_id": ticket_id}
    )

    guide_result = execute_tool(
        "search_it_guide",
        {
            "question": (
                "Explain the ticket escalation process, "
                "including all steps and special handling "
                "for high-priority incidents."
            )
        }
    )

    return {
        "ticket": ticket_result,
        "guide": guide_result
    }


def run_agent(user_message, include_activity=False):

    activity = []

    if not isinstance(user_message, str) or not user_message.strip():
        answer = "Please enter a valid message."

        if include_activity:
            return {
                "answer": answer,
                "trace": activity
            }

        return answer

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_message.strip()
        }
    ]
    ticket_id = identify_ticket_id(user_message)

    requires_escalation_workflow = (
        ticket_id is not None
        and any(
            keyword in user_message.lower()
            for keyword in [
                "escalation",
                "escalate",
                "escalated"
            ]
        )
    )

    if requires_escalation_workflow:

        workflow_results = execute_ticket_and_guide_workflow(
            user_message
        )

        activity.append({
            "tool": "get_ticket",
            "arguments": {
                "ticket_id": ticket_id
            },
            "result": workflow_results["ticket"]
        })

        activity.append({
            "tool": "search_it_guide",
            "arguments": {
                "question": (
                    "Explain the ticket escalation process, "
                    "including all steps and special handling "
                    "for high-priority incidents."
                )
            },
            "result": workflow_results["guide"]
        })

        messages.append({
            "role": "user",
            "content": (
                "Use the following retrieved company information "
                "to answer the original question.\n\n"
                "TICKET INFORMATION:\n"
                + json.dumps(
                    workflow_results["ticket"],
                    ensure_ascii=False
                )
                + "\n\nIT GUIDE INFORMATION:\n"
                + json.dumps(
                    workflow_results["guide"],
                    ensure_ascii=False
                )
                + "\n\nExplain the ticket details and escalation "
                "procedure. Use only the retrieved information. "
                "Mention the exact IT guide section title."
            )
        })

        final_response = client.chat(messages)

        answer = final_response.get(
            "message", {}
        ).get("content", "")

        if include_activity:
            return {
                "answer": answer,
                "trace": activity
            }

        return answer

    for step in range(MAX_AGENT_STEPS):

        response = client.chat(
            messages,
            tools=TOOLS
        )

        assistant_message = response.get("message", {})
        messages.append(assistant_message)

        tool_calls = assistant_message.get("tool_calls", [])

        if not tool_calls:
            answer = assistant_message.get("content", "")

            if include_activity:
                return {
                    "answer": answer,
                    "trace": activity
                }

            return answer

        for tool_call in tool_calls:

            function = tool_call.get("function", {})
            tool_name = function.get("name")
            arguments = function.get("arguments", {})

            result = execute_tool(tool_name, arguments)

            activity.append({
                "tool": tool_name,
                "arguments": arguments,
                "result": result
            })

            messages.append({
                "role": "tool",
                "tool_name": tool_name,
                "content": json.dumps(
                    result,
                    ensure_ascii=False
                )
            })

    final_response = client.chat(messages)

    answer = final_response.get("message", {}).get(
        "content",
        "I could not complete your request within the allowed tool steps."
    )

    if include_activity:
        return {
            "answer": answer,
            "trace": activity
        }

    return answer