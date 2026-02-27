import gdb
import collections
import time

class GDBProfiler(gdb.Command):
    """Simple GDB Profiler: Samples the call stack to find bottlenecks."""
    
    def __init__(self):
        super(GDBProfiler, self).__init__("profile-start", gdb.COMMAND_USER)
        self.samples = collections.Counter()

    def invoke(self, arg, from_tty):
        print("🚀 Starting Profiler... Run your program. Press Ctrl+C to stop.")
        try:
            while True:
                # Get the current frame (where the CPU is right now)
                try:
                    frame = gdb.selected_frame()
                    if frame:
                        func_name = frame.name() or "unknown"
                        self.samples[func_name] += 1
                except gdb.error:
                    pass
                
                # Resume execution briefly
                gdb.execute("continue", to_string=True)
                time.sleep(0.01) # Sample every 10ms
                
        except KeyboardInterrupt:
            self.report()

    def report(self):
        print("\n--- 📊 Profiler Report ---")
        total = sum(self.samples.values())
        if total == 0:
            print("No samples collected.")
            return
            
        for func, count in self.samples.most_common(10):
            percentage = (count / total) * 100
            print(f"{func:25} : {percentage:.2f}% ({count} samples)")

# Register the command with GDB
GDBProfiler()
