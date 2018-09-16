#define BITSLICE(x, a, b) ((x) >> (b)) & ((1 << ((a)-(b)+1)) - 1)
#include<stdio.h>
#include<stdint.h>
#include<stdlib.h>

int assert_forward = 1;
int action_run;

void end_assertions();


 int standard_metadata_ingress_port_eq_1_136804;

 int hdr_ipv4_dstAddr_eq_2_136804;

void NoAction_6_136435();
void set_local_dest_0_136518();
void get_source_color_136470();
void forward_136646();
void set_source_color_0_136452();
void place_holder_table_136831();
void core_pass_through_0_136629();
void color_check_136707();
void accept();
void start();
void NoAction_7_136830();
void set_remote_dest_0_136551();
void NoAction_0_136424();
void parse_ipv4_option();
void reject();
void NoAction_1_136434();
void parse_ipv4();
void drop_0_136436();
void parse_stag();

typedef struct {
	uint32_t ingress_port : 9;
	uint32_t egress_spec : 9;
	uint32_t egress_port : 9;
	uint32_t clone_spec : 32;
	uint32_t instance_type : 32;
	uint8_t drop : 1;
	uint32_t recirculate_port : 16;
	uint32_t packet_length : 32;
	uint32_t enq_timestamp : 32;
	uint32_t enq_qdepth : 19;
	uint32_t deq_timedelta : 32;
	uint32_t deq_qdepth : 19;
	uint64_t ingress_global_timestamp : 48;
	uint32_t lf_field_list : 32;
	uint32_t mcast_grp : 16;
	uint8_t resubmit_flag : 1;
	uint32_t egress_rid : 16;
	uint8_t checksum_error : 1;
} standard_metadata_t;

void mark_to_drop() {
	assert_forward = 0;
	end_assertions();
	exit(0);
}

typedef uint64_t macAddr_t;

typedef uint32_t ip4Addr_t;

typedef struct {
	uint8_t isValid : 1;
	macAddr_t dstAddr: 48;
	macAddr_t srcAddr: 48;
	uint32_t etherType : 16;
} ethernet_t;

typedef struct {
	uint8_t isValid : 1;
	uint8_t version : 4;
	uint8_t ihl : 4;
	uint8_t diffserv : 8;
	uint32_t totalLen : 16;
	uint32_t identification : 16;
	uint8_t flags : 3;
	uint32_t fragOffset : 13;
	uint8_t ttl : 8;
	uint8_t protocol : 8;
	uint32_t hdrChecksum : 16;
	ip4Addr_t srcAddr: 32;
	ip4Addr_t dstAddr: 32;
} ipv4_t;

typedef struct {
	uint8_t isValid : 1;
	uint8_t copyFlag : 1;
	uint8_t optClass : 2;
	uint8_t option : 5;
	uint8_t optionLength : 8;
} ipv4_option_t;

typedef struct {
	uint8_t isValid : 1;
	uint8_t source_color : 8;
} stag_t;

typedef struct {
	uint8_t isValid : 1;
	uint8_t src_port_color : 8;
	uint8_t dst_port_color : 8;
	uint8_t toLocal : 1;
} local_md_t;

typedef struct {
	local_md_t local_md;
} metadata;

typedef struct {
	ethernet_t ethernet;
	ipv4_t ipv4;
	ipv4_option_t ipv4_option;
	stag_t stag;
} headers;

headers hdr;
metadata meta;
standard_metadata_t standard_metadata;


void start() {
	//Extract hdr.ethernet
	hdr.ethernet.isValid = 1;
	if((hdr.ethernet.etherType == 2048)){
		parse_ipv4();
	} else {
		accept();
	}
}


void parse_ipv4() {
	//Extract hdr.ipv4
	hdr.ipv4.isValid = 1;
	if(hdr.ipv4.ihl >= 5) { exit(1); }
	if((hdr.ipv4.ihl == 5)){
		accept();
	} else {
		parse_ipv4_option();
	}
}


void parse_ipv4_option() {
	//Extract hdr.ipv4_option
	hdr.ipv4_option.isValid = 1;
	if((hdr.ipv4_option.option == 31)){
		parse_stag();
	} else {
		accept();
	}
}


void parse_stag() {
	//Extract hdr.stag
	hdr.stag.isValid = 1;
	meta.local_md.src_port_color = hdr.stag.source_color;
	accept();
}


void accept() {
	
}


void reject() {
	assert_forward = 0;
	end_assertions();
	exit(0);
}


void ParserImpl() {
	klee_make_symbolic(&hdr, sizeof(hdr), "hdr");
	klee_make_symbolic(&meta, sizeof(meta), "meta");
	klee_make_symbolic(&standard_metadata, sizeof(standard_metadata), "standard_metadata");

	start();
}

//Control

