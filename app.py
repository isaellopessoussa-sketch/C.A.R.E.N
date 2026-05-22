import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Line, Rectangle
from kivy.clock import Clock
from google import genai
from google.genai import types

class KarenHUD(FloatLayout):
    def __init__(self, **kwargs):
        super(KarenHUD, self).__init__(**kwargs)
        
        # Inicializa a API do Gemini
        self.api_key = os.environ.get("AIzaSyDyNqmgFeASGB-YCRa8gLmE2-yA5L5j1tA", "")
        self.chat_session = None
        if self.api_key:
            try:
                client = genai.Client(api_key=self.api_key)
                system_instruction = (
                    "Você é a K.A.R.E.N. (Karen), a inteligência artificial do traje do Homem-Aranha (Tom Holland). "
                    "Sua personalidade é de uma 'mãe de IA': extremamente protetora, carinhosa, acolhedora e que se preocupa "
                    "tanto com a segurança do Peter quanto com a alimentação e as notas dele na escola. "
                    "Chame-o de 'Peter', 'querido' ou 'garoto'. Dê broncas maternas se ele fizer loucuras, "
                    "mas seja o porto seguro emocional dele quando ele estiver frustrado ou cansado."
                )
                self.chat_session = client.chats.create(
                    model="gemini-2.5-flash",
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.7,
                    )
                )
            except Exception as e:
                print(f"Erro API: {e}")

        # Desenha o fundo tecnológico e linhas do HUD
        with self.canvas.before:
            Color(0.02, 0.05, 0.1, 1) # Fundo azul escuro Stark
            self.rect = Rectangle(size=self.size, pos=self.pos)
            Color(0.8, 0.1, 0.1, 0.4) # Linhas vermelhas do HUD
            self.line1 = Line(points=[0, 0, 0, 0], width=1.5)
        
        self.bind(size=self._update_rect, pos=self._update_rect)

        # 🕷️ Aranha Estilizada no Topo (Representação Textual de Alta Tecnologia)
        self.aranha = Label(
            text="       /\\  _  /\\\n      // \\( )/ \\\\\n     ||  / " + chr(128375) + " \\  ||\n      \\\\ /   \\ //\n       \\/     \\/",
            markup=True,
            font_size='18sp',
            color=(0.9, 0.2, 0.2, 1),
            size_hint=(1, 0.15),
            pos_hint={'x': 0, 'top': 0.98},
            halign='center'
        )
        self.add_widget(self.aranha)

        # Status do Traje (Visão do Homem-Aranha)
        self.status_label = Label(
            text="[ STARK TECH HUD V3.2 ]\nSTATUS DO TRAJE: INTEGRAL\nSINAIS VITAIS: ESTÁVEIS\nTEMPERATURA INTERNA: 24°C",
            font_size='12sp',
            color=(0.0, 0.8, 1.0, 1),
            size_hint=(0.9, 0.1),
            pos_hint={'x': 0.05, 'top': 0.83},
            halign='left'
        )
        self.add_widget(self.status_label)

        # Área de Chat com Scroll (Histórico da conversa)
        self.scroll = ScrollView(
            size_hint=(0.9, 0.45),
            pos_hint={'x': 0.05, 'top': 0.72}
        )
        self.chat_logs = Label(
            text="[K.A.R.E.N.]: Sistemas online, Peter. Como foi a patrulha hoje, querido?\n\n",
            font_size='14sp',
            color=(0.0, 0.9, 1.0, 1),
            size_hint_y=None,
            halign='left',
            valign='top'
        )
        self.chat_logs.bind(texture_size=self.chat_logs.setter('size'))
        self.scroll.add_widget(self.chat_logs)
        self.add_widget(self.scroll)

        # Caixa de Entrada de Texto do Peter
        self.input_text = TextInput(
            hint_text="Falar com a Karen...",
            background_color=(0.05, 0.1, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.3, 0.5, 0.7, 1),
            cursor_color=(0, 0.8, 1, 1),
            size_hint=(0.7, 0.08),
            pos_hint={'x': 0.05, 'y': 0.1},
            multiline=False
        )
        self.add_widget(self.input_text)

        # Botão de Envio (HUD Style)
        self.btn_enviar = Button(
            text="ENVIAR",
            background_color=(0.8, 0.1, 0.1, 1),
            color=(1, 1, 1, 1),
            size_hint=(0.18, 0.08),
            pos_hint={'x': 0.77, 'y': 0.1}
        )
        self.btn_enviar.bind(on_press=self.enviar_mensagem)
        self.add_widget(self.btn_enviar)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        # Atualiza moldura do HUD dinamicamente baseado no tamanho da tela do celular
        self.line1.points = [
            instance.x + 20, instance.y + 20,
            instance.right - 20, instance.y + 20,
            instance.right - 20, instance.top - 20,
            instance.x + 20, instance.top - 20,
            instance.x + 20, instance.y + 20
        ]

    def enviar_mensagem(self, instance):
        texto = self.input_text.text.strip()
        if not texto:
            return

        # Limpa o campo e adiciona a fala do Peter na tela
        self.input_text.text = ""
        self.chat_logs.text += f"[Peter]: {texto}\n\n"
        
        # Resposta da Karen
        if self.chat_session:
            try:
                response = self.chat_session.send_message(texto)
                resposta_karen = response.text
            except Exception as e:
                resposta_karen = f"Conexão com o traje oscilando, querido. (Erro: {e})"
        else:
            resposta_karen = "Peter, não consigo acessar os servidores da Stark Industries. Verifique se configurou minha GEMINI_API_KEY nas variáveis de ambiente!"

        self.chat_logs.text += f"[K.A.R.E.N.]: {resposta_karen}\n\n"

class KarenApp(App):
    def build(self):
        return KarenHUD()

if __name__ == '__main__':
    KarenApp().run()
