from transformers import pipeline
import gradio as gr
import PyPDF2

# AI model
generator = pipeline("text-generation", model="gpt2")


# -------- CV TEXT EXTRACT --------


def extract_text_from_pdf(file):
    if file is None:
        return ""

    pdf_reader = PyPDF2.PdfReader(file)
    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text() or ""

    return text


# -------- CAREER BOT LOGIC --------
def career_bot(message, history, file):

    history = history or []

    # 📄 If CV uploaded
    if file is not None:
        try:
            import PyPDF2

            pdf_reader = PyPDF2.PdfReader(file)
            text = ""

            for page in pdf_reader.pages:
                text += page.extract_text() or ""

            reply = f"""📄 CV Analysis:

{text[:1000]}

💡 Suggestions:
- Add more projects
- Improve skills section
- Highlight achievements
- Use clean formatting
"""
        except Exception as e:
            reply = "❌ Error reading CV file."

    else:
        text = message.lower()

        if "ai engineer" in text:
            reply = "Learn Python → ML → Projects"

        elif "web developer" in text:
            reply = "Learn HTML, CSS, JS → React"

        else:
            result = generator(message, max_length=80)
            reply = result[0]["generated_text"]

    history.append((message, reply))
    return history, history

    # RULE-BASED CAREER RESPONSES
    if "ai engineer" in text:
        reply = """👨‍💻 AI Engineer Roadmap:
1. Python
2. Mathematics (basic linear algebra)
3. Machine Learning
4. Deep Learning
5. Projects + GitHub"""

    elif "web developer" in text:
        reply = """🌐 Web Developer Roadmap:
1. HTML, CSS
2. JavaScript
3. React
4. Backend (Node/Python)
5. Projects"""

    elif "beginner" in text:
        reply = "🎯 Start with Python basics + simple projects."

    elif "job" in text:
        reply = "💼 Focus on skills, portfolio, internships, and LinkedIn profile."

    else:
        result = generator(message, max_length=80)
        reply = result[0]["generated_text"]

    history.append((message, reply))
    return history, None


# -------- PROFESSIONAL UI --------
with gr.Blocks() as demo:

    gr.Markdown("# 🎓 AI Career Mentor Pro")
    gr.Markdown("Your smart AI assistant for career guidance, roadmap & CV analysis")

    # 🧑 Avatar section (simple professional feel)
    with gr.Row():
        gr.Image(
            "https://cdn-icons-png.flaticon.com/512/4712/4712027.png",
            width=120,
            height=120
        )
        gr.Markdown("""
        ### 👨‍💼 AI Career Mentor
        Ask me anything about your career, skills, or upload your CV for analysis.
        """)

    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Ask your career question...")
    file = gr.File(label="📄 Upload Your CV (PDF)")

    btn = gr.Button("Send")
    clear = gr.Button("Clear Chat")

    state = gr.State([])

    msg.submit(career_bot, [msg, chatbot, file], [chatbot, chatbot])
    btn.click(career_bot, [msg, chatbot, file], [chatbot, chatbot])

    clear.click(lambda: [], None, chatbot)

demo.launch(share=True)