void ingress() {
	if(!hdr.stag.isValid) {
	get_source_color_136470();
}
	forward_136646();
	if(action_run == 136518) {
		 standard_metadata_ingress_port_eq_1_136804 = (standard_metadata.ingress_port  ==  1);
	hdr_ipv4_dstAddr_eq_2_136804 = (hdr.ipv4.dstAddr  ==  167772162);
		color_check_136707();

	}
}

// Action
void NoAction_0_136424() {
	action_run = 136424;
	
}


// Action
void NoAction_1_136434() {
	action_run = 136434;
	
}


// Action
void NoAction_6_136435() {
	action_run = 136435;
	
}


// Action
void drop_0_136436() {
	action_run = 136436;
		mark_to_drop();

}


// Action
void set_source_color_0_136452() {
	action_run = 136452;
	uint8_t color;
	klee_make_symbolic(&color, sizeof(color), "color");
	meta.local_md.src_port_color = color;

}


// Action
void set_local_dest_0_136518() {
	action_run = 136518;
	uint32_t egr_port;
	klee_make_symbolic(&egr_port, sizeof(egr_port), "egr_port");
uint8_t color;
	klee_make_symbolic(&color, sizeof(color), "color");
	standard_metadata.egress_spec = egr_port;
	meta.local_md.dst_port_color = color;
	hdr.stag.isValid = 0;

}


// Action
void set_remote_dest_0_136551() {
	action_run = 136551;
	uint32_t egr_port;
	klee_make_symbolic(&egr_port, sizeof(egr_port), "egr_port");
	standard_metadata.egress_spec = egr_port;
	hdr.ipv4_option.isValid = 1;
	hdr.ipv4_option.copyFlag = 1;
	hdr.ipv4_option.optClass = 2;
	hdr.ipv4_option.option = 31;
	hdr.ipv4_option.optionLength = 4;
	hdr.ipv4.ihl = hdr.ipv4.ihl + 1;
	hdr.stag.isValid = 1;
	hdr.stag.source_color = meta.local_md.src_port_color;

}


// Action
void core_pass_through_0_136629() {
	action_run = 136629;
	uint32_t egr_port;
	klee_make_symbolic(&egr_port, sizeof(egr_port), "egr_port");
	standard_metadata.egress_spec = egr_port;

}


//Table
void get_source_color_136470() {
	// keys: standard_metadata.ingress_port:exact
	int symbol;
	klee_make_symbolic(&symbol, sizeof(symbol), "symbol");
	switch(symbol) {
		case 0: set_source_color_0_136452(); break;
		default: NoAction_0_136424(); break;
	}
	// default_action NoAction_0();

}


//Table
void forward_136646() {
	// keys: hdr.ipv4.dstAddr:ternary
	int symbol;
	klee_make_symbolic(&symbol, sizeof(symbol), "symbol");
	switch(symbol) {
		case 0: set_local_dest_0_136518(); break;
		case 1: set_remote_dest_0_136551(); break;
		case 2: core_pass_through_0_136629(); break;
		default: NoAction_1_136434(); break;
	}
	// size 1024
	// default_action NoAction_1();

}


//Table
void color_check_136707() {
	// keys: meta.local_md.dst_port_color:exact, meta.local_md.src_port_color:exact
	int symbol;
	klee_make_symbolic(&symbol, sizeof(symbol), "symbol");
	switch(symbol) {
		case 0: drop_0_136436(); break;
		default: NoAction_6_136435(); break;
	}
	// size 1024
	// default_action drop_0();

}



//Control

void egress() {
	place_holder_table_136831();
}

// Action
void NoAction_7_136830() {
	action_run = 136830;
	
}


//Table
void place_holder_table_136831() {
	int symbol;
	klee_make_symbolic(&symbol, sizeof(symbol), "symbol");
	switch(symbol) {
		default: NoAction_7_136830(); break;
	}
	// size 2
	// default_action NoAction_7();

}



//Control

void computeChecksum() {
	
}


//Control

void verifyChecksum() {
	
}


//Control

void DeparserImpl() {
	//Emit hdr.ethernet
	
	//Emit hdr.ipv4
	
	//Emit hdr.ipv4_option
	
	//Emit hdr.stag
	
}


int main() {
	ParserImpl();
	ingress();
	egress();
	DeparserImpl();
	end_assertions();
	return 0;
}

void assert_error(int id, char msg[]) {
	klee_print_once(id, msg);
	//klee_abort();
}

void end_assertions() {
	if (!(!((standard_metadata_ingress_port_eq_1_136804) && (hdr_ipv4_dstAddr_eq_2_136804)) || (!assert_forward)))
		assert_error(0, "Assertion error: !((standard_metadata_ingress_port_eq_1_136804) && (hdr_ipv4_dstAddr_eq_2_136804)) || (!assert_forward)");
}


