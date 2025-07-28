"""
Manufacturing IoT Integration System
Comprehensive IoT integration for manufacturing machines (3D printers, CNC, laser engravers, etc.)
"""

import asyncio
import json
import uuid
import time
import threading
import queue
import socket
import serial
import struct
from typing import Dict, List, Optional, Any, Union, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import base64
import websockets
import aiohttp
import numpy as np

class MachineType(Enum):
    THREE_D_PRINTER = "3d_printer"
    CNC_MILL = "cnc_mill"
    CNC_LATHE = "cnc_lathe"
    LASER_ENGRAVER = "laser_engraver"
    LASER_CUTTER = "laser_cutter"
    WATERJET_CUTTER = "waterjet_cutter"
    PLASMA_CUTTER = "plasma_cutter"
    INJECTION_MOLDING = "injection_molding"
    PICK_AND_PLACE = "pick_and_place"
    ROBOTIC_ARM = "robotic_arm"
    CONVEYOR_SYSTEM = "conveyor_system"
    QUALITY_SCANNER = "quality_scanner"

class MachineStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"
    SETUP = "setup"
    WARMING_UP = "warming_up"
    COOLING_DOWN = "cooling_down"

class FileFormat(Enum):
    GCODE = "gcode"
    STL = "stl"
    OBJ = "obj"
    STEP = "step"
    DXF = "dxf"
    SVG = "svg"
    GERBER = "gerber"
    NC = "nc"
    TAP = "tap"
    PLT = "plt"

class CommunicationProtocol(Enum):
    SERIAL = "serial"
    ETHERNET = "ethernet"
    USB = "usb"
    WIFI = "wifi"
    BLUETOOTH = "bluetooth"
    MODBUS = "modbus"
    OPCUA = "opcua"
    MQTT = "mqtt"
    HTTP_REST = "http_rest"
    WEBSOCKET = "websocket"

@dataclass
class MachineCapabilities:
    supported_materials: List[str]
    supported_file_formats: List[FileFormat]
    max_build_volume: Dict[str, float]  # x, y, z in mm
    resolution: Dict[str, float]  # x, y, z resolution in mm
    max_speed: float  # mm/min
    temperature_range: Optional[Dict[str, float]]  # min, max in Celsius
    power_rating: float  # Watts
    precision: float  # mm
    repeatability: float  # mm

@dataclass
class MachineConfiguration:
    id: str
    name: str
    machine_type: MachineType
    manufacturer: str
    model: str
    serial_number: str
    firmware_version: str
    capabilities: MachineCapabilities
    communication: Dict[str, Any]
    location: Dict[str, str]
    installation_date: datetime
    last_maintenance: datetime
    next_maintenance: datetime

@dataclass
class JobParameters:
    material: str
    layer_height: Optional[float]  # For 3D printing
    infill_percentage: Optional[float]  # For 3D printing
    cutting_speed: Optional[float]  # For CNC/Laser
    spindle_speed: Optional[float]  # For CNC
    laser_power: Optional[float]  # For laser cutting/engraving
    coolant: Optional[bool]  # For CNC
    temperature: Optional[Dict[str, float]]  # Extruder/bed temps
    custom_parameters: Dict[str, Any]

@dataclass
class ManufacturingJob:
    id: str
    name: str
    description: str
    machine_id: str
    file_path: str
    file_format: FileFormat
    parameters: JobParameters
    estimated_duration: float  # minutes
    estimated_cost: float
    priority: int
    created_by: str
    created_at: datetime
    scheduled_start: Optional[datetime]
    actual_start: Optional[datetime]
    actual_end: Optional[datetime]
    status: str
    progress_percentage: float
    quality_requirements: Dict[str, Any]

@dataclass
class MachineMetrics:
    timestamp: datetime
    machine_id: str
    status: MachineStatus
    temperature: Dict[str, float]
    position: Dict[str, float]
    speed: float
    power_consumption: float
    vibration: Dict[str, float]
    error_codes: List[str]
    job_progress: float
    material_usage: float
    tool_wear: float

