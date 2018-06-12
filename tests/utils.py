import json

from openlobby.core.auth import create_access_token


def call_api(client, query, input=None, username=None):
    variables = json.dumps({"input": input or {}})
    if username is None:
        res = client.post("/graphql", {"query": query, "variables": variables})
    else:
        token = create_access_token(username)
        auth_header = "Bearer {}".format(token)
        res = client.post(
            "/graphql",
            {"query": query, "variables": variables},
            HTTP_AUTHORIZATION=auth_header,
        )
    return res.json()


def strip_value(data, *path):
    element = path[0]
    value = data.get(element)
    if len(path) == 1:
        data[element] = "__STRIPPED__"
        return value
    else:
        return strip_value(value, *path[1:])
