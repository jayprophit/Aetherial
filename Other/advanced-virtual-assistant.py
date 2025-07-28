# handlers/visualization.py - Additional methods
class VisualizationHandler:
    def create_advanced_plot(self, 
                           data: Dict[str, List[float]], 
                           plot_type: str = 'line',
                           **kwargs) -> Figure:
        """Create advanced visualization plots."""
        plt.figure(figsize=kwargs.get('figsize', (10, 6)))
        
        if plot_type == 'violin':
            sns.violinplot(data=data)
        elif plot_type == 'box':
            sns.boxplot(data=data)
        elif plot_type == '3d_scatter':
            ax = plt.axes(projection='3d')
            ax.scatter3D(data['x'], data['y'], data['z'])
        elif plot_type == 'contour':
            plt.contour(data['x'], data['y'], data['z'])
        elif plot_type == 'network':
            import networkx as nx
            G = nx.Graph()
            G.add_edges_from(data['edges'])
            nx.draw(G, with_labels=True)
            
        if 'title' in kwargs:
            plt.title(kwargs['title'])
        
        self.current_figure = plt.gcf()
        return self.current_figure
    
    def create_animation(self, 
                        data: List[Dict[str, List[float]]], 
                        animation_type: str = 'line',
                        interval: int = 100) -> None:
        """Create animated plots."""
        import matplotlib.animation as animation
        
        fig, ax = plt.subplots()
        
        def update(frame):
            ax.clear()
            frame_data = data[frame]
            if animation_type == 'line':
                ax.plot(frame_data['x'], frame_data['y'])
            elif animation_type == 'scatter':
                ax.scatter(frame_data['x'], frame_data['y'])
        
        anim = animation.FuncAnimation(
            fig, update, frames=len(data), interval=interval)
        
        self.current_figure = fig
        return anim

# handlers/modeling.py - Additional methods
class BlenderHandler:
    def create_complex_object(self,
                            vertices: List[Tuple[float, float, float]],
                            faces: List[Tuple[int, ...]],
                            name: str) -> str:
        """Generate Python code for creating complex mesh objects in Blender."""
        commands = [
            "import bmesh",
            "mesh = bpy.data.meshes.new('mesh')",
            f"obj = bpy.data.objects.new('{name}', mesh)",
            "bpy.context.collection.objects.link(obj)",
            "bm = bmesh.new()",
        ]
        
        # Add vertices
        for i, (x, y, z) in enumerate(vertices):
            commands.append(f"v{i} = bm.verts.new(({x}, {y}, {z}))")
        commands.append("bm.verts.ensure_lookup_table()")
        
        # Add faces
        for face in faces:
            verts = [f"bm.verts[{i}]" for i in face]
            commands.append(f"bm.faces.new(({', '.join(verts)}))")
        
        commands.extend([
            "bm.to_mesh(mesh)",
            "bm.free()"
        ])
        
        return "\n".join(commands)
    
    def add_modifiers(self, obj_name: str, modifiers: List[Dict]) -> str:
        """Generate code for adding Blender modifiers."""
        commands = []
        
        for mod in modifiers:
            mod_type = mod['type']
            mod_settings = mod.get('settings', {})
            
            commands.extend([
                f"obj = bpy.data.objects['{obj_name}']",
                f"mod = obj.modifiers.new(name='{mod_type}', type='{mod_type}')"
            ])
            
            for setting, value in mod_settings.items():
                commands.append(f"mod.{setting} = {value}")
        
        return "\n".join(commands)
    
    def create_animation(self, 
                        obj_name: str,
                        keyframes: List[Dict[str, Any]]) -> str:
        """Generate animation keyframes in Blender."""
        commands = [f"obj = bpy.data.objects['{obj_name}']"]
        
        for kf in keyframes:
            frame = kf['frame']
            if 'location' in kf:
                x, y, z = kf['location']
                commands.extend([
                    f"obj.location = ({x}, {y}, {z})",
                    f"obj.keyframe_insert(data_path='location', frame={frame})"
                ])
            if 'rotation' in kf:
                x, y, z = kf['rotation']
                commands.extend([
                    f"obj.rotation_euler = ({x}, {y}, {z})",
                    f"obj.keyframe_insert(data_path='rotation_euler', frame={frame})"
                ])
            if 'scale' in kf:
                x, y, z = kf['scale']
                commands.extend([
                    f"obj.scale = ({x}, {y}, {z})",
                    f"obj.keyframe_insert(data_path='scale', frame={frame})"
                ])
        
        return "\n".join(commands)

