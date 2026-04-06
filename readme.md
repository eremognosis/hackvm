
# HACK VM

It is a python implemtnatiohn of the HACK virtual mchine as specified by Nand2Tetris.


## Documentation

Yoiu dont need a mastery in rocket science
- The basic syntax is 
- Start with a virtual environment (feels good)
    - Windows: `python -m venv .venv`
    - Linux: `python3 -m venv .venv` (mac should be the same as far as i know)

- Activate it (babysitting)
    - Windows : `.venv\Scripts\activate.bat` (i just googled might be different for ps etc idk windows nuances)
    - Linux: `source .venv/bin/activate`
- The idea is to 
```bash
$ python main.py filename.vm
```
- It will create a file named `filename.asm` in the same directory as the .vm

If you wanna forcefully test it
- Have a VM file (make a .vm file in vscode or somethng and write some lines or copy)
- Do this once (it handles the test file from my repo which is from the [nand2tetris website](https://nand2tetris.org))
```
bash

git clone https://github.com/eremognosis/hackvm.git
cd hackvm
python3 -m venv .venv
source .venv/bin/activate
python main.py test.vm
```

## Testing
I created a test mopdule with `pytest` but with not 100s of tests. I will add more tests in the future. More test cases are welcome.
You can run the tests with 
```bash
cd tests
pytest test.py -vv
```

It should run and pass and output something like this
```bash
(.venv) you@yourpc:~/path/to/hackvm/tests$ pytest test.py -v
============================================================== test session starts ==============================================================
platform linux -- Python 3.13.9, pytest-9.0.2, pluggy-1.6.0 -- /home/you/path/to/hackvm/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /home/you/path/to/hackvm/tests
collected 10 items                                                                                                                              

test.py::test_arith_basic[add-@SP\nAM=M-1\nD=M\nA=A-1\nM=M+D] PASSED                                                                      [ 10%]
test.py::test_arith_basic[sub-@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D] PASSED                                                                      [ 20%]
test.py::test_arith_basic[and-@SP\nAM=M-1\nD=M\nA=A-1\nM=M&D] PASSED                                                                      [ 30%]
test.py::test_arith_basic[neg-@SP\nA=M-1\nM=-M] PASSED                                                                                    [ 40%]
test.py::test_arith_logical_with_labels PASSED                                                                                            [ 50%]
test.py::test_push_constant PASSED                                                                                                        [ 60%]
test.py::test_pop_local PASSED                                                                                                            [ 70%]
test.py::test_parse_skips_garbage_and_compiles PASSED                                                                                     [ 80%]
test.py::test_function_call PASSED                                                                                                        [ 90%]
test.py::test_full_translation_pipeline PASSED                                                                                            [100%]

============================================================== 10 passed in 0.01s ===============================================================

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

Please adhere to this project's `code of conduct`. (if i had one)

