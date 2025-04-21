import os
import re
import uuid
import base64
from django.conf import settings

def save_base64_images_from_content(content: str) -> str:
    os.makedirs(os.path.join(settings.MEDIA_ROOT, 'notes'), exist_ok=True)

    pattern = r'<img src="data:(image/\w+);base64,([^"]+)">'
    matches = re.findall(pattern, content)

    for mime_type, b64data in matches:
        extension = mime_type.split('/')[-1]
        filename = f"{uuid.uuid4()}.{extension}"
        file_path = os.path.join(settings.MEDIA_ROOT, 'notes', filename)

        with open(file_path, 'wb') as f:
            f.write(base64.b64decode(b64data))

        new_src = f'{settings.DOMAIN}/media/notes/{filename}'
        content = content.replace(f'data:{mime_type};base64,{b64data}', new_src)

    return content
