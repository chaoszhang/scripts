import sys

print("begin paup;")
print("exec " + sys.argv[1] + ";")
print("svdquartets nthreads=64 evalQuartets=all seed=5000;")
print("savetrees file=" + sys.argv[2] + " replace=yes format=altnex;")
print("quit;")
print("end;")