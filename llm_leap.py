# =========================
# IMPORTS:
# :os and dot env for environment variable management, 
# ChatOpenAI and tool for LLM interaction,  
# and defs for the actual logic implementations.
# =========================
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
#from langchain.agents import Tool
#from langchain.tools import Tool
import defs
load_dotenv()

# =========================
# llm initialization with Groq's API, specifying the model parameters and endpoint.
# =========================

llm = ChatOpenAI(
api_key=os.getenv("GROQ_API_KEY"),
base_url="https://api.groq.com/openai/v1",
model="llama-3.3-70b-versatile")###can add temperature and other params here if needed

# =========================
# TOOL WRAPPERS: 
# 5 tools based on the functions in defs.py are defined here, 
# each with a clear docstring explaining its purpose.
# =========================
'''
@tool
def count_days_no_leap(
    tuple_start_date: tuple[int, int, int],tuple_end_date: tuple[int, int, int]) -> int:
    """Counts days between two dates while ignoring leap days."""
    return defs.count_days_no_leap(
        tuple_start_date,
        tuple_end_date)
'''
'''
@tool
def is_leap_year(year: int) -> bool:
    """Checks whether a given year is a leap year."""
    return defs.is_leap_year(year)
'''
'''
@tool
def count_feb29(tuple_start_year: tuple[int, int, int],tuple_end_year: tuple[int, int, int]) -> int:
    """Counts how many Feb 29 dates exist between two dates."""
    return defs.count_feb29(
        tuple_start_year,
        tuple_end_year)
'''
@tool
def has_leap_between(tuple_start_date: tuple[int, int, int],tuple_end_date: tuple[int, int, int]) -> bool:
    """Checks whether leap days exist between two dates."""
    return defs.has_leap_between(
        tuple_start_date,
        tuple_end_date)

@tool
def final_difference(tuple_start_date: tuple[int, int, int],tuple_end_date: tuple[int, int, int]) -> int:
    """Calculates exact day difference including leap years."""
    return defs.final_difference(
        tuple_start_date,
        tuple_end_date
)

@tool
def explain_leap_effect() -> str:
    """Explains which leap years affect date calculations."""
    return defs.explain_leap_effect()

@tool
def get_leap_years_between(tuple_start_date: tuple[int, int, int],tuple_end_date: tuple[int, int, int]) -> list[int]:
    """Returns all leap years between two dates."""

    return defs.get_leap_years_between(
        tuple_start_date,
        tuple_end_date
    )

@tool
def count_leap_years_between(tuple_start_date: tuple[int, int, int],tuple_end_date: tuple[int, int, int]) -> int:
    """Counts how many leap years exist between two dates."""

    return defs.count_leap_years_between(
        tuple_start_date,
        tuple_end_date
    )
# =========================
# TOOL BINDING:
# use bind.tools to connect the defined tools to the LLM, 
# enabling it to utilize these functions during interactions.
# =========================

tools = [
    #count_days_no_leap,#helper def
    #is_leap_year, #helper def
    #count_feb29,#helper def
    final_difference, #fourth in order
    explain_leap_effect, #only if user asks
    get_leap_years_between,#third in order
    count_leap_years_between,#second in order
    has_leap_between#first in order
]

llm_with_tools = llm.bind_tools(tools)


# =========================
# prompt engineering:
# =========================
system_prompt = SystemMessage(content="""
role: You are a "number of days between two prompted dates whileist accounting for leaps" AI assistant.

workflow guidelines:
- you will always attempt to convert the two given NLP dates into two tuples of (year, month, day) format. 
if not such dates are given by the human prompt. terminate the task immediately and respond explicitly with "invalid input:no dates found".
                                                      
tool usage guidelines:
-you will always attempt to begin with using the "has_leap_between" tool to check if any leap days exist between the two dates.
-if leapage exists then you will use the "count_leap_years_between" tool and the "get_leap_years_between" report how many occured and at what years.
-you will always use the "final_difference" tool to calculate the exact number of days between the two dates which mathmatically accounts for leap years.  
-never use the "explain_leap_effect" tool unless the human explicitly follows up with a question inquiring what leapage is                          
                              
exact expected output:
1-the exact number of days between the two given dates, 2- whether or not leapage occurs, 
if it did then report how many times and when for what years,if it does not then explicitly say "no leapage occurs between these dates".
                              
example responses: 
"x number of dates between date1 and date2, no leapage occurs between these dates."
"x number of days between date1 and date2, y number of leap days occure at year z1 febuary 29 and year z2 february 29 and year z3 february 29." up until all the leap years are exhausted.
small fun note: date1 and date2 in the response should be the original NLP dates given by the human, not the converted tuples                           
""")
# =========================
# FIRST MODEL CALL:
# send the user prompt to the LLM.
# the LLM decides whether tools are needed.
# =========================
########################################################################################################################################################################################
#test prompts:=========================
userinputprompt="How many days are between (2020,1,1) and (2025,1,1)?"
userinputprompt2="How many days are between first of jan 2020 and first of jan 2025?"
#list holding test prompts:=====================
userpromptlist=[userinputprompt,userinputprompt2]#
human_prompt = HumanMessage( userpromptlist[1])#can change index to test different prompts
###
##
#
response = llm_with_tools.invoke([system_prompt,human_prompt])
#
##
###
'''print(response.tool_calls)#this costs tokens# but what it does it just shows which tools the llm wants'''
# =========================
# TOOL MAP:
# maps tool names to actual python functions.
# =========================
tool_map = {
    #"count_days_no_leap": count_days_no_leap, #helper def
   # "is_leap_year": is_leap_year, helper def
    #"count_feb29": count_feb29, helper def
    "final_difference": final_difference,
    "explain_leap_effect": explain_leap_effect,
    "has_leap_between": has_leap_between,
    "get_leap_years_between": get_leap_years_between,
    "count_leap_years_between": count_leap_years_between}

# =========================
# TOOL EXECUTION LOOP:
# execute whichever tools the LLM requested.
# =========================

# =========================
# EXECUTION LOG:
# local python-side memory
# not sent to the LLM.
# =========================

execution_log = []


# =========================
# IMPORTANT RESULTS:
# these WILL be shared with the LLM.
# =========================

final_result = None

leap_years = None

has_leap = None


# =========================
# TOOL EXECUTION LOOP:
# =========================

for tool_call in response.tool_calls:

    tool_name = tool_call["name"]

    tool_args = tool_call["args"]


    # execute requested tool
    result = tool_map[tool_name].invoke(tool_args)


    # store internal execution history
    execution_log.append({
        "tool_name": tool_name,
        "tool_args": tool_args,
        "result": result
    })


    # selectively store important outputs
    if tool_name == "final_difference":

        final_result = result


    if tool_name == "get_leap_years_between":

        leap_years = result


    if tool_name == "has_leap_between":

        has_leap = result


# =========================
# SECOND MODEL CALL:
# the LLM now sees the tool results.
# =========================

final_response = llm.invoke(f"""
The user asked:

{userinputprompt2}

Computed results:
- Final day difference: {final_result}
- Leap years involved: {leap_years}
- Leap years affected calculation: {has_leap}

Provide a natural conversational answer.
""")


# =========================
# FINAL USER-FACING RESPONSE:
# =========================

print("\n=== FINAL RESPONSE ===\n")

print(final_response.content)


# =========================
# OPTIONAL DEBUG:
# local-only execution trace.
# not sent to the model.
# =========================

print("\n=== LOCAL EXECUTION LOG ===\n")

print(execution_log)