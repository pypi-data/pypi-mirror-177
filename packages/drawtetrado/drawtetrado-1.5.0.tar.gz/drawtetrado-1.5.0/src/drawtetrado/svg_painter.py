import svgwrite
import sys
import math
from enum import Enum
import cairo
import tempfile
import json

class ConnType(Enum):
    SIMPLE = 1
    SAME_LEVEL = 2
    RIGHT = 4
    RIGHT_CROSS = 5
    LEFT = 6
    LEFT_CROSS = 7
    FRONT_BACK_CROSS = 11
    FRONT_TO_BACK = 12

    UNKNOWN = -1

class ConnFlow(Enum):
    UP = -1
    DOWN = 1
    UNKNOWN = -1.001 # different value but act as UP

class Side(Enum):
    RIGHT = 1.0
    LEFT = -1.0
    NONE = 0.0

class Point(tuple):
    def __new__(self, x = 0, y = 0):
        return tuple.__new__(Point, (x, y))

    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __add__(self, rhs):
        return Point(self.x + rhs.x, self.y + rhs.y)

    def Distance(self, point):
        return math.sqrt(pow(point.y - self.y, 2.0) +
                    pow(point.x - self.x, 2.0))


class Config:
    def __init__(self, scale = 1.0, config_path = None):
        if config_path == None:
            json_data = json.loads("{}");
        else:
            with open(config_path) as file:
                json_data = json.load(file)
        self.scale = scale if not "scale" in json_data else json_data["scale"]
        # Size parameters of the nucleotides and tetrade.
        self.longer = self.scale * (100.0 if not "nucl-longer" in json_data else json_data["nucl-longer"])
        self.shorter = self.scale * (70.0 if not "nucl-shorter" in json_data else json_data["nucl-shorter"])
        self.spacing = self.scale * (10.0 if not "nucl-spacing" in json_data else json_data["nucl-spacing"])
        self.angle = 50.0 if not "angle" in json_data else json_data["angle"]
        self.tetrade_spacing = self.scale * (50.0 if not "tetrad-spacing" in json_data else json_data["tetrad-spacing"])
        self.stroke_width = self.scale * (3.0 if not "line-stroke" in json_data else json_data["line-stroke"])
        self.point_size = self.scale * (6.0 if not "point-size" in json_data else json_data["point-size"])
        self.point_stroke = self.scale * (2.0 if not "point-stroke" in  json_data else json_data["point-stroke"])
        # Start End label (5' and 3')
        self.se_label_spacing = self.scale * (20.0 if not "se-label-spacing" in json_data else json_data["se-label-spacing"])
        self.se_label_font_size = self.scale * (24.0 if not "se-label-font-size" in json_data else json_data["se-label-font-size"])
        self.font_family = "Arial, Helvetica" if not "font-family" in json_data else json_data["font-family"]
        self.label_font_size = self.scale * (20.0 if not "nucl-font-size" in json_data else json_data["font-family"])
        self.tilted_labels = True if not "tilted-labels" in json_data else json_data["tilted-labels"]

        self.label_chain = True if not "label-chain" in json_data else json_data["label-chain"]
        self.label_nucleotide_full = True if not "label-nucl-fullname" in json_data else json_data["label-nucl-fullname"]
        self.label_nucleotide = True if not "label-nucl-name" in json_data else json_data["label-nucl-name"]
        if self.label_nucleotide == False and self.label_nucelotide_full == True:
            self.label_nucleotide_full = False
        self.label_number = True if not "label-number" in json_data else json_data["label-number"]

        self.colors = {}
        json_colors = {} if not "colors" in json_data else json_data["colors"]
        self.colors["connection"] = "#000000FF" if not "connection" in json_colors else json_colors["connection"]
        self.colors["border"] = "#E23D28FF" if not "border" in json_colors else json_colors["border"]
        self.colors["text"] = "#000000FF" if not "text" in json_colors else json_colors["text"]
        self.colors["point"] = "#FFFFFFFF" if not "point" in json_colors else json_colors["point"]
        # Those refer to the text color on the nucleotyde block.
        self.colors["anti"] = "#FFFFFFFF" if not "anti" in json_colors else json_colors["anti"]
        self.colors["syn"] = "#000000FF" if not "syn" in json_colors else json_colors["syn"]
        self.colors["n/a"] = "#606060FF" if not "n/a" in json_colors else json_colors["n/a"]
        # Those refer to the fill color on the nucleotyde block.
        # Default alpha is 85% -> D9 
        self.colors["onz_default"] = "#646464D9" if not "onz_default" in json_colors else json_colors["onz_default"]
        self.colors["o_plus"] = "#1F78B4D9" if not "o_plus" in json_colors else json_colors["o_plus"]
        self.colors["o_minus"] = "#A6CEE3D9" if not "o_minus" in json_colors else json_colors["o_minus"]
        self.colors["n_plus"] = "#33A02CD9" if not "n_plus" in json_colors else json_colors["n_plus"]
        self.colors["n_minus"] = "#B2DF8AD9" if not "n_minus" in json_colors else json_colors["n_minus"]
        self.colors["z_plus"] = "#FF7F00D9" if not "z_plus" in json_colors else json_colors["z_plus"]
        self.colors["z_minus"] = "#FDBF6FD9" if not "z_minus" in json_colors else json_colors["z_minus"]
        # Allow for ONZ colors above to be overriden if necessary for 
        # individual nucleotides
        # "nucl.full_name": "RGBA"
        self.nucl_colors = {} if not "nucl-color-override" in json_data else json_data["nucl-color-override"]

