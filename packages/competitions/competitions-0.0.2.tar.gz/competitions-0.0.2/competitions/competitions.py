from datetime import datetime
from functools import partial

import gradio as gr

from . import AUTOTRAIN_BACKEND_API, AUTOTRAIN_TOKEN, AUTOTRAIN_USERNAME, COMPETITION_ID, competition_info
from .leaderboard import Leaderboard
from .submissions import Submissions
from .text import SUBMISSION_LIMIT_TEXT, SUBMISSION_TEXT


leaderboard = Leaderboard(
    end_date=competition_info.end_date,
    eval_higher_is_better=competition_info.eval_higher_is_better,
    competition_id=COMPETITION_ID,
    autotrain_token=AUTOTRAIN_TOKEN,
)

submissions = Submissions(
    competition_id=competition_info.competition_id,
    submission_limit=competition_info.submission_limit,
    end_date=competition_info.end_date,
    autotrain_username=AUTOTRAIN_USERNAME,
    autotrain_token=AUTOTRAIN_TOKEN,
    autotrain_backend_api=AUTOTRAIN_BACKEND_API,
)

with gr.Blocks() as demo:
    with gr.Tabs() as tab_container:
        with gr.TabItem("Overview", id="overview"):
            gr.Markdown(f"# Welcome to {competition_info.competition_name}! 👋")
            gr.Markdown(f"{competition_info.competition_description}")
            gr.Markdown("## Dataset")
            gr.Markdown(f"{competition_info.dataset_description}")
        with gr.TabItem("Public Leaderboard", id="public_leaderboard") as public_leaderboard:
            # fetch_lb = gr.Button("Fetch Leaderboard")
            output_df_public = gr.DataFrame()
            # fetch_lb_partial = partial(leaderboard.fetch, private=False)
            # fetch_lb.click(fn=fetch_lb_partial, outputs=[output_df])
        with gr.TabItem("Private Leaderboard", id="private_leaderboard"):
            current_date_time = datetime.now()
            if current_date_time >= competition_info.end_date:
                output_df = gr.DataFrame()
                fetch_lb_partial = partial(leaderboard.fetch, private=True)
                fetch_lb_partial(outputs=[output_df])
            else:
                gr.Markdown("Private Leaderboard will be available after the competition ends")
        with gr.TabItem("New Submission", id="new_submission"):
            gr.Markdown(SUBMISSION_TEXT)
            user_token = gr.Textbox(max_lines=1, value="hf_XXX", label="Please enter your Hugging Face token")
            uploaded_file = gr.File()
            output_text = gr.Markdown(visible=True, show_label=False)
            new_sub_button = gr.Button("Upload Submission")
            new_sub_button.click(
                fn=submissions.new_submission,
                inputs=[user_token, uploaded_file],
                outputs=[output_text],
            )
        with gr.TabItem("My Submissions", id="my_submissions"):
            gr.Markdown(SUBMISSION_LIMIT_TEXT)
            user_token = gr.Textbox(max_lines=1, value="hf_XXX", label="Please enter your Hugging Face token")
            output_text = gr.Markdown(visible=True, show_label=False)
            output_df = gr.DataFrame(visible=False)
            my_subs_button = gr.Button("Fetch Submissions")
            my_subs_button.click(
                fn=submissions.my_submissions,
                inputs=[user_token],
                outputs=[output_text, output_df],
            )

        fetch_lb_partial = partial(leaderboard.fetch, private=False)
        public_leaderboard.select(fetch_lb_partial, inputs=[], outputs=[output_df_public])
