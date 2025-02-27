#include <core.p4>
#include <v1model.p4>

header ethernet_t {
    bit<48> dstAddr;
    bit<48> srcAddr;
    bit<16> etherType;
}

header ipv4_t {
    bit<4>  version;
    bit<4>  ihl;
    bit<8>  diffserv;
    bit<16> totalLen;
    bit<16> identification;
    bit<3>  flags;
    bit<13> fragOffset;
    bit<8>  ttl;
    bit<8>  protocol;
    bit<16> hdrChecksum;
    bit<32> srcAddr;
    bit<32> dstAddr;
}

header rtp_t {
    bit<2>  version;
    bit<1>  padding;
    bit<1>  extension;
    bit<4>  CSRC_count;
    bit<1>  marker;
    bit<7>  payload_type;
    bit<16> sequence_number;
    bit<32> timestamp;
    bit<32> SSRC;
}

header udp_t {
    bit<16> srcPort;
    bit<16> dstPort;
    bit<16> hdr_length;
    bit<16> checksum;
}

struct metadata {
}

struct headers {
    @name(".ethernet") 
    ethernet_t ethernet;
    @name(".ipv4") 
    ipv4_t     ipv4;
    @name(".rtp") 
    rtp_t      rtp;
    @name(".udp") 
    udp_t      udp;
}

parser ParserImpl(packet_in packet, out headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {
    @name(".parse_ethernet") state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            16w0x800: parse_ipv4;
            default: accept;
        }
    }
    @name(".parse_ipv4") state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition select(hdr.ipv4.protocol) {
            8w0x11: parse_udp;
            default: accept;
        }
    }
    @name(".parse_rtp") state parse_rtp {
        packet.extract(hdr.rtp);
        transition accept;
    }
    @name(".parse_udp") state parse_udp {
        packet.extract(hdr.udp);
        transition parse_rtp;
    }
    @name(".start") state start {
        transition parse_ethernet;
    }
}

control egress(inout headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {
    apply {
    }
}

control ingress(inout headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {
    //@name(".my_direct_counter") direct_counter(CounterType.bytes) my_direct_counter;
    @name(".take_video") action take_video(bit<32> dst_ip) {
        standard_metadata.egress_spec = 9w1;
        hdr.ipv4.dstAddr = dst_ip;
    }
    @name("._drop") action _drop() {
        mark_to_drop();
    }
    /*@name(".take_video_0") action take_video_0(bit<32> dst_ip) {
        my_direct_counter.count();
        standard_metadata.egress_spec = 9w1;
        hdr.ipv4.dstAddr = dst_ip;
    }*/
    /*@name("._drop_0") action _drop_0() {
        my_direct_counter.count();
        mark_to_drop();
    }*/
    //TODO-v2: Process case where assertions are inserted before table declarations
    //@assert("if(forward && hdr.ipv4.dstAddr == 4009820417, !(hdr.rtp.timestamp == 3 || hdr.rtp.timestamp == 4))")
    table schedule_table {
        actions = {
            take_video;
            _drop;
        }
        key = {
            hdr.ipv4.dstAddr : exact;
            //ASSERT-P4: Modified to use a supported match type
            //hdr.rtp.timestamp: range;
            hdr.rtp.timestamp: exact;
        }
        size = 16384;
        @name(".my_direct_counter") counters = direct_counter(CounterType.bytes);
    }
    apply 
    @assert("if(forward && hdr.ipv4.dstAddr == 4009820417, !(hdr.rtp.timestamp == 3 || hdr.rtp.timestamp == 4))")
    {
        schedule_table.apply();
    }
}

control DeparserImpl(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.udp);
        packet.emit(hdr.rtp);
    }
}

control verifyChecksum(inout headers hdr, inout metadata meta) {
    apply {
    }
}

control computeChecksum(inout headers hdr, inout metadata meta) {
    apply {
    }
}

V1Switch(ParserImpl(), verifyChecksum(), ingress(), egress(), computeChecksum(), DeparserImpl()) main;
