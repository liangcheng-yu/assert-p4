import json
import sys
import Node
import C_translation
import parse_forwarding_rules

from os.path import splitext, basename

with open(sys.argv[1]) as data_file:    
    program = json.load(data_file)

forwardingRulesProvided = (len(sys.argv) > 2)
if forwardingRulesProvided:
    forwardingRules = parse_forwarding_rules.parse(sys.argv[2])
else:
    forwardingRules = None

model = C_translation.run(Node.NodeFactory(program), forwardingRules)
model = C_translation.post_processing(model)

#Print output to file
p4_program_name = splitext(basename(sys.argv[1]))[0]
assert_p4_outfile = "{}.c".format(p4_program_name)

with open(assert_p4_outfile, "w") as output:
    output.write(model)