
# Ukrainian Sign Language Detection
This project focuses on translating Ukrainian Sign Language into text using advanced machine learning models. The real-time interface processes camera feed and provides textual representations of Ukrainian Sign Language gestures(in our case letters).

![image](https://github.com/andriipletinka/Sign_Language_Detection/assets/93386415/466d22d2-e597-412c-b191-829caeac53c4)

![ScreenRecording2024-05-18at10 08 49PMonline-video-cutter com-ezgif com-video-to-gif-converter (1)](https://github.com/andriipletinka/Sign_Language_Detection/assets/92575176/41715f34-19eb-421c-9e37-4d23d6bd4df3)
## Data Description

- **Total Videos:** 638
- **Duration:** Each video is 2-3 seconds long
- **Participants:** 8 different individuals
- **Letters:** І, Ї, А, В, Д, И, К, Л, М, Н, О, Р, С, Т, У, Ю.
- **Conditions:** Various dynamic backgrounds

## Data Processing

1. **Frame Extraction:** Extract the first 60 frames (2 seconds) from each video.
2. **Frame Sampling:** Sample frames to reduce the data size.
3. **Rescaling:** Lower the resolution and crop frames from 16:9 to 1:1.
4. **Tensor Formation:** Create tensors of shape (12, 360, 360, 3) representing (Time, Height, Width, Channels).

## Models and Approaches

### Initial Attempts
1. **Data Augmentation:** Using the Kornia library.
2. **Models Tried:**
   - CNN-LSTM
   - (2+1)D CNN
   - Long-term Recurrent Convolutional Networks

**Challenges:** Encountered low accuracy with initial models.

### Final Model
- **Architecture:** ResNet50V2 base with additional 3D convolutional and pooling layers, followed by fully connected layers.
- **Training:** Stratified K-Fold (3 Folds) with ADAM Optimizer.
- **Improvements:** Added L2 Regularization and Dropout to enhance performance.

### Results
**Final Test Accuracy:** 85.93%

<img width="576" alt="image" src="https://github.com/andriipletinka/Sign_Language_Detection/assets/92575176/8605c2e6-9485-4710-bd3b-77376d238194">

### How to Run the Project
1. Downloaded the trained model from [here](https://drive.google.com/file/d/1wdR0deBDdmCuUNQjkH7ezNT4w3luQtFx/view?usp=sharing).
2. Download and run [`real_time_interface.py`](https://github.com/andriipletinka/Sign_Language_Detection/blob/main/real_time_interface.py). **Note:** specify the correct path to the model inside the file.

## Contributors

- Mykhailo Humeniuk
- Andrii Pletinka



Note: Dataset is not attached.
