from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel

from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc

from clarifai_grpc.grpc.api.status import status_code_pb2

from workflow_utils import text_input_workflow_call


def spanish_translate(input_text: str, clarif_ai_pat):
    PAT = clarif_ai_pat
    USER_ID = 'bphigh'

    APP_ID = 'ai_world'

    # Change these to whatever model and text URL you want to use

    WORKFLOW_ID = 'spanish-speech-synth'

    try:

        results = text_input_workflow_call(input_text=input_text, clarif_ai_pat=PAT, user_id=USER_ID, app_id=APP_ID,
                                       workflow_id=WORKFLOW_ID)

    except Exception as e:
        print(f"Exception: {str(e)}")
        return "There has been an exception"

    spanish_translation = "Default"
    spanish_base64_audio = "Default"

    for output in results.outputs:

        model = output.model

        if model.id == "GPT-3_5-turbo":
            spanish_translation = output.data.text.raw

        elif model.id == "speech-synthesis":
            spanish_base64_audio = output.data.audio.base64

        else:
            pass

    return spanish_translation, spanish_base64_audio


def arabic_translate(input_text: str, clarif_ai_pat):
    PAT = clarif_ai_pat
    USER_ID = 'bphigh'

    APP_ID = 'ai_world'

    # Change these to whatever model and text URL you want to use

    WORKFLOW_ID = 'arabic-speech-synth'

    try:

        results = text_input_workflow_call(input_text=input_text, clarif_ai_pat=PAT, user_id=USER_ID, app_id=APP_ID,
                                       workflow_id=WORKFLOW_ID)

    except Exception as e:
        print(f"Exception: {str(e)}")
        return "There has been an exception"

    arabic_translation = "Default"
    arabic_base64_audio = "Default"

    for output in results.outputs:

        model = output.model

        if model.id == "GPT-3_5-turbo":
            arabic_translation = output.data.text.raw

        elif model.id == "speech-synthesis":
            arabic_base64_audio = output.data.audio.base64

        else:
            pass
    return arabic_translation, arabic_base64_audio


def chinese_translate(input_text: str, clarif_ai_pat):
    PAT = clarif_ai_pat
    USER_ID = 'bphigh'

    APP_ID = 'ai_world'

    # Change these to whatever model and text URL you want to use

    WORKFLOW_ID = 'chinese-speech-synth'

    try:

        results = text_input_workflow_call(input_text=input_text, clarif_ai_pat=PAT, user_id=USER_ID, app_id=APP_ID,
                                           workflow_id=WORKFLOW_ID)

    except Exception as e:
        print(f"Exception: {str(e)}")
        return "There has been an exception"

    chinese_translation = "Default"
    chinese_base64_audio = "Default"

    for output in results.outputs:

        model = output.model

        if model.id == "GPT-3_5-turbo":
            chinese_translation = output.data.text.raw

        elif model.id == "speech-synthesis":
            chinese_base64_audio = output.data.audio.base64

        else:
            pass
    return chinese_translation, chinese_base64_audio






