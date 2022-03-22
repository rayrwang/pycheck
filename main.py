from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.graphics import *


class MyGrid(Widget):
    def on_touch_down(self, touch):
        print("down", touch)

    def on_touch_move(self, touch):
        print("move", touch)

    def on_touch_up(self, touch):
        print("up", touch)

    # def draw_lines(self):
    #     with self.canvas:
    #         Color(1., 0, 0)
    #         Rectangle(pos=(10, 10), size = (500, 500))


class CheckersAIApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    grid = CheckersAIApp().run()
