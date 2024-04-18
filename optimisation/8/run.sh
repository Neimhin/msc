# sleep  $((60 * 30))

# # # # # # a
# cmd="python src/c-a.py --N 10 --M -1 --n 500 --iterations 3"
# echo $cmd >> cmd-history
# 2>a.stderr $cmd | ts | tee a.stdout
# 
# cmd="python src/c-a.py --N 10 --M -1 --n 1000 --iterations 3"
# echo $cmd >> cmd-history
# 2>a.stderr $cmd | ts | tee a.stdout

# cmd="python src/c-a.py --N 99 --M -1 --n 1000 --iterations 1"
# echo $cmd >> cmd-history
# 2>a.stderr $cmd | ts | tee a.stdout
# 
# # # # # # # b_mod
# cmd="python src/c-b_mod.py --N 33 --M 10 --n 1000 --iterations 3"
# echo $cmd >> cmd-history
# 2>b_mod.stderr $cmd | ts | tee b_mod.stdout

cmd="python src/c-b.py --N 33 --M 10 --n 1000 --iterations 3"
echo $cmd >> cmd-history
2>b_mod.stderr $cmd | ts | tee b_mod.stdout
