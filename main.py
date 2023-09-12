import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import cv2
import os
import random


# Function to save the API key to a file
def save_api_key(api_key):
    with open("api_key.txt", "w") as file:
        file.write(api_key)


# Function to load the API key from the file
def load_api_key():
    if os.path.exists("api_key.txt"):
        with open("api_key.txt", "r") as file:
            return file.read().strip()
    else:
        return None


# Function to handle setting/changing the API key
def set_api_key():
    new_api_key = api_key_entry.get()

    if new_api_key:
        save_api_key(new_api_key)
        tk.messagebox.showinfo("Success", "API Key has been saved.")
        api_key_entry.delete(0, tk.END)
        upload_button.configure(state="active")
        change_button.configure(state="active")
    else:
        tk.messagebox.showerror("Error", "API Key cannot be empty.")


# Function to handle changing the API key
def change_api_key():
    result = tk.messagebox.askyesno(
        "Change API Key", "Are you sure you want to change the API Key?"
    )
    if result:
        os.remove("api_key.txt")
        tk.messagebox.showinfo(
            "Success", "API Key has been removed. Please set a new one."
        )
        upload_button.configure(state="disabled")
        change_button.configure(state="disabled")
    else:
        return


# Function to extract frames from a video with a maximum of 10 frames
def extract_frames(video_path, output_directory):
    os.makedirs(output_directory, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    max_frames_to_capture = min(10, frame_count)  # Set maximum frames to 10

    frames_to_capture = random.sample(range(frame_count), max_frames_to_capture)

    for frame_num in frames_to_capture:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()

        if ret:
            frame_path = os.path.join(output_directory, f"frame_{frame_num}.jpg")
            cv2.imwrite(frame_path, frame)

    cap.release()


# Function to upload images to ImgBB
def upload_images():
    api_key = load_api_key()
    if api_key is None:
        tk.messagebox.showerror(
            "Error", "API Key not found. Please set the API Key first."
        )
        return

    video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")])

    frames_directory = "frames"
    extract_frames(video_path, frames_directory)

    for frame_num in os.listdir(frames_directory):
        frame_path = os.path.join(frames_directory, frame_num)
        with open(frame_path, "rb") as file:
            response = requests.post(
                "https://api.imgbb.com/1/upload",
                params={"key": api_key},
                files={"image": file},
            )
            result = response.json()
            img_url = result["data"]["url"]

            with open("bb_codes.txt", "a") as bb_file:
                bb_file.write(f"[img]{img_url}[/img]\n")

    tk.messagebox.showinfo("Finished", "Job Finished!")


# Create the GUI
root = tk.Tk()
root.title("Image Uploader")
root.geometry("400x300")  # Set default width and height
# Increase font size
font_style = ("Consolas", 15)

# api_key_entry = tk.Entry(root, show="*")
api_key_entry = tk.Entry(root, show="*", font=font_style)  # Increase font size


api_key = load_api_key()
if api_key:
    tk.Label(root, text="API Key already set.").pack(pady=10)
    upload_button = tk.Button(
        root, text="Upload Images from Video", command=upload_images
    )
    change_button = tk.Button(root, text="Change API Key", command=change_api_key)
else:
    tk.Label(root, text="Enter API Key:").pack(pady=10)
    api_key_entry.pack(pady=10)
    tk.Button(root, text="Set API Key", command=set_api_key).pack(pady=10)
    upload_button = tk.Button(
        root, text="Upload Images", command=upload_images, state="disabled"
    )
    change_button = tk.Button(
        root, text="Change API Key", command=change_api_key, state="disabled"
    )

upload_button.pack(pady=20)
change_button.pack(pady=5)

root.mainloop()


# import tkinter as tk
# from tkinter import filedialog, messagebox
# from cryptography.fernet import Fernet
# import requests
# import os


# # Function to encrypt and save the API key to a file
# def save_api_key(api_key):
#     key = Fernet.generate_key()
#     cipher_suite = Fernet(key)
#     encrypted_api_key = cipher_suite.encrypt(api_key.encode())

#     with open("api_key.txt", "wb") as file:
#         file.write(encrypted_api_key)


# # Function to load and decrypt the API key from the file
# def load_api_key():
#     if os.path.exists("api_key.txt"):
#         with open("api_key.txt", "rb") as file:
#             encrypted_api_key = file.read()

#         key = Fernet.generate_key()
#         cipher_suite = Fernet(key)
#         decrypted_api_key = cipher_suite.decrypt(encrypted_api_key).decode()

#         return decrypted_api_key
#     else:
#         return None


# # Function to handle the upload process
# def upload_images():
#     api_key = load_api_key()
#     if api_key is None:
#         tk.messagebox.showerror(
#             "Error", "API Key not found. Please set the API Key first."
#         )
#         return

#     # Rest of your upload process using the API key


# # Function to handle setting/changing the API key
# def set_api_key():
#     new_api_key = api_key_entry.get()

#     if new_api_key:
#         save_api_key(new_api_key)
#         tk.messagebox.showinfo("Success", "API Key has been saved.")
#         api_key_entry.delete(0, tk.END)
#     else:
#         tk.messagebox.showerror("Error", "API Key cannot be empty.")


# # Create the GUI
# root = tk.Tk()
# root.title("API Key Manager")

# # Check if API key exists
# api_key = load_api_key()

# if api_key:
#     tk.Label(root, text="API Key already set.").pack(pady=10)
# else:
#     tk.Label(root, text="Enter API Key:").pack(pady=10)
#     api_key_entry = tk.Entry(root, show="*")
#     api_key_entry.pack(pady=10)
#     tk.Button(root, text="Set API Key", command=set_api_key).pack(pady=10)

# # Add a button to trigger the upload process
# upload_button = tk.Button(root, text="Upload Images", command=upload_images)
# upload_button.pack(pady=20)

# # Start the GUI application
# root.mainloop()


# import tkinter as tk
# from tkinter import filedialog
# import requests
# import cv2
# import os
# import random


# # Function to handle the upload process
# def upload_images():
#     # Open file dialog to select a video file
#     video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")])

#     # Create a directory to save frames
#     frames_directory = "frames"
#     os.makedirs(frames_directory, exist_ok=True)

#     # Use OpenCV to capture frames from the video
#     cap = cv2.VideoCapture(video_path)
#     frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

#     # Define the maximum number of frames to capture (15 in this case)
#     max_frames_to_capture = min(15, frame_count)

#     # Generate a random set of frame indices to capture
#     frames_to_capture = random.sample(range(frame_count), max_frames_to_capture)

#     for frame_num in frames_to_capture:
#         cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
#         ret, frame = cap.read()

#         if ret:
#             frame_path = os.path.join(frames_directory, f"frame_{frame_num}.jpg")
#             cv2.imwrite(frame_path, frame)

#     cap.release()

#     # Iterate through the frames and upload them to ImgBB
#     for frame_num in frames_to_capture:
#         frame_path = os.path.join(frames_directory, f"frame_{frame_num}.jpg")
#         with open(frame_path, "rb") as file:
#             response = requests.post(
#                 "https://api.imgbb.com/1/upload",
#                 params={"key": "api_key"},
#                 files={"image": file},
#             )
#             result = response.json()
#             img_url = result["data"]["url"]

#             # Save the BB-Code to a text file
#             with open("bb_codes.txt", "a") as bb_file:
#                 bb_file.write(f"[img]{img_url}[/img]\n")

#     # Show a pop-up message
#     tk.messagebox.showinfo("Finished", "Job Finished!")


# # Create the GUI
# root = tk.Tk()
# root.title("Frame Uploader")

# # Add a button to trigger the upload process
# upload_button = tk.Button(root, text="Upload Video", command=upload_images)
# upload_button.pack(pady=20)

# # Start the GUI application
# root.mainloop()
