# Ghidra headless script to check current names at specific addresses
from ghidra.program.model.address import AddressSet

addrs = [
    "0801b91c", "0801b93c", "0801ba04", "0801ba4c", "0801ba5c",
    "0801ba78", "0801bb28", "0801bbd4", "0801c2ac", "0801c310",
    "0801c3f4", "0801c484", "0801c4c0", "0801c50c", "0801c5d8",
    "0801c668", "0801c694", "0801c6b0", "0801c728", "0801c74c"
]

for addr_str in addrs:
    addr = currentProgram.getAddressFactory().getAddress("0x0" + addr_str)
    func = getFunctionAt(addr)
    if func is not None:
        print("[found] 0x%s -> %s" % (addr_str, func.getName()))
    else:
        print("[none]  0x%s (no function at this address)" % addr_str)
