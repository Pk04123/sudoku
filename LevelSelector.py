from cmu_graphics import *

class SelectorButton:
    def __init__(self, x, y, text, color):
        self.cx = x
        self.cy = y
        self.width = 100
        self.height = 60
        self.fill = color
        self.text = text

def LevelSelector_onScreenActivate(app):
    app.levelList = ['easy', 'medium', 'hard', 'expert', 'evil']
    app.level = None
    app.easy = SelectorButton(0.5 * app.width / 5, app.height / 2, 
                              'easy', 'cyan')
    app.medium = SelectorButton(1.5 * app.width / 5, app.height / 2, 
                                'medium', 'green')
    app.hard = SelectorButton(2.5 * app.width / 5, app.height / 2, 
                              'hard', 'yellow')
    app.expert = SelectorButton(3.5 * app.width / 5, app.height / 2,
                                'expert', 'orange')
    app.evil = SelectorButton(4.5 * app.width / 5, app.height / 2,
                              'evil', 'red')
    app.buttons = (app.easy, app.medium, app.hard, app.expert, app.evil)

#fonts taken from https://academy.cs.cmu.edu/docs/label
def LevelSelector_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill = 'lightCyan')
    drawLabel('SUDOKU LEVEL SELECTOR', 
              app.width / 2, 50, bold = True, size = 30, font = 'monospace')
    drawLabel('Choose the difficulty level by clicking on one of the buttons',
              app.width / 2, (app.height / 2) - 150, size = 24)
    drawLabel('Enjoy!', app.width / 2, app.height / 2 + 200, size = 30, font = 'cursive')
        
    for button in app.buttons:
        drawRect(button.cx, button.cy, button.width, button.height,
                 fill = button.fill, align = 'center', border = 'black')
        drawLabel(button.text, button.cx, button.cy, size = 20, font = 'cursive',
                  bold = True)


def LevelSelector_onMousePress(app, mouseX, mouseY):
    for button in app.buttons:
        if (button.cx - button.width / 2 <= mouseX <= button.cx + button.width / 2 and
            button.cy - button.height / 2 <= mouseY <= button.cy + button.height / 2):
            app.level = button.text
            setActiveScreen('Sudoku')