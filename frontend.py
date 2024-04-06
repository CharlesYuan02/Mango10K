import gradio as gr
from query import chatbot
from dotenv import load_dotenv

def main(message, history, ticker):
    load_dotenv()
    output = chatbot(ticker, message)
    return output

gr.ChatInterface(
    main,
    additional_inputs=[gr.Textbox(placeholder="Type your ticker here...", label="Ticker")],
    retry_btn=None,
    undo_btn=None,
).launch()