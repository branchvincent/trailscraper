from importlib import resources
from trailscraper.boto_service_definitions import service_definition_file, operation_definition


def test_should_find_most_recent_service_definition_file_for_ec2():
    botocore_data_dir = resources.files("botocore") / "data"
    expected_filename = botocore_data_dir / "ec2" / "2016-11-15" / "service-2.json.gz"

    assert service_definition_file("ec2") == str(expected_filename)


def test_should_find_operation_definitions():
    assert operation_definition("apigateway", "UpdateApiKey") == {
        "name": "UpdateApiKey",
        "http": {
            "method": "PATCH",
            "requestUri": "/apikeys/{api_Key}"
        },
        "input": {"shape": "UpdateApiKeyRequest"},
        "output": {"shape": "ApiKey"},
        "errors": [
            {"shape": "BadRequestException"},
            {"shape": "ConflictException"},
            {"shape": "LimitExceededException"},
            {"shape": "NotFoundException"},
            {"shape": "UnauthorizedException"},
            {"shape": "TooManyRequestsException"}
        ],
        "documentation": "<p>Changes information about an ApiKey resource.</p>"
    }
