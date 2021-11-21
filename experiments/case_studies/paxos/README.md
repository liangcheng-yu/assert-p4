## Case study: NetPaxos

NetPaxos is a network-based implementation of the Paxos consensus protocol. There are two different types of P4 programs in this application, one for Leaders/Coordinators and another for Acceptors. All the other actors are assumed to be entirely implemented in end hosts.

Here, we study the NetPaxos Leader P4 program.

Huynh Tu Dang, Marco Canini, Fernando Pedone, and Robert Soulé. 2016. Paxos Made Switch-y. _SIGCOMM Comput. Commun. Rev._ 46, 2 (May 2016), 18–24. https://doi.org/10.1145/2935634.2935638

### Annotated assertions

| Assertion | Property |
| --------- | -------- |
| if(traverse<sup>1</sup>, hdr.paxos.msgtype == 2) | Leader increases round number at each instance |
| if(traverse<sup>2</sup>, !forward) | Packets set to drop while resetting the instance should not be forwarded |

<sup>1</sup>At the `increase_instance` action.

<sup>2</sup>At the `reset_instance` action.

#### Expected output

```
Assertion error: !(traverse_179492) || (hdr_paxos_msgtype_eq_2_179492)
Assertion error: !(traverse_179565) || (!assert_forward)
```