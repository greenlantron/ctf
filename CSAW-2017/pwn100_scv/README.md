## SCV (Pwnable, 100 points, 218 solves)

    SCV is too hungry to mine the minerals. Can you give him some food?

A fairly enjoyable 100 point pwnable. When feeding SCV we have a stack buffer overflow with a stack cookie guard. We can leak this stack cookie by reading back what we feed to SCV. With the ability to obtain the stack cookie we can overflow and restore it. Allowing us to obtain RIP control. Having been provided with the corresponding [libc](libc-2.23.so) of the server it makes for a great target and we can use a [bespoke gadget (aka one gadget)](https://david942j.blogspot.com/2017/02/project-one-gadget-in-glibc.html). My quick and dirty final solution is inside [scv.py](scv.py).

`flag{sCv_0n1y_C0st_50_M!n3ra1_tr3at_h!m_we11}`
