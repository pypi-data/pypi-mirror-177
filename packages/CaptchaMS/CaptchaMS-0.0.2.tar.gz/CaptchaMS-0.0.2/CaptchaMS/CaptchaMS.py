from string import digits, ascii_letters
from random import randint, choice
from PIL import Image, ImageDraw, ImageFont


class Captcha:
    def __init__(self, count_ellipses: int = 50, count_lines: int = 5, font_path: str = 'NotoSans-Black.ttf',
                 background_color: tuple = (0, 0, 0, 0)):
        self.symbols = digits + ascii_letters
        self.text = self.random_text()
        self.count_ellipses = count_ellipses
        self.count_lines = count_lines
        self.font_path = font_path
        self.background_color = background_color # r g b a
        self.image = None

    def random_text(self):
        """ Text Generation"""
        text = ''
        for i in range(8):
            text += choice(self.symbols)
        return text

    def random_color(self):
        """ Color Generation"""
        color = ''
        for i in range(6):
            color += choice('ABCDEF0123456789')
        return '#' + color

    def random_ellipses(self, ):
        """ Ellipses Generation"""
        draw = ImageDraw.Draw(self.image)
        for i in range(self.count_ellipses):
            x = randint(10, 290)
            y = randint(10, 70)
            draw.ellipse((x, y, x + 5, y + 5), fill=self.random_color())

    def random_lines(self):
        """ Line Generation"""
        draw = ImageDraw.Draw(self.image)
        for i in range(self.count_lines):
            x1 = randint(10, 290)
            y1 = randint(10, 70)
            x2 = randint(10, 290)
            y2 = randint(10, 70)
            draw.line((x1, y1, x2, y2), width=4, fill=self.random_color())

    def generate(self):
        """ Generate captcha and random line """
        self.image = Image.new('RGBA', (300, 80), self.background_color)
        self.random_ellipses()

        px = -20
        py = -6
        const_y = py
        text_width, text_height = 50, 50

        for symbol in self.text:
            image_symbol = Image.new('RGBA', (text_width, text_height))
            draw2 = ImageDraw.Draw(image_symbol)
            draw2.text((0, 0), text=symbol, fill=self.random_color(), font=ImageFont.truetype(self.font_path, 39))

            image_symbol = image_symbol.rotate(randint(10, 40))

            rand_y = randint(3, 6)
            px, py = px + randint(30, 40), const_y + rand_y if randint(0, 1) == 1 else const_y - rand_y
            self.image.paste(image_symbol, (px, py, px + text_width, py + text_height), image_symbol)

        self.random_lines()

    def text(self):
        """ Returns captcha text """
        return self.text

    def show(self):
        """ Displays captcha """
        if self.image is None:
            self.generate()
        self.image.show()

    def save(self, fp):
        """ Saves the captcha """
        if self.image is None:
            self.generate()
        self.image.save(fp)
