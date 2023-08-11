import openai

openai.api_key = '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'

def refine_data(tag_list):
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You exclusively return a list of words. You are a image tag enhancer. Your job consists in refining the tags a computer vision system returns. All the images tha computer vision system was fed consist on photos from a chain of hotels spread all over Mexico. Your main focus is always to rewrite tags thinking of the hotel. Also you will have to return said list of words in mexican spanish."},
        {"role": "user", "content": f"{tag_list}  Be specific. Don't use words as cutlery or spoon. Rather if you see spoon try to infer soup."}
    ]
    )

    return completion.choices[0].message.get("content")


