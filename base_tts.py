from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel

from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc

from clarifai_grpc.grpc.api.status import status_code_pb2
import base64
import re


def limit_string_to_500_characters(input_text: str):
    # Define a regular expression pattern to split text into sentences.
    sentence_pattern = r'(?<=[.!?])\s+'

    # Split the input text into sentences.
    sentences = re.split(sentence_pattern, input_text)

    # Initialize variables to track the character count and store valid sentences.
    char_count = 0
    valid_sentences = []

    for sentence in sentences:
        sentence_length = len(sentence)

        # Check if adding the current sentence would exceed the 500-character limit.
        if char_count + sentence_length <= 500:
            valid_sentences.append(sentence)
            char_count += sentence_length
        else:
            break  # Stop adding sentences when the limit is reached.

    # Join the valid sentences into a string.
    limited_text = ' '.join(valid_sentences)

    return limited_text


def convert_base64_to_bytes(base64_string: str):
    # Decode the Base64 string to bytes
    decoded_bytes = base64.b64decode(base64_string)

    return decoded_bytes


def base_tts_call(input_text: str, clarif_ai_pat: str):
    PAT = clarif_ai_pat
    USER_ID = 'eleven-labs'

    APP_ID = 'audio-generation'

    # Change these to whatever model and text URL you want to use

    MODEL_ID = 'speech-synthesis'

    MODEL_VERSION_ID = 'f588d92c044d4487a38c8f3d7a3b0eb2'

    channel = ClarifaiChannel.get_grpc_channel()

    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + PAT),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

    # To use a local text file, uncomment the following lines

    # with open(TEXT_FILE_LOCATION, "rb") as f:

    #    file_bytes = f.read()

    post_model_outputs_response = stub.PostModelOutputs(

        service_pb2.PostModelOutputsRequest(

            user_app_id=userDataObject,
            # The userDataObject is created in the overview and is required when using a PAT

            model_id=MODEL_ID,

            version_id=MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version

            inputs=[

                resources_pb2.Input(

                    data=resources_pb2.Data(

                        text=resources_pb2.Text(

                            raw=input_text


                        )

                    )

                )

            ]

        ),

        metadata=metadata

    )

    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        return "There has been an exception"

    # Since we have one input, one output will exist here

    output = post_model_outputs_response.outputs[0]

    base_64_audio = output.data.audio.base64

    return base_64_audio
