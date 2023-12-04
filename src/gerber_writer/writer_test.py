#KT, 2022 04 18

version = '0.3.1'

import hashlib
import unittest
from src.gerber_writer.writer import DataLayer
from src.gerber_writer.writer import (
    Path, set_generation_software,
    Circle, Rectangle, RoundedRectangle, ChamferedRectangle,
    Thermal, RoundedThermal, RegularPolygon,  UserPolygon,
    )

class TestDataLayer(unittest.TestCase):
        
    def test_DataLayer(self):
    
        output_gerbers = True # Useful during debugging to have the gerbers for inspection
        #adf r'...' linux & windows
        folder = r'../../tools/gerbers/' # Root directory for gerbers

        def body_md5(layer):
            """Return a string with the md5 of the body of the gerber string of the layer"""
            tested_gerber_section = (layer.dumps_gerber().partition('.CreationDate')[2])[30:]
            return (hashlib.md5(tested_gerber_section .encode())).hexdigest()

        # Test Circle
        #------------
        via = Circle(0.1, 'ViaPad', negative=False)
        self.assertEqual(via.diameter, 0.1)       
        self.assertEqual(via.function, 'ViaPad')
        self.assertEqual(via.negative, False)
        # Test invalid diameter
        try:            
            via = Circle(-0.1, 'ViaPad')
            self.assertTrue(False, 'Invalid Circle accepted')
        except ValueError:
            pass
        except TypeError:
            pass
        test_layer = DataLayer('Other,Test')
        test_layer.add_pad(via, (-2, 0), angle=22.5)
        test_layer.add_pad(Circle(0.5, 'ComponentPad'), (-1, 0))
        test_layer.add_pad(Circle(0.2, 'Other,test'), (0, 1), 0)
        test_layer.add_pad(Circle(0.2, 'Other,test'), (0, 2))       
        test_layer.add_pad(Circle(0.2, 'Other,test', negative=True), (1, 1))
        test_layer.add_pad(Circle(0.2, 'Other,test'), (0, 3))   
        test_layer.add_pad(Circle(0.2, 'Other,test'), (0, 4))        
        test_layer.add_pad(Circle(0.2, 'Other,test', negative=True), (1, 2))     
        test_layer.add_pad(Circle(0.2, 'Other,test', negative=True), (1, 3))             
        test_layer.add_pad(Circle(0.0, 'Other,test', negative=True), (2, 0))
        marker = Circle(0, 'Other,test_zero_size')
        test_layer.add_pad(marker, (1, 1))
        if output_gerbers:
            with open(folder + 'gerber_writer_test_circle.gbr', 'w') as outfile:
                test_layer.dump_gerber(outfile)
        self.assertEqual(body_md5(test_layer), 'c95feb8a9bb064c2504d4df6102fef81')
        
        #Test Rectangle
        #--------------
        smd_pnt = (0.5, 0)
        smd = Rectangle(0.5, 0.25, 'SMDPad,CuDef', negative=False)
        self.assertEqual(smd.function, 'SMDPad,CuDef')
        self.assertEqual(smd.x_size, 0.5)
        self.assertEqual(smd.y_size, 0.25)
        self.assertEqual(smd.negative, False)
        test_layer = DataLayer('Other,Test')
        test_layer.add_pad(smd, smd_pnt)
        test_layer.add_pad(smd, smd_pnt)
        # Test zero y size
        try:
            shape = Rectangle(1.1, 0, function='Zonk')
            self.assertTrue(False, 'Invalid RoundedRectangle accepted')
        except ValueError:
            pass
        except TypeError:
            pass
        test_layer.add_pad(smd, (1, 0))
        test_layer.add_pad(smd, (0, -0.5), angle=45)
        test_layer.add_pad(smd, (1, 1) , angle=180)

        if output_gerbers:
            with open(folder + 'gerber_writer_test_rectangle.gbr', 'w') as outfile:
                test_layer.dump_gerber(outfile)        
        self.assertEqual(body_md5(test_layer), '576cd742a6460a88aae0febabe88ea30')
        
        # Test RoundedRectangle
        #----------------------
        shape = RoundedRectangle(0.6, 0.2, 0.05, 'SMDPad,CuDef')
        self.assertEqual(shape.x_size, 0.6)
        self.assertEqual(shape.y_size, 0.2)
        self.assertEqual(shape.radius, 0.05)          
        self.assertEqual(shape.function, 'SMDPad,CuDef')
        self.assertEqual(shape.negative, False)
         # Test function value that is not string        
        try:
            zonk = RoundedRectangle(1.1, 0.6, 0.05, function=1.23)
            self.assertTrue(False, 'Invalid RoundedRectangle accepted')
        except ValueError:
            pass
        except TypeError:
            pass
        # Test invalid radius, too large
        try:            
            zonk = RoundedRectangle(1.1, 0.6, radius=0.4, function='Other,Invalid')
            self.assertTrue(False, 'Invalid RoundedRectangle accepted')
        except ValueError:
            pass
        except TypeError:
            pass
        # Test invalid radius negative
        try:            
            zonk = RoundedRectangle(1.1, 0.6, radius=-0.001, function='Other,Invalid')
            self.assertTrue(False, 'Invalid RoundedRectangle accepted')
        except ValueError:
            pass
        except TypeError:
            pass      
        test_layer = DataLayer('Other,Test')
        test_layer.add_pad(shape, (0, 3), angle=22.5)
        test_layer.add_pad(shape, (-1, -2.5))
        test_layer.add_pad(RoundedRectangle(0.45, 0.2, 0.0999999, 'SMDPad,CuDef'), (1, -2)) # Test obround - angle 0
        test_layer.add_pad(RoundedRectangle(0.45, 0.2, 0.1, 'SMDPad,CuDef'), (1, -3), angle=45) # Test obround - rotated    
        rectangle = RoundedRectangle(1-0.5, 0.25, 0, 'Other,Test_zero_radius')
        test_layer.add_pad(rectangle, (1, 1))
        test_layer.add_pad(rectangle, (1, 2), 30)        
        if output_gerbers: 
            with open(folder + 'gerber_writer_test_rounded_rectangle.gbr', 'w') as outfile:
                test_layer.dump_gerber(outfile)
        self.assertEqual(body_md5(test_layer), '9cd39f3c4971fdcba392ff707d59d44e')
        
        # Test ChamferedRectangle
        #------------------------
        shape = ChamferedRectangle(0.6, 0.2, 0.05, 'SMDPad,CuDef')
        self.assertEqual(shape.x_size, 0.6)
        self.assertEqual(shape.y_size, 0.2)
        self.assertEqual(shape.cutoff, 0.05)          
        self.assertEqual(shape.function, 'SMDPad,CuDef')
        self.assertEqual(shape.negative, False)
         # Test invalid y_size       
        try:
            shape = ChamferedRectangle(1.1, 0, 0.5, function='Test,invalid_y')
            self.assertTrue(False, 'Invalid ChamferedRectangle accepted')
        except ValueError:
            pass
        except TypeError:
            pass
        # Test invalid cutoff, too large
        try:            
            shape = ChamferedRectangle(1.1, 0.6, cutoff=0.4, function='Test,invalid')
            self.assertTrue(False, 'Invalid ChamferedRectangle accepted')
        except ValueError:
            pass
        except TypeError:
            pass      
        # Test invalid cutoff, negative
        try:            
            shape = ChamferedRectangle(1.1, 0.6, cutoff=-0.001, function='Test,invalid')
            self.assertTrue(False, 'Invalid ChamferedRectangle accepted')
        except ValueError:
            pass
        except TypeError:
            pass      
        test_layer = DataLayer('Other,Test')
        test_layer.add_pad(shape, (0, 3), angle=22.5)
        test_layer.add_pad(shape, (3, 0))        
        test_layer.add_pad(ChamferedRectangle(0.45, 0.22, 0.06, 'SMDPad,CuDef'), (0, 1), 45)
        rectangle = ChamferedRectangle(0.5, 0.25, 0, 'Test,zero_cutoff')
        test_layer.add_pad(rectangle, (-1, 0))
        test_layer.add_pad(rectangle, (-1, 1), 35)
        if output_gerbers:
            with open(folder + 'gerber_writer_test_chamfered_rectangle.gbr', 'w') as outfile:
                test_layer.dump_gerber(outfile)        
        self.assertEqual(body_md5(test_layer), '73e14a62dd4b406af8af6cf37236e9cc')

        # Test Thermal
        # ------------
        thermal = Thermal(0.5, 0.4, 0.1, function='ThermalReliefPad', negative=True)
        self.assertEqual(thermal.gap, 0.1)
        self.assertEqual(thermal.negative, True)
        try:            
            thermal = Thermal(0.5, 0.4, 0.4, function='Test,invalid', negative=True)
            self.assertTrue(False, 'Invalid Thermal accepted')
        except ValueError:
            pass
        except TypeError:
            pass        
        test_layer = DataLayer('Other,Test')
        test_layer.add_pad(thermal, (0, 0))
        test_layer.add_pad(thermal, (0, 1))
        test_layer.add_pad(Thermal(0.8, 0.6, 0.15, function=''), (1.2, 1), angle=-22.5)
        test_layer.add_pad(thermal, (1, 0), angle=45)             
        self.assertEqual(len(test_layer), 4)
        if output_gerbers:
            with open(folder + 'gerber_writer_test_thermal.gbr', 'w') as outfile:
                test_layer.dump_gerber(outfile)
        self.assertEqual(body_md5(test_layer), 'e9a2da5b8197860e24146ee70ac78f40')
        
        # Test RoundedThermal
        # --------------------
        thermal = RoundedThermal(1, 0.8, 0.1, function='ThermalReliefPad', negative=True)
        self.assertEqual(thermal.gap, 0.1)
        self.assertEqual(thermal.negative, True)
        try:            
            temp = RoundedThermal(1.1, 0.9, 0.5072, function='ThermalReliefPad', negative=True) # gap just too large
            self.assertTrue(False, 'Invalid RoundedThermal accepted')
        except ValueError:
            pass
        except TypeError:
            pass        
        test_layer = DataLayer('Other,Test')
        test_layer.add_pad(thermal, (0, 0))
        test_layer.add_pad(thermal, (0, 1.5), angle=-22.5)
        test_layer.add_pad(thermal, (0, 3), angle=45)
        test_layer.add_pad(thermal, (0, 4.5), angle=0)       
        test_layer.add_pad(RoundedThermal(1.1, 0.9, 0.2949, function='Other,interior rounding'), (1.5, 0)) # gap just ok for interior rounding
        test_layer.add_pad(RoundedThermal(1.1, 0.9, 0.3, function='Other,symmetric rounding just'), (1.5, 1.5)) # gap just requires symmetric rounding
        test_layer.add_pad(RoundedThermal(1.1, 0.9, 0.5071, function='Other,symmetric rounding max'), (1.5, 3)) # nearly largest possible gap 
        self.assertEqual(len(test_layer), 7)
        if output_gerbers:
            with open(folder + 'gerber_writer_test_rounded_thermal.gbr', 'w') as outfile:
                test_layer.dump_gerber(outfile)
        self.assertEqual(body_md5(test_layer), '22be4a6fcbbeceead62b660b0cad60fe')
        
        # Test RegularPolygon
        #--------------------
        hexagon = RegularPolygon(0.44, 6, '')
        self.assertEqual(hexagon.outer_diameter, 0.44)
        self.assertEqual(hexagon.vertices, 6)
        self.assertEqual(hexagon.function, '')
        self.assertEqual(hexagon.negative, False)
        # Test invalid outer_diameter
        try:            
            hexagon = RegularPolygon('zonk', 6, 'Test,invalid')
            self.assertTrue(False, 'Invalid RoundedRectangle accepted')
        except ValueError:
            pass
        except TypeError:
            pass
        # Test invalid too many vertices
        try:            
            hexagon = RegularPolygon(20, 13, 'Testinvalid')
            self.assertTrue(False, 'Invalid RoundedRectangle accepted')
        except ValueError:
            pass
        except TypeError:
            pass
        test_layer = DataLayer('Other,Test')
        test_layer.add_pad(hexagon, (1, -1), angle=22.5)
        test_layer.add_pad(hexagon, (1, 0), angle=0)
        test_layer.add_pad(RegularPolygon(0.55, 8, function='TestPad'), (1, 1))
        if output_gerbers:
            with open(folder + 'gerber_writer_test_regular_polygon.gbr', 'w') as outfile:
                test_layer.dump_gerber(outfile)
        self.assertEqual(body_md5(test_layer), 'ae904fe1d5c42f8af90675b18a94ff6d')
        
        # Test UserPolygon
        #-----------------
        polygon = (
            (0, 0),
            (0.1, 0.2),
            (0.5, 0.2),
            (0.4, 0),
            (0,0)
            )
        shape = UserPolygon(polygon, 'Other,test' )
        self.assertEqual(shape.polygon, polygon)
        self.assertEqual(shape.function, 'Other,test')
        # Test open polygon
        try:            
            zap = UserPolygon(polygon[:-1],'Test,invalid')
            self.assertTrue(False, 'Invalid open polygon accepted')
        except ValueError:
            pass
        except TypeError:
            pass
        # Test polygon with two vertices
        try:            
            zap = UserPolygon(polygon[0:1],'Test,invalid')
            self.assertTrue(False, 'Invalid open polygon accepted')
        except ValueError:
            pass
        except TypeError:
            pass
        # Test polygon not tuple
        try:            
            shape = UserPolygon('zonk', 'TestPad')
            self.assertTrue(False, 'Invalid polygon accepted')
        except ValueError:
            pass
        except TypeError:
            pass
        test_layer = DataLayer('Other,Test')
        test_layer.add_pad(shape, (1, 0), angle=-10)
        test_layer.add_pad(shape, (0, 0))
        triangle = (
            (0, 0),
            (0.01, 0.02),
            (0.05, 0.02),
            (0, 0)
            )  
        test_layer.add_pad(UserPolygon(triangle, 'Other,Test', negative=True), (1.1, 0.1))
        test_layer.add_pad(shape, (0, 1))        
        test_layer.add_pad(UserPolygon(triangle, 'Other,Test', negative=True), (0.1, 0.1), angle=180)
        if output_gerbers:
            with open(folder + 'gerber_writer_test_user_polygon.gbr', 'w') as outfile:
                test_layer.dump_gerber(outfile)
        self.assertEqual(body_md5(test_layer), '724b079ff974573ab7aa90b52062b7d2')       

        # Test Path
        # ---------
        test_layer = DataLayer('Other,Test')
        region_2 = Path()
        region_2.moveto((0, 0))
        region_2.lineto((1, 0))
        region_2.arcto((1 ,1), (1, 0.5), '+')
        region_2.lineto((0, 1))
        region_2.lineto((0, 0))
        region_2.moveto((3, 0))
        region_2.lineto((4, 0))
        region_2.lineto((3, 1))
        region_2.lineto((3, 0))       
        self.assertEqual(len(region_2), 9)
        test_layer.add_pad(Circle(0.1, 'Other,test'), (0, 0)) #Force current point to start of contour
        test_layer.add_region(region_2, 'Other,region', negative=False)
        connection = Path()  
        connection.moveto((11, 0))
        connection.lineto((11, 1))
        connection.arcto((12, 2), (12, 1), '-')
        self.assertEqual(len(connection), 3)             
        test_layer.add_traces_path(connection, 0.11, 'Other,std_path')
        self.assertEqual(len(test_layer), 3)
        null_path = Path()
        self.assertEqual(len(null_path), 0)            
        test_layer.add_traces_path(null_path, 0.12, 'Other,null_path')
        self.assertEqual(len(test_layer), 4)
        move_path = Path()
        move_path.moveto((5, 0))
        self.assertEqual(len(move_path), 1)              
        test_layer.add_traces_path(move_path, 0.13, 'Other,move_path')
        self.assertEqual(len(test_layer), 5)
        if output_gerbers:
            with open(folder + 'gerber_writer_test_Path.gbr', 'w') as outfile:
                test_layer.dump_gerber(outfile)
        self.assertEqual(body_md5(test_layer), '87708dd46ec498eb669d295e6d93967b')      

        # Test add_trace_line
        #--------------------
        
        test_layer = DataLayer('Other,Test')     
        try:            
            test_layer.add_trace_line((-1, -1), (-2, -2), -0.1, 'Conductor')       
            self.assertTrue(False, 'Invalid trace line accepted')
        except ValueError:
            pass
        except TypeError:
            pass
        test_layer.add_trace_line((-1, -1), (-2, -2), 0.1, 'Conductor')
        test_layer.add_trace_line((-2, -1), (-1, -2), 0.1, 'Conductor', negative=True)
        test_layer.add_trace_line((-1, -1.5), (-1.5, -2), 0.1, 'Conductor')
        test_layer.add_trace_line((0, 0), (-1, -1), 0.2, 'Conductor')
        if output_gerbers:
            with open(folder + 'gerber_writer_test_line.gbr', 'w') as outfile:
                test_layer.dump_gerber(outfile)
        self.assertEqual(body_md5(test_layer), 'aed53ae8168ad9ef2ef0418691e34b98')

        # Test add_trace_arc
        #------------------- 
        test_layer = DataLayer('Other,Test')
        # Test negative width
        try:            
            test_layer.add_trace_arc((-2, 2), (-2, -2), (-1.5, 2),'+', -0.2, 'Test,invalid')       
            self.assertTrue(False, 'Arc with negative width accepted')
        except ValueError:
            pass
        except TypeError:
            pass        
        test_layer.add_trace_arc((-2, 2), (-1.5, 1.5), (-1.5, 2), '+', 0.04, 'Conductor')
        test_layer.add_trace_arc((-1.5, 1.5), (-1, 1), (-1.5, 1), '-', 0.04, 'Conductor')
        if output_gerbers:
            with open(folder + 'gerber_writer_test_arc.gbr', 'w') as outfile:
                test_layer.dump_gerber(outfile)
        self.assertEqual(body_md5(test_layer), 'c0d9c35dbf1389cfdadb2db04bf0b9da')
        

        # Test mix of circles from pads and traces
        # ----------------------------------------
        test_layer = DataLayer('Other,Mix circles test')        
        test_layer.add_trace_line((-1, -1), (-2, -2), 0.1, 'Conductor')
        test_layer.add_trace_line((-2, -1), (-1, -2), 0.1, 'Conductor', negative=True)
        test_layer.add_trace_line((-1, -1.5), (-1.5, -2), 0.2, 'Conductor')
        test_layer.add_trace_line((0, 0), (-1, -1), 0.2, 'Other,testx')
        test_layer.add_pad(Circle(0.1, 'ViaPad'), (-1, 0))
        test_layer.add_pad(Circle(0.1, 'Other,testx', negative=True), (-1, 0))
        test_layer.add_pad(Circle(0.1, 'ViaPad'), (-1, 0))        
        if output_gerbers:
            with open(folder + 'gerber_writer_test_circles_mix.gbr', 'w') as outfile:
                test_layer.dump_gerber(outfile)
        self.assertEqual(body_md5(test_layer), '76bf1fddcc3ec0f2477f9cd0641d6a3c')        

        # Test DataLayer
        # --------------      
        set_generation_software('Karel*Tavernier  ', ' gerber_writer_unittest', '2022.06.10 alfa')       
        test_layer = DataLayer('Other,test')
        self.assertEqual(test_layer.function, 'Other,test')
        self.assertEqual(test_layer.negative, False)
        self.assertEqual(test_layer.g_o_stream, list())
        self.assertEqual(len(test_layer), 0)
        test_layer.add_pad(Circle(0.1, 'ViaPad'), (1.1, 1))
        self.assertEqual(len(test_layer), 1)
        
        # Test Mix
        # --------
        set_generation_software('Karel%Tavernier  ', ' gerber_writer_unittest', '1.0')             
        test_layer = DataLayer('Other,Test') 
        cmf_pnt = (1.125, 0)
        cmf = ChamferedRectangle(0.5, 0.25, 0.05, 'SMDPad,CuDef', negative=False)
        test_layer.add_pad(cmf, cmf_pnt, 22.5)  
        test_layer.add_pad(Rectangle(1.1, 0.2, 'Other,test', negative=True), (0, 2), -25)
        test_layer.add_trace_line((-2, -2), (-1, -2), width=0.2, function='Conductor')
        test_layer.add_trace_line((-1, -2), (-0.5, -1.5), 0.2, 'Conductor')
        try:            
            test_layer.add_trace_line((0, 0))      
            self.assertTrue(False, 'add_traces with invalid argument accepted')
        except TypeError:
            pass
        test_layer.add_trace_arc((-2, 2), (-2, -2), (-1.5, 0),'+', 0.2, 'Conductor')
        test_layer.add_trace_arc((-1.5, 1.5), (-1, 1), (-1, 1.5), '-', 0.04, 'Conductor')
        test_layer.add_region(region_2, 'Other,test', negative=False)
        try:            
            test_layer.add_region((-1, -2), (-0.5, -1.5), 0.2, 'Conductor')
            self.assertTrue(False, 'add_region with invalid argument accepted')
        except TypeError:
            pass        
        test_layer.add_pad(Thermal(0.5, 0.4, 0.125, 'ThermalReliefPad', negative=True), (1.5, 1.5), 45) 
        self.assertEqual(len(test_layer), 8)
        
        repr = str(test_layer)

        if output_gerbers:
            with open(folder + 'gerber_writer_test_mix.gbr', 'w') as outfile:
                test_layer.dump_gerber(outfile)

if __name__ == '__main__':
    unittest.main()

