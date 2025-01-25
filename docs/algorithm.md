# Iterate through each file in the directory
    - Check if the directory contains an mkv or mp4 file
        - If file exists
            - Check format of directory name
                - If format is not correct
                    - Format directory name
            - Move into directory
            - Check format of mkv/mp4 file name
                # If format is not correct
                    # Format file name
            - Check for Subs directory
                - If directory exists, extract sub files to current directory
                - Delete Subs directory
            - Rename .srt files
            - Clean video file with ffmpeg
            - Delete old video
            - Delete any unnecessary files

# Convert to CLI tool that takes directory as argument
