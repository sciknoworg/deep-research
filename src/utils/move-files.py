import os
import shutil

def move_markdown_files(base_folder):
    # Confirm input path is a directory
    if not os.path.isdir(base_folder):
        print(f"❌ The path '{base_folder}' is not a valid directory.")
        return

    o3_folder = os.path.join(base_folder, "o3")
    o3_mini_folder = os.path.join(base_folder, "o3-mini")

    # Ensure the destination folders exist
    if not os.path.exists(o3_folder) or not os.path.exists(o3_mini_folder):
        print("❌ Both 'o3' and 'o3-mini' subfolders must exist in the input folder.")
        return

    for filename in os.listdir(base_folder):
        if filename.endswith(".md"):
            src_path = os.path.join(base_folder, filename)
            if "o3-mini" in filename:
                dst_path = os.path.join(o3_mini_folder, filename)
                shutil.move(src_path, dst_path)
                print(f"📁 Moved: {filename} → o3-mini/")
            elif "o3" in filename:
                dst_path = os.path.join(o3_folder, filename)
                shutil.move(src_path, dst_path)
                print(f"📁 Moved: {filename} → o3/")

if __name__ == "__main__":
    folder = input("📂 Enter the path to the folder: ").strip()
    move_markdown_files(folder)
