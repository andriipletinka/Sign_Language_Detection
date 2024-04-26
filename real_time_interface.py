import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image, ImageDraw, ImageFont

letters = ['І', 'Ї', 'А', 'В', 'Д', 'И', 'К', 'Л', 'М', 'Н', 'О', 'Р', 'С', 'Т', 'У', 'Ю']
label_mapping = {index: letter for index, letter in enumerate(letters)}
model_path = 'resnet50v2_regularized.h5'
model = load_model(model_path)


def predict_on_frames(frames):
    frames_array = np.array(frames)

    frames_array = np.expand_dims(frames_array, axis=0)

    predictions = model.predict(frames_array)
    predicted_class = np.argmax(predictions, axis=1)

    predicted_letter = label_mapping[predicted_class[0]]

    return predicted_letter


cv2.namedWindow("Camera")
cap = cv2.VideoCapture(0)
font_path = 'SF-Pro-Rounded-Regular.ttf'
font = ImageFont.truetype(font_path, 24)


if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()
frames = []
frame_counter = 0
cooldown = 0
collect_frames = False
display_letters = []
message = " "
while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to read frame.")
        break

    if not collect_frames:
        cooldown += 1
        if cooldown % 3 == 0:
            message = f"Perform gesture in {round((45 - cooldown)/30, 2)} seconds."
        if cooldown > 45:
            cooldown = 0
            collect_frames = True
    else:
        message = f"Recording gesture."
        frame_counter += 1
        if frame_counter >= 5 and (frame_counter - 5) % 5 == 0:
            height, width = frame.shape[:2]
            min_dim = min(height, width)
            start_x = (width - min_dim) // 2
            start_y = (height - min_dim) // 2
            cropped_frame = frame[start_y:start_y + min_dim, start_x:start_x + min_dim]
            resized_frame = cv2.resize(cropped_frame, (360, 360), interpolation=cv2.INTER_LINEAR)
            resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            resized_frame = resized_frame / 255.0
            frames.append(resized_frame)

            if len(frames) == 12:
                display_letters.append(predict_on_frames(frames))
                frames = []
                frame_counter = 0
                collect_frames = False

    cv2_im_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_im = Image.fromarray(cv2_im_rgb)
    draw = ImageDraw.Draw(pil_im)
    size = draw.multiline_textbbox((50, 50), message + "\n" + ''.join(display_letters), font=font, spacing=10)
    draw.rectangle(size, fill="black", outline="black")
    draw.multiline_text(size, message + "\n" + ''.join(display_letters), fill=(255, 255, 255), font=font)
    frame_with_text = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
    cv2.imshow('Video', frame_with_text)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
