2>c-b-20000.stderr python src/c-b.py --N 100 --M 20 --n 20000 --iterations 3 | tee c-b-20000.stdout;
2>c-b_mod-20000.stderr python src/c-b_mod.py --N 100 --M 20 --n 20000 --iterations 3 | tee c-b_mod-20000.stdout;
2>c-a-20000.stderr python src/c-a.py --N 100 --M -1 --n 20000 --iterations 3 | tee c-a-20000.stdout;
