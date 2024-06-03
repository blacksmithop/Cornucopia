from time import sleep


def simulate_streaming(text: str, obj_ref) -> object:
    full_response = ""

    for chunk in text.split():
        full_response += chunk + " "
        sleep(0.05)
        # Add a blinking cursor to simulate typing
        yield obj_ref.markdown(full_response + "▌")
