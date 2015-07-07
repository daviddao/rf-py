# rf-py
RF Opt Algorithm as stand-alone program in Python.
RF-Optimizer is a program for evolutionary analysis of large datasets. 
Given a large evolutionary tree topology, 
it uses a large set of smaller tree topologies to analyse the plausibility of the large tree and proposes corrections as a listing of 
"weak" taxa. A high score for a taxa set stands for low plausibility.

### Dependencies 
- Python3
- bitarray module
- numpy module

### Current Workflow (will be edited, before production-ready)

- Use RAxML fast plausibility to extract all small bipartitions and induced bipartitions

```ssh
raxmlHPC -f R -m GTRCAT -t largetree -z referencetrees -n T1
```

- This will automatically save the results in a file called bips.txt

- In rf-opt.py, edit the settings

```python
rf_optimize(starting_tree, end_tree, "path/to/your/raxml-bips")

# Example usage:
rf_optimize(10000, 10020, "bips.txt")
```

- Start the algorithm with

```ssh
python rf-opt.py
```

- All results will be saved in a file called scoring.txt

