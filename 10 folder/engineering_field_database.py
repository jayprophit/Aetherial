"""
Engineering Field Database
Comprehensive engineering database with research papers, tools, CAD files, and technical specifications
"""

import numpy as np
import json
import uuid
import hashlib
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import asyncio
import math

class EngineeringDiscipline(Enum):
    MECHANICAL = "mechanical"
    ELECTRICAL = "electrical"
    CIVIL = "civil"
    CHEMICAL = "chemical"
    AEROSPACE = "aerospace"
    BIOMEDICAL = "biomedical"
    COMPUTER = "computer"
    ENVIRONMENTAL = "environmental"
    INDUSTRIAL = "industrial"
    MATERIALS = "materials"
    NUCLEAR = "nuclear"
    PETROLEUM = "petroleum"
    MARINE = "marine"
    AUTOMOTIVE = "automotive"
    ROBOTICS = "robotics"
    TELECOMMUNICATIONS = "telecommunications"
    STRUCTURAL = "structural"
    GEOTECHNICAL = "geotechnical"
    THERMAL = "thermal"
    FLUID_DYNAMICS = "fluid_dynamics"

class CADFileFormat(Enum):
    SOLIDWORKS = "sldprt"
    AUTOCAD = "dwg"
    INVENTOR = "ipt"
    FUSION360 = "f3d"
    CATIA = "catpart"
    STEP = "step"
    IGES = "iges"
    STL = "stl"
    OBJ = "obj"
    PLY = "ply"
    GCODE = "gcode"

class ManufacturingProcess(Enum):
    CNC_MACHINING = "cnc_machining"
    THREE_D_PRINTING = "3d_printing"
    INJECTION_MOLDING = "injection_molding"
    CASTING = "casting"
    FORGING = "forging"
    WELDING = "welding"
    LASER_CUTTING = "laser_cutting"
    WATERJET_CUTTING = "waterjet_cutting"
    SHEET_METAL_FORMING = "sheet_metal_forming"
    ASSEMBLY = "assembly"
    SURFACE_TREATMENT = "surface_treatment"
    HEAT_TREATMENT = "heat_treatment"

class MaterialType(Enum):
    STEEL = "steel"
    ALUMINUM = "aluminum"
    TITANIUM = "titanium"
    CARBON_FIBER = "carbon_fiber"
    PLASTIC = "plastic"
    CERAMIC = "ceramic"
    COMPOSITE = "composite"
    COPPER = "copper"
    BRASS = "brass"
    STAINLESS_STEEL = "stainless_steel"
    RUBBER = "rubber"
    GLASS = "glass"
    CONCRETE = "concrete"
    WOOD = "wood"
    FABRIC = "fabric"

@dataclass
class MaterialProperties:
    density: float  # kg/m³
    youngs_modulus: float  # GPa
    yield_strength: float  # MPa
    ultimate_strength: float  # MPa
    poissons_ratio: float
    thermal_conductivity: float  # W/m·K
    specific_heat: float  # J/kg·K
    melting_point: float  # °C
    cost_per_kg: float  # USD/kg
    recyclable: bool
    corrosion_resistance: str
    machinability_rating: float  # 1-10 scale

@dataclass
class CADFile:
    id: str
    name: str
    description: str
    file_format: CADFileFormat
    file_size_mb: float
    created_by: str
    created_at: datetime
    discipline: EngineeringDiscipline
    tags: List[str]
    materials_used: List[MaterialType]
    manufacturing_processes: List[ManufacturingProcess]
    dimensions: Dict[str, float]  # length, width, height in mm
    mass: float  # kg
    complexity_score: float  # 1-10 scale
    download_url: str
    preview_images: List[str]
    technical_drawings: List[str]
    assembly_instructions: Optional[str]
    bill_of_materials: List[Dict[str, Any]]

@dataclass
class EngineeringTool:
    id: str
    name: str
    category: str
    manufacturer: str
    model: str
    description: str
    specifications: Dict[str, Any]
    price_range: Dict[str, float]
    applications: List[EngineeringDiscipline]
    precision: str
    power_requirements: Optional[str]
    dimensions: Dict[str, float]
    weight_kg: float
    certification: List[str]
    maintenance_requirements: str
    training_required: bool
    safety_protocols: List[str]

@dataclass
class EngineeringProject:
    id: str
    title: str
    description: str
    discipline: EngineeringDiscipline
    project_type: str
    complexity_level: str  # beginner, intermediate, advanced, expert
    estimated_duration: str
    budget_estimate: Dict[str, float]
    required_tools: List[str]
    required_materials: List[MaterialType]
    cad_files: List[str]
    documentation: List[str]
    learning_objectives: List[str]
    prerequisites: List[str]
    step_by_step_guide: List[Dict[str, str]]
    troubleshooting_guide: List[Dict[str, str]]