class OpenSCADHandler:
    def create_complex_shape(self, operations: List[Dict]) -> str:
        """Create complex OpenSCAD models with multiple operations."""
        scad_code = []
        
        for op in operations:
            if op['type'] == 'primitive':
                scad_code.append(self.create_basic_shape(
                    op['shape_type'],
                    op['dimensions']
                ))
            elif op['type'] == 'transform':
                params = op.get('params', {})
                if op['operation'] == 'translate':
                    x, y, z = params['vector']
                    scad_code.append(f"translate([{x}, {y}, {z}])")
                elif op['operation'] == 'rotate':
                    x, y, z = params['angles']
                    scad_code.append(f"rotate([{x}, {y}, {z}])")
                elif op['operation'] == 'scale':
                    x, y, z = params['factors']
                    scad_code.append(f"scale([{x}, {y}, {z}])")
            elif op['type'] == 'boolean':
                if op['operation'] == 'union':
                    scad_code.append("union() {")
                elif op['operation'] == 'difference':
                    scad_code.append("difference() {")
                elif op['operation'] == 'intersection':
                    scad_code.append("intersection() {")
                
                if 'children' in op:
                    child_code = self.create_complex_shape(op['children'])
                    scad_code.append(child_code)
                
                scad_code.append("}")
        
        return "\n".join(scad_code)
    
    def create_parametric_model(self, parameters: Dict[str, Any], code: str) -> str:
        """Create parametric OpenSCAD model."""
        scad_code = []
        
        # Define parameters
        for name, value in parameters.items():
            if isinstance(value, (int, float)):
                scad_code.append(f"{name} = {value};")
            elif isinstance(value, str):
                scad_code.append(f"{name} = \"{value}\";")
        
        scad_code.append("\n// Parametric model")
        scad_code.append(code)
        
        return "\n".join(scad_code)

# Add to VirtualAssistant class process_command method:
    def process_command(self, command: str) -> Optional[str]:
        try:
            # ... existing command processing ...
            
            # Advanced visualization
            if 'create advanced plot' in command:
                # Example: parse command for plot type and data
                data = {'x': [1, 2, 3], 'y': [4, 5, 6], 'z': [7, 8, 9]}
                plot_type = '3d_scatter'  # Extract from command
                fig = self.viz.create_advanced_plot(data, plot_type)
                self.viz.save_plot('advanced_plot.png')
                return "Advanced plot created and saved"
            
            elif 'create animation' in command:
                # Example: create animated visualization
                data = [
                    {'x': [1, 2, 3], 'y': [1, 2, 3]},
                    {'x': [1, 2, 3], 'y': [2, 3, 4]},
                    {'x': [1, 2, 3], 'y': [3, 4, 5]}
                ]
                anim = self.viz.create_animation(data)
                return "Animation created"
            
            # Complex 3D modeling
            elif 'create complex model' in command:
                if 'blender' in command:
                    # Example: create complex Blender object
                    vertices = [(0,0,0), (1,0,0), (1,1,0), (0,1,0)]
                    faces = [(0,1,2,3)]
                    commands = [
                        self.blender.create_complex_object(vertices, faces, 'complex_obj'),
                        self.blender.add_modifiers('complex_obj', [
                            {'type': 'SUBSURF', 'settings': {'levels': 2}}
                        ])
                    ]
                    script = self.blender.create_python_script(commands, 'complex.blend')
                    self.blender.execute_script(script)
                    return "Complex Blender model created"
                
                elif 'scad' in command:
                    # Example: create complex OpenSCAD model
                    operations = [
                        {'type': 'primitive', 'shape_type': 'cube', 
                         'dimensions': {'x': 10, 'y': 10, 'z': 10}},
                        {'type': 'transform', 'operation': 'translate',
                         'params': {'vector': [5, 0, 0]}},
                        {'type': 'boolean', 'operation': 'union',
                         'children': [
                             {'type': 'primitive', 'shape_type': 'sphere',
                              'dimensions': {'radius': 5}}
                         ]}
                    ]
                    scad_code = self.openscad.create_complex_shape(operations)
                    self.openscad.render_scad(scad_code, 'complex.stl')
                    return "Complex OpenSCAD model created"
            
            # ... continue with existing command processing ...
            
        except Exception as e:
            logging.error(f"Command processing error: {str(e)}")
            return "Sorry, I encountered an error"