class MachineController:
    """Base class for machine controllers"""
    
    def __init__(self, machine_config: MachineConfiguration):
        self.config = machine_config
        self.connection = None
        self.is_connected = False
        self.current_job = None
        self.metrics_queue = queue.Queue()
        self.command_queue = queue.Queue()
        self.status = MachineStatus.OFFLINE
        
        # Start monitoring thread
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
    
    async def connect(self) -> bool:
        """Connect to machine"""
        try:
            protocol = self.config.communication.get('protocol')
            
            if protocol == CommunicationProtocol.SERIAL.value:
                await self._connect_serial()
            elif protocol == CommunicationProtocol.ETHERNET.value:
                await self._connect_ethernet()
            elif protocol == CommunicationProtocol.WEBSOCKET.value:
                await self._connect_websocket()
            else:
                await self._connect_generic()
            
            self.is_connected = True
            self.status = MachineStatus.IDLE
            return True
            
        except Exception as e:
            print(f"Connection error for {self.config.name}: {e}")
            return False
    
    async def _connect_serial(self):
        """Connect via serial port"""
        port = self.config.communication.get('port', '/dev/ttyUSB0')
        baudrate = self.config.communication.get('baudrate', 115200)
        
        # Simulate serial connection
        await asyncio.sleep(0.1)
        print(f"Connected to {self.config.name} via serial {port}")
    
    async def _connect_ethernet(self):
        """Connect via Ethernet"""
        host = self.config.communication.get('host', '192.168.1.100')
        port = self.config.communication.get('port', 80)
        
        # Simulate TCP connection
        await asyncio.sleep(0.1)
        print(f"Connected to {self.config.name} via Ethernet {host}:{port}")
    
    async def _connect_websocket(self):
        """Connect via WebSocket"""
        url = self.config.communication.get('url', 'ws://192.168.1.100:8080')
        
        # Simulate WebSocket connection
        await asyncio.sleep(0.1)
        print(f"Connected to {self.config.name} via WebSocket {url}")
    
    async def _connect_generic(self):
        """Generic connection method"""
        await asyncio.sleep(0.1)
        print(f"Connected to {self.config.name} via generic protocol")
    
    async def disconnect(self):
        """Disconnect from machine"""
        self.is_connected = False
        self.status = MachineStatus.OFFLINE
        print(f"Disconnected from {self.config.name}")
    
    async def send_file(self, file_path: str, file_format: FileFormat) -> bool:
        """Send file to machine"""
        if not self.is_connected:
            return False
        
        try:
            # Validate file format
            if file_format not in self.config.capabilities.supported_file_formats:
                raise ValueError(f"Unsupported file format: {file_format}")
            
            # Simulate file transfer
            file_size = 1024 * 1024  # 1MB simulation
            transfer_speed = 100 * 1024  # 100KB/s
            transfer_time = file_size / transfer_speed
            
            print(f"Transferring {file_path} to {self.config.name}...")
            await asyncio.sleep(transfer_time)
            print(f"File transfer completed to {self.config.name}")
            
            return True
            
        except Exception as e:
            print(f"File transfer error: {e}")
            return False
    
    async def start_job(self, job: ManufacturingJob) -> bool:
        """Start manufacturing job"""
        if not self.is_connected or self.status != MachineStatus.IDLE:
            return False
        
        try:
            # Validate job parameters
            if not self._validate_job_parameters(job):
                return False
            
            # Send file to machine
            if not await self.send_file(job.file_path, job.file_format):
                return False
            
            # Configure machine parameters
            await self._configure_machine(job.parameters)
            
            # Start job
            self.current_job = job
            self.status = MachineStatus.RUNNING
            job.actual_start = datetime.now()
            job.status = "running"
            
            print(f"Started job {job.name} on {self.config.name}")
            return True
            
        except Exception as e:
            print(f"Job start error: {e}")
            return False
    
    def _validate_job_parameters(self, job: ManufacturingJob) -> bool:
        """Validate job parameters against machine capabilities"""
        # Check material compatibility
        if job.parameters.material not in self.config.capabilities.supported_materials:
            print(f"Unsupported material: {job.parameters.material}")
            return False
        
        # Check file format
        if job.file_format not in self.config.capabilities.supported_file_formats:
            print(f"Unsupported file format: {job.file_format}")
            return False
        
        # Check temperature limits
        if job.parameters.temperature and self.config.capabilities.temperature_range:
            for temp_type, temp_value in job.parameters.temperature.items():
                min_temp = self.config.capabilities.temperature_range.get('min', 0)
                max_temp = self.config.capabilities.temperature_range.get('max', 300)
                
                if not (min_temp <= temp_value <= max_temp):
                    print(f"Temperature {temp_value}°C out of range [{min_temp}, {max_temp}]")
                    return False
        
        return True
    
    async def _configure_machine(self, parameters: JobParameters):
        """Configure machine with job parameters"""
        config_commands = []
        
        # Temperature settings
        if parameters.temperature:
            for temp_type, temp_value in parameters.temperature.items():
                config_commands.append(f"SET_TEMP_{temp_type.upper()}:{temp_value}")
        
        # Speed settings
        if parameters.cutting_speed:
            config_commands.append(f"SET_SPEED:{parameters.cutting_speed}")
        
        if parameters.spindle_speed:
            config_commands.append(f"SET_SPINDLE:{parameters.spindle_speed}")
        
        # Laser power
        if parameters.laser_power:
            config_commands.append(f"SET_LASER_POWER:{parameters.laser_power}")
        
        # Send configuration commands
        for command in config_commands:
            await self._send_command(command)
            await asyncio.sleep(0.1)
    
    async def _send_command(self, command: str) -> str:
        """Send command to machine"""
        if not self.is_connected:
            return "ERROR: Not connected"
        
        # Simulate command execution
        await asyncio.sleep(0.05)
        
        # Generate response based on command
        if command.startswith("GET_STATUS"):
            return f"STATUS:{self.status.value}"
        elif command.startswith("GET_POSITION"):
            return "POSITION:X100.5,Y200.3,Z50.1"
        elif command.startswith("GET_TEMP"):
            return "TEMP:EXTRUDER:210,BED:60"
        else:
            return "OK"
    
    async def pause_job(self) -> bool:
        """Pause current job"""
        if self.status == MachineStatus.RUNNING:
            await self._send_command("PAUSE")
            self.status = MachineStatus.PAUSED
            if self.current_job:
                self.current_job.status = "paused"
            return True
        return False
    
    async def resume_job(self) -> bool:
        """Resume paused job"""
        if self.status == MachineStatus.PAUSED:
            await self._send_command("RESUME")
            self.status = MachineStatus.RUNNING
            if self.current_job:
                self.current_job.status = "running"
            return True
        return False
    
    async def stop_job(self) -> bool:
        """Stop current job"""
        if self.status in [MachineStatus.RUNNING, MachineStatus.PAUSED]:
            await self._send_command("STOP")
            self.status = MachineStatus.IDLE
            if self.current_job:
                self.current_job.status = "stopped"
                self.current_job.actual_end = datetime.now()
                self.current_job = None
            return True
        return False
    
    def _monitoring_loop(self):
        """Background monitoring loop"""
        while True:
            try:
                if self.is_connected:
                    metrics = self._collect_metrics()
                    self.metrics_queue.put(metrics)
                
                time.sleep(1)  # Collect metrics every second
                
            except Exception as e:
                print(f"Monitoring error for {self.config.name}: {e}")
                time.sleep(5)
    
    def _collect_metrics(self) -> MachineMetrics:
        """Collect current machine metrics"""
        # Simulate metric collection
        metrics = MachineMetrics(
            timestamp=datetime.now(),
            machine_id=self.config.id,
            status=self.status,
            temperature={
                'extruder': 210.5 + np.random.uniform(-2, 2),
                'bed': 60.2 + np.random.uniform(-1, 1),
                'ambient': 22.0 + np.random.uniform(-0.5, 0.5)
            },
            position={
                'x': 100.0 + np.random.uniform(-0.1, 0.1),
                'y': 200.0 + np.random.uniform(-0.1, 0.1),
                'z': 50.0 + np.random.uniform(-0.05, 0.05)
            },
            speed=1500.0 + np.random.uniform(-50, 50),
            power_consumption=250.0 + np.random.uniform(-10, 10),
            vibration={
                'x': np.random.uniform(0, 0.1),
                'y': np.random.uniform(0, 0.1),
                'z': np.random.uniform(0, 0.05)
            },
            error_codes=[],
            job_progress=self._calculate_job_progress(),
            material_usage=self._calculate_material_usage(),
            tool_wear=np.random.uniform(0, 100)
        )
        
        return metrics
    
    def _calculate_job_progress(self) -> float:
        """Calculate current job progress"""
        if not self.current_job or self.status != MachineStatus.RUNNING:
            return 0.0
        
        if not self.current_job.actual_start:
            return 0.0
        
        elapsed_time = (datetime.now() - self.current_job.actual_start).total_seconds() / 60
        progress = min(100.0, (elapsed_time / self.current_job.estimated_duration) * 100)
        
        # Update job progress
        self.current_job.progress_percentage = progress
        
        # Check if job is complete
        if progress >= 100.0:
            self.status = MachineStatus.IDLE
            self.current_job.status = "completed"
            self.current_job.actual_end = datetime.now()
            self.current_job = None
        
        return progress
    
    def _calculate_material_usage(self) -> float:
        """Calculate material usage"""
        if not self.current_job:
            return 0.0
        
        # Simulate material usage based on progress
        return self.current_job.progress_percentage * 0.5  # 50g max usage

class ThreeDPrinterController(MachineController):
    """Specialized controller for 3D printers"""
    
    def __init__(self, machine_config: MachineConfiguration):
        super().__init__(machine_config)
        self.extruder_temp = 0.0
        self.bed_temp = 0.0
        self.filament_remaining = 1000.0  # grams
    
    async def load_filament(self, filament_type: str) -> bool:
        """Load filament into printer"""
        if self.status != MachineStatus.IDLE:
            return False
        
        print(f"Loadi
(Content truncated due to size limit. Use line ranges to read in chunks)