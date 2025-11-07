# uv run main.py "D:\Nishant\Pictures&Vedios"
import os
import glob
import sys
import time
import pandas as pd
import subprocess
from pathlib import Path
import json

# Supported media file extensions
MEDIA_EXTENSIONS = (".jpg", ".jpeg", ".png", ".mp4", ".mov", ".avi", ".mkv")

def get_base_folder_path():
    if len(sys.argv) < 2:
        print("Usage: python media_group_player.py <folder_path> [group_name]")
        sys.exit(1)

    base_folder = sys.argv[1]

    if not os.path.exists(base_folder):
        print(f"Error: Folder does not exist: {base_folder}")
        sys.exit(1)

    return base_folder

def get_media_files(base_folder):
    """Recursively get all media files under a folder."""
    all_files = []
    for ext in MEDIA_EXTENSIONS:
        all_files.extend(glob.glob(os.path.join(base_folder, "**", f"*{ext}"), recursive=True))
    
    if not all_files:
        print("Warning: No media files found in the provided folder.")
        sys.exit(0)

    """Create a Pandas DataFrame from file metadata."""
    df = pd.DataFrame(data=all_files,columns=['FilePath'])
    return df

def get_base_folder_name(filePath):
    return os.path.basename(os.path.normpath(filePath))

def get_csv_file_name():
    base_folder_name = get_base_folder_name(get_base_folder_path())
    output_csv = f"{base_folder_name}_media_list.csv"
    return output_csv

def read_excel_to_df(ExcelFile):
    return pd.read_excel(ExcelFile)

def read_Group_Filter():
    return read_excel_to_df(r"C:\Users\lenovo\OneDrive\Documents\GroupFilter.xlsx")

def create_csv(media_files_df):
    """Save DataFrame to CSV with the base folder name."""
    
    media_files_df.to_csv(get_csv_file_name(), index=False)
    print(f"\n CSV file created...")

def create_Json_file(media_files_df):
    base_folder_name = get_base_folder_name(get_base_folder_path())
    output_json = f"{base_folder_name}.json"
    # media_files_df['FilePath'].to_json(output_json,orient="records", indent=4)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(media_files_df['FilePath'].tolist(), f, indent=4)
 
def run_powershell():
    # ======= Call PowerShell =======
        base_folder_name = get_base_folder_name(get_base_folder_path())
        output_json = Path(f"{base_folder_name}.json")
        powershell_script = Path("open_photos_slideshow.ps1")

        subprocess.run([
                "powershell", "-ExecutionPolicy", "Bypass", "-File", str(powershell_script),
                "-jsonPath", str(output_json.resolve())
            ], check=True)
        
def open_photos_slideshow(media_files_df):
    """Open Windows Photos for the given folder path."""
    try:
        # run_powershell()

        
        print("Photos opened. Use slideshow option to play automatically.")
    except Exception as e:
        print(f"Failed to open Photos app: {e}")

def play_media (media_files_df):
    open_photos_slideshow(media_files_df)
    # for file in media_files_df['FilePath']:
    #     print(f"Opening: {file}")
    #     os.startfile(file)   # Opens in default app (Photos or Movies & TV)
    #     time.sleep(1)        # Delay between files (optional)   

def extraxt_folder_name(media_files_df):
    # Extract base folder (directory path)
    media_files_df['BaseFolder'] = media_files_df['FilePath'].apply(os.path.dirname)

def get_distinct_folder_Name(media_files_df):
    # Find unique folder names
    unique_folders = pd.DataFrame(media_files_df['BaseFolder'].unique(),columns=['unique_folders'])
    return unique_folders


def get_filtered_folder_names():
    load_filter_df = read_Group_Filter()
    filtered_df= load_filter_df[load_filter_df['Required']=='Y']
    return filtered_df

def assign_groups_to_filtered_folders(media_files_df):
    merged_df = pd.merge(
                    media_files_df,
                    get_filtered_folder_names(),
                    how='left',                      # keep all rows from main_data
                    left_on='FilePath',
                    right_on='unique_folders'
                )
    return merged_df

def generateFile(media_files_df):
    with pd.ExcelWriter("FinalFile.xlsx", engine='openpyxl') as writer:
        print("Writing All-Files to excel...")
        media_files_df['FilePath'].to_excel(writer,sheet_name='All-Files', index=False)

        print("Writing distinct folder names to excel...")
        get_distinct_folder_Name(media_files_df).to_excel(writer,sheet_name='unique_folders', index=False)

        print("Writing filtered folder names to excel...")
        get_filtered_folder_names().to_excel(writer,sheet_name='filtered_folders', index=False)

        print("Writing assign_groups_to_filtered_folders to excel...")
        assign_groups_to_filtered_folders(media_files_df).to_excel(writer,sheet_name='asigned_groups', index=False)

        

def main():
    print("Hello from my-photos-media!")
    print("Extrating media file path list....")
    # Extract media files
    media_files_df = get_media_files(get_base_folder_path())

    print("Extrating folder list....")
    extraxt_folder_name(media_files_df)
    # print(media_files_df)

    # print("Get unique folder names...")
    # get_distinct_folder_Name(media_files_df)

    # print("Creating csv....")
    # create_csv(media_files_df)

    # print("Creating Json File....")
    # create_Json_file(media_files_df)

    # Generate excel file 
    generateFile(media_files_df)
    # play_media(media_files_df)

if __name__ == "__main__":
    main()
