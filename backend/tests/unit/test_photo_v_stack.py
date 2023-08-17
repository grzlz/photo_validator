import aws_cdk as core
import aws_cdk.assertions as assertions

from photo_v.photo_v_stack import PhotoVStack

# example tests. To run these tests, uncomment this file along with the example
# resource in photo_v/photo_v_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = PhotoVStack(app, "photo-v")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
