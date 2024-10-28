import flet as ft
import openai
import webbrowser
import asyncio
from typing import Optional
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class DajareGenerator:
    def __init__(self):
        self.system_prompt = """
        あなたは優秀なダジャレ生成AIです。
        与えられたお題に関連する面白いダジャレを1つ生成してください。
        ダジャレは必ず日本語で、相手が理解しやすい形で出力してください。
        出力は「ダジャレ：」という接頭辞の後にダジャレ本文のみを出力してください。
        説明は不要です。
        """

    async def generate_dajare(self, theme: str) -> str:
        """
        OpenAI APIを使用してダジャレを生成する
        
        Args:
            theme (str): ダジャレのお題
            
        Returns:
            str: 生成されたダジャレ
            
        Raises:
            Exception: API呼び出しに失敗した場合
        """
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"お題：{theme}"}
                ]
            )
            return response.choices[0].message.content.replace("ダジャレ：", "").strip()
        except Exception as e:
            raise Exception(f"ダジャレの生成に失敗しました: {str(e)}")

class DajareApp:
    def __init__(self):
        self.generator = DajareGenerator()
        self.current_dajare: Optional[str] = None

    def main(self, page: ft.Page):
        """メインアプリケーションの設定と実行"""
        # ページ設定
        page.title = "AIダジャレジェネレーター"
        page.window_width = 400
        page.window_height = 500
        page.window_resizable = False
        page.theme_mode = ft.ThemeMode.LIGHT

        # UIコンポーネント
        title = ft.Text("AIダジャレジェネレーター", size=24, weight=ft.FontWeight.BOLD)
        theme_input = ft.TextField(
            label="お題",
            hint_text="お題を入力してください",
            width=300
        )
        result_text = ft.Text(
            size=16,
            width=300,
            text_align=ft.TextAlign.CENTER,
            selectable=True
        )
        loading = ft.ProgressRing(visible=False)

        async def generate_button_clicked(e):
            """ダジャレ生成ボタンのクリックハンドラー"""
            if not theme_input.value:
                result_text.value = "お題を入力してください"
                page.update()
                return

            try:
                loading.visible = True
                generate_button.disabled = True
                share_button.disabled = True
                page.update()

                self.current_dajare = await self.generator.generate_dajare(theme_input.value)
                result_text.value = self.current_dajare
                share_button.disabled = False

            except Exception as e:
                result_text.value = str(e)
                share_button.disabled = True

            finally:
                loading.visible = False
                generate_button.disabled = False
                page.update()

        def share_button_clicked(e):
            """シェアボタンのクリックハンドラー"""
            if self.current_dajare:
                tweet_text = f"AIが生成したダジャレ：\n{self.current_dajare}\n\n#AIダジャレ"
                url = f"https://twitter.com/intent/tweet?text={tweet_text}"
                webbrowser.open(url)

        # ボタン定義
        generate_button = ft.ElevatedButton(
            "ダジャレを生成",
            on_click=lambda e: asyncio.create_task(generate_button_clicked(e)),
            width=300
        )
        share_button = ft.ElevatedButton(
            "Xでシェア",
            on_click=share_button_clicked,
            width=300,
            disabled=True
        )

        # レイアウト構成
        page.add(
            ft.Column(
                controls=[
                    title,
                    theme_input,
                    generate_button,
                    loading,
                    ft.Text("結果：", size=16),
                    result_text,
                    share_button
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        )

if __name__ == "__main__":
    app = DajareApp()
    ft.app(target=app.main)