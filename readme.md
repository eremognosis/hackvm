
# HACK VM

It is a python implemtnatiohn of the HACK virtual mchine as specified by Nand2Tetris.


## Documentation

Yoiu dont need a mastery in rocket science
- The basic syntax is 
- Start with a virtual environment (feels good)
    - Windows: `python -m venv .venv`
    - Linux: `python3 -m venv .venv`

- Activate it (babysitting)
    - Windows : `.venv\Scripts\activate.bat`
    - Linux: `source .venv/bin/activate`
- The idea is to 
```bash
$ python main.py filename.vm
```
- It will create a file named `filename.asm` in the same directory as the .vm

If you wanna forcefully test it
- Have a VM file (make a .vm file in vscode or somethng and write some lines or copy)
- Do this shit once (it handles the test file from my repo which is from the [nand2tetris website](https://nand2tetris.org))
```
bash

git clone https://github.com/eremognosis/hackvm.git
cd hackvm
python3 -m venv .venv
source .venv/bin/activate
python main.py test.vm
```

## License

[MIT](https://choosealicense.com/licenses/mit/)


## Authors

- [@eremognosis](https://www.github.com/eremognosis)


## REFER

 - [Nand2Tetris Website](https://nand2tetris.org/)
 - [The Book](http://f.javier.io/rep/books/The%20Elements%20of%20Computing%20Systems.pdf)


## Contributing

Contributions are always welcome!

Theres nothing to contribute here tho. But you can defenitely make the parsing more safe by checks. Send PR (Pull Requests, not Political Reporting or Public Relations) 

Please adhere to this project's `code of conduct`.

