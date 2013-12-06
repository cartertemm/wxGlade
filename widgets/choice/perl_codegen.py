# perl_codegen.py : perl generator functions for wxChoice objects
#
# Copyright (c) 2002-2004 D.H. aka crazyinsomniac on sourceforge.net
#
# License: MIT (see license.txt)
# THIS PROGRAM COMES WITH NO WARRANTY


import common
from ChoicesCodeHandler import *

class PerlCodeGenerator:
    def get_code(self, obj):
        init = []
        plgen = common.code_writers['perl']
        prop = obj.properties
        id_name, id = plgen.generate_code_id(obj)
        choices = prop.get('choices', [])

        if not obj.parent.is_toplevel:
            parent = '$self->{%s}' % obj.parent.name
        else:
            parent = '$self'

        style = prop.get("style")
        if not style:
            style = ''

        if id_name:
            init.append(id_name)

        klass = obj.base
        if klass != obj.klass:
            klass = obj.klass
        else:
            klass = klass.replace('wx', 'Wx::', 1)

        choices = ', '.join([plgen.quote_str(c) for c in choices])
        init.append('$self->{%s} = %s->new(%s, %s, wxDefaultPosition, \
wxDefaultSize, [%s], %s);\n' %
                    (obj.name, klass, parent, id, choices, style))
        props_buf = plgen.generate_common_properties(obj)

        selection = prop.get('selection')
        if selection is not None:
            props_buf.append('$self->{%s}->SetSelection(%s);\n' %
                             (obj.name, selection))

        return init, props_buf, []


# end of class PerlCodeGenerator

def initialize():
    common.class_names['EditChoice'] = 'wxChoice'

    plgen = common.code_writers.get('perl')
    if plgen:
        plgen.add_widget_handler('wxChoice', PerlCodeGenerator())
        plgen.add_property_handler('choices', ChoicesCodeHandler)
