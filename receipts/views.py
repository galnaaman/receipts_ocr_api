from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views
from rest_framework.response import Response
from .models import Receipt
from .serializers import ReceiptSerializer
from PIL import Image, ImageEnhance
import pytesseract

class ReceiptUploadView(views.APIView):
    @swagger_auto_schema(
        request_body=ReceiptSerializer,
        responses={200: ReceiptSerializer()}
    )
    def post(self, request, *args, **kwargs):
        serializer = ReceiptSerializer(data=request.data)
        if serializer.is_valid():
            receipt = serializer.save()

            # Process the image and extract text
            processed_data = self.process_receipt(receipt.image.path)
            receipt.processed_data = processed_data
            receipt.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def process_receipt(self, image_path):
        # Open the image
        img = Image.open(image_path)

        # Convert to grayscale
        img = img.convert('L')

        # Increase contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)

        # Apply a binary threshold to increase sharpness
        img = img.point(lambda x: 0 if x < 128 else 255, '1')

        # Use Tesseract to do OCR on the image with Hebrew language
        text = pytesseract.image_to_string(img, lang='heb')
        print("OCR Text Output:", text)  # Debugging purpose

        # Parse the text to extract product names and prices
        parsed_data = self.parse_receipt_text(text)
        return parsed_data

    def parse_receipt_text(self, text):
        lines = text.splitlines()
        products = []

        for line in lines:
            # This example assumes a simple format. You need to customize the parsing logic as per the receipt format.
            parts = line.split(' ')
            if len(parts) >= 2 and any(char.isdigit() for char in parts[-1]):
                product_name = ' '.join(parts[:-1])
                price = parts[-1]
                products.append({
                    "product_name": product_name,
                    "price": price,
                })

        return {"products": products}
