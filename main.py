import os
import openai
import time

openai.api_key = "YOUR_API_KEY_HERE"


def traverse(rootdir):
    file_data = {}
    for subdir, dirs, files in os.walk(rootdir):
        print(f"Directory: {subdir}")
        for file in files:
            filepath = os.path.join(subdir, file)
            print(f"File: {filepath}")
            with open(filepath, "r") as f:
                file_contents = f.read()
                file_data[filepath] = file_contents
                # do something with the file contents here
    return file_data


if __name__ == "__main__":
    root_dir = "/path/to/root/directory"
    file_data = traverse(root_dir)
    for filepath, contents in file_data.items():
        try:
            response = openai.Completion.create(
                engine="davinci-codex",
                prompt=f"I have a file located at {filepath}. Its contents are as follows:\n\n{contents}\n\nAsk me "
                       f"any question related to this codebase.",
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.7,
            )
            print(f"Question: {response.choices[0].text}")
            time.sleep(0.5)  # optional sleep to avoid rate limiting
        except Exception as e:
            print(f"Error processing file {filepath}: {e}")
