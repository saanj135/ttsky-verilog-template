# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge, ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("### RUNNING ACCUMULATOR VERSION 1.0 ###")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # reset
    dut._log.info("Starting Reset...")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    
    # rerify reset
    val = dut.uo_out.value.to_unsigned()
    assert val == 0, f"Reset failed: expected 0, got {val}"
    dut._log.info("PASS: Reset successful")

    # test sequential add
    # 0 + 10 = 10
    dut.ui_in.value = 10
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    assert dut.uo_out.value.to_unsigned() == 10, "Addition 1 failed"

    # 10 + 25 = 35
    dut.ui_in.value = 25
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    assert dut.uo_out.value.to_unsigned() == 35, "Addition 2 failed"
    dut._log.info("PASS: Basic addition verified")

    # test adding 0 (value should stay at 35)
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 3)
    assert dut.uo_out.value.to_unsigned() == 35, "Value changed after adding 0"
    dut._log.info("PASS: Adding zero works (value held)")

    # test 8 bit overflow (wrap around)
    # current value: 35. to wrap past 255, we can add 230.
    # (35 + 230) = 265. 
    # 265 % 256 = 9.
    dut.ui_in.value = 230
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    
    val_overflow = dut.uo_out.value.to_unsigned()
    assert val_overflow == 9, f"Overflow failed: expected 9, got {val_overflow}"
    dut._log.info("PASS: 8-bit overflow wrapped correctly")

    # final reset check
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    assert dut.uo_out.value.to_unsigned() == 0, "Final reset failed"
    dut._log.info("PASS: Final reset successful")

    dut._log.info("All tests passed successfully!")