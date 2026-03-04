<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This project implements a simple 8-bit synchronous accumulator. On every rising edge of the clock, the design samples an 8-bit input value (`ui_in`) and adds it to the current value stored in an internal register.

The design features:
* **Asynchronous Active-Low Reset:** Bringing `rst_n` low immediately clears the accumulator to zero.

* **Enable Signal:** The `ena` signal must be high for the accumulation to occur.

* **Overflow Handling:** The accumulator performs standard 8-bit unsigned addition. If the sum exceeds 255 (28−1), the value wraps around modulo 256.

The 8-bit output is visible on the dedicated output pins (`uo_out`).

## How to test

The project can be tested by providing a clock signal and manipulating the reset and input pins. The following test were conducted:

* **Reset:** Set `rst_n` to 0 to ensure the output uo_out is 0x00.

* **Enable:** Set ena to 1 and `rst_n` to 1 to begin operation.

* **Accumulate:** Provide a value on `ui_in` (e.g., 10). On the next clock cycle, the output will show 10.

* **Hold:** Set `ui_in` to 0. The output should remain constant at the previous sum.

* **Overflow:** Add a value that forces the sum above 255 (e.g., if the sum is 200, add 100) and verify that the output wraps around (e.g., to 44).

### Testbench Justification

The Cocotb testbench is sufficient because it verifies the four critical states of the hardware:

* **Initial Power-on/Reset:** Ensures the register starts at a known state.

* **Linear Accumulation:** Verifies that addition logic is correct for multiple sequential values.

* **No-op State:** Confirms that adding zero does not inadvertently change the register state.

* **Boundary Conditions (Overflow):** Confirms the 8-bit wrap-around behavior, ensuring the logic remains stable at the maximum bit-width.

The testbench utilizes FallingEdge timing to drive inputs, which prevents simulation race conditions and ensures the hardware is tested with stable setup and hold times.

## External hardware

No specific external hardware is required. The design can be interfaced with standard switches/buttons for inputs and LEDs or a logic analyzer for the 8-bit output.

## Use of GenAI

I used the Gemini AI to help me develop this project. Gemini helped in:

* Figuring out the initial Verilog model for the accumulator.

* Debugging simulation race conditions in the Cocotb testbench (specifically moving from ClockCycles to FallingEdge triggers).
