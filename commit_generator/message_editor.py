from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import get_app

class MessageEditor:
    def capture_multiline_input(self, prompt_message, initial_message=""):
        bindings = KeyBindings()

        @bindings.add('c-d')
        def _(event):
            event.app.exit(result=event.app.current_buffer.text)

        input_message = prompt(prompt_message, multiline=True, key_bindings=bindings, default=initial_message)
        return input_message
