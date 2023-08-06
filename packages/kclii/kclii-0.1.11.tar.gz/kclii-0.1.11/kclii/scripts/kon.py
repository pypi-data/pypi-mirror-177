SCRIPT = """
#!/bin/bash
echo "K-ON $(k version)"
echo "** Initialize profile: $(k profile current) **"

echo "$(k profile ls-env --raw)" > /tmp/k.env

while read -r line
do
  export $line
done < /tmp/k.env

# export $(grep -v '^#' /tmp/k.env | xargs -0)
"""
