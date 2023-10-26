from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel

from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc

from clarifai_grpc.grpc.api.status import status_code_pb2

from workflow_utils import text_input_workflow_call


def base_campaign_post_generator(product_description: str, clarif_ai_pat: str):
    USER_ID = 'bphigh'

    APP_ID = 'ai_world'

    # Change these to whatever model and text URL you want to use

    WORKFLOW_ID = 'workflow-0f7502'

    PAT = clarif_ai_pat

    try:

        results = text_input_workflow_call(input_text=product_description, clarif_ai_pat=PAT, user_id=USER_ID, app_id=APP_ID,
                                       workflow_id=WORKFLOW_ID)

    except Exception as e:
        print(f"Exception: {str(e)}")
        return "There has been an exception"

    for output in results.outputs:
        model = output.model

        if model.id == "GPT-4":
            final_result = output.data.text.raw
            return final_result


