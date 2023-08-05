from vialactea.sirius import *

log = report()
bifrost = bifrost()
tools = bifrost.tools()

bifrost.set_value('paths', {})

bifrost.set_path({'MSQL': f'{VIALACTEA_DIRECTORY}MSQL/'})
bifrost.set_path({'xml': f'{VIALACTEA_DIRECTORY}xml/'})
bifrost.set_path({'xml_pool': f'{VIALACTEA_DIRECTORY}xml_pool/'})
bifrost.set_path({'xml_pool_update': f'{VIALACTEA_DIRECTORY}xml_pool_update/'})
bifrost.set_path({'log': f'{VIALACTEA_DIRECTORY}log/'})
bifrost.set_path({'documents': f'{C_USER}/Documents/VIALACTEA/'})

bifrost.check_paths()
