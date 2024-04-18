PYTHON := python3
all-exp-same-num-stepss: exp-same-num-steps/1.touch exp-same-num-steps/8.touch exp-same-num-steps/16.touch exp-same-num-steps/32.touch exp-same-num-steps/64.touch exp-same-num-steps/128.touch exp-same-num-steps/256.touch exp-same-num-steps/1024.touch exp-same-num-steps/2048.touch exp-same-num-steps/4096.touch

exp-same-num-steps/4096.touch: exp-same-num-steps/4096/0 exp-same-num-steps/4096/1 exp-same-num-steps/4096/2 exp-same-num-steps/4096/3 exp-same-num-steps/4096/4

exp-same-num-steps/4096/0:
	$(PYTHON) src/baseline_same_num_steps.py --run-name 0 --fold 0 --batch-size 4096
exp-same-num-steps/4096/1:
	$(PYTHON) src/baseline_same_num_steps.py --run-name 1 --fold 1 --batch-size 4096
exp-same-num-steps/4096/2:
	$(PYTHON) src/baseline_same_num_steps.py --run-name 2 --fold 2 --batch-size 4096
exp-same-num-steps/4096/3:
	$(PYTHON) src/baseline_same_num_steps.py --run-name 3 --fold 3 --batch-size 4096
exp-same-num-steps/4096/4:
	$(PYTHON) src/baseline_same_num_steps.py --run-name 4 --fold 4 --batch-size 4096

exp-same-num-steps/2048.touch: exp-same-num-steps/2048/0 exp-same-num-steps/2048/1 exp-same-num-steps/2048/2 exp-same-num-steps/2048/3 exp-same-num-steps/2048/4

exp-same-num-steps/2048/0:
	$(PYTHON) src/baseline_same_num_steps.py --run-name 0 --fold 0 --batch-size 2048
exp-same-num-steps/2048/1:                                          
	$(PYTHON) src/baseline_same_num_steps.py --run-name 1 --fold 1 --batch-size 2048
exp-same-num-steps/2048/2:                                          
	$(PYTHON) src/baseline_same_num_steps.py --run-name 2 --fold 2 --batch-size 2048
exp-same-num-steps/2048/3:                                          
	$(PYTHON) src/baseline_same_num_steps.py --run-name 3 --fold 3 --batch-size 2048
exp-same-num-steps/2048/4:                                          
	$(PYTHON) src/baseline_same_num_steps.py --run-name 4 --fold 4 --batch-size 2048

exp-same-num-steps/1024.touch: exp-same-num-steps/1024/0 exp-same-num-steps/1024/1 exp-same-num-steps/1024/2 exp-same-num-steps/1024/3 exp-same-num-steps/1024/4

exp-same-num-steps/1024/0:
	$(PYTHON) src/baseline_same_num_steps.py --run-name 0 --fold 0 --batch-size 1024
exp-same-num-steps/1024/1:                                          
	$(PYTHON) src/baseline_same_num_steps.py --run-name 1 --fold 1 --batch-size 1024
exp-same-num-steps/1024/2:                                          
	$(PYTHON) src/baseline_same_num_steps.py --run-name 2 --fold 2 --batch-size 1024
exp-same-num-steps/1024/3:                                          
	$(PYTHON) src/baseline_same_num_steps.py --run-name 3 --fold 3 --batch-size 1024
exp-same-num-steps/1024/4:                                          
	$(PYTHON) src/baseline_same_num_steps.py --run-name 4 --fold 4 --batch-size 1024

exp-same-num-steps/512.touch: exp-same-num-steps/512/0 exp-same-num-steps/512/1 exp-same-num-steps/512/2 exp-same-num-steps/512/3 exp-same-num-steps/512/4

exp-same-num-steps/512/0:
	$(PYTHON) src/baseline_same_num_steps.py --run-name 0 --fold 0 --batch-size 512
exp-same-num-steps/512/1:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 1 --fold 1 --batch-size 512
exp-same-num-steps/512/2:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 2 --fold 2 --batch-size 512
exp-same-num-steps/512/3:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 3 --fold 3 --batch-size 512
exp-same-num-steps/512/4:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 4 --fold 4 --batch-size 512

exp-same-num-steps/256.touch: exp-same-num-steps/256/0 exp-same-num-steps/256/1 exp-same-num-steps/256/2 exp-same-num-steps/256/3 exp-same-num-steps/256/4

exp-same-num-steps/256/0:
	$(PYTHON) src/baseline_same_num_steps.py --run-name 0 --fold 0 --batch-size 256
