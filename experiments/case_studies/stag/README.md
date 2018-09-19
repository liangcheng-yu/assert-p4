## Case study: Stag

Stag is a P4 program that adds a security tag in packets - routers can add a security tag that is carried internally and stripped before leaving the network.

George Varghese, Nuno Lopes, Nikolaj Bjorner, Andrey Rybalchenko, Nick McKeown, Dan Talayco. 2016. _Automatically verifying reachability and well-formedness in P4 Networks_. Technical Report. https://www.microsoft.com/en-us/research/publication/automatically-verifying-reachability-well-formedness-p4-networks

### Annotated assertions

| Assertion | Property |
| --------- | -------- |
| if(standard_metadata.ingress_port == 1 && hdr.ipv4.dstAddr == 167772162, !forward)<sup>1</sup> | Hosts connected to ports of different colors cannot commnunicate |

<sup>1</sup>The ingress port is assigned to a color A while the IPv4 destination address is assigned to a color B


### Verifying Stag

From the root directory of `assert-p4`:

```
bash assert-p4.sh experiments/case_studies/stag/stag.p4
```

From inside this folder:
```
p4c-bm2-ss stag.p4 --toJSON stag.json
python src/P4_to_C.py stag.json 
clang -emit-llvm -g -c stag.c
klee --search=dfs --no-output --optimize stag.bc
```

#### Expected output

```
Assertion error: !((standard_metadata_ingress_port_eq_1_160337) && (hdr_ipv4_dstAddr_eq_2_160337)) || (!assert_forward)
```