# Referece  - https://algomaster.io/learn/lld/decorator

"""
The Problem: Adding Features to a Text Renderer
Imagine you’re building a rich text rendering system (like a simple word processor or a markdown preview tool). At the core of your system is a TextView component that renders plain text on screen.

Soon, product requirements evolve:

You need to support bold text
Then italic text
Then underlined text
Then scrollable and bordered text containers
And possibly combinations of those (e.g., bold + italic + underlined)

"""

## Naive Approach

class TextView:

    def render(text):
        print(f"Rendering Plain {text}")
        return text
    

class BoldView:

    def render(text):
        bold_text = "<b>"+text+"</b>"
        return bold_text

class ItalicView:

    def render(text):
        italic_text = "<i>"+text+"</i>"
        return italic_text

class UnderlineView:

    def render(text):
        underline_text = "<u>"+text+"</u>"
        return underline_text
    
class StyleManager:
    def __init__(self, text):
        self.text = text
        self.bold = False
        self.italic = False
        self.underline = False

    def toggle_bold(self):
        self.bold = not self.bold

    def toggle_italic(self):
        self.italic = not self.italic

    def toggle_underline(self):
        self.underline = not self.underline

    def render(self):
        component = self.text

        if self.bold:
            component = BoldView.render(component)

        if self.italic:
            component = ItalicView.render(component)

        if self.underline:
            component = UnderlineView.render(component)

        return component


plain_text = TextView.render("Hello")

## Underline + Italic + Bold

bolder_text = BoldView.render(plain_text)
italic_bold_text = ItalicView.render(bolder_text)
underline_italic_bold_text = UnderlineView.render(italic_bold_text)


print("Underline + Italic + Bold - ",underline_italic_bold_text)

## Bold + Itaic

italic_text = ItalicView.render(plain_text)
bold_italic = BoldView.render(italic_text)

print("Bold + Italic - ",bold_italic)

#===============================================

text = TextView.render("Hello")
manager = StyleManager(text)

manager.toggle_bold()
print(manager.render())
# <b>Hello World</b>

manager.toggle_italic()
print(manager.render())
# <i><b>Hello World</b></i>

manager.toggle_underline()
print(manager.render())
# <u><i><b>Hello World</b></i></u>

manager.toggle_bold()   # turn BOLD OFF
print(manager.render())
# <u><i>Hello World</i></u>


t1 = TextView.render("Hello ")
t3 = UnderlineView.render(TextView.render("World"))
t2 = TextView.render("\nThis is ChatGPT")

print(t1)
print(t3)
print(t2)

## Draw Backs
"""
1. There is no Wrapping of objects, it's just a Text Transformation
2. It's not scalable (if need changes in text transformation, need to manually change in all implementation)
3. chances of Data Loss due to transformations

"""

#======================= Decorator Pattern ===================

"""
The Decorator Design Pattern is a structural pattern that lets you dynamically add new behavior or responsibilities to objects without modifying their underlying code.
"""

# Component Interface

from abc import ABC,abstractmethod

class TextView(ABC):

    @abstractmethod
    def render(self):
        pass

# Concrete Component

class PlainText(TextView):

    def __init__(self,text):

        self.text = text

    def render(self):

        return self.text

# BaseDecorator Component

class TextDecorator(TextView):

    def __init__(self,decorator):
        
        self.decorator = decorator

    def render(self):
        pass

class BoldView(TextDecorator):

    def __init__(self, decorator):
        
        super().__init__(decorator)
    
    def render(self):
        
        return f"<b>{self.decorator.render()}</b>"
    
class ItalicView(TextDecorator):

    def __init__(self, decorator):
        
        super().__init__(decorator)
    
    def render(self):
        
        return f"<i>{self.decorator.render()}</i>"
    
class UnderlineView(TextDecorator):

    def __init__(self, decorator):

        super().__init__(decorator)
    
    def render(self):

        return f"<u>{self.decorator.render()}</u>"

        
class TextRendererAppV1:

    def main():


        txt1 = PlainText("Hello")
        
        italic_bold = ItalicView(BoldView(txt1))
        print(f" Italic + Bold - {italic_bold.render()}")

        italic_underline = ItalicView(UnderlineView(txt1))
        print(f" Italic + Underline - {italic_underline.render()}")

        underline_bold_italic = UnderlineView(BoldView(ItalicView(txt1)))
        print(f"Underline + Bold + Italic - {underline_bold_italic.render()}")

if __name__ == "__main__":

    TextRendererAppV1.main()


#====================== Toggling Functionality ====================

class StateManager:

    def __init__(self,text):
        
        self.bold = False
        self.underline = False
        self.italic = False

        self.text = text
    
    def toggle_bold(self):

        self.bold = not self.bold

    def toggle_italic(self):

        self.italic = not self.italic

    def toggle_underline(self):

        self.underline = not self.underline

    def render(self):

        component = PlainText(self.text)

        if self.bold:

            component = BoldView(component)

        if self.italic:

            component = ItalicView(component)

        if self.underline:

            component = UnderlineView(component)
        
        return component.render()


class TextRendererAppV2:

    def main():


        state = StateManager("World")

        # Plain Text
        
        print(state.render())

        state.toggle_bold()

        state.toggle_italic()

        print(f"Italic + Bold - {state.render()}")

        state.toggle_bold()

        print(f"Italic + Bold Off - {state.render()}")
        
        state.toggle_bold()
        state.toggle_underline()

        print(f"Underline + Italic + Bold - {state.render()}")

        state.toggle_italic()

        print(f"Underline + Italic Off + Bold - {state.render()}")


        
if __name__ == "__main__":

    TextRendererAppV2.main()