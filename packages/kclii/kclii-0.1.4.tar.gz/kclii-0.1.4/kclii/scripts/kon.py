SCRIPT = """
#!/bin/bash
echo "** Initialize profile **"

input=".env"

while read -r line
do
  export $line
done < "$input"
"""
