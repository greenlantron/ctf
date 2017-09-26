echo -n $1 | base64 -d > /tmp/jde
if [ ! -f /tmp/jdeserialize-1.2.jar ]; then
    wget "https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/jdeserialize/jdeserialize-1.2.jar" -O "/tmp/jdeserialize-1.2.jar"
fi
java -jar /tmp/jdeserialize-1.2.jar /tmp/jde
