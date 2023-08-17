from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
    aws_lambda_python_alpha as _alambda,
    aws_apigateway as apigw,
    aws_iam as iam
)
from constructs import Construct

class PhotoValidatorStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api = apigw.RestApi(self, 'ImageTagAPI',
            rest_api_name='Image tagger',
            description='This service tags images.'
        )      
                
        tag_lambda = _alambda.PythonFunction(
            self, 'TagLambda',
            entry='./lambda',
            runtime=_lambda.Runtime.PYTHON_3_7,
            index='image_tagger.py',
            handler='handler'
        )


        tag_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=["rekognition:DetectLabels"],
                resources=["*"]
            )
        )

        resize_image = api.root.add_resource('getTag') # esto define un endpoint
        resize_image.add_method('POST', apigw.LambdaIntegration(tag_lambda)) # esto define el metodo de ese endpoint y la funcionalidad