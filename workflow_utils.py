from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel

from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc

from clarifai_grpc.grpc.api.status import status_code_pb2


def text_input_workflow_call(input_text: str, clarif_ai_pat: str, user_id: str, app_id: str, workflow_id: str):
    PAT = clarif_ai_pat
    USER_ID = user_id

    APP_ID = app_id

    # Change these to whatever model and text URL you want to use

    WORKFLOW_ID = workflow_id

    channel = ClarifaiChannel.get_grpc_channel()

    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + PAT),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

    post_workflow_results_response = stub.PostWorkflowResults(

        service_pb2.PostWorkflowResultsRequest(

            user_app_id=userDataObject,

            workflow_id=WORKFLOW_ID,

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

    if post_workflow_results_response.status.code != status_code_pb2.SUCCESS:
        print(post_workflow_results_response.status)

        raise Exception("Post workflow results failed, status: " + post_workflow_results_response.status.description)

    # We'll get one WorkflowResult for each input we used above. Because of one input, we have here one WorkflowResult

    results = post_workflow_results_response.results[0]

    return results

