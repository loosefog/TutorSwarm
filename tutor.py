import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown


load_dotenv()
console = Console()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)
MODEL_NAME = os.getenv("LLM_MODEL", "deepseek-chat")

class AITutorSwarm:
    def __init__(self):
        self.workspace = "workspace_ts"
        if not os.path.exists(self.workspace):
            os.makedirs(self.workspace)
        self.context = {} 

    def call_llm(self, system_prompt, user_prompt, json_mode=False):
        try:
            params = {
                "model": MODEL_NAME,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            }
            # DeepSeek V3 官方 API 建议不用 json_mode 参数，直接在 Prompt 里强调
            response = client.chat.completions.create(**params)
            return response.choices[0].message.content
        except Exception as e:
            console.print(f"[red]LLM 调用失败: {e}[/red]")
            return None

    def agent_curriculum(self, topic):
        console.print(Panel(f"[bold blue]🎓 Curriculum Agent: 正在为 {topic} 设计大纲...[/bold blue]"))
        system = "你是一个资深技术课程设计师。请根据主题生成 3 个知识点。必须返回严格的 JSON 格式：{\"chapters\": [\"知识点1\", \"知识点2\", \"知识点3\"]}"
        res = self.call_llm(system, f"我想学 {topic}")
        if res and "```json" in res: res = res.split("```json")[1].split("```")[0]
        try:
            self.context['syllabus'] = json.loads(res)['chapters']
            console.print(f"[green]大纲已生成：{self.context['syllabus']}[/green]")
        except:
            console.print("[red]JSON 解析失败[/red]")

    def agent_instructor(self, chapter):
        console.print(Panel(f"[bold cyan]👩‍🏫 Instructor Agent: 正在讲解 {chapter}...[/bold cyan]"))
        content = self.call_llm("你是一个技术讲师。请用 Markdown 格式简短地解释概念。", f"讲解：{chapter}")
        console.print(Markdown(content))
        self.context['current_theory'] = content

    def agent_lab_engineer(self, chapter):
        console.print(Panel(f"[bold yellow]🛠️ Lab Agent: 正在生成练习题...[/bold yellow]"))
        code = self.call_llm("你是一个 TypeScript 出题人。输出带有 TODO 注释的 TS 代码练习。", f"针对 {chapter} 出题。")
        code = code.replace("```typescript", "").replace("```", "")
        filename = f"{self.workspace}/exercise.ts"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(code)
        return filename

    def agent_grader(self, filename):
        console.print(Panel("[bold magenta]🧐 Grader Agent: 正在检查...[/bold magenta]"))
        with open(filename, "r", encoding="utf-8") as f:
            user_code = f.read()
        feedback = self.call_llm("你是一个严格的 TS 代码审查员。只输出 PASS 或修改建议。", f"用户代码：{user_code}")
        console.print(Markdown(feedback))
        return "PASS" in feedback

    def run(self, topic="TypeScript"):
        self.agent_curriculum(topic)
        for chapter in self.context['syllabus']:
            console.rule(f"[bold red]开始学习: {chapter}[/bold red]")
            self.agent_instructor(chapter)
            file_path = self.agent_lab_engineer(chapter)
            input(f"\n>>> 请编辑 {file_path}，完成后按回车...")
            if self.agent_grader(file_path):
                console.print("[green]通过！[/green]")

if __name__ == "__main__":
    AITutorSwarm().run("TypeScript 基础类型")