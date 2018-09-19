## Case study: Timestamp switching

This application is a demo showing the use of programmable data plane to obtain "clean" video switching of (pre-standard) SMPTE ST 2110-20 uncompressed HD video flows based on the RTP timestamp.

Tomas G. Edwards and Nick Ciarleglio. 2017. Timestamp-Aware RTP Video Switching Using Programmable Data Plan. Industrial Demo. In _ACM SIGCOMM_.

### Annotated assertions

| Assertion | Property |
| --------- | -------- |
| if(forward && hdr.ipv4.dstAddr == 4009820417, !(hdr.rtp.timestamp == 3 || hdr.rtp.timestamp == 4)) | TODO: |

### Verifying Timestamp switching

From the root directory of `assert-p4`:

```
bash assert-p4.sh experiments/case_studies/ts_switching/ts_swithing-16.p4
```

From inside this folder:
```
p4c-bm2-ss ts_swithing-16.p4 --toJSON ts_swithing-16.json
python src/P4_to_C.py ts_swithing-16.json 
clang -emit-llvm -g -c ts_swithing-16.c
klee --search=dfs --no-output --optimize ts_swithing-16.bc
```

#### Expected output

The annotated assertion is not violated in any execution path. For this reason, no message is outputed by our tool.