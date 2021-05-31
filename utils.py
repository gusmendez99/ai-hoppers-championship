import xmltodict

"""
    A new move represented in XML:
    <move>
        <from row="1" col="8"/>
        <to row="8" col="7"/>
    </move>
"""
  
def to_xml(move):
    xml_data = {
        'move': {
            'from': {
                '@row': move['from'][0],
                '@col': move['from'][1],
            },
            'to': {
                '@row': move['to'][0],
                '@col': move['to'][1],
           },
        }
    }

    xml = xmltodict.unparse(xml_data, pretty = True)
    return xml

def from_xml(move_str):
    original_xml = xmltodict.parse(move_str)
    move_info = original_xml['move']
    return move_info