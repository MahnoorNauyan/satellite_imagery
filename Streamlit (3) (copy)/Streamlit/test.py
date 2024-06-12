import os

file_name_with_extension = "lat_33.49491509137658_lng_73.19766794205108_zoom_18.png"
file_name_without_extension, file_extension = os.path.splitext(file_name_with_extension)

print("File name without extension:", file_name_without_extension)
print("File extension:", file_extension)


