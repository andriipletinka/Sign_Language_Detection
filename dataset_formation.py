import os
import subprocess
import shutil

# Dictionary of participant names to IDs
participant_mapping = {
    "Andrii": 1, "Dima": 2, "Liza": 3, "Vitalik": 4,
    "Tanya": 5, "Lyuda": 6, "Khrystya": 7, "Misha": 8
}

# List of letters in the order they were recorded
letters = ["А", "В", "Д", "И", "І", "Ї", "К", "Л", "М", "Н", "О", "Р", "С", "Т", "У", "Ю"]

# Base path of the dataset
base_path = "Dataset"


def is_valid_video(file_name):
    valid_extensions = ['.mov', '.mp4']  # Add other video extensions if necessary
    return file_name.lower().endswith(tuple(valid_extensions)) and not file_name.startswith('.')


for letter in letters:
    letter_path = os.path.join(base_path, letter)
    if not os.path.exists(letter_path):
        os.makedirs(letter_path)

    for participant_name, participant_id in participant_mapping.items():
        participant_folder = os.path.join(base_path, participant_name)
        participant_new_folder = os.path.join(letter_path, str(participant_id))
        if not os.path.exists(participant_new_folder):
            os.makedirs(participant_new_folder)

        # List all videos in the participant folder
        videos = sorted(
            [f for f in os.listdir(participant_folder) if is_valid_video(f)],
            key=lambda x: int(x[-7:-4])
        )

        # Calculate the correct index for videos of this letter
        letter_index = letters.index(letter)

        # Select every 16th video starting from the letter_index
        for i in range(5):  # Since there've been 5 locations
            video_index = letter_index + 16 * i
            if video_index < len(videos):
                video_name = videos[video_index]
                new_video_name = f"{letter}_{participant_id}_{i + 1}.mp4"
                source_path = os.path.join(participant_folder, video_name)
                destination_path = os.path.join(participant_new_folder, new_video_name)

                # Rename and move the file
                command = [
                    "ffmpeg",
                    "-i", source_path,
                    "-c:v", "libx264",
                    "-crf", "23",  # Controls the quality, lower values mean better quality
                    "-preset", "fast",
                    destination_path
                ]
                subprocess.run(command, check=True)
                # shutil.copy(source_path, destination_path)

print("Dataset restructuring complete.")
