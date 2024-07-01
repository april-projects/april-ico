import os


def scan_directories(base_path, ignore_dirs, ignore_files):
    """Scan the base directory for subdirectories and image files, ignoring specified directories and files."""
    directory_images = {}
    for root, dirs, files in os.walk(base_path):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if os.path.relpath(os.path.join(root, d), base_path) not in ignore_dirs]

        # Skip ignored files
        image_files = [f for f in files if f not in ignore_files]
        if image_files:
            relative_dir = os.path.relpath(root, base_path)
            directory_images[relative_dir] = image_files
    return directory_images


def generate_markdown(directory_images, base_url):
    """Generate Markdown content for the images in directories."""
    markdown_content = "# 图标列表\n\n"

    for directory, images in directory_images.items():
        markdown_content += f"## {directory}\n\n"
        markdown_content += "| " + " | ".join([""] * 3) + " |\n"
        markdown_content += "| " + " | ".join(["----"] * 3) + " |\n"

        row = []
        for img in images:
            # Ensure proper path format for Markdown
            img_path = os.path.join(directory, img).replace("\\", "/")
            img_url = f"{base_url}/{img_path}"
            row.append(f"![{img}]({img_url})")
            if len(row) == 3:
                markdown_content += "| " + " | ".join(row) + " |\n"
                row = []

        if row:
            # Add remaining images in the last row if any
            while len(row) < 3:
                row.append("")
            markdown_content += "| " + " | ".join(row) + " |\n"

        markdown_content += "\n"

    return markdown_content


def main():
    # You can change this to any directory you want to scan
    base_path = "."
    # Add directories to ignore here
    ignore_dirs = ['.git']
    # Add files to ignore here
    ignore_files = ['main.py', 'README.md']
    # Base URL for target addresses
    base_url = "https://cdn.jsdelivr.net/gh/april-projects/april-ico/"

    directory_images = scan_directories(base_path, ignore_dirs, ignore_files)
    markdown_content = generate_markdown(directory_images, base_url)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print("Markdown file 'README.md' generated successfully.")


if __name__ == "__main__":
    main()
