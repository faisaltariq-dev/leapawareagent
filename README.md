# Leap-Aware Date Difference Agent

## Overview

This project explores two different approaches to solving the same problem:

> calculating the exact number of days between two dates while correctly accounting for leap years.

The repository contains:

1. **A classic deterministic Python implementation**
2. **An experimental LLM-powered tool-calling agent implementation**

The project was built as an exploration into:

* dynamic programming style date traversal
* leap year logic
* tool orchestration
* agentic software architecture
* LLM tool calling with LangChain
* execution tracing and conversational synthesis

---
# Leap Year Rule

A leap year is a year with an extra day added to February, making it 366 days instead of 365.

This happens because the Earth takes slightly more than 365 days to orbit the Sun, so the calendar occasionally adds February 29 to stay aligned with the seasons.

Mathematically:


year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

# Project Structure

leapawareagent/
├── outputs
│   ├── llm_leap_output.txt
│   └── classic_dynamic_programming_output.txt
├── defs.py
├── example.env
├── llm_leap.py
├── classic_dynamic_programming_leap.py
├── README.md
└── requirements.txt

---

# defs.py

Contains the deterministic core logic shared by both implementations.

Functions include:

| Function                     | Purpose                                            |
| ---------------------------- | -------------------------------------------------- |
| `count_days_no_leap()`       | Counts days while intentionally ignoring leap days |
| `is_leap_year()`             | Determines whether a year is leap year             |
| `count_feb29()`              | Counts leap days between two dates                 |
| `has_leap_between()`         | Checks whether leap years affect the range         |
| `final_difference()`         | Calculates true calendar day difference            |
| `get_leap_years_between()`   | Returns all leap years in the range                |
| `count_leap_years_between()` | Counts leap years in the range                     |
| `explain_leap_effect()`      | Explains leap year behavior                        |

Some functions are intentionally used only as internal helper functions and are not exposed as LLM tools.

Examples:

* `count_days_no_leap()`
* `count_feb29()`
* `is_leap_year()`

This separation was done to reduce unnecessary tool exposure and improve agent orchestration quality.

---

# classic_dynamic_programming_leap.py

A traditional deterministic implementation.

This version:

* uses direct procedural logic
* imports deterministic functions from `defs.py`
* computes all leap-aware calculations explicitly
* produces deterministic outputs without AI involvement

Example real output:


1827 is the number of days between (2020, 1, 1) and (2025, 1, 1) leapage does occur between these dates 2 times at [2020, 2024] at Feb 29th each

A leap year is a year with an extra day added to February, making it 366 days instead of 365.


This script represents:


classical deterministic software architecture


---

# llm_leap.py

An experimental agentic implementation using:

* LangChain
* Groq-hosted LLMs
* tool calling
* orchestration prompts
* execution logging
* conversational synthesis

The LLM is provided with:

* tool descriptions
* orchestration instructions
* execution feedback
* system prompting

The model then:

1. selects tools
2. generates arguments
3. requests execution
4. receives tool outputs
5. synthesizes a conversational response based on excuted tool's results

This script represents:


agentic orchestration architecture

---

# Agent Workflow

```text
User Prompt
    ↓
LLM Chooses Tools
    ↓
Python Executes Tools
    ↓
Execution Log Stored
    ↓
Results Returned To LLM
    ↓
Conversational Final Response
```

---

# Example real agent output


=== FINAL RESPONSE ===

There are 1827 days between January 1st, 2020 and January 1st, 2025.
This calculation takes into account the leap years 2020 and 2024,
which added an extra day to the total count.


=== LOCAL EXECUTION LOG ===

[
    {
        'tool_name': 'has_leap_between',
        'tool_args': {
            'tuple_end_date': [2025, 1, 1],
            'tuple_start_date': [2020, 1, 1]
        },
        'result': True
    },

    {
        'tool_name': 'count_leap_years_between',
        'tool_args': {
            'tuple_end_date': [2025, 1, 1],
            'tuple_start_date': [2020, 1, 1]
        },
        'result': 2
    },

    {
        'tool_name': 'get_leap_years_between',
        'tool_args': {
            'tuple_end_date': [2025, 1, 1],
            'tuple_start_date': [2020, 1, 1]
        },
        'result': [2020, 2024]
    },

    {
        'tool_name': 'final_difference',
        'tool_args': {
            'tuple_end_date': [2025, 1, 1],
            'tuple_start_date': [2020, 1, 1]
        },
        'result': 1827
    }
]
```

---

# Concepts Explored

## Classical Deterministic Programming

* procedural decomposition
* helper functions
* date traversal
* state mutation
* leap year mathematics

## Agentic Software Engineering

* LLM tool calling
* orchestration prompting
* execution loops
* structured tool schemas
* execution logging
* conversational synthesis
* tool selection reasoning

---




---

# Technologies Used

* Python
* LangChain
* Groq API
* Llama 3.3 70B Versatile
* dotenv

---

# Notes

This project is intentionally experimental.

The goal was not only to solve date calculations, but also to compare and study the strengths and weaknesses of both architectures:


1-Traditional Deterministic Software
pros: cost-efficent
cons: non-adaptive

vs

2-LLM-driven Agent Orchestration
pros: creative, adaptive, 
cons: token cost via api subscriptions/local computation


---
