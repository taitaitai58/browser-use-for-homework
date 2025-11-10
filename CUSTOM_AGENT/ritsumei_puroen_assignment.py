"""
プロ演の課題を自動化するスクリプトです。
スクリプト概要とセットアップ:
0. OpenAI API Key を環境変数(.envファイル) `OPENAI_API_KEY` に設定する。
1. Ritsumeikan Rainbow のログイン情報を環境変数 `RITSUMEI_RAINBOW_ID` と `RITSUMEI_RAINBOW_PASSWORD` に設定する。
2. `uv` で Python 3.11 仮想環境を用意し、`uv sync` で Browser-Use と依存関係をインストールする。
3. スクリプト実行後、コンソール入力で「週番号」「課題番号」を指定すると、Agent が Rainbow にログインし、課題ファイルの保存・提出補助を自動実行する。
"""

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


dynamic_available_file_paths: list[str] = []


def _register_upload_whitelist(path: Path) -> None:
    absolute_path = str(path.resolve())
    original_path = str(path)

    if absolute_path not in dynamic_available_file_paths:
        dynamic_available_file_paths.append(absolute_path)

    if original_path and original_path not in dynamic_available_file_paths:
        dynamic_available_file_paths.append(original_path)

rainbow_id = os.environ.get("RITSUMEI_RAINBOW_ID")
rainbow_password = os.environ.get("RITSUMEI_RAINBOW_PASSWORD")


if not rainbow_id or not rainbow_password:
    raise RuntimeError(
        "Environment variables `RITSUMEI_RAINBOW_ID` and `RITSUMEI_RAINBOW_PASSWORD` must be set."
    )


class AssignmentFile(BaseModel):
    """Assignment file payload for saving homework output."""

    filename: str
    content: str


@controller.action('Save assignment file', param_model=AssignmentFile)
def save_assignment_file(params: AssignmentFile) -> ActionResult:
    """Persist the generated assignment program to disk and mark the workflow complete."""

    file_path = Path(params.filename).expanduser().resolve()
    file_path.parent.mkdir(parents=True, exist_ok=True)

    _register_upload_whitelist(file_path)

    if file_path.exists():
        existing_content = file_path.read_text(encoding='utf-8')
        if existing_content == params.content:
            return ActionResult(
                extracted_content=f"File `{file_path}` already exists with identical content.",
                is_done=False,
            )

    file_path.write_text(params.content, encoding='utf-8')

    return ActionResult(
        extracted_content=f"Saved file to `{file_path}`.",
        is_done=False,
    )


class AssignmentFileReference(BaseModel):
    """Assignment file locator for subsequent upload steps."""

    filename: str


@controller.action('Provide assignment file path', param_model=AssignmentFileReference)
def provide_assignment_file_path(params: AssignmentFileReference) -> ActionResult:
    """Return the absolute path of a previously saved assignment file for browser upload."""

    file_path = Path(params.filename).expanduser().resolve()

    if not file_path.exists():
        return ActionResult(
            extracted_content=f"File `{file_path}` does not exist. Save it before attempting to upload.",
            success=False,
            is_done=False,
        )

    _register_upload_whitelist(file_path)

    return ActionResult(
        extracted_content=(
            f"Assignment file is ready at `{file_path}`. "
            "Use the built-in `upload_file` action with this absolute path when the file input is focused."
        ),
        attachments=[str(file_path)],
        is_done=False,
    )


agent = Agent(
    task = (
    f"You are a university student completing your class assignment.\n"
    f"The assignment to complete is Week {week_index}, Task {assignment_number}.\n"
    "Follow the steps below:\n"
    "1. Access http://red.isprogex.is.ritsumei.ac.jp/Ctop/ and log in.\n"
    f"Input Rainbow ID `{rainbow_id}` and password `{rainbow_password}`, then submit the login form.\n"
    f"2. Navigate to the specified week by clicking the element "
    f"`<th class=\"week-index\"><a href=\"{week_index}\">{week_index}</a></th>`.\n"
    f"3. Click the element `<span class=\"butExerciseTitle\"><a href=\"\">{assignment_number}. 宿題基本</a></span>` "
    "to display the assignment details.\n"
    "The assignment is displayed inside an iframe, so either scroll through the iframe or inspect the DOM elements to fully understand its content.\n"
    "4. Review the assignment requirements, then call the custom tool `Save assignment file` "
    "to save the homework locally with the appropriate filename and program content.\n"
    "5. Call the custom tool `Provide assignment file path` using the same filename to retrieve the absolute path for upload.\n"
    "6. If the upload input is not visible, click the resubmission button (`再提出`) to enable file upload, then use the built-in `upload_file` action with the returned absolute path to attach the program file and submit the assignment.\n"
    "7. After submitting, verify that the uploaded program satisfies all assignment requirements; if any requirements are unmet, return to step 4 and repeat until everything is correct.\n"
    "8. Finally, provide a brief summary and end the task."
    ),
    llm=ChatOpenAI(model='gpt-5'),
    controller=controller,
    available_file_paths=dynamic_available_file_paths,
    llm_timeout=120,
)

agent.run_sync()

