import gradio as gr
import ollama
import os


def get_available_models():
    try:
        models = ollama.list()
        if "models" in models:
            model_names = []
            for model in models["models"]:
                if "name" in model:
                    model_names.append(model["name"])
                elif "model" in model:
                    model_names.append(model["model"])
                else:
                    model_names.append(str(model))
            return model_names
        else:
            return []
    except Exception as e:
        print(f"Error while retrieving model list: {e}")
        return []

def export_chat_to_markdown(chat_history):
    md = ""
    for message in chat_history:
        if message["role"] == "user":
            md += f"**User:** {message['content']}\n\n"
        elif message["role"] == "assistant":
            md += f"**Assistant:** {message['content']}\n\n"
    return md


def get_next_chat_filename():
    files = os.listdir(os.getcwd())
    chat_numbers = []
    for file in files:
        if file.startswith("chat") and file.lower().endswith(".md"):
            try:
                number_str = file[4:-3]  
                number = int(number_str)
                chat_numbers.append(number)
            except:
                continue
    next_number = max(chat_numbers) + 1 if chat_numbers else 1
    return f"chat{next_number}.md"


def save_chat(chat_history):
    if not chat_history:
        return "No chat to save."
    try:
        file_name = get_next_chat_filename()
        file_path = os.path.join(os.getcwd(), file_name)
        md_text = export_chat_to_markdown(chat_history)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(md_text)
        return f"Chat successfully saved as {file_name}"
    except Exception as e:
        return f"Error during saving: {e}"


def chat_with_model(model_name, user_input, chat_history):
    if not user_input.strip():
        return chat_history, "", chat_history
    try:
        chat_history = chat_history.copy()
        chat_history.append({"role": "user", "content": user_input})
        response = ollama.chat(model=model_name, messages=[{"role": "user", "content": user_input}])
        response_text = response["message"]["content"]
        chat_history.append({"role": "assistant", "content": response_text})
        return chat_history, "", chat_history
    except Exception as e:
        chat_history.append({"role": "assistant", "content": f"Error: {e}"})
        return chat_history, "", chat_history


def new_chat():
    return [], []


custom_css = """
<style>
button {
    background-color: #007BFF !important;
    color: white !important;
    border: none !important;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1.2em !important;
}
button:hover {
    background-color: #0056b3 !important;
}
</style>
"""

with gr.Blocks(css=custom_css) as demo:
    gr.HTML(custom_css) 
    with gr.Row():

        with gr.Column(scale=1, min_width=250):
            gr.Markdown("## Settings")
            model_dropdown = gr.Dropdown(
                choices=get_available_models(),
                label="Select Model",
                value="llama3.2:3b",
                interactive=True,
                allow_custom_value=True
            )
            new_chat_button = gr.Button("New Chat")
            gr.Markdown("## Save Chat")
            save_button = gr.Button("Save Chat")
            save_status = gr.Textbox(label="Save Status", lines=2)
        
        with gr.Column(scale=3):
            chatbox_new = gr.Chatbot(label="Chat", height=800, type="messages")
            user_input = gr.Textbox(
                label="Enter your message",
                placeholder="Type your message here...",
                lines=2
            )
            send_button = gr.Button("Send")
    

    chat_state = gr.State([])
    

    new_chat_button.click(fn=new_chat, outputs=[chatbox_new, chat_state])
    

    send_button.click(
        fn=chat_with_model,
        inputs=[model_dropdown, user_input, chat_state],
        outputs=[chatbox_new, user_input, chat_state]
    )
    

    save_button.click(
        fn=save_chat,
        inputs=[chat_state],
        outputs=save_status
    )

demo.launch()



##   .----------------.  .----------------.  .----------------.  .----------------.   .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------. 
##  | .--------------. || .--------------. || .--------------. || .--------------. | | .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
##  | |   ______     | || |  _________   | || |  _______     | || |  ___  ____   | | | |     ______   | || |     _____    | || |  ___  ____   | || |     _____    | || |  ___  ____   | || |     ______   | || |     _____    | |
##  | |  |_   _ \    | || | |_   ___  |  | || | |_   __ \    | || | |_  ||_  _|  | | | |   .' ___  |  | || |    |_   _|   | || | |_  ||_  _|  | || |    |_   _|   | || | |_  ||_  _|  | || |   .' ___  |  | || |    |_   _|   | |
##  | |    | |_) |   | || |   | |_  \_|  | || |   | |__) |   | || |   | |_/ /    | | | |  / .'   \_|  | || |      | |     | || |   | |_/ /    | || |      | |     | || |   | |_/ /    | || |  / .'   \_|  | || |      | |     | |
##  | |    |  __'.   | || |   |  _|  _   | || |   |  __ /    | || |   |  __'.    | | | |  | |         | || |      | |     | || |   |  __'.    | || |      | |     | || |   |  __'.    | || |  | |         | || |      | |     | |
##  | |   _| |__) |  | || |  _| |___/ |  | || |  _| |  \ \_  | || |  _| |  \ \_  | | | |  \ `.___.'\  | || |     _| |_    | || |  _| |  \ \_  | || |     _| |_    | || |  _| |  \ \_  | || |  \ `.___.'\  | || |     _| |_    | |
##  | |  |_______/   | || | |_________|  | || | |____| |___| | || | |____||____| | | | |   `._____.'  | || |    |_____|   | || | |____||____| | || |    |_____|   | || | |____||____| | || |   `._____.'  | || |    |_____|   | |
##  | |              | || |              | || |              | || |              | | | |              | || |              | || |              | || |              | || |              | || |              | || |              | |
##  | '--------------' || '--------------' || '--------------' || '--------------' | | '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
##  '----------------'  '----------------'  '----------------'  '----------------'   '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 
