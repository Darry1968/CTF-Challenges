## Pyception:

Basic programming concepts needed to solve this.

![image](https://github.com/Darry1968/CTF-Challenges/assets/104063375/65dc19e6-0fc1-43ac-9af2-21c9ec65fff0)

We have to provide some string in double quotes only so to solve this challenge use this Payload:
```
"\x22+open('static/flag.txt').read()+\x22"
```

\x22 represents double quote

so this can break the condition and we can concatenate our payload which can give you flag.