import os
import shutil

folder_path = input("Enter folder path: ")
extensions = {
    'Images': ['.jpeg', '.jpg', '.png', '.gif','.JPG'],
    'Documents': ['.doc', '.docx', '.pdf', '.txt','.xls','.xlsx','.rtf','.xlsm'],
    'Music': ['.mp3', '.wav'],
    'Videos': ['.mp4', '.avi', '.mkv','.webm'],
    'Compressed': ['.zip','.rar'],
    'Software' : ['.exe'],
    'Adobe Preset' : ['.prfpset'],
    'Icon Pack' : ['.ico'],
    'RainMeter' : ['.rmskin'],
    'NodeJs' : ['.msi']
}

#%%
for filename in os.listdir(folder_path):
    for category, exts in extensions.items():
        for ext in exts:
            if filename.endswith(ext):
                source_path = os.path.join(folder_path, filename)
                destination_path = os.path.join(folder_path, category)
                
                # create category folder if it doesn't exist
                if not os.path.exists(destination_path):
                    os.makedirs(destination_path)
                
                # move file to category folder
                shutil.move(source_path, destination_path)
                print(f"Moved {filename} to {category}")
                
                # exit inner for loop if file has been moved
                break