from dotenv import load_dotenv

import os
from pathlib import Path

from browser_use import Agent, Browser, ChatOpenAI, Controller
from browser_use.agent.views import ActionResult
from pydantic import BaseModel


load_dotenv()


controller = Controller()


week_index = input("週番号を入力してください: ").strip()
assignment_number = input("課題番号を入力してください: ").strip()



rainbow_id = os.environ.get("RITSUMEI_RAINBOW_ID")
rainbow_password = os.environ.get("RITSUMEI_RAINBOW_PASSWORD")


if not rainbow_id or not rainbow_password:
    raise RuntimeError(
        "Environment variables `RITSUMEI_RAINBOW_ID` and `RITSUMEI_RAINBOW_PASSWORD` must be set."
    )


agent = Agent(
    task = (
    f"You are a university student completing Week {week_index}, Task {assignment_number} of your course assignment.\n"
    "Always reason step by step, document key findings, and return structured answers.\n"
    "Follow this workflow:\n"
    f"1. Access http://red.isprogex.is.ritsumei.ac.jp/Ctop/ and log in by entering Rainbow ID `{rainbow_id}` and password `{rainbow_password}`, then submit the login form.\n"
    f"2. Navigate to the specified week by clicking `<th class=\"week-index\"><a href=\"{week_index}\">{week_index}</a></th>` and open the assignment by clicking `<span class=\"butExerciseTitle\"><a href=\"\">{assignment_number}. 宿題穴埋</a></span>`.\n"
    "3. Once on the assignment page, capture and understand the complete problem statement and save it with `write_file` so it can be referenced later.\n"
    "4. Identify every answer field (`input` and `textarea`) that requires a value. For each one, analyze the necessary logic or snippet needed—answers may not align perfectly with whole instructions or code blocks, and braces `}` might fall outside the field so a block may remain open—stay flexible and record your reasoning to a file (reuse or append to the same file if convenient). Note that the feedback `div` inside the same `<span>` simply switches class between `result correct` and `result incorrect`—there is no text message inside, so rely on the class change when recording outcomes. When code outside the input field interferes with your solution, you may use `continue`, `break`, `return`, `longjmp`/`setjmp`, or other control flow statements as needed. Approach the problem with flexible thinking.\n"
    "5. Update fields one at a time. Before each change, review the saved context and current page state, then generate the specific answer and apply it to the corresponding `input` or `textarea`. Do not batch-fill all fields at once.\n"
    "6. After all fields have been populated, press the `採点` button to grade the submission, then wait 10 seconds before inspecting the results.\n"
    "7. If any results remain incorrect, pause to re-read the full assignment description. With the current inputs and captured snippets, mentally stitch together the program as a whole to understand how the pieces combine, identify every spot that needs revision, and record those insights. Then review the feedback `div` inside the same `<span>` (its class will be `result incorrect`), adjust the targeted field(s) one by one based on that refreshed understanding, grade again, and repeat until every feedback `div` has the class `result correct`.\n"
    "8. When grading succeeds, provide a concise summary that references the saved notes and highlights the final corrections made, then end the task."
    ),
    llm=ChatOpenAI(model='gpt-5'),
    controller=controller,
    llm_timeout=180,
)



agent.run_sync()