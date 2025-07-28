// App.js - Main entry point for the Multi-Bluetooth Speaker App

import React, { useState, useEffect, useRef } from 'react';
import {
  SafeAreaView,
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  FlatList,
  Alert,
  Platform,
  PermissionsAndroid,
} from 'react-native';
import { BleManager } from 'react-native-ble-plx';
import Slider from '@react-native-community/slider';
import { check, request, PERMISSIONS, RESULTS } from 'react-native-permissions';
import TrackPlayer from 'react-native-track-player';

// Initialize BLE Manager
const bleManager = new BleManager();

const App = () => {
  // State management
  const [scanning, setScanning] = useState(false);
  const [devices, setDevices] = useState([]); // All discovered devices
  const [connectedDevices, setConnectedDevices] = useState([]); // Connected speakers
  const [masterVolume, setMasterVolume] = useState(0.8);
  const [isPlaying, setIsPlaying] = useState(false);
  const [hasPermissions, setHasPermissions] = useState(false);
  
  // Refs for audio synchronization
  const audioSyncRef = useRef(null);
  const deviceManagerRef = useRef(null);
  
  // Track player setup
  useEffect(() => {
    const setupTrackPlayer = async () => {
      try {
        await TrackPlayer.setupPlayer();
        await TrackPlayer.updateOptions({
          stopWithApp: true,
          capabilities: [
            TrackPlayer.CAPABILITY_PLAY,
            TrackPlayer.CAPABILITY_PAUSE,
            TrackPlayer.CAPABILITY_STOP,
          ],
          compactCapabilities: [
            TrackPlayer.CAPABILITY_PLAY,
            TrackPlayer.CAPABILITY_PAUSE,
          ],
        });
      } catch (error) {
        console.error('Failed to setup track player:', error);
      }
    };
    
    setupTrackPlayer();
    
    // Cleanup
    return () => {
      TrackPlayer.destroy();
      disconnectAllDevices();
    };
  }, []);
  
  // Request necessary permissions
  useEffect(() => {
    const requestPermissions = async () => {
      if (Platform.OS === 'android') {
        // Android requires special permissions for Bluetooth scanning
        const bluetoothScanPermission = await PermissionsAndroid.request(
          PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
          {
            title: 'Bluetooth Permission',
            message: 'This app needs access to your location to scan for Bluetooth devices.',
            buttonPositive: 'OK',
          }
        );
        
        // Additional permissions for Android 12+ (S)
        if (Platform.Version >= 31) {
          const bluetoothConnectPermission = await PermissionsAndroid.request(
            PermissionsAndroid.PERMISSIONS.BLUETOOTH_CONNECT
          );
          const bluetoothScanPermission12 = await PermissionsAndroid.request(
            PermissionsAndroid.PERMISSIONS.BLUETOOTH_SCAN
          );
          
          setHasPermissions(
            bluetoothConnectPermission === PermissionsAndroid.RESULTS.GRANTED &&
            bluetoothScanPermission12 === PermissionsAndroid.RESULTS.GRANTED
          );
        } else {
          setHasPermissions(bluetoothScanPermission === PermissionsAndroid.RESULTS.GRANTED);
        }
      } else {
        // iOS permission handling
        const bluetoothPermission = await check(PERMISSIONS.IOS.BLUETOOTH_PERIPHERAL);
        
        if (bluetoothPermission !== RESULTS.GRANTED) {
          const result = await request(PERMISSIONS.IOS.BLUETOOTH_PERIPHERAL);
          setHasPermissions(result === RESULTS.GRANTED);
        } else {
          setHasPermissions(true);
        }
      }
    };
    
    requestPermissions();
  }, []);
  
  // Initialize BLE scanning
  useEffect(() => {
    if (!hasPermissions) return;
    
    // Setup BLE subscription
    const subscription = bleManager.onStateChange((state) => {
      if (state === 'PoweredOn') {
        startScan();
        subscription.remove();
      }
    }, true);
    
    return () => {
      subscription.remove();
      if (scanning) {
        bleManager.stopDeviceScan();
        setScanning(false);
      }
    };
  }, [hasPermissions]);
  
  // Start scanning for Bluetooth devices
  const startScan = () => {
    if (!hasPermissions) {
      Alert.alert('Permission Required', 'Bluetooth permissions are required to scan for devices.');
      return;
    }
    
    if (!scanning) {
      // Clear previously scanned devices
      setDevices([]);
      setScanning(true);
      
      // A2DP profile for audio devices - this is where platform limitations come in
      // iOS generally limits connections to one audio device
      bleManager.startDeviceScan(
        // Use A2DP service UUID if targeting audio devices specifically
        // For general scanning, use null for both parameters
        null, 
        null, 
        (error, device) => {
          if (error) {
            console.error('Scan error:', error);
            setScanning(false);
            return;
          }
          
          // Filter only audio devices (you may need to adjust this based on testing)
          if (
            device && 
            device.name && 
            !devices.find(d => d.id === device.id) && 
            (device.name.toLowerCase().includes('speaker') || 
             device.name.toLowerCase().includes('audio') ||
             device.name.toLowerCase().includes('sound'))
          ) {
            setDevices(prevDevices => [...prevDevices, device]);
          }
        }
      );
      
      // Stop scan after 10 seconds to preserve battery
      setTimeout(() => {
        bleManager.stopDeviceScan();
        setScanning(false);
      }, 10000);
    }
  };
  
  // Connect to a specific Bluetooth device
  const connectToDevice = async (device) => {
    try {
      // Check if already connected
      if (connectedDevices.find(d => d.id === device.id)) {
        console.log('Already connected to this device');
        return;
      }
      
      console.log(`Connecting to device: ${device.name}`);
      
      // Connect to the device
      const connectedDevice = await device.connect();
      
      // Discover services and characteristics
      const discoveredDevice = await connectedDevice.discoverAllServicesAndCharacteristics();
      
      // Retrieve services
      const services = await discoveredDevice.services();
      
      // Look for A2DP (Advanced Audio Distribution Profile) service
      // This is a simplification - actual implementation requires more complex service discovery
      const audioService = services.find(service => 
        service.uuid.toLowerCase().includes('110a') || // A2DP service UUID
        service.uuid.toLowerCase().includes('110b')    // Audio service
      );
      
      if (!audioService) {
        Alert.alert('Not an audio device', 'This device does not support audio streaming.');
        await connectedDevice.cancelConnection();
        return;
      }
      
      // Add to connected devices
      setConnectedDevices(prev => [...prev, {
        ...device,
        volume: 0.8, // Default volume for this speaker
        latencyOffset: 0, // Will be calibrated during playback
      }]);
      
      // Success message
      Alert.alert('Connected', `Successfully connected to ${device.name}`);
      
      // If this is the first device, initialize synchronized audio context
      if (connectedDevices.length === 0) {
        initAudioSynchronization();
      } else {
        // If already playing, sync this new speaker
        if (isPlaying) {
          syncNewSpeaker(device);
        }
      }
    } catch (error) {
      console.error(`Connection error: ${error.message}`);
      Alert.alert('Connection Failed', `Could not connect to ${device.name}. ${error.message}`);
    }
  };
  
  // Disconnect from a specific device
  const disconnectDevice = async (deviceId) => {
    try {
      const device = connectedDevices.find(d => d.id === deviceId);
      if (device) {
        await bleManager.cancelDeviceConnection(deviceId);
        setConnectedDevices(prev => prev.filter(d => d.id !== deviceId));
        
        // If all devices disconnected, stop playback
        if (connectedDevices.length === 1) { // Will be 0 after state update
          if (isPlaying) {
            stopPlayback();
          }
        }
      }
    } catch (error) {
      console.error(`Disconnect error: ${error.message}`);
    }
  };
  
  // Disconnect all devices
  const disconnectAllDevices = async () => {
    try {
      for (const device of connectedDevices) {
        await bleManager.cancelDeviceConnection(device.id);
      }
      setConnectedDevices([]);
      if (isPlaying) {
        stopPlayback();
      }
    } catch (error) {
      console.error(`Disconnect all error: ${error.message}`);
    }
  };
  
  // Update volume for a specific device
  const updateDeviceVolume = (deviceId, volume) => {
    setConnectedDevices(prev => 
      prev.map(d => d.id === deviceId ? { ...d, volume } : d)
    );
    
    // Send volume command to the device
    // Implementation depends on the device's characteristics
    // This is a placeholder for device-specific implementation
    try {
      const device = connectedDevices.find(d => d.id === deviceId);
      if (device) {
        // This is where you'd send the volume command to the actual device
        // The implementation varies based on the speaker's protocol
        console.log(`Set ${device.name} volume to ${volume}`);
        
        // Example implementation:
        // device.writeCharacteristicWithResponseForService(
        //   'audio_service_uuid',
        //   'volume_characteristic_uuid',
        //   Base64.encode(`${Math.round(volume * 100)}`)
        // );
      }
    } catch (error) {
      console.error(`Set volume error: ${error.message}`);
    }
  };
  
  // Update master volume
  const updateMasterVolume = (volume) => {
    setMasterVolume(volume);
    
    // Apply master volume to all connected devices
    connectedDevices.forEach(device => {
      // Apply individual device volume scaled by master volume
      const effectiveVolume = device.volume * volume;
      // Send the volume command to each device
      // This is a placeholder for device-specific implementation
      console.log(`Set ${device.name} effective volume to ${effectiveVolume}`);
    });
  };
  
  // Initialize audio synchronization
  const initAudioSynchronization = () => {
    // This would be a complex implementation that:
    // 1. Measures latency to each speaker
    // 2. Creates a buffer management system
    // 3. Sets up timing mechanisms for perfect sync
    
    // Placeholder for actual implementation
    audioSyncRef.current = {
      startTime: null,
      bufferLength: 500, // ms
      // More properties for sync management
    };
    
    console.log('Audio synchronization initialized');
  };
  
  // Synchronize a newly added speaker
  const syncNewSpeaker = (device) => {
    // 1. Send test audio to measure latency
    // 2. Add latency offset to device configuration
    // 3. Adjust buffer timing
    
    // Placeholder implementation
    console.log(`Synchronizing new speaker: ${device.name}`);
    
    // Measure round-trip latency (simplified)
    setTimeout(() => {
      // Set a mock latency offset for demonstration
      setConnectedDevices(prev => 
        prev.map(d => d.id === device.id ? { ...d, latencyOffset: 120 } : d)
      );
    }, 500);
  };
  
  // Start playback
  const startPlayback = async () => {
    if (connectedDevices.length === 0) {
      Alert.alert('No Speakers', 'Please connect at least one speaker.');
      return;
    }
    
    try {
      // Setup audio track (example)
      await TrackPlayer.reset();
      await TrackPlayer.add({
        id: 'test_track',
        url: 'file:///your-audio-file.mp3', // Replace with actual file or stream URL
        title: 'Test Audio',
        artist: 'MultiSpeaker App',
      });
      
      // Initialize synchronization timing
      initAudioSynchronization();
      audioSyncRef.current.startTime = Date.now();
      
      // Start playback
      await TrackPlayer.play();
      setIsPlaying(true);
      
      // Apply volume settings
      updateMasterVolume(masterVolume);
    } catch (error) {
      console.error(`Playback error: ${error.message}`);
      Alert.alert('Playback Failed', error.message);
    }
  };
  
  // Stop playback
  const stopPlayback = async () => {
    try {
      await TrackPlayer.stop();
      setIsPlaying(false);
      
      // Reset sync state
      if (audioSyncRef.current) {
        audioSyncRef.current.startTime = null;
      }
    } catch (error) {
      console.error(`Stop playback error: ${error.message}`);
    }
  };
  
  // Toggle playback
  const togglePlayback = () => {
    if (isPlaying) {
      stopPlayback();
    } else {
      startPlayback();
    }
  };
  
  // Component for each discovered device item
  const DeviceItem = ({ device }) => {
    const isConnected = connectedDevices.some(d => d.id === device.id);
    
    return (
      <TouchableOpacity
        style={[styles.deviceItem, isConnected && styles.connectedDevice]}
        onPress={() => isConnected ? disconnectDevice(device.id) : connectToDevice(device)}
      >
        <Text style={styles.deviceName}>{device.name || 'Unknown Device'}</Text>
        <Text style={styles.deviceInfo}>ID: {device.id}</Text>
        <Text style={styles.deviceStatus}>
          {isConnected ? 'Connected (Tap to disconnect)' : 'Tap to connect'}
        </Text>
      </TouchableOpacity>
    );
  };
  
  // Component for each connected speaker with volume control
  const ConnectedSpeakerItem = ({ device }) => {
    return (
      <View style={styles.connectedSpeaker}>
        <Text style={styles.speakerName}>{device.name || 'Unknown Speaker'}</Text>
        
        <View style={styles.volumeControl}>
          <Text>Volume:</Text>
          <Slider
            style={styles.slider}
            minimumValue={0}
            maximumValue={1}
            value={device.volume}
            onValueChange={(value) => updateDeviceVolume(device.id, value)}
            minimumTrackTintColor="#4CAF50"
            maximumTrackTintColor="#000000"
          />
          <Text>{Math.round(device.volume * 100)}%</Text>
        </View>
        
        <TouchableOpacity
          style={styles.disconnectButton}
          onPress={() => disconnectDevice(device.id)}
        >
          <Text style={styles.disconnectText}>Disconnect</Text>
        </TouchableOpacity>
      </View>
    );
  };
  
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>MultiSpeaker Connector</Text>
      </View>
      
      {/* Connected Speakers Section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Connected Speakers ({connectedDevices.length})</Text>
        
        {connectedDevices.length === 0 ? (
          <Text style={styles.noDevicesText}>No speakers connected</Text>
        ) : (
          <FlatList
            data={connectedDevices}
            renderItem={({ item }) => <ConnectedSpeakerItem device={item} />}
            keyExtractor={item => item.id}
            style={styles.connectedList}
          />
        )}
        
        {/* Master Volume Control */}
        {connectedDevices.length > 0 && (
          <View style={styles.masterVolumeContainer}>
            <Text style={styles.masterVolumeText}>Master Volume:</Text>
            <Slider
              style={styles.masterSlider}
              minimumValue={0}
              maximumValue={1}
              value={masterVolume}
              onValueChange={updateMasterVolume}
              minimumTrackTintColor="#2196F3"
              maximumTrackTintColor="#000000"
            />
            <Text>{Math.round(masterVolume * 100)}%</Text>
          </View>
        )}
        
        {/* Playback Controls */}
        {connectedDevices.length > 0 && (
          <TouchableOpacity
            style={[styles.playbackButton, isPlaying && styles.stopButton]}
            onPress={togglePlayback}
          >
            <Text style={styles.playbackButtonText}>
              {isPlaying ? 'Stop Playback' : 'Start Playback'}
            </Text>
          </TouchableOpacity>
        )}
      </View>
      
      {/* Available Devices Section */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Available Devices</Text>
          <TouchableOpacity
            style={styles.scanButton}
            onPress={startScan}
            disabled={scanning || !hasPermissions}
          >
            <Text style={styles.scanButtonText}>
              {scanning ? 'Scanning...' : 'Scan'}
            </Text>
          </TouchableOpacity>
        </View>
        
        {!hasPermissions && (
          <Text style={styles.permissionText}>
            Bluetooth permissions are required. Please grant permissions in settings.
          </Text>
        )}
        
        {devices.length === 0 ? (
          <Text style={styles.noDevicesText}>
            {scanning ? 'Searching for devices...' : 'No devices found. Tap Scan to search.'}
          </Text>
        ) : (
          <FlatList
            data={devices}
            renderItem={({ item }) => <DeviceItem device={item} />}
            keyExtractor={item => item.id}
            style={styles.deviceList}
          />
        )}
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  header: {
    backgroundColor: '#2196F3',
    padding: 16,
    alignItems: 'center',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    color: 'white',
  },
  section: {
    margin: 16,
    backgroundColor: 'white',
    borderRadius: 8,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  scanButton: {
    backgroundColor: '#4CAF50',
    padding: 8,
    borderRadius: 4,
  },
  scanButtonText: {
    color: 'white',
    fontWeight: 'bold',
  },
  deviceList: {
    maxHeight: 200,
  },
  deviceItem: {
    padding: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  connectedDevice: {
    backgroundColor: '#E8F5E9',
  },
  deviceName: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  deviceInfo: {
    fontSize: 12,
    color: '#757575',
  },
  deviceStatus: {
    fontSize: 14,
    color: '#2196F3',
    marginTop: 4,
  },
  noDevicesText: {
    textAlign: 'center',
    padding: 16,
    color: '#757575',
  },
  permissionText: {
    textAlign: 'center',
    padding: 16,
    color: '#F44336',
  },
  connectedList: {
    maxHeight: 300,
  },
  connectedSpeaker: {
    padding: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  speakerName: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  volumeControl: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 8,
  },
  slider: {
    flex: 1,
    marginHorizontal: 8,
  },
  disconnectButton: {
    alignSelf: 'flex-end',
    backgroundColor: '#F44336',
    padding: 6,
    borderRadius: 4,
    marginTop: 8,
  },
  disconnectText: {
    color: 'white',
  },
  masterVolumeContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    backgroundColor: '#E3F2FD',
    borderRadius: 8,
    marginVertical: 16,
  },
  masterVolumeText: {
    fontWeight: 'bold',
    marginRight: 8,
  },
  masterSlider: {
    flex: 1,
    marginHorizontal: 8,
  },
  playbackButton: {
    backgroundColor: '#2196F3',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  stopButton: {
    backgroundColor: '#F44336',
  },
  playbackButtonText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 16,
  },
});

export default App;