class MaterialDatabase:
    """Database of engineering materials and their properties"""
    
    def __init__(self):
        self.materials = {}
        self.material_combinations = {}
        self.cost_database = {}
        
        # Initialize with comprehensive material data
        self._initialize_materials()
    
    def _initialize_materials(self):
        """Initialize comprehensive material database"""
        materials_data = [
            {
                'type': MaterialType.STEEL,
                'name': 'Carbon Steel (AISI 1018)',
                'properties': MaterialProperties(
                    density=7850,
                    youngs_modulus=200,
                    yield_strength=370,
                    ultimate_strength=440,
                    poissons_ratio=0.29,
                    thermal_conductivity=51.9,
                    specific_heat=486,
                    melting_point=1425,
                    cost_per_kg=0.80,
                    recyclable=True,
                    corrosion_resistance='Poor',
                    machinability_rating=7.5
                ),
                'applications': ['General construction', 'Automotive parts', 'Machinery'],
                'heat_treatment': ['Annealing', 'Normalizing', 'Hardening'],
                'welding_compatibility': ['Arc welding', 'MIG', 'TIG', 'Resistance welding']
            },
            {
                'type': MaterialType.ALUMINUM,
                'name': 'Aluminum 6061-T6',
                'properties': MaterialProperties(
                    density=2700,
                    youngs_modulus=68.9,
                    yield_strength=276,
                    ultimate_strength=310,
                    poissons_ratio=0.33,
                    thermal_conductivity=167,
                    specific_heat=896,
                    melting_point=582,
                    cost_per_kg=1.85,
                    recyclable=True,
                    corrosion_resistance='Excellent',
                    machinability_rating=8.5
                ),
                'applications': ['Aerospace', 'Automotive', 'Marine', 'Architecture'],
                'heat_treatment': ['T6 temper', 'Annealing'],
                'welding_compatibility': ['TIG', 'MIG', 'Resistance welding']
            },
            {
                'type': MaterialType.TITANIUM,
                'name': 'Titanium Grade 2',
                'properties': MaterialProperties(
                    density=4510,
                    youngs_modulus=103.4,
                    yield_strength=275,
                    ultimate_strength=345,
                    poissons_ratio=0.34,
                    thermal_conductivity=16.4,
                    specific_heat=523,
                    melting_point=1668,
                    cost_per_kg=35.00,
                    recyclable=True,
                    corrosion_resistance='Excellent',
                    machinability_rating=4.0
                ),
                'applications': ['Aerospace', 'Medical implants', 'Chemical processing'],
                'heat_treatment': ['Stress relief', 'Annealing'],
                'welding_compatibility': ['TIG', 'Electron beam', 'Laser welding']
            },
            {
                'type': MaterialType.CARBON_FIBER,
                'name': 'Carbon Fiber Composite (T300/5208)',
                'properties': MaterialProperties(
                    density=1600,
                    youngs_modulus=181,
                    yield_strength=1500,
                    ultimate_strength=1500,
                    poissons_ratio=0.28,
                    thermal_conductivity=8.7,
                    specific_heat=712,
                    melting_point=3500,  # Sublimation point
                    cost_per_kg=25.00,
                    recyclable=False,
                    corrosion_resistance='Excellent',
                    machinability_rating=3.0
                ),
                'applications': ['Aerospace', 'Automotive racing', 'Sports equipment'],
                'heat_treatment': ['Curing', 'Post-cure'],
                'welding_compatibility': ['Not applicable - bonding only']
            },
            {
                'type': MaterialType.PLASTIC,
                'name': 'ABS Plastic',
                'properties': MaterialProperties(
                    density=1050,
                    youngs_modulus=2.3,
                    yield_strength=40,
                    ultimate_strength=40,
                    poissons_ratio=0.35,
                    thermal_conductivity=0.25,
                    specific_heat=1386,
                    melting_point=105,
                    cost_per_kg=2.50,
                    recyclable=True,
                    corrosion_resistance='Good',
                    machinability_rating=9.0
                ),
                'applications': ['Consumer products', '3D printing', 'Automotive trim'],
                'heat_treatment': ['Annealing'],
                'welding_compatibility': ['Ultrasonic welding', 'Hot air welding']
            }
        ]
        
        for material_data in materials_data:
            material_id = str(uuid.uuid4())
            self.materials[material_id] = material_data
    
    def search_materials(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search materials based on criteria"""
        results = []
        
        for material_id, material in self.materials.items():
            match = True
            
            # Check material type
            if 'material_type' in criteria:
                if material['type'] != criteria['material_type']:
                    match = False
            
            # Check property ranges
            properties = material['properties']
            for prop, value_range in criteria.items():
                if prop.startswith('min_') or prop.startswith('max_'):
                    prop_name = prop[4:]  # Remove min_/max_ prefix
                    if hasattr(properties, prop_name):
                        prop_value = getattr(properties, prop_name)
                        
                        if prop.startswith('min_') and prop_value < value_range:
                            match = False
                        elif prop.startswith('max_') and prop_value > value_range:
                            match = False
            
            if match:
                result = material.copy()
                result['id'] = material_id
                results.append(result)
        
        return results
    
    def compare_materials(self, material_ids: List[str]) -> Dict[str, Any]:
        """Compare multiple materials"""
        comparison = {
            'materials': [],
            'property_comparison': {},
            'cost_analysis': {},
            'recommendations': []
        }
        
        materials = [self.materials[mid] for mid in material_ids if mid in self.materials]
        
        if not materials:
            return comparison
        
        comparison['materials'] = materials
        
        # Property comparison
        properties = ['density', 'youngs_modulus', 'yield_strength', 'cost_per_kg']
        for prop in properties:
            values = [getattr(mat['properties'], prop) for mat in materials]
            comparison['property_comparison'][prop] = {
                'values': values,
                'min': min(values),
                'max': max(values),
                'range': max(values) - min(values)
            }
        
        # Generate recommendations
        if len(materials) >= 2:
            # Strength-to-weight ratio
            strength_to_weight = []
            for mat in materials:
                props = mat['properties']
                ratio = props.yield_strength / (props.density / 1000)  # MPa/(g/cm³)
                strength_to_weight.append((mat['name'], ratio))
            
            best_strength_to_weight = max(strength_to_weight, key=lambda x: x[1])
            comparison['recommendations'].append(
                f"Best strength-to-weight ratio: {best_strength_to_weight[0]} ({best_strength_to_weight[1]:.1f})"
            )
            
            # Cost effectiveness
            cost_effectiveness = []
            for mat in materials:
                props = mat['properties']
                effectiveness = props.yield_strength / props.cost_per_kg
                cost_effectiveness.append((mat['name'], effectiveness))
            
            best_cost_effective = max(cost_effectiveness, key=lambda x: x[1])
            comparison['recommendations'].append(
                f"Most cost-effective: {best_cost_effective[0]} ({best_cost_effective[1]:.1f} MPa/USD)"
            )
        
        return comparison
    
    def calculate_material_cost(self, material_id: str, volume_cm3: float, 
                              waste_factor: float = 1.2) -> Dict[str, float]:
        """Calculate material cost for given volume"""
        if material_id not in self.materials:
            return {'error': 'Material not found'}
        
        material = self.materials[material_id]
        properties = material['properties']
        
        # Calculate mass
        volume_m3 = volume_cm3 / 1e6
        mass_kg = volume_m3 * properties.density
        
        # Apply waste factor
        total_mass_kg = mass_kg * waste_factor
        
        # Calculate costs
        material_cost = total_mass_kg * properties.cost_per_kg
        
        return {
            'volume_cm3': volume_cm3,
            'mass_kg': mass_kg,
            'total_mass_with_waste_kg': total_mass_kg,
            'waste_factor': waste_factor,
            'material_cost_usd': material_cost,
            'cost_per_cm3': material_cost / volume_cm3
        }

class CADFileDatabase:
    """Database for CAD files and 3D models"""
    
    def __init__(self):
        self.cad_files = {}
        self.file_categories = {}
        self.download_stats = {}
        
        # Initialize with sample CAD files
        self._initialize_sample_files()
    
    def _initialize_sample_files(self):
        """Initialize with sample CAD files"""
        sample_files = [
            {
                'name': 'Mechanical Bearing Assembly',
                'description': 'Complete ball bearing assembly with housing and seals',
                'file_format': CADFileFormat.SOLIDWORKS,
                'file_size_mb': 15.2,
                'created_by': 'MechEngineer_Pro',
                'discipline': EngineeringDiscipline.MECHANICAL,
                'tags': ['bearing', 'assembly', 'mechanical', 'rotating'],
                'materials_used': [MaterialType.STEEL, MaterialType.RUBBER],
                'manufacturing_processes': [ManufacturingProcess.CNC_MACHINING, ManufacturingProcess.ASSEMBLY],
                'dimensions': {'length': 120, 'width': 120, 'height': 40},
                'mass': 2.5,
                'complexity_score': 7.5,
                'bill_of_materials': [
                    {'part': 'Inner race', 'material': 'Steel', 'quantity': 1, 'cost': 15.00},
                    {'part': 'Outer race', 'material': 'Steel', 'quantity': 1, 'cost': 18.00},
                    {'part': 'Ball bearings', 'material': 'Steel', 'quantity': 12, 'cost': 0.50},
                    {'part': 'Seal', 'material': 'Rubber', 'quantity': 2, 'cost': 2.00}
                ]
            },
            {
                'name': 'Electronic Enclosure Box',
                'description': 'Waterproof electronic enclosure with mounting brackets',
                'file_format': CADFileFormat.FUSION360,
                'file_size_mb': 8.7,
                'created_by': 'ElectroDesign_Studio',
                'discipline': EngineeringDisciplin
(Content truncated due to size limit. Use line ranges to read in chunks)