## Case study: Timestamp switching

This application is a demo showing the use of programmable data plane to obtain "clean" video switching of (pre-standard) SMPTE ST 2110-20 uncompressed HD video flows based on the RTP timestamp.

Tomas G. Edwards and Nick Ciarleglio. 2017. Timestamp-Aware RTP Video Switching Using Programmable Data Plan. Industrial Demo. In _ACM SIGCOMM_.

### Annotated assertions

| Assertion | Property |
| --------- | -------- |
| if(forward && hdr.ipv4.dstAddr == 4009820417, !(hdr.rtp.timestamp == 3 || hdr.rtp.timestamp == 4)) | <> |

#### Expected output

The annotated assertion is not violated in any execution path. For this reason, no message is outputed by our tool.