**Typescriptlearner**
An Agentic Engineering experiment: A multi-agent system that acts as a personalized technical tutor.
This project demonstrates an automated learning pipeline driven by **5 heterogeneous AI agents**, showcasing system decomposition, human-in-the-loop (HITL) workflows, and prompt engineering.

**Architecture**
This system implements a modular pipeline where each agent has a specialized role:
1. Curriculum Architect: Decomposes complex topics into a structured, learnable syllabus.
2. Theory Instructor: Generates personalized Markdown lessons with clear examples.
3. Lab Engineer: Automatically creates interactive TypeScript practice exercises with TODOs.
4. QA Grader: Performs static analysis and provides constructive feedback on user code.
5. Knowledge Librarian: Summarizes lessons and compiles a professional `notebook.md` for long-term retention.

**get ready to learn!**
first，Setup Environment:
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Install dependencies:
pip install -r requirements.txt
```
next，Configure API Keys:
```bash
Create a .env file in the root directory:
OPENAI_API_KEY=your_deepseek_or_openai_key
OPENAI_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-chat
```
finally，Run the Tutor:
```bash
python tutor.py
```

**Engineering Highlights**
Model Agnostic Design: Configurable via .env to seamlessly switch between OpenAI, DeepSeek, or local LLMs.
Agentic Orchestration: Uses rich for visualization and JSON Mode for robust inter-agent communication.
Human-in-the-loop (HITL): Intentionally introduces manual coding steps to balance automation with deep learning practice.
Error Robustness: Built with defensive programming practices, including JSON cleaning and recursive retry mechanisms to handle LLM non-determinism.

❤️ Built by a curious engineer exploring the future of AI-native software.
