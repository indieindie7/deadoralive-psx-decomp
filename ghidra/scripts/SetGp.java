// SetGp.java <hex value>: set register gp to a constant over the whole program (PsyQ small-data base), so the
// decompiler resolves gp-relative loads/stores to DAT_ globals.
//@category ShamanKing
import ghidra.app.script.GhidraScript;
import ghidra.program.model.lang.Register;
import ghidra.program.model.address.*;
import java.math.BigInteger;
public class SetGp extends GhidraScript {
    public void run() throws Exception {
        long v = Long.parseLong(getScriptArgs()[0].replace("0x", ""), 16);
        Register gp = currentProgram.getRegister("gp");
        for (AddressRange r : currentProgram.getMemory().getAddressRanges())
            currentProgram.getProgramContext().setValue(gp, r.getMinAddress(), r.getMaxAddress(), BigInteger.valueOf(v));
        println("gp set to 0x" + Long.toHexString(v));
    }
}
