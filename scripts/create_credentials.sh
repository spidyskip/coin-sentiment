#!/bin/bash

# Set your values here
USER_KEY=""
SECRET_KEY=""
PSW=""
USERNAME=""

# Specify the file path
file_path="config/credentials/keys.json"

# Check if the file already exists
if [ -f "$file_path" ]; then
    echo "JSON file already exists: $file_path"
else
    # Create the directory if it doesn't exist
    mkdir -p "$(dirname "$file_path")"

    # Create the JSON content
    json_content=$(cat <<EOF
{
    "reddit": {
        "USER_KEY": "$USER_KEY",
        "SECRET_KEY": "$SECRET_KEY",
        "PSW": "$PSW",
        "USERNAME": "$USERNAME"
    }
}
EOF
    )

    # Write the JSON content to the file
    echo "$json_content" > "$file_path"

    echo "JSON file created: $file_path"
fi
