import textwrap

from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from play_ground.test_gpt import create_test_scenario, convert_test_case, get_json_agent, create_user_story


# Create your views here.
def home(request):
    return render(request, 'play_ground/home.html')


def ask_document(request):
    return render(request, 'play_ground/ask_document.html')


def user_story(request):
    return render(request, 'play_ground/user_story.html')


def test_scenario(request):
    return render(request, 'play_ground/test_scenario.html')


def test_script(request):
    return render(request, 'play_ground/test_script.html')


@csrf_exempt
@require_http_methods(["POST"])
def test_gpt(request):
    # Parse request body
    data = json.loads(request.body)
    usage = data["usage"]
    if usage == "create_test_scenario":
        res = create_test_scenario(data["content"])
    elif usage == "convert_test_case":
        res = convert_test_case(data["content"])
    elif usage == "create_user_story":
        res = create_user_story(data["content"])
    else:
        res = "Unsupported usage"
    res = textwrap.dedent(res).strip()
    # print(textwrap.dedent(res).strip())
    return HttpResponse(res)


@csrf_exempt
@require_http_methods(["POST"])
def test_agent(request):
    data = json.loads(request.body)
    #    file_path = data["path"]
    question = data["question"]
    agent = get_json_agent("/Users/buddy/PycharmProjects/test_AI/resource/cds_banking.yaml")
    agent.handle_parsing_errors = True
    output = agent.run(question)

    return HttpResponse(output)
