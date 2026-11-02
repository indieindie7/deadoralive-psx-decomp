// AddBss.java <start hex> <end hex>: add an uninitialized RW block "bss" over [start,end) where nothing is mapped yet.
//@category ShamanKing
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
public class AddBss extends GhidraScript {
  public void run() throws Exception {
    String[] a = getScriptArgs();
    Address s = toAddr(Long.parseLong(a[0], 16)), e = toAddr(Long.parseLong(a[1], 16));
    Address hi = currentProgram.getMemory().getMaxAddress();
    if (hi.compareTo(s) >= 0) s = hi.add(1);
    long len = e.subtract(s);
    var b = currentProgram.getMemory().createUninitializedBlock("bss", s, len, false);
    b.setRead(true); b.setWrite(true);
    println("bss " + s + " len 0x" + Long.toHexString(len));
  }
}
