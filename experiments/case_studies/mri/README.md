## Case study: MRI

Multi-Hop Route Inspection (MRI) allows users to track the path and the length of queues that every packet travels through.

The P4.org language consortium. 2017. MRI Exercise. https://github.com/p4lang/tutorials/blob/master/exercises/mri/mri.p4. (2017).

### Annotated assertions

| Assertion | Property |
| --------- | -------- |
| <> | <> |

### Verifying MRI

From the root directory of `assert-p4`:

```
bash assert-p4.sh experiments/case_studies/mri/mri.p4
```

From inside this folder:
```
p4c-bm2-ss mri.p4 --toJSON mri.json
python src/P4_to_C.py mri.json 
clang -emit-llvm -g -c mri.c
klee --search=dfs --no-output --optimize mri.bc
```

#### Expected output

<>