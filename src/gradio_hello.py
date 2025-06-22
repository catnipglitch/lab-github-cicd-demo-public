import gradio as gr

def hello():
    return "Hello world"

demo = gr.Interface(fn=hello, inputs=None, outputs="text", title="Hello World Demo")

if __name__ == "__main__":
    demo.launch()