class SvgMaker:
    def PrepareMarker(self):
        arrowhead = self.svg.marker(insert = (7.6, 4.1), size = (8.0, 6.4), \
                orient = "auto", markerUnits = "strokeWidth", id = "arrowhead")
        arrowhead.add(self.svg.polyline([(0.8, 1.6), (7.6, 4.1), (0.8, 6.4)], \
            stroke = "none", fill = self.GetColor("connection"), \
            fill_opacity = self.GetAlpha("connection")))
        self.svg.defs.add(arrowhead)

    def GetCanvasSize(self, padding, height, width):
        return Point(width + padding * 2, padding + height)


    def __init__(self, config, file_path, quadruplex):
        self.config = config
        self.quadruplex = quadruplex
        sin_val = math.sin(math.radians(config.angle))
        cos_val = math.cos(math.radians(config.angle))

        padding = (config.longer + config.shorter + config.spacing) * sin_val
        padding *= max(len(quadruplex.tetrads) / 5.0, 1.0)
        width = (config.longer + config.shorter + config.spacing) * (cos_val + 1)
        height = ((config.longer + config.shorter + config.spacing) * sin_val + \
                   config.tetrade_spacing) * len(quadruplex.tetrads)

        self.cairo_tempfile = tempfile.NamedTemporaryFile(suffix=".svg")
        self.svg = svgwrite.Drawing(file_path, size = self.GetCanvasSize(padding, height, width), \
                profile = "full")
        self.PrepareMarker()
        self.base_shift = Point(padding, padding * 0.5 + height)

    def ShiftCoords(self, coords, shift):
        if type(coords) == list:
            shifted = []
            for coord in coords:
                shifted.append(coord + shift)
            return shifted
        else:
            return coords + shift

    def RGBAtoAlpha(self, rgba, def_alpha = 0.85):
        if rgba != None and len(rgba[7:9]) == 2:
            return float(int(rgba[7:9], 16)) / 255.0
        return def_alpha

    def RGBAtoRGB(self, rgba):
        return rgba[0:7]

    # Only used for ONZ nucleotide fill or override of the color.
    # Default opacity is 0.85
    def GetAlpha(self, name):
        return self.RGBAtoAlpha(self.config.colors[name])

    def GetColor(self, name):
        if name in self.config.colors:
            return self.RGBAtoRGB(self.config.colors[name])
        return self.RGBAtoRGB(self.config.colors["n/a"]) # Default color

    def GetNuclOverride(self, name):
        # We are checking it before running this function but just in case
        # there is some error we want to return default_onz.
        if name in self.config.nucl_colors:
            return self.RGBAtoRGB(self.config.nucl_colors[name]), \
                   self.RGBAtoAlpha(self.config.nucl_colors[name])
        return self.RGBAtoRGB(self.config.colors["onz_default"]), \
               self.RGBAtoAlpha(self.config.colors["onz_default"])

    def Prepare(self):
        for name, nucl in self.quadruplex.nucl_quad.items():
            nucl.CalculateCoordinates(self.config)

        self.quadruplex.DetermineConnectionTypes()
        for _, chain in self.quadruplex.chains.items():
            self.quadruplex.CalculateFlow(chain)


        for name, nucl in self.quadruplex.nucl_quad.items():
            nucl.UpdatePriorities(self.quadruplex.nucl_quad)


    def DrawPriority(self, priority):
        for name, nucl in self.quadruplex.nucl_quad.items():
            if nucl.priority_nucl == priority:
                self.DrawNucleotide(nucl)

            if nucl.priority_edge == priority:
                self.DrawTetradeBorder(nucl, self.quadruplex)

            if nucl.priority_conn == priority:
                self.DrawConnection(nucl, self.quadruplex.nucl_quad)

    def DrawAll(self):
        self.Prepare();
        # Tetrade numbering of the nucleotides.
        #  2  3
        # 1  4 
        # Draw things in the priority order (first to last) 1 - 5
        # 1 - Conn at the back + Conn FRONT_TO_BACK +
        #     Conn on the left + Conn SAME_LEVEL (down)
        # 2 - Nucleotides with Conn SAME_LEVEL (up-down, down-up)
        # 3 - Connection SAME_LEVEL (up-down, down-up).
        # 4 - Nucleotides Rest
        # 5 - Tetrade border
        # 6 - Connection SAME_LEVEL rest + Rest of connections
        self.DrawPriority(1)
        self.DrawPriority(2)
        self.DrawPriority(3)
        self.DrawPriority(4)
        self.DrawPriority(5)
        self.DrawPriority(6)

        # Draw corner points. As last thing to cover connection 
        # (or should it be earlier)
        for name, nucl in self.quadruplex.nucl_quad.items():
            self.DrawNucleotidePoint(nucl)
            self.DrawNucleotideLabel(nucl)

        # Draw first and last label.
        for _, chain in self.quadruplex.chains.items():
            if chain["first"] != chain["last"]:
                self.DrawLabel(self.quadruplex.nucl_quad[chain["first"]], "5'")
                self.DrawLabel(self.quadruplex.nucl_quad[chain["last"]], "3'")

    def DrawNucleotide(self, nucl):
        shift = self.base_shift
        conf = self.config

        color = self.GetColor(nucl.onz)
        alpha = self.GetAlpha(nucl.onz)
        # Override colors of the nucleotide if it exists in the nucl_color dict.
        if nucl.full_name in conf.nucl_colors:
            color, alpha = self.GetNuclOverride(nucl.full_name)

        block = self.svg.polygon(self.ShiftCoords(nucl.coords, shift), \
                fill = color, fill_opacity = alpha, \
                stroke = color, stroke_width = conf.stroke_width)

        self.svg.add(block)

    def NuclFromFullname(self, nucl):
        fullname = nucl.full_name
        start = max(fullname.find(".") + 1, 0)
        end = fullname.rfind(str(nucl.number))
        if end == -1:
            end = len(fullname) - 1

        return fullname[start:end]


    def NucleotideName(self, nucl):
        # <chain>.<nucleotide-full><number>
        name = ""
        conf = self.config
        if conf.label_chain == True:
            name += str(nucl.chain)
            if conf.label_nucleotide == True or conf.label_number == True:
                name += "."
        if conf.label_nucleotide == True:
            if conf.label_nucleotide_full == True:
                name += str(self.NuclFromFullname(nucl))
            else:
                name += str(nucl.short_name)

        if conf.label_number == True:
            name += str(nucl.number)

        return name

    def ProperFontSize(self, text, fontsize, font, desired_width):
        surface = cairo.SVGSurface(self.cairo_tempfile.name, 1280, 200)
        cr = cairo.Context(surface)
        cr.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(fontsize)
        xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(text)
        while width > desired_width:
            fontsize -= 0.25
            cr.set_font_size(fontsize)
            xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(text)

        return fontsize

    def DrawNucleotideLabel(self, nucl):
        shift = self.base_shift
        conf = self.config
        name = self.NucleotideName(nucl)
        font_family = conf.font_family
        font_size = self.ProperFontSize(name, conf.label_font_size, font_family, conf.longer)

        nucl.center = self.ShiftCoords(nucl.center, shift)
        tan_val = math.tan(math.radians(conf.angle))
        sin_val = math.sin(math.radians(conf.angle))

        if (nucl.GetOnzPlusMinus() == "+" and (nucl.position == 0 or nucl.position == 2)) or \
           (nucl.GetOnzPlusMinus() == "-" and (nucl.position == 1 or nucl.position == 3)):
            nucl.center.x += font_size * (sin_val - 0.5)

            rotation = int(360 - conf.angle)
            if conf.tilted_labels == True:
                skewX = 90 - conf.angle
            else:
                skewX = 0
        else:
            nucl.center.y += font_size * (sin_val - 0.5)  # Movie it a little down
            if conf.tilted_labels:
                nucl.center.x += font_size * (sin_val - 1)
            rotation = 0
            if conf.tilted_labels == True:
                skewX = 90 + conf.angle
            else:
                skewX = 0

        outer_color = self.GetColor(nucl.onz)
        # Override colors of the nucleotide if it exists in the nucl_color dict.
        if nucl.full_name in conf.nucl_colors:
            outer_color, _ = self.GetNuclOverride(nucl.full_name)

        label_outline = self.svg.text(name, fill = outer_color, \
                transform = "translate({0}, {1}) rotate({2}) skewX({3})".format( \
                nucl.center.x, nucl.center.y, rotation, skewX, rotation), \
                style = "text-anchor:middle", \
                font_weight = "bold", font_size = font_size, font_family = font_family, \
                stroke = outer_color, stroke_width = "2px", \
                stroke_linejoin = "round")

        label_fill = self.svg.text(name, fill = self.GetColor(nucl.bond), \
                transform = "translate({0}, {1}) rotate({2}) skewX({3})".format( \
                nucl.center.x, nucl.center.y, rotation, skewX), \
                style = "text-anchor:middle", \
                font_weight = "bold", font_size = font_size, font_family = font_family)

        self.svg.add(label_outline)
        self.svg.add(label_fill)


    def DrawTetradeBorder(self, nucl_a, quad):
        point_a = self.ShiftCoords(nucl_a.coords[nucl_a.position], self.base_shift)
        nucl_b = quad.nucl_quad[quad.tetrads[nucl_a.tetrade_no][(nucl_a.position + 1) % 4]]
        point_b = self.ShiftCoords(nucl_b.coords[nucl_b.position], self.base_shift)


        line = self.svg.polyline([point_a, point_b], stroke = self.GetColor("border"), \
                stroke_width = self.config.stroke_width, fill = "none", \
                stroke_opacity = self.GetAlpha("border"))

        self.svg.add(line)


    # For drawinf 5' and 3' labels.
    def DrawLabel(self, nucl, label):
        pos = nucl.position
        pos_str = self.ShiftCoords(nucl.coords[pos], self.base_shift)
        font_size = self.config.se_label_font_size
        pos_str.y += font_size / 5.0
        spacing = self.config.se_label_spacing
        if pos == 0 or pos == 1:
            pos_str.x -= spacing
            anchor = "text-anchor:end"
        else:
            pos_str.x += spacing
            anchor = "text-anchor:begin"
        label_outline = self.svg.text(label, fill = self.GetColor("text"), \
                transform = "translate({0}, {1})".format(pos_str.x, pos_str.y), \
                style = anchor, font_size = font_size, font_weight = "bold", \
                font_family = self.config.font_family,
                stroke = "white", stroke_width = "2px", stroke_linejoin = "round")

        label_fill = self.svg.text(label, fill = self.GetColor("text"), \
                transform = "translate({0}, {1})".format(pos_str.x, pos_str.y), \
                font_family = self.config.font_family,
                style = anchor, font_size = font_size, font_weight = "bold")

        self.svg.add(label_outline)
        self.svg.add(label_fill)

    # Draw simple stright line from A to B.
    def DrawSimpleLine(self, point_a, point_b):
        conf = self.config
        midpoint = (point_a.y - point_b.y) / 2.0
        if point_a.y > point_b.y:
            midpoint += 6.0 * conf.stroke_width
        else:
            midpoint -= 6.0 * conf.stroke_width

        line = self.svg.polyline([point_a, (point_a.x, point_a.y - midpoint), point_b], \
                stroke = self.GetColor("connection"), stroke_width = conf.stroke_width, \
                fill = "none", marker_mid = "url(#arrowhead)", \
                stroke_opacity = self.GetAlpha("connection"))

        self.svg.add(line)

    def DrawSameLevel(self, point_a, point_b, flow_out, flow_in, divisor):
        conf = self.config
        bezier = self.svg.path(d="M", stroke = self.GetColor("connection"), \
                stroke_width = conf.stroke_width, fill = "none", \
                stroke_opacity = self.GetAlpha("connection"))
        distance = point_a.Distance(point_b)

        bezier.push(point_a)
        bezier.push("C")
        bezier.push(point_a + Point(0, flow_out.value * distance / divisor), \
                    point_b + Point(0, flow_in.value * distance / divisor))
        bezier.push(point_b)
        self.svg.add(bezier)


    def DrawSide(self, point_a, point_b, flow_out, flow_in, side, angle, divisor):
        conf = self.config
        bezier = self.svg.path(d="M", stroke = self.GetColor("connection"), \
                stroke_width = conf.stroke_width, fill = "none", \
                stroke_opacity = self.GetAlpha("connection"))
        distance = point_a.Distance(point_b)

        bezier.push(point_a)
        bezier.push("C")

        # If flows are against each other, increase flow (devcrease divisor).
        # Detect this specific cross.
        if point_a.x != point_b.x:
            # Is A above B?
            if point_a.y < point_b.y and flow_out == ConnFlow.UP:
                if flow_in == ConnFlow.DOWN:
                    divisor = divisor / 1.15
                else:
                    divisor = divisor / 1.1
            elif point_a.y > point_b.y and flow_out == ConnFlow.DOWN:
                if flow_in == ConnFlow.DOWN:
                    divisor = divisor / 1.1
                else:
                    divisor = divisor / 1.15

        radians = math.radians(angle) #  math.radians(conf.angle)
        shift_x = distance * math.cos(radians) / divisor
        shift_y = distance * math.sin(radians) / divisor
        if side != Side.NONE:
            bezier.push(point_a + Point(side.value * shift_x, flow_out.value * shift_y))
            bezier.push(point_b + Point(side.value * shift_x, flow_in.value * shift_y))
        else:
            if point_a.x < point_b.x:
                bezier.push(point_a + Point(shift_x, flow_out.value * shift_y))
                bezier.push(point_b + Point(-shift_x, flow_in.value * shift_y))
            else:
                bezier.push(point_a + Point(-shift_x, flow_out.value * shift_y))
                bezier.push(point_b + Point(shift_x, flow_in.value * shift_y))


        bezier.push(point_b)
        self.svg.add(bezier)

    def DrawConnection(self, nucl_a, nucl_quad):
        if nucl_a.connected_to == "":
            return

        point_a = self.ShiftCoords(nucl_a.coords[nucl_a.position], self.base_shift)
        nucl_b = nucl_quad[nucl_a.connected_to]
        point_b = self.ShiftCoords(nucl_b.coords[nucl_b.position], self.base_shift)

        flow_out = nucl_a.flow_out
        flow_in = nucl_a.flow_in
        if nucl_a.connection_type == ConnType.SIMPLE:
            self.DrawSimpleLine(point_a, point_b)
        elif nucl_a.connection_type == ConnType.SAME_LEVEL:
            if (nucl_b.position == 0 and nucl_a.position == 2) or \
                (nucl_b.position == 2 and nucl_a.position == 0):
                self.DrawSameLevel(point_a, point_b, flow_out, flow_in, 3.5)
            else:
                self.DrawSameLevel(point_a, point_b, flow_out, flow_in, 2.5)
        elif nucl_a.connection_type == ConnType.RIGHT:
            self.DrawSide(point_a, point_b, flow_out, flow_in, Side.RIGHT, \
                    self.config.angle, 3.5)
        elif nucl_a.connection_type == ConnType.LEFT:
            self.DrawSide(point_a, point_b, flow_out, flow_in, Side.LEFT, \
                    self.config.angle, 3.5)
        elif nucl_a.connection_type == ConnType.RIGHT_CROSS:
            self.DrawSide(point_a, point_b, flow_out, flow_in, Side.NONE, \
                    80, 2.25)
        elif nucl_a.connection_type == ConnType.LEFT_CROSS:
            self.DrawSide(point_a, point_b, flow_out, flow_in, Side.NONE, \
                    80, 2.25)
        elif nucl_a.connection_type == ConnType.FRONT_BACK_CROSS:
            self.DrawSide(point_a, point_b, flow_out, flow_in, Side.NONE, \
                    80, 2.25)
        elif nucl_a.connection_type == ConnType.FRONT_TO_BACK:
            self.DrawSide(point_a, point_b, flow_out, flow_in, Side.RIGHT, \
                    45, 1.75)
        elif nucl_a.connection_type == ConnType.UNKNOWN:
            print("WARNINMG: Unknown connection type!")
            #line = self.svg.polyline([point_a, point_b], fill = "none", \
            #        stroke = self.GetColor("connection"), stroke_width = self.config.stroke_width, \
            #        marker_mid = "url(#arrowhead)", stroke_opacity = 0.95)

            #self.svg.add(line)

    def DrawNucleotidePoint(self, nucl):
        #print("draw_point")
        conf = self.config
        point = self.ShiftCoords(nucl.coords[nucl.position], self.base_shift)
        self.svg.add(self.svg.circle(point, r = conf.point_size, \
                stroke = self.GetColor("connection"), stroke_width = conf.point_stroke, \
                stroke_opacity = self.GetAlpha("connection"), \
                fill = self.GetColor("point"), fill_opacity = self.GetAlpha("point")))

