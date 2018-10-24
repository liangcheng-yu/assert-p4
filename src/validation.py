#!/usr/bin/env python2

from json import load as load_json
from os import path
from P4_to_C import run as p4_to_c

MAX_TEST_CASES = 10
P4PKTGEN_OUTFILE = 'test-cases.json'
ASSERTP4_JSON_FILE = 'stag-assertp4.json'

def hexchar_to_binstr(hexchar):
    return '{0:04b}'.format(int(hexchar, 16))

class Validator:

    def __init__(self):
        self.p4pktgen_in_json = ''
        self.assertp4_in_json = ASSERTP4_JSON_FILE
        self.p4pktgen_outfile = P4PKTGEN_OUTFILE
        self.max_test_cases = MAX_TEST_CASES

        self.test_cases = []
        self.p4_program_name = path.splitext(path.basename(self.assertp4_in_json))[0]
        self.structs = {}
        self.hdr_extractors = {}
        self.hdr_emitters = {}

    def run(self):
        self.parse_p4pktgen_output()
        self.generate_commands_txt()
        self.generate_c_models()

    def parse_p4pktgen_output(self):
        '''
        Parses the JSON output of p4pktgen pointed by 'p4pktgen_outfile'
        '''
        with open(self.p4pktgen_outfile) as p4pktgen_out:
            test_cases = load_json(p4pktgen_out)
            count = 0

            for case in test_cases:
                if case['result'] == 'NO_PACKET_FOUND': continue
                if count >= self.max_test_cases: break

                saved_test = {}
                saved_test['id'] = count
                saved_test['result'] = case['result']
                saved_test['commands'] = case['ss_cli_setup_cmds']

                saved_test['packet'] = case['input_packets'][0]
                saved_test['packet']['packet_binstr'] = ''
                for i in range(len(saved_test['packet']['packet_hexstr'])):
                    saved_test['packet']['packet_binstr'] += \
                        hexchar_to_binstr(saved_test['packet']['packet_hexstr'][i])

                saved_test['parser_path'] = []
                for i in range(len(case['parser_path'])):
                    src, _, dst = case['parser_path'][i].split()
                    if i == 0: 
                        saved_test['parser_path'].append(src)
                        saved_test['parser_path'].append(dst)
                    else:
                        saved_test['parser_path'].append(dst)

                self.test_cases.append(saved_test)
                count += 1

    def generate_commands_txt(self):
        '''
        Writes the commands.txt files based on the test cases from p4pktgen
        '''
        for test_case in self.test_cases:
            test_case['cmdfile'] = 'commands{}.txt'.format(test_case['id'])
            with open(test_case['cmdfile'], 'w') as f:
                for cmd in test_case['commands']:
                    f.write('{}\n'.format(cmd))
                f.close()

    def generate_c_models(self):
        '''
        Generates the C model of the P4 program with an input packet set.
        '''
        for test_case in self.test_cases:
            test_case['c_model'] = '{}{}.c'.format(self.p4_program_name, test_case['id'])
            p4_to_c(self.assertp4_in_json, test_case['cmdfile'], test_case['c_model'])

            lines = []
            with open(test_case['c_model'], 'r+') as c_model:
                lines = c_model.readlines()

            # add include for 'memcpy'
            lines.insert(1, '#include<string.h> // [VALIDATION]\n')
            # add include for validation functions
            lines.insert(1, '#include "validation.h" // [VALIDATION]\n')

            # lines to be inserted into 'ParserImpl'
            memset1 = '\tmemset(&hdr, 0, sizeof(headers));\n'
            memset2 = '\tmemset(&meta, 0, sizeof(metadata));\n'
            memset3 = '\tmemset(&standard_metadata, 0, sizeof(standard_metadata_t));\n'
            port = '\tstandard_metadata.ingress_port = {};\n'.format(
                test_case['packet']['port']
            )
            packet_len = '\tstandard_metadata.packet_length = {};\n'.format(
                test_case['packet']['packet_len_bytes']
            )
            validation_lines = [memset1, memset2, memset3, port, packet_len]

            # erase all contents of the file and rewrite it while adding the input packet
            with open(test_case['c_model'], 'w') as c_model:
                inside_ParserImpl = False
                packet_inserted = False
                
                line = 0
                while line < len(lines):
                    # parse each header field for future processing
                    if 'typedef struct {' in lines[line]:
                        self.parse_struct(lines, line)

                    # create functions to fill header with information from input packets
                    if '//Extract ' in lines[line]:
                        self.place_hdr_extraction(lines, line)

                    # create functions to "emit" output packet
                    if '//Emit ' in lines[line]:
                        self.place_hdr_emitter(lines, line)

                    # TODO: place function to print output packet

                    # comment out unnecessary klee calls
                    if 'klee_print_once' in lines[line]:
                        lines[line] = '// {}'.format(lines[line])
                        lines.insert(line+1, '\tprintf("%s\\n", msg);\n')

                    if not packet_inserted:
                        # comment out 'klee_make_symbolic' calls
                        if 'klee_make_symbolic' in lines[line]:
                            lines[line] = '// {}'.format(lines[line])

                        # check if the current line is inside the 'ParserImpl' function
                        if 'void ParserImpl()' in lines[line]:
                            inside_ParserImpl = True

                        # write test packet information before 'start()' call
                        if inside_ParserImpl and 'start()' in lines[line]:
                            c_model.write('\t// [VALIDATION]\n')
                            for validation_line in validation_lines:
                                c_model.write(validation_line)
                            c_model.write('\n')
                            packet_inserted = True
                    
                    c_model.write(lines[line])
                    line += 1

                # include validation functions in the C model
                self.emit_validation_functions(c_model, test_case['packet'])

                c_model.close()

        # emit header file for validation functions
        self.emit_validation_h()
        
    def parse_struct(self, lines, start):
        '''
        Parses a C struct.

        Parameters
        ----------
        lines : string array
            lines of the C program

        start : integer
            line where the struct definition begins (index of `lines`)
        '''
        struct = []
        name = ''
        i = start+1
        finished = False

        while not finished:
            # each line will be either
            #   <type> <field_name>[ : <size_in_bits>];\n 
            # OR
            #   } <struct_name>;\n
            tokens = lines[i][:-2].split() # ignore ';\n'

            # end of struct
            if tokens[0] == '}':
                finished = True
                name = tokens[1]
            
            # field definition
            else:
                type_ = tokens[0]
                name_ = tokens[1]

                grouped_colon = name_[-1] == ':'
                
                field = {}
                field['name'] = name_ if not grouped_colon else name_[:-1]
                field['type'] = type_

                # <type> <field_name>: <size_in_bits>
                if grouped_colon:
                    field['bitsize'] = int(tokens[2])
                # <type> <field_name> : <size_in_bits>
                elif len(tokens) >= 4:
                    field['bitsize'] = int(tokens[3])
                else:
                    field['bitsize'] = 0

                struct.append(field)

            i += 1       

        self.structs[name] = struct     

    def place_hdr_extraction(self, lines, pos):
        '''
        Place the C function to fill the header variables based on the input packet.

        Parameters
        ----------
        lines : string array
            lines of the C program

        pos : integer
            index of `lines` where '//Extract [...]' line is located    
        '''
        # '//Extract hdr.<hdr_name>'
        tokens = lines[pos].split()
        hdr_variable = tokens[1]
        _, hdr_name = hdr_variable.split('.')

        # insert line to call header extractor function
        caller_name = 'v_set_packet_fields_{}'.format(hdr_name)
        lines.insert(pos+1, '\t{}(); // [VALIDATION]\n\n'.format(caller_name))

        # no need to redefine the header extractor funcion
        if hdr_name in self.hdr_extractors: return
        
        # gets the type of the header defined as `hdr_name`
        hdr_type = next((hdr for hdr in self.structs['headers'] \
            if hdr['name'] == hdr_name))['type']

        header_fields = self.structs[hdr_type]

        # defining the function that will get the field values from the input packet
        definition = 'void {}()'.format(caller_name)
        function = '{} {}\n'.format(definition, '{')

        for i in range(len(header_fields)):
            field = header_fields[i]
            if field['name'] == 'isValid': continue

            assignment = '\thdr.{}.{} = v_get_value_from_packet({} {});\n'.format(
                hdr_name, field['name'], '(uint64_t)', field['bitsize']
            )

            function += assignment

        function += '}'
        self.hdr_extractors[hdr_name] = definition, function

    def place_hdr_emitter(self, lines, pos):
        '''
        Place the C functions to "emit" the output packet after processing the input 
        packet

        Parameters
        ----------
        lines : string array
            lines of the C program

        pos : integer
            index of `lines` where '//Emit [...]' line is located    
        '''
        # '//Emit hdr.<hdr_name>'
        tokens = lines[pos].split()
        hdr_variable = tokens[1]
        _, hdr_name = hdr_variable.split('.')

        # insert line to call header emitter function
        caller_name = 'v_emit_header_{}'.format(hdr_name)
        lines.insert(pos+1, '\t{}(); // [VALIDATION]\n\n'.format(caller_name))

        # no need to redefine the header emitter funcion
        if hdr_name in self.hdr_emitters: return
        
        # gets the type of the header defined as `hdr_name`
        hdr_type = next((hdr for hdr in self.structs['headers'] \
            if hdr['name'] == hdr_name))['type']

        header_fields = self.structs[hdr_type]

        # defining the function that will set the header values on the output packet
        definition = 'void {}()'.format(caller_name)
        function = '{} {}\n'.format(definition, '{')
        function += '\tif (hdr.{}.isValid != 1) return;\n\n'.format(hdr_name)

        # TODO: create logic
        # for i in range(len(header_fields)):
        #     field = header_fields[i]
        #     if field['name'] == 'isValid': continue

        #     emitter = '\thdr.{}.{} = v_add_value_to_packet({} {});\n'.format(
        #         hdr_name, field['name'], '(uint64_t)', field['bitsize']
        #     )

        #     function += emitter

        function += '}'
        self.hdr_emitters[hdr_name] = definition, function
  
    def emit_validation_functions(self, c_model, packet):
        '''
        Writes into the C model the helper functions for test packet processing

        Parameters
        ----------
        c_model : file descriptor
            file descriptor of the C model being generated
        
        packet : dict
            input packet parsed from the p4pktgen output
        '''
        c_model.write('\n// [VALIDATION]\n')

        # helper variables
        c_model.write('char* v_input_packet = "{}";\n'.format(packet['packet_binstr']))
        c_model.write('uint64_t v_input_packet_offset = 0;\n\n')
        # TODO: packet emitting variables

        # packet parser function
        c_model.write('uint64_t v_get_value_from_packet(uint64_t n_bits) {\n')
        c_model.write('\tchar* start = &v_input_packet[v_input_packet_offset];\n')
        c_model.write('\tuint64_t count = 0;\n')
        c_model.write('\tuint64_t result = 0;\n')
        c_model.write('\twhile (count < n_bits) {\n')
        c_model.write('\t\tif (v_input_packet_offset >= strlen(v_input_packet)) break;\n')
    	c_model.write('\t\tresult <<= 1;\n')
        c_model.write('\t\tif (*start++ == \'1\') result ^= 1;\n')
    	c_model.write('\t\tcount++;\n')
    	c_model.write('\t\tv_input_packet_offset++;\n')
        c_model.write('\t}\n')
        c_model.write('\treturn result;\n')
        c_model.write('}\n\n')

        # header extraction functions
        for function in self.hdr_extractors.values():
            c_model.write('{}\n\n'.format(function[1]))

        # header emitting functions
        for function in self.hdr_emitters.values():
            c_model.write('{}\n\n'.format(function[1]))

        # TODO: output packet printer function

    def emit_validation_h(self):
        '''
        Creates a file called 'validation.h' which contain the definition of helper 
        functions for test packet processing
        '''
        with open('validation.h', 'w') as h:
            h.write('#include<stdint.h>\n\n')
            h.write('uint64_t v_get_value_from_packet(uint64_t n_bits);\n')
            for function in self.hdr_extractors.values():
                h.write('{};\n'.format(function[0]))
            for function in self.hdr_emitters.values():
                h.write('{};\n'.format(function[0]))
            h.close()

if __name__ == '__main__':
    validator = Validator()
    validator.run()