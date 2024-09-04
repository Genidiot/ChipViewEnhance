import ezdxf


class DxfCell:
    def __init__(self, config: ChipViewLayout):
        self.dwg = ezdxf.new(dxfversion='AC1021')
        ezdxf.setup_linetypes(self.dwg)
        self.msp = self.dwg.modelspace()
        self.config = config
        self.insert_x = {}
        self.insert_y = {}