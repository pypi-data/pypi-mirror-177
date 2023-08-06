SCRIPT = """
#!/bin/bash
input=".env"

while read -r line
do
  key=$(echo $line | cut -d "=" -f 1)

  unset $key
done < "$input"
"""
