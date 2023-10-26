from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2


def moderate_text(text: str, moderation_threshold: int, clarif_ai_pat) -> tuple:
    CLARIFAI_PAT = clarif_ai_pat
    MODERATION_USER_ID = 'clarifai'
    MODERATION_APP_ID = 'main'
    # Change these to whatever model and text URL you want to use
    MODERATION_MODEL_ID = 'moderation-multilingual-text-classification'
    MODERATION_MODEL_VERSION_ID = '79c2248564b0465bb96265e0c239352b'

    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + CLARIFAI_PAT),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=MODERATION_USER_ID, app_id=MODERATION_APP_ID)

    # To use a local text file, uncomment the following lines
    # with open(TEXT_FILE_LOCATION, "rb") as f:
    #    file_bytes = f.read()

    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,
            # The userDataObject is created in the overview and is required when using a PAT
            model_id=MODERATION_MODEL_ID,
            version_id=MODERATION_MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            raw=text
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

    # Since we have one input, one output will exist here
    output = post_model_outputs_response.outputs[0]
    moderation_reasons = ""
    intervention_required = False
    for concept in output.data.concepts:
        if concept.value > moderation_threshold:
            moderation_reasons += concept.name + ","
            intervention_required = True

    return moderation_reasons, intervention_required
