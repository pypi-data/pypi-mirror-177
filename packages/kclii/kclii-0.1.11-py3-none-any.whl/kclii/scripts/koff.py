SCRIPT = """
#!/bin/bash
echo "K-OFF $(k version)"
echo "** Deactive profile: $(k profile current) **"

while read -r line
do
  key=$(echo $line | cut -d "=" -f 1)

  unset $key
done < /tmp/k.env

# while read -r line
# do
#   key=$(echo $line | cut -d "=" -f 1)

#   unset $key
# done < "$input"

"""
