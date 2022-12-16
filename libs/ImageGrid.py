# Import the necessary libraries
import requests
from PIL import Image
from io import BytesIO
import os

dir_path = os.getcwd()

# Create a grid of four images
def create_image_grid(urlList):
  # Open the images using PIL
  image1 = Image.open(BytesIO(requests.get(urlList[0]).content))
  image2 = Image.open(BytesIO(requests.get(urlList[1]).content))
  image3 = Image.open(BytesIO(requests.get(urlList[2]).content))
  image4 = Image.open(BytesIO(requests.get(urlList[3]).content))

  # Get the width and height of the images
  width1, height1 = image1.size
  width2, height2 = image2.size
  width3, height3 = image3.size
  width4, height4 = image4.size

  # Calculate the maximum width and height of the images
  max_width = max(width1, width2, width3, width4)
  max_height = max(height1, height2, height3, height4)

  # Create an empty image with the maximum width and height
  grid_image = Image.new("RGB", (max_width * 2, max_height * 2))

  # Paste the images into the grid image
  grid_image.paste(image1, (0, 0))
  grid_image.paste(image2, (max_width, 0))
  grid_image.paste(image3, (0, max_height))
  grid_image.paste(image4, (max_width, max_height))

  # Save the resulting grid image
  grid_image.save(dir_path+"/cache/image_grid.jpg")
  return dir_path+"/cache/image_grid.jpg"