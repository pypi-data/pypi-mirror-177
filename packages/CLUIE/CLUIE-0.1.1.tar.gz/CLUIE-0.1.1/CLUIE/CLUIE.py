import resources.view_generator as vgen
import resources.models as models
from pynput import keyboard
import os
import cursor

class engine:
    def __init__(self, model, resolution, controlling_keys):
        self.settings = {
            'margin_left': 0,
            'margin_right': 0,
            'margin_top': 0,
            'margin_bottom': 0,
            'top_header': [],
            'bottom_footer': [],
            'pointer': '',
            'column_label_margin': 0,
            'row_entry_margin': 0,
            'list_scroll_margin': 1
        }

        self.submitted = []
        self.position = [0, 0]
        self.content = []
        self.content_ids = []
        self.columns = []

        try:
            self.canvas_width = int(resolution.split('x')[0])
            self.canvas_height = int(resolution.split('x')[1])
            self.view_anchor = 1
            os.system('mode ' + str(self.canvas_width+2) + ',' + str(self.canvas_height))
        except:
            print('CLUIE: Canvas resolution fetching error. Check if you typed it in following format [WIDTH]x[HEIGHT].')

        try:
            match model:
                case 'FramedList':
                    self.model = models.get_model(self, model)
        except:
            print('CLUIE: Model importing error. Make sure it\'s placed in the same folder and is properly prepared.')
        
        try:
            match controlling_keys:
                case 'WSADE':
                    self.key_up, self.key_down, self.key_left, self.key_right, self.key_submit = 'w', 's', 'a', 'd', 'Key.enter'
                case 'ARROWSE':
                    self.key_up, self.key_down, self.key_left, self.key_right, self.key_submit = 'Key.up', 'Key.down', 'Key.left', 'Key.right', 'Key.enter'
                case 'WSADS':
                    self.key_up, self.key_down, self.key_left, self.key_right, self.key_submit = 'w', 's', 'a', 'd', 'Key.space'
                case 'ARROWSS':
                    self.key_up, self.key_down, self.key_left, self.key_right, self.key_submit = 'Key.up', 'Key.down', 'Key.left', 'Key.right', 'Key.space'
                case _:
                    self.key_up = controlling_keys[0]
                    self.key_down = controlling_keys[1]
                    self.key_left = controlling_keys[2]
                    self.key_right = controlling_keys[3]
                    self.key_submit = controlling_keys[4]
        except:
            print('CLUIE: Controlling keys assign error. Check documentation for more information.')

    def save(self, name):
        with open((name if name[-5:] != '.menu' else name[:-5]) + '.menu', 'w') as save_menu:
            save_menu.write(str(self.canvas_width) + '\n')
            save_menu.write(str(self.canvas_height) + '\n')
            save_menu.write(str(self.settings) + '\n')
            save_menu.write(str(self.columns) + '\n')
            save_menu.write(str(self.column_widths) + '\n')
            save_menu.write(str(self.content) + '\n')
            save_menu.write(str(self.content_ids) + '\n')

    def load(self, name):
        with open((name if name[-5:] != '.menu' else name[:-5]) + '.menu', 'r') as load_menu:
            data = load_menu.readlines()
        exec('self.canvas_width = ' + str(data[0][:-1]))
        exec('self.canvas_height = ' + str(data[1][:-1]))
        exec('self.settings = ' + str(data[2][:-1]))
        exec('self.columns = ' + str(data[3][:-1]))
        exec('self.column_widths = ' + str(data[4][:-1]))
        exec('self.content = ' + str(data[5][:-1]))
        exec('self.content_ids = ' + str(data[6][:-1]))
        self.model = models.get_model(self, self.model['model_id'])
        os.system('mode ' + str(self.canvas_width+2+int(self.settings['margin_left']+self.settings['margin_right'])) + ',' + str(self.canvas_height+self.settings['margin_top']+self.settings['margin_bottom']))

    def display(self):
        listener = keyboard.Listener(on_press=self.on_press).start()
        vgen.update_canvas(None, self)
        cursor.hide()

    def configure(self, setting, value=None):
        if type(setting) == list:
            for i in setting:
                self.configure(i[0], i[1])
        elif value != None:
            if setting in self.settings.keys():
                self.settings[setting] = value
                match setting:
                    case 'margin_left'|'margin_right'|'margin_top'|'margin_bottom':
                        os.system('mode ' + str(self.canvas_width+2+int(self.settings['margin_left']+self.settings['margin_right'])) + ',' + str(self.canvas_height+self.settings['margin_top']+self.settings['margin_bottom']))
                self.model = models.get_model(self, self.model['model_id'])
            else:
                print('CLUIE: There is no such setting as ' + str(setting) + '. Check documentation for available settings to configure.')
        else:
            print('CLUIE: You cannot leave empty value.')

    def add_row(self, row, id=None):
        if type(row) == str:
            row = [row]
        if len(row) > len(self.columns):
            row = row[:len(self.columns)]
        elif len(row) < len(self.columns):
            for i in range(len(self.columns)-len(row)):
                row.append('')
        self.content_ids.append(id)
        self.content.append(list(map(str, row)))

    def add_column(self, name, width='auto'):
        if type(name) == list:
            for column in name:
                self.add_column(column[0], column[1] if len(column) > 1 else 'auto')
        else:
            if len(self.columns) == 0 or (0 not in models.calculate_widths(self, [name, width]) and 1 not in models.calculate_widths(self, [name, width]) and 2 not in models.calculate_widths(self, [name, width])):
                self.columns.append([name, width])
                self.model = models.get_model(self, self.model['model_id'])
                self.column_widths = models.calculate_widths(self)
            else:
                print('CLUIE: One column must be at least 3 units wide.')

    def await_submission(self):
        with keyboard.Events() as events:
            for event in events:
                if str(event.key) == self.key_submit:
                    break
        temp = self.submitted
        self.submitted = []
        return temp

    def on_press(self, key):
        key = str(key).replace('\'', '')
        pressed_key = None
        match key:
            case self.key_up: pressed_key = 'up'; self.position[1] -= 1
            case self.key_down: pressed_key = 'down'; self.position[1] += 1
            case self.key_left: pressed_key = 'left'; self.position[0] += 1
            case self.key_right: pressed_key = 'right'; self.position[0] -= 1
            case self.key_submit:
                if self.model['model_id'] == 'FramedList':
                    self.submitted = [self.content[self.position[1]], self.content_ids[self.position[1]]]
                pressed_key = 'submit'; self.position = [0, 0]; self.view_anchor = 1
        if pressed_key != None: vgen.update_canvas(pressed_key, self)