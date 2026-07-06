import cv2

#Load the image
image = cv2.imread('/Users/gurpreetsingh/Documents/AI/Computer Vision/f.jpg')

#Convert the image to grayscale

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#Resize the grayscale image to 224x224

resized_image = cv2.resize(gray_image, (224, 300))

#Display the resized grayscale image in a single window

cv2.imshow("Processed Image", resized_image)

#Wait for key press

key = cv2.waitKey(0) #Wait indefinetly for a key press

#Check if the "s" key was pressed (ASCII for "s" is 83)

if key == ord('s'):
    #Save the processed image when "s" is pressed
    cv2.imwrite('grayscale_resized_image.jpg', resized_image)

    print("Image saved as grayscale_resized_image.jpg")

else:
    print("Image not saved.")

#Close the window

cv2.destroyAllWindows()

#Print processed image properties

print(f"Processed image dimensions: {resized_image.shape}")