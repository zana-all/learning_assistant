from app.exceptions import ImageGenerationError
from google import genai
from google.genai import types
from google.genai.errors import ClientError

client = genai.Client()


def generate_image_from_prompt(prompt: str) -> str:
    try:
        response = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="16:9",
            ),
        )

        # image_bytes is base64 text in the SDK examples
        generated = response.generated_images[0]
        image_bytes = generated.image.image_bytes
        print(f"image_bytes: {image_bytes}")
        if not image_bytes:
            raise ImageGenerationError(message="No Image", status_code=502)

        return image_bytes
    except ClientError as e:
        status_code = getattr(e, "status_code", 400)
        message = str(e)
        raise ImageGenerationError(message=message, status_code=status_code) from e
