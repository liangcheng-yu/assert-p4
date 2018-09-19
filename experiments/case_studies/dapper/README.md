## Case study: Dapper

Dapper is a data plane performance diagnosis tool that infers TCP bottlenecks by analyzing packets in real time.

Mojgan Ghasemi, Theophilus Benson, and Jennifer Rexford. 2017. Dapper: Data Plane Performance Diagnosis of TCP. In _Proceedings of the Symposium on SDN Research (SOSR ’17)_. ACM, New York, NY, USA, 61–74. https://doi.org/10.1145/3050220.3050228

### Annotated assertions

| Assertion | Property |
| --------- | -------- |
| if(hdr.tcp.ack, traverse<sup>1</sup>) | Load flow registers when is Ack packet |
| if(meta.stats_metadata.dupack < 3, !traverse) | TODO: |
| if(hdr.ipv4.ttl == 0, !forward) | Don't forward IPv4 packets if the TTL field is zero |
| constant(hdr.tcp.dstPort)<sup>2</sup> | TCP destination port does not change |

<sup>1</sup>Inside path that load registers.

<sup>2</sup>There is a similar `constant` assertion for all TCP fields. For brevity, these are omitted in this table.

### Verifying Dapper

From the root directory of `assert-p4`:

```
bash assert-p4.sh experiments/case_studies/dapper/dapper.p4
```

From inside this folder:
```
p4c-bm2-ss dapper.p4 --toJSON dapper.json
python src/P4_to_C.py dapper.json 
clang -emit-llvm -g -c dapper.c
klee --search=dfs --no-output --optimize dapper.bc
```

#### Expected output

```
Assertion error: !(hdr_ipv4_ttl_eq_0_522866) || (!assert_forward)
```