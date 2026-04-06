import pytest
from src.basic import *
@pytest.mark.parametrize("opcode, expected_asm", [
    ("add", "@SP\nAM=M-1\nD=M\nA=A-1\nM=M+D"),
    ("sub", "@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D"),
    ("and", "@SP\nAM=M-1\nD=M\nA=A-1\nM=M&D"),
    ("neg", "@SP\nA=M-1\nM=-M"),
])
def test_arith_basic(opcode, expected_asm):
    # n2 is 0 here since these don't generate labels
    result = (arith(opcode, 0))
    assert result == expected_asm

def test_arith_logical_with_labels():
    # eq/gt/lt use the instruction index (n2) to create unique jump labels
    result = (arith("eq", 42))
    assert "@EQ42" in result
    assert "(EQ42)" in result
    assert "D;JEQ" in result
    
def test_push_constant():
    # push constant 17
    op = Operation("push", "constant", 17, fname="Sys", n2=0)
    expected = "@17\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1"
    
    assert (op.do()) == expected

def test_pop_local():
    # pop local 2
    op = Operation("pop", "local", 2, fname="Sys", n2=0)
    result = (op.do())
    
    # Check that it resolves the base address correctly and uses R13
    assert "@LCL" in result
    assert "@2" in result
    assert "@R13" in result
    
    
def test_parse_skips_garbage_and_compiles():
    vm_code = """
    // This is a comment that should be ignored
    
    push constant 10
    push constant 20
    add // Add them up
    """
    

    output = parse(vm_code, "TestFile")
    
    assert len(output) == 3
    
    # Verify the final addition block compiled correctly
    assert (output[2]) == "@SP\nAM=M-1\nD=M\nA=A-1\nM=M+D"
    
    
def test_function_call():
    # call Sys.main 2 (at instruction 99)
    result = (handlefun("call", "Sys.main", 2, 99))
    
    # Did it generate the return label correctly?
    assert "@Sys.main$ret.99" in result
    assert "(Sys.main$ret.99)" in result
    # Did it jump to the function?
    assert "@Sys.main\n0;JMP" in result
    
    
import os
from main import process_logic

def test_full_translation_pipeline():
    test_file = "test.vm"
    process_logic(test_file)
    expected_out_file = "test.asm"
    assert os.path.exists(expected_out_file)

