from os import listdir, path
import music_tag
import json
import shutil

with open("config.json", "r") as file:
    config = json.loads(file.read())

image_data = None
if config["album_artwork"]:
    with open(config["album_artwork"], "rb") as image:
        image_data = image.read()

root_directory = config["source_directory"]
root_folders = listdir(root_directory)

print("Copying files...")
# shutil.copytree(root_directory, config["output_directory"])
print("Complete!")

print("Writing meta data...")
for folder in root_folders:
    folder_path = f"{root_directory}\\{folder}"
    folder_files = listdir(folder_path)

    for file in folder_files:
        print(f"Writing meta data for file '{file}'...")

        audio_file = music_tag.load_file(f"{folder_path}\\{file}")
        audio_file["album"] = config["book_name"]
        audio_file["artist"] = config["book_author"]
        audio_file["totaldiscs"] = len(root_folders)
        audio_file["discnumber"] = file[:-4].split(" ")[-1]
        audio_file["totaltracks"] = len(folder_files)
        audio_file["tracknumber"] = file[:-4].split(" ")[0]

        if image_data:
            audio_file["artwork"] = image_data

        audio_file.save()

print("Complete!")
