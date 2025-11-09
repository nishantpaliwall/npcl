# uv run main.py "D:\Nishant\Pictures&Vedios"
import os
import glob
import sys
import time
import pandas as pd
import subprocess
from pathlib import Path
import json
import shutil
import re

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

def is_pattern_search():
    return len(sys.argv) > 2
 
def get_filepath_pattern():
    if is_pattern_search():
        return f".*{sys.argv[2]}.*"
    else :
        return "====== No Matcing pattern provided ======"

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
    print(filtered_df)
    return filtered_df

def assign_groups_to_filtered_folders(media_files_df,filtered_df):
    # Normalize keys first (recommended)
    media_files_df['_key']= media_files_df['BaseFolder'].astype(str).str.strip()
    filtered_df['filter_key']= filtered_df['unique_folders'].astype(str).str.strip()
    merged_df = pd.merge(
                    media_files_df[['FilePath','BaseFolder','_key']],
                    filtered_df[['unique_folders','Group','Required','filter_key']],
                    how='left',                      # keep all rows from main_data
                    left_on='_key',
                    right_on='filter_key', indicator=True
                )
    
    # Clean up
    # merged_df[merged_df['Required']!='Y'].drop(inplace=True)

    # Fill missing group/required values
    # merged_df['Group'] = merged_df['Group'].fillna('N/A')
    # merged_df['Required'] = merged_df['Required'].fillna('N')
    selected_df = merged_df[merged_df['Required']=='Y']
    return selected_df

def match_any(pattern):
    return re.search(pattern=pattern,)

def select_matching_files(media_files_df):
    pattern = get_filepath_pattern()
    media_files_df['is_maching_pattern'] = media_files_df['FilePath'].apply(lambda x: True if re.search(pattern, x,re.IGNORECASE) else False)
    # This column has been created to generate single folder for all the files while patern search
    media_files_df['Group'] = "PATTERN_SEARCH"
    return media_files_df[media_files_df['is_maching_pattern']]


def copy_selected_files(selected_groups_paths):
    
    # Copy files by group
    for _, row in selected_groups_paths.iterrows():
        src = row['FilePath']
        group = row['Group']
        dest_folder = os.path.join(get_base_folder_path(), f"Temp_{group}")

        # Ensure group folder exists
        os.makedirs(dest_folder, exist_ok=True)

        # Build destination file path
        dest = os.path.join(dest_folder, os.path.basename(src))

        # Copy the file (with metadata)
        try:
            shutil.copy2(src, dest)
            print(f"Copied: {src} → {dest}")
        except Exception as e:
            print(f"Failed to copy {src}: {e}")

    print("\nAll files copied by group successfully!")    

def generateFile(media_files_df):
    with pd.ExcelWriter("FinalFile.xlsx", engine='openpyxl') as writer:
        print("Writing All-Files to excel...")
        media_files_df['FilePath'].to_excel(writer,sheet_name='All-Files', index=False)

        print("Writing distinct folder names to excel...")
        get_distinct_folder_Name(media_files_df).to_excel(writer,sheet_name='unique_folders', index=False)

        print("Writing filtered folder names to excel...")
        filtered_df= get_filtered_folder_names()
        filtered_df.to_excel(writer,sheet_name='filtered_folders', index=False)

        print("Writing assign_groups_to_filtered_folders to excel...")
        selected_groups_paths=assign_groups_to_filtered_folders(media_files_df,filtered_df)
        selected_groups_paths.to_excel(writer,sheet_name='asigned_groups', index=False)

        print("Writing pattern matching file path to excel...")
        pattern_match__paths=select_matching_files(media_files_df)
        pattern_match__paths.to_excel(writer,sheet_name='pattern_match', index=False)
        

        print("Copying selected media items to new folder")
        df = pattern_match__paths if is_pattern_search() else selected_groups_paths
        copy_selected_files(df)

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
