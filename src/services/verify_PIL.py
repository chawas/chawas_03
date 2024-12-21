from PIL import Image

# Create a new image
image = Image.new('RGB', (100, 100), color = 'blue')
image.save('test_image.png')

print("Pillow is working correctly!")