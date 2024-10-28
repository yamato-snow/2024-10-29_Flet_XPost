import flet as ft
from openai import OpenAI
import webbrowser
from dotenv import load_dotenv
import os

# 環境変数の読み込み
load_dotenv()

class DajareGenerator:
    def __init__(self):
        # OpenAI clientの初期化
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def generate_dajare(self, theme):
        # GPT-4を使用してダジャレを生成
        prompt = f"""
        以下のお題に関連したダジャレを1つ考えてください。
        お題: {theme}
        
        ダジャレは1行で、シンプルに返してください。
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content.strip()

def main(page: ft.Page):
    # ページ設定
    page.title = "AIダジャレジェネレーター"
    page.window_width = 400
    page.window_height = 500
    page.padding = 20

    # ジェネレーターの初期化
    generator = DajareGenerator()

    # UIコンポーネント
    title = ft.Text("AIダジャレジェネレーター", size=24, weight=ft.FontWeight.BOLD)
    theme_input = ft.TextField(
        label="お題",
        hint_text="ダジャレのお題を入力してください",
        width=360
    )
    result_text = ft.TextField(
        label="生成結果",
        read_only=True,
        multiline=True,
        min_lines=2,
        width=360
    )

    # ダジャレ生成処理
    def generate_clicked(e):
        if theme_input.value:
            # ボタンを無効化して処理中表示
            generate_btn.disabled = True
            generate_btn.text = "生成中..."
            page.update()
            
            try:
                # ダジャレの生成
                result = generator.generate_dajare(theme_input.value)
                result_text.value = result
                # シェアボタンを有効化
                share_btn.disabled = False
            except Exception as err:
                result_text.value = f"エラーが発生しました: {str(err)}"
            finally:
                # ボタンを元に戻す
                generate_btn.disabled = False
                generate_btn.text = "ダジャレを生成"
                page.update()

    # Xでシェア
    def share_clicked(e):
        if result_text.value:
            tweet_text = f"【AIが考えたダジャレ】\n{result_text.value}\n\nお題: {theme_input.value}\n#AIダジャレ"
            url = f"https://twitter.com/intent/tweet?text={tweet_text}"
            webbrowser.open(url)

    # ボタンの作成
    generate_btn = ft.ElevatedButton(
        text="ダジャレを生成",
        width=360,
        on_click=generate_clicked
    )
    
    share_btn = ft.ElevatedButton(
        text="Xでシェア",
        width=360,
        on_click=share_clicked,
        disabled=True  # 初期状態は無効
    )

    # レイアウトの構築
    page.add(
        ft.Column(
            controls=[
                title,
                ft.Container(height=20),
                theme_input,
                ft.Container(height=10),
                generate_btn,
                ft.Container(height=20),
                result_text,
                ft.Container(height=10),
                share_btn
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.START
        )
    )

if __name__ == '__main__':
    ft.app(target=main)