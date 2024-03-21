import flet as ft
import aiohttp
import uvicorn

base_url = "http://localhost:8000"

class TodoApp(ft.UserControl):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.tasks = []
        self.tasks_display = None  # Definindo tasks_display como None inicialmente


    async def load_tasks(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/tasks/") as response:
                self.tasks = await response.json()
        await self.update_async()

    async def add_task(self, task_name):
        async with aiohttp.ClientSession() as session:
            payload = {"task_name": task_name}
            async with session.post(f"{self.base_url}/tasks/", json=payload) as response:
                if response.status == 200:
                    self.tasks.append(await response.json())
                    await self.load_tasks()

    async def delete_task(self, task_id):
        async with aiohttp.ClientSession() as session:
            async with session.delete(f"{self.base_url}/tasks/{task_id}") as response:
                if response.status == 200:
                    await self.load_tasks()

    async def update_task(self, task_id, completed):
        async with aiohttp.ClientSession() as session:
            payload = {"completed": completed}
            async with session.put(f"{self.base_url}/tasks/{task_id}", json=payload) as response:
                if response.status == 200:
                    await self.load_tasks()

    def build(self):
        self.new_task = ft.TextField(
            hint_text="O que precisa ser feito?", on_submit=self.add_clicked, expand=True
        )
        self.tasks_display = ft.Column()
        return ft.Column(
            width=600,
            controls=[
                ft.Row(
                    [ft.Text(value="Lembretes", style=ft.TextThemeStyle.HEADLINE_MEDIUM)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    controls=[
                        self.new_task,
                        ft.FloatingActionButton(
                            icon=ft.icons.ADD, on_click=self.add_clicked
                        ),
                    ],
                ),
                self.tasks_display,
            ],
        )

    async def add_clicked(self, e):
        if self.new_task.value:
            await self.add_task(self.new_task.value)
            self.new_task.value = ""

    async def task_checkbox_changed(self, task_id, value):
        await self.update_task(task_id, value)

    async def task_delete_clicked(self, task_id):
        await self.delete_task(task_id)

    async def update_async(self):
        self.tasks_display.controls = []
        for idx, task in enumerate(self.tasks):
            checkbox = ft.Checkbox(
                value=task["completed"], label=task["task_name"], on_change=lambda e, idx=idx: self.task_checkbox_changed(idx, e)
            )
            delete_button = ft.IconButton(
                ft.icons.DELETE_OUTLINE, tooltip="Deletar", on_click=lambda e, idx=idx: self.task_delete_clicked(idx)
            )
            self.tasks_display.controls.append(ft.Row(controls=[checkbox, delete_button]))


async def main(page: ft.Page):
    base_url = "http://localhost:8000"  # Update with your FastAPI server URL
    page.title = "Agenda de Lembretes"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    todo_app = TodoApp(base_url)
    await todo_app.load_tasks()
    await page.add_async(todo_app)


ft.app(main)
