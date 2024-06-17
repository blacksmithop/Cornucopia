import base64


def encode_image(image_ptr):
    image_base64 = base64.b64encode(image_ptr.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{image_base64}"
