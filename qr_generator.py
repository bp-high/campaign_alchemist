import modal


def get_qr_image(qr_code_content: str, prompt: str):
    try:
        f = modal.Function.lookup("qr-generator", "main")
        output = f.call(qr_code_content, prompt)
        return output
    except Exception as e:
        return "Default"
