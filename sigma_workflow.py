from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel

from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc

from clarifai_grpc.grpc.api.status import status_code_pb2

from workflow_utils import text_input_workflow_call


def sigma_output(input_text: str, clarif_ai_pat):
    PAT = clarif_ai_pat
    USER_ID = 'bphigh'

    APP_ID = 'ai_world'

    # Change these to whatever model and text URL you want to use

    WORKFLOW_ID = 'sigma-workflow'

    try:

        results = text_input_workflow_call(input_text=input_text,clarif_ai_pat=PAT,user_id=USER_ID,app_id=APP_ID,
                                       workflow_id=WORKFLOW_ID)
    except Exception as e:
        print(f"Exception: {str(e)}")
        return "There has been an exception"

    image_base_64 = "Default"
    english_post = "Default"
    chinese_translation = "Default"
    arabic_translation = "Default"
    spanish_translation = "Default"

    for output in results.outputs:

        model = output.model

        if model.id == "GPT-4":
            english_post = output.data.text.raw

        elif model.id == "llama2-70b-chat":
            spanish_translation = output.data.text.raw

        elif model.id == "GPT-3_5-turbo":
            chinese_translation = output.data.text.raw

        elif model.id == "gpt-3_5-turbo-instruct":
            arabic_translation = output.data.text.raw



        else:
            pass

    return arabic_translation, chinese_translation, spanish_translation, english_post



