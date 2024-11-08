from google.cloud import vision
import openai
from PIL import Image

# Function to detect text from an image using Google Vision API
def detect_text_from_image(image_content):
    """يكتشف النص من محتوى الصورة ويعيد النصوص المستخرجة."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    if response.error.message:
        raise Exception(
            f"{response.error.message}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors"
        )
    return "\n".join([text.description for text in texts])

# Function to analyze text with GPT-4 and return the response
def analyze_text_with_gpt(page_text, page_number):
    """تحليل النص المستخرج من صفحة باستخدام ChatGPT وإرجاع الرد."""
    gpt_response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "  خليها كفتورة مختصرة بشكل مرتب ودقيق واذا كان فيه بيانات على شكل جدول ارسمها على شكل جدول"},
            {"role": "user", "content": f"الصفحة {page_number}:\n{page_text}"},
        ],
    )
    return gpt_response['choices'][0]['message']['content']