exp-same-num-steps/256/1:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 1 --fold 1 --batch-size 256
exp-same-num-steps/256/2:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 2 --fold 2 --batch-size 256
exp-same-num-steps/256/3:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 3 --fold 3 --batch-size 256
exp-same-num-steps/256/4:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 4 --fold 4 --batch-size 256

exp-same-num-steps/128.touch: exp-same-num-steps/128/0 exp-same-num-steps/128/1 exp-same-num-steps/128/2 exp-same-num-steps/128/3 exp-same-num-steps/128/4

exp-same-num-steps/128/0:
	$(PYTHON) src/baseline_same_num_steps.py --run-name 0 --fold 0 --batch-size 128
exp-same-num-steps/128/1:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 1 --fold 1 --batch-size 128
exp-same-num-steps/128/2:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 2 --fold 2 --batch-size 128
exp-same-num-steps/128/3:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 3 --fold 3 --batch-size 128
exp-same-num-steps/128/4:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 4 --fold 4 --batch-size 128

exp-same-num-steps/64.touch: exp-same-num-steps/64/0 exp-same-num-steps/64/1 exp-same-num-steps/64/2 exp-same-num-steps/64/3 exp-same-num-steps/64/4

exp-same-num-steps/64/0:
	$(PYTHON) src/baseline_same_num_steps.py --run-name 0 --fold 0 --batch-size 64
exp-same-num-steps/64/1:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 1 --fold 1 --batch-size 64
exp-same-num-steps/64/2:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 2 --fold 2 --batch-size 64
exp-same-num-steps/64/3:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 3 --fold 3 --batch-size 64
exp-same-num-steps/64/4:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 4 --fold 4 --batch-size 64

exp-same-num-steps/32.touch: exp-same-num-steps/32/0 exp-same-num-steps/32/1 exp-same-num-steps/32/2 exp-same-num-steps/32/3 exp-same-num-steps/32/4

exp-same-num-steps/32/0:
	$(PYTHON) src/baseline_same_num_steps.py --run-name 0 --fold 0 --batch-size 32
exp-same-num-steps/32/1:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 1 --fold 1 --batch-size 32
exp-same-num-steps/32/2:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 2 --fold 2 --batch-size 32
exp-same-num-steps/32/3:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 3 --fold 3 --batch-size 32
exp-same-num-steps/32/4:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 4 --fold 4 --batch-size 32

exp-same-num-steps/16.touch: exp-same-num-steps/16/0 exp-same-num-steps/16/1 exp-same-num-steps/16/2 exp-same-num-steps/16/3 exp-same-num-steps/16/4

exp-same-num-steps/16/0:
	$(PYTHON) src/baseline_same_num_steps.py --run-name 0 --fold 0 --batch-size 16
exp-same-num-steps/16/1:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 1 --fold 1 --batch-size 16
exp-same-num-steps/16/2:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 2 --fold 2 --batch-size 16
exp-same-num-steps/16/3:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 3 --fold 3 --batch-size 16
exp-same-num-steps/16/4:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 4 --fold 4 --batch-size 16

exp-same-num-steps/8.touch: exp-same-num-steps/8/0 exp-same-num-steps/8/1 exp-same-num-steps/8/2 exp-same-num-steps/8/3 exp-same-num-steps/8/4

exp-same-num-steps/8/0:
	$(PYTHON) src/baseline_same_num_steps.py --run-name 0 --fold 0 --batch-size 8
exp-same-num-steps/8/1:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 1 --fold 1 --batch-size 8
exp-same-num-steps/8/2:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 2 --fold 2 --batch-size 8
exp-same-num-steps/8/3:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 3 --fold 3 --batch-size 8
exp-same-num-steps/8/4:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 4 --fold 4 --batch-size 8

exp-same-num-steps/1.touch: exp-same-num-steps/1/0 exp-same-num-steps/1/1 exp-same-num-steps/1/2 exp-same-num-steps/1/3 exp-same-num-steps/1/4

exp-same-num-steps/1/0:
	$(PYTHON) src/baseline_same_num_steps.py --run-name 0 --fold 0 --batch-size 1
exp-same-num-steps/1/1:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 1 --fold 1 --batch-size 1
exp-same-num-steps/1/2:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 2 --fold 2 --batch-size 1
exp-same-num-steps/1/3:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 3 --fold 3 --batch-size 1
exp-same-num-steps/1/4:                                           
	$(PYTHON) src/baseline_same_num_steps.py --run-name 4 --fold 4 --batch-size 1
