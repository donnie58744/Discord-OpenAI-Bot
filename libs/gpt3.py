import openai
from urllib.request import urlopen

openai.organization = "YOUR_ORG_IDI"
openai.api_key = "YOUR_API_KEY"

pictureDims="1024x1024"

def imgPrompt(input):
    try:
        imageList = []
        image_resp = openai.Image.create(prompt=str(input), n=4, size=pictureDims)
        for x in image_resp['data']:
            imageList.append(x["url"])
        return imageList
    except openai.InvalidRequestError as e:
        return 'pornblocker'

def imgVariation(imgUrl):
    imageList = []
    response = openai.Image.create_variation(
        image=urlopen(imgUrl),
        n=4,
        size=pictureDims
    )

    for x in response['data']:
        imageList.append(x["url"])
    return imageList

def textPrompt(input):
    try:
        resp = openai.Completion.create(
            model="text-davinci-003",
            prompt=input,
            max_tokens=4000,
            temperature=0
        )
        return(resp["choices"][0]["text"])
    except openai.InvalidRequestError as e:
        return 'badprompt'
    except Exception as e:
        return 'trialEnd'