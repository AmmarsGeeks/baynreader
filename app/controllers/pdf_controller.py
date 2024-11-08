import os
from PIL import Image
import fitz
from app.models.text_analysis import detect_text_from_image, analyze_text_with_gpt

# def process_page_sequentially(doc_path, num_pages):
#     # Create a folder named after the PDF file in app/results
#     file_name = os.path.basename(doc_path).split('.')[0]
#     result_folder = os.path.join("app/results", file_name)
#     os.makedirs(result_folder, exist_ok=True)

#     # Copy the PDF to the result folder
#     result_pdf_path = os.path.join(result_folder, f"{file_name}.pdf")
#     os.rename(doc_path, result_pdf_path)

#     return_dict = {}

#     # Process each page sequentially
#     doc = fitz.open(result_pdf_path)
#     for page_num in range(num_pages):
#         page = doc[page_num]
#         pix = page.get_pixmap()

#         # Save each page as a PNG image
#         img_path = os.path.join(result_folder, f"page_{page_num + 1}.png")
#         img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#         img.save(img_path)

#         # Detect text from image
#         with open(img_path, "rb") as img_file:
#             image_content = img_file.read()
#             page_text = detect_text_from_image(image_content)

#         # Analyze text with GPT
#         page_response = analyze_text_with_gpt(page_text, page_num + 1)
#         return_dict[page_num] = page_response

#     doc.close()
#     return return_dict


def process_page_sequentially(doc_path, num_pages):
    """معالجة الصفحات واحدة تلو الأخرى."""
    doc = fitz.open(doc_path)
    return_dict = {}
    
    for page_num in range(num_pages):
        page = doc[page_num]
        pix = page.get_pixmap()
        
        # تحويل الصورة إلى صيغة PIL لمعالجة Google Vision API
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.save(f"temp_image_{page_num}.jpg")
        
        # قراءة الصورة المؤقتة وتحليل النص
        with open(f"temp_image_{page_num}.jpg", "rb") as img_file:
            image_content = img_file.read()
            page_text = detect_text_from_image(image_content)
        
        # إرسال النص المستخرج من الصفحة إلى ChatGPT وتخزين الرد
        page_response = analyze_text_with_gpt(page_text, page_num + 1)
        return_dict[page_num] = page_response
        
        # حذف الصورة المؤقتة
        os.remove(f"temp_image_{page_num}.jpg")
        
    doc.close()
    return return_dict