// src/services/SecureAudioChannel.js

import CryptoJS from 'crypto-js';

/**
 * Secure Audio Channel
 * 
 * Provides end-to-end encrypted audio streaming between devices
 * using WebRTC and custom encryption protocols.
 */
class SecureAudioChannel {
  constructor() {
    this.initialized = false;
    this.peerConnections = {};
    this.dataChannels = {};
    this.encryptionKeys = {};
    this.signaling = null;
    this.localStream = null;
    this.audioContext = null;
    this.encryptionEnabled = true;
    this.audioProcessingNode = null;
    this.bufferSize = 4096;
    this.channelId = null;
    this.userId = null;
    this.peers = [];
    this.latencyCompensation = {};
    this.cryptoSuite = 'AES-256-GCM';
    this.keyRotationInterval = 30 * 60 * 1000; // 30 minutes
    this.keyRotationTimer = null;
    this.connectionStateCallbacks = [];
    this.errorCallbacks = [];
  }
  
  /**
   * Initialize the secure audio channel
   * @param {Object} options - Initialization options
   * @returns {Promise<boolean>} Success status
   */
  async initialize(options = {}) {
    try {
      const { 
        channelId, 
        userId, 
        signalingServer, 
        encryptionEnabled = true,
        cryptoSuite = 'AES-256-GCM',
        keyRotationInterval = 30 * 60 * 1000
      } = options;
      
      if (!channelId || !userId || !signalingServer) {
        throw new Error('Missing required parameters for SecureAudioChannel');
      }
      
      this.channelId = channelId;
      this.userId = userId;
      this.encryptionEnabled = encryptionEnabled;
      this.cryptoSuite = cryptoSuite;
      this.keyRotationInterval = keyRotationInterval;
      
      // Initialize Web Audio API
      window.AudioContext = window.AudioContext || window.webkitAudioContext;
      this.audioContext = new AudioContext();
      
      // Connect to signaling server
      this.signaling = new WebSocket(signalingServer);
      
      // Set up signaling channel handlers
      this.signaling.onopen = this.handleSignalingOpen.bind(this);
      this.signaling.onmessage = this.handleSignalingMessage.bind(this);
      this.signaling.onerror = this.handleSignalingError.bind(this);
      this.signaling.onclose = this.handleSignalingClose.bind(this);
      
      // Generate initial encryption keys
      if (this.encryptionEnabled) {
        await this.generateEncryptionKeys();
        this.startKeyRotation();
      }
      
      this.initialized = true;
      console.log(`Secure Audio Channel initialized for channel ${channelId}`);
      
      return true;
    } catch (error) {
      console.error('Failed to initialize SecureAudioChannel:', error);
      this.notifyError('initialization', error.message);
      return false;
    }
  }
  
  /**
   * Handle signaling channel open
   */
  handleSignalingOpen() {
    console.log('Signaling connection established');
    
    // Join channel
    this.sendSignalingMessage({
      type: 'join',
      channelId: this.channelId,
      userId: this.userId
    });
  }
  
  /**
   * Handle signaling channel message
   * @param {MessageEvent} event - WebSocket message event
   */
  handleSignalingMessage(event) {
    try {
      const message = JSON.parse(event.data);
      
      switch (message.type) {
        case 'peers':
          this.handlePeersList(message.peers);
          break;
        case 'offer':
          this.handleOffer(message);
          break;
        case 'answer':
          this.handleAnswer(message);
          break;
        case 'ice-candidate':
          this.handleIceCandidate(message);
          break;
        case 'key-exchange':
          this.handleKeyExchange(message);
          break;
        case 'peer-joined':
          this.handlePeerJoined(message.peerId);
          break;
        case 'peer-left':
          this.handlePeerLeft(message.peerId);
          break;
        case 'latency-data':
          this.handleLatencyData(message);
          break;
        default:
          console.warn('Unknown signaling message type:', message.type);
      }
    } catch (error) {
      console.error('Failed to handle signaling message:', error);
    }
  }
  
  /**
   * Handle signaling channel error
   * @param {Event} error - WebSocket error event
   */
  handleSignalingError(error) {
    console.error('Signaling connection error:', error);
    this.notifyError('signaling', 'Connection error with signaling server');
  }
  
  /**
   * Handle signaling channel close
   */
  handleSignalingClose() {
    console.log('Signaling connection closed');
    this.reconnectSignaling();
  }
  
  /**
   * Attempt to reconnect to signaling server
   */
  reconnectSignaling() {
    setTimeout(() => {
      if (this.signaling && this.signaling.readyState === WebSocket.CLOSED) {
        console.log('Attempting to reconnect to signaling server...');
        this.signaling = new WebSocket(this.signaling.url);
        this.signaling.onopen = this.handleSignalingOpen.bind(this);
        this.signaling.onmessage = this.handleSignalingMessage.bind(this);
        this.signaling.onerror = this.handleSignalingError.bind(this);
        this.signaling.onclose = this.handleSignalingClose.bind(this);
      }
    }, 5000); // Retry after 5 seconds
  }
  
  /**
   * Send message through signaling channel
   * @param {Object} message - Message to send
   */
  sendSignalingMessage(message) {
    if (this.signaling && this.signaling.readyState === WebSocket.OPEN) {
      this.signaling.send(JSON.stringify(message));
    } else {
      console.warn('Signaling channel not open, message not sent');
    }
  }
  
  /**
   * Handle peers list received from server
   * @param {Array<string>} peers - List of peer IDs
   */
  handlePeersList(peers) {
    console.log('Received peers list:', peers);
    
    // Filter out own ID
    this.peers = peers.filter(peerId => peerId !== this.userId);
    
    // Create peer connections for each peer
    this.peers.forEach(peerId => {
      this.createPeerConnection(peerId, true); // Initiator = true
    });
  }
  
  /**
   * Handle new peer joined
   * @param {string} peerId - ID of peer that joined
   */
  handlePeerJoined(peerId) {
    console.log('Peer joined:', peerId);
    
    if (peerId !== this.userId) {
      // Add to peers list
      if (!this.peers.includes(peerId)) {
        this.peers.push(peerId);
      }
      
      // Create peer connection
      this.createPeerConnection(peerId, true); // Initiator = true
    }
  }
  
  /**
   * Handle peer left
   * @param {string} peerId - ID of peer that left
   */
  handlePeerLeft(peerId) {
    console.log('Peer left:', peerId);
    
    // Remove from peers list
    this.peers = this.peers.filter(id => id !== peerId);
    
    // Close peer connection
    this.closePeerConnection(peerId);
  }
  
  /**
   * Create peer connection
   * @param {string} peerId - ID of peer to connect to
   * @param {boolean} isInitiator - Whether this peer is the initiator
   */
  async createPeerConnection(peerId, isInitiator) {
    try {
      // Skip if connection already exists
      if (this.peerConnections[peerId]) {
        return;
      }
      
      console.log(`Creating peer connection with ${peerId} (initiator: ${isInitiator})`);
      
      const configuration = {
        iceServers: [
          { urls: 'stun:stun.l.google.com:19302' },
          { urls: 'stun:stun1.l.google.com:19302' }
        ]
      };
      
      // Create peer connection
      const peerConnection = new RTCPeerConnection(configuration);
      this.peerConnections[peerId] = peerConnection;
      
      // Create data channel for control messages
      if (isInitiator) {
        const dataChannel = peerConnection.createDataChannel('control', {
          ordered: true
        });
        this.setupDataChannel(peerId, dataChannel);
      } else {
        peerConnection.ondatachannel = (event) => {
          this.setupDataChannel(peerId, event.channel);
        };
      }
      
      // Set up event handlers
      peerConnection.onicecandidate = (event) => {
        if (event.candidate) {
          this.sendSignalingMessage({
            type: 'ice-candidate',
            candidate: event.candidate,
            targetId: peerId,
            senderId: this.userId
          });
        }
      };
      
      peerConnection.oniceconnectionstatechange = () => {
        console.log(`ICE connection state with ${peerId}: ${peerConnection.iceConnectionState}`);
        this.notifyConnectionState(peerId, peerConnection.iceConnectionState);
      };
      
      peerConnection.onconnectionstatechange = () => {
        console.log(`Connection state with ${peerId}: ${peerConnection.connectionState}`);
        this.notifyConnectionState(peerId, peerConnection.connectionState);
      };
      
      // Add local stream if available
      if (this.localStream) {
        this.localStream.getTracks().forEach(track => {
          peerConnection.addTrack(track, this.localStream);
        });
      }
      
      // Create and send offer if initiator
      if (isInitiator) {
        const offer = await peerConnection.createOffer();
        await peerConnection.setLocalDescription(offer);
        
        this.sendSignalingMessage({
          type: 'offer',
          sdp: peerConnection.localDescription,
          targetId: peerId,
          senderId: this.userId
        });
      }
      
      // Exchange encryption keys if enabled
      if (this.encryptionEnabled) {
        this.exchangeEncryptionKeys(peerId);
      }
    } catch (error) {
      console.error(`Failed to create peer connection with ${peerId}:`, error);
      this.notifyError('peerConnection', `Failed to connect with peer ${peerId}`);
    }
  }
  
  /**
   * Set up data channel
   * @param {string} peerId - ID of peer
   * @param {RTCDataChannel} dataChannel - WebRTC data channel
   */
  setupDataChannel(peerId, dataChannel) {
    this.dataChannels[peerId] = dataChannel;
    
    dataChannel.onopen = () => {
      console.log(`Data channel with ${peerId} opened`);
    };
    
    dataChannel.onclose = () => {
      console.log(`Data channel with ${peerId} closed`);
    };
    
    dataChannel.onerror = (error) => {
      console.error(`Data channel error with ${peerId}:`, error);
    };
    
    dataChannel.onmessage = (event) => {
      this.handleDataChannelMessage(peerId, event);
    };
  }
  
  /**
   * Handle data channel message
   * @param {string} peerId - ID of peer
   * @param {MessageEvent} event - Data channel message event
   */
  handleDataChannelMessage(peerId, event) {
    try {
      const message = JSON.parse(event.data);
      
      switch (message.type) {
        case 'latency-ping':
          this.handleLatencyPing(peerId, message);
          break;
        case 'latency-pong':
          this.handleLatencyPong(peerId, message);
          break;
        case 'audio-control':
          this.handleAudioControl(peerId, message);
          break;
        case 'encryption-key':
          this.handleEncryptionKey(peerId, message);
          break;
        default:
          console.warn('Unknown data channel message type:', message.type);
      }
    } catch (error) {
      console.error('Failed to handle data channel message:', error);
    }
  }
  
  /**
   * Handle WebRTC offer
   * @param {Object} message - Offer message
   */
  async handleOffer(message) {
    try {
      const { sdp, senderId } = message;
      
      // Create peer connection if it doesn't exist
      if (!this.peerConnections[senderId]) {
        this.createPeerConnection(senderId, false); // Initiator = false
      }
      
      const peerConnection = this.peerConnections[senderId];
      
      // Set remote description
      await peerConnection.setRemoteDescription(new RTCSessionDescription(sdp));
      
      // Create answer
      const answer = await peerConnection.createAnswer();
      await peerConnection.setLocalDescription(answer);
      
      // Send answer
      this.sendSignalingMessage({
        type: 'answer',
        sdp: peerConnection.localDescription,
        targetId: senderId,
        senderId: this.userId
      });
    } catch (error) {
      console.error('Failed to handle offer:', error);
      this.notifyError('offer', 'Failed to process connection offer');
    }
  }
  
  /**
   * Handle WebRTC answer
   * @param {Object} message - Answer message
   */
  async handleAnswer(message) {
    try {
      const { sdp, senderId } = message;
      
      // Check for peer connection
      if (!this.peerConnections[senderId]) {
        console.warn(`No peer connection found for ${senderId}`);
        return;
      }
      
      const peerConnection = this.peerConnections[senderId];
      
      // Set remote description
      await peerConnection.setRemoteDescription(new RTCSessionDescription(sdp));
      
      console.log(`Answer processed for peer ${senderId}`);
    } catch (error) {
      console.error('Failed to handle answer:', error);
      this.notifyError('answer', 'Failed to process connection answer');
    }
  }
  
  /**
   * Handle ICE candidate
   * @param {Object} message - ICE candidate message
   */
  async handleIceCandidate(message) {
    try {
      const { candidate, senderId } = message;
      
      // Check for peer connection
      if (!this.peerConnections[senderId]) {
        console.warn(`No peer connection found for ${senderId}`);
        return;
      }
      
      const peerConnection = this.peerConnections[senderId];
      
      // Add ICE candidate
      await peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
      
      console.log(`ICE candidate added for peer ${senderId}`);
    } catch (error) {
      console.error('Failed to handle ICE candidate:', error);
      this.notifyError('iceCandidate', 'Failed to process network information');
    }
  }
  
  /**
   * Start audio streaming
   * @param {MediaStream} stream - Audio stream to send
   * @returns {Promise<boolean>} Success status
   */
  async startStreaming(stream) {
    try {
      if (!this.initialized) {
        throw new Error('SecureAudioChannel not initialized');
      }
      
      this.localStream = stream;
      
      // Create audio processor node
      this.createAudioProcessor();
      
      // Add stream to all existing peer connections
      Object.keys(this.peerConnections).forEach(peerId => {
        const peerConnection = this.peerConnections[peerId];
        stream.getTracks().forEach(track => {
          peerConnection.addTrack(track, stream);
        });
      });
      
      console.log('Audio streaming started');
      return true;
    } catch (error) {
      console.error('Failed to start streaming:', error);
      this.notifyError('streaming', 'Failed to start audio streaming');
      return false;
    }
  }
  
  /**
   * Create audio processor node
   */
  createAudioProcessor() {
    try {
      // Get audio source from stream
      const source = this.audioContext.createMediaStreamSource(this.localStream);
      
      // Create script processor node
      this.audioProcessingNode = this.audioContext.createScriptProcessor(
        this.bufferSize, 
        1, // Input channels (mono)
        1  // Output channels (mono)
      );
      
      // Set up processing function
      this.audioProcessingNode.onaudioprocess = this.processAudio.bind(this);
      
      // Connect nodes
      source.connect(this.audioProcessingNode);
      this.audioProcessingNode.connect(this.audioContext.destination);
      
      console.log('Audio processor created');
    } catch (error) {
      console.error('Failed to create audio processor:', error);
      this.notifyError('audioProcessor', 'Failed to set up audio processing');
    }
  }
  
  /**
   * Process audio data
   * @param {AudioProcessingEvent} event - Audio processing event
   */
  processAudio(event) {
    if (!this.encryptionEnabled || Object.keys(this.peerConnections).length === 0) {
      return;
    }
    
    try {
      // Get input data
      const inputData = event.inputBuffer.getChannelData(0);
      
      // Create data view for processing
      const inputArray = new Float32Array(inputData);
      
      // Encrypt audio data for each peer
      Object.keys(this.dataChannels).forEach(peerId => {
        const dataChannel = this.dataChannels[peerId];
        
        if (dataChannel.readyState === 'open') {
          // Get encryption key for peer
          const encryptionKey = this.encryptionKeys[peerId];
          
          if (!encryptionKey) {
            return;
          }
          
          // Encrypt data
          const encryptedData = this.encryptAudioData(inputArray, encryptionKey);
          
          // Send encrypted data
          dataChannel.send(encryptedData);
        }
      });
    } catch (error) {
      console.error('Failed to process audio:', error);
    }
  }
  
  /**
   * Encrypt audio data
   * @param {Float32Array} audioData - Audio data to encrypt
   * @param {string} encryptionKey - Encryption key
   * @returns {string} Encrypted data
   */
  encryptAudioData(audioData, encryptionKey) {
    // Convert Float32Array to string (base64)
    const binaryString = String.fromCharCode.apply(null, new Uint8Array(audioData.buffer));
    const base64Data = btoa(binaryString);
    
    // Encrypt using AES
    const encrypted = CryptoJS.AES.encrypt(base64Data, encryptionKey).toString();
    
    return encrypted;
  }
  
  /**
   * Decrypt audio data
   * @param {string} encryptedData - Encrypted audio data
   * @param {string} encryptionKey - Encryption key
   * @returns {Float32Array} Decrypted audio data
   */
  decryptAudioData(encryptedData, encryptionKey) {
    // Decrypt using AES
    const decrypted = CryptoJS.AES.decrypt(encryptedData, encryptionKey).toString(CryptoJS.enc.Utf8);
    
    // Convert base64 to Float32Array
    const binaryString = atob(decrypted);
    const bytes = new Uint8Array(binaryString.length);
    
    for (let i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }
    
    return new Float32Array(bytes.buffer);
  }
  
  /**
   * Generate encryption keys
   * @returns {Promise<void>}
   */
  async generateEncryptionKeys() {
    try {
      // Use Web Crypto API to generate strong keys
      const key = await window.crypto.subtle.generateKey(
        {
          name: 'AES-GCM',
          length: 256
        },
        true, // Extractable
        ['encrypt', 'decrypt'] // Key usages
      );
      
      // Export key to raw format
      const keyBuffer = await window.crypto.subtle.exportKey('raw', key);
      
      // Convert to base64 string
      const keyBase64 = btoa(String.fromCharCode.apply(null, new Uint8Array(keyBuffer)));
      
      // Store master key
      this.masterKey = keyBase64;
      
      console.log('Encryption keys generated');
    } catch (error) {
      console.error('Failed to generate encryption keys:', error);
      this.notifyError('encryption', 'Failed to set up secure communication');
      
      // Fallback to less secure method if Web Crypto API is not available
      const randomBytes = new Uint8Array(32); // 256 bits
      window.crypto.getRandomValues(randomBytes);
      this.masterKey = btoa(String.fromCharCode.apply(null, randomBytes));
    }
  }
  
  /**
   * Exchange encryption keys with peer
   * @param {string} peerId - ID of peer
   */
  exchangeEncryptionKeys(peerId) {
    try {
      if (!this.encryptionEnabled || !this.masterKey) {
        return;
      }
      
      // Generate per-peer key using master key and peer ID
      const peerKey = CryptoJS.PBKDF2(
        this.masterKey,
        peerId,
        { keySize: 256 / 32, iterations: 1000 }
      ).toString();
      
      // Store key for this peer
      this.encryptionKeys[peerId] = peerKey;
      
      // Send key through signaling
      this.sendSignalingMessage({
        type: 'key-exchange',
        targetId: peerId,
        senderId: this.userId,
        keyId: Date.now().toString(),
        // Only send a key verification hash, not the actual key
        keyCheck: CryptoJS.SHA256(peerKey).toString().substr(0, 8)
      });
      
      console.log(`Encryption key exchange initiated with peer ${peerId}`);
    } catch (error) {
      console.error(`Failed to exchange encryption keys with ${peerId}:`, error);
      this.notifyError('keyExchange', 'Failed to establish secure connection');
    }
  }
  
  /**
   * Handle key exchange message
   * @param {Object} message - Key exchange message
   */
  handleKeyExchange(message) {
    try {
      const { senderId, keyId, keyCheck } = message;
      
      if (!this.masterKey) {
        return;
      }
      
      // Generate peer key using the same algorithm
      const peerKey = CryptoJS.PBKDF2(
        this.masterKey,
        senderId,
        { keySize: 256 / 32, iterations: 1000 }
      ).toString();
      
      // Verify key check
      const localKeyCheck = CryptoJS.SHA256(peerKey).toString().substr(0, 8);
      
      if (keyCheck !== localKeyCheck) {
        console.error(`Key verification failed for peer ${senderId}`);
        this.notifyError('keyVerification', 'Security verification failed');
        return;
      }
      
      // Store key for this peer
      this.encryptionKeys[senderId] = peerKey;
      
      // Acknowledge key exchange
      this.sendDataChannelMessage(senderId, {
        type: 'encryption-key',
        keyId,
        status: 'confirmed'
      });
      
      console.log(`Encryption key exchange completed with peer ${senderId}`);
    } catch (error) {
      console.error('Failed to handle key exchange:', error);
      this.notifyError('keyExchange', 'Failed to process security information');
    }
  }
  
  /**
   * Handle encryption key message
   * @param {string} peerId - ID of peer
   * @param {Object} message - Encryption key message
   */
  handleEncryptionKey(peerId, message) {
    console.log(`Encryption key confirmed by peer ${peerId}`);
  }
  
  /**
   * Start key rotation timer
   */
  startKeyRotation() {
    if (this.keyRotationTimer) {
      clearInterval(this.keyRotationTimer);
    }
    
    this.keyRotationTimer = setInterval(() => {
      this.rotateEncryptionKeys();
    }, this.keyRotationInterval);
  }
  
  /**
   * Rotate encryption keys
   */
  async rotateEncryptionKeys() {
    try {
      console.log('Rotating encryption keys');
      
      // Generate new master key
      await this.generateEncryptionKeys();
      
      // Exchange new keys with all peers
      this.peers.forEach(peerId => {
        this.exchangeEncryptionKeys(peerId);
      });
    } catch (error) {
      console.error('Failed to rotate encryption keys:', error);
    }
  }
  
  /**
   * Measure and exchange latency with peers
   */
  measureLatency() {
    this.peers.forEach(peerId => {
      this.sendLatencyPing(peerId);
    });
  }
  
  /**
   * Send latency ping to peer
   * @param {string} peerId - ID of peer
   */
  sendLatencyPing(peerId) {
    this.sendDataChannelMessage(peerId, {
      type: 'latency-ping',
      timestamp: Date.now()
    });
  }
  
  /**
   * Handle latency ping from peer
   * @param {string} peerId - ID of peer
   * @param {Object} message - Latency ping message
   */
  handleLatencyPing(peerId, message) {
    // Reply with pong
    this.sendDataChannelMessage(peerId, {
      type: 'latency-pong',
      originalTimestamp: message.timestamp,
      responseTimestamp: Date.now()
    });
  }
  
  /**
   * Handle latency pong from peer
   * @param {string} peerId - ID of peer
   * @param {Object} message - Latency pong message
   */
  handleLatencyPong(peerId, message) {
    const now = Date.now();
    const roundTripTime = now - message.originalTimestamp;
    const oneWayLatency = roundTripTime / 2;
    
    // Store latency for this peer
    this.latencyCompensation[peerId] = {
      latency: oneWayLatency,
      roundTripTime,
      timestamp: now
    };
    
    console.log(`Latency to peer ${peerId}: ${oneWayLatency.toFixed(2)}ms (RTT: ${roundTripTime.toFixed(2)}ms)`);
    
    // Share latency data with all peers
    this.broadcastLatencyData();
  }
  
  /**
   * Broadcast latency data to all peers
   */
  broadcastLatencyData() {
    // Send through signaling server for reliability
    this.sendSignalingMessage({
      type: 'latency-data',
      senderId: this.userId,
      latencyData: this.latencyCompensation
    });
  }
  
  /**
   * Handle latency data from peer
   * @param {Object} message - Latency data message
   */
  handleLatencyData(message) {
    const { senderId, latencyData } = message;
    
    // Integrate peer's latency data
    Object.keys(latencyData).forEach(peerId => {
      // Only add if we don't have data for this peer yet
      if (!this.latencyCompensation[peerId] && peerId !== this.userId) {
        this.latencyCompensation[peerId] = latencyData[peerId];
      }
    });
  }
  
  /**
   * Handle audio control message
   * @param {string} peerId - ID of peer
   * @param {Object} message - Audio control message
   */
  handleAudioControl(peerId, message) {
    // Handle audio control messages (e.g., volume, mute)
    console.log(`Audio control from peer ${peerId}:`, message);
  }
  
  /**
   * Send message through data channel
   * @param {string} peerId - ID of peer
   * @param {Object} message - Message to send
   */
  sendDataChannelMessage(peerId, message) {
    try {
      const dataChannel = this.dataChannels[peerId];
      
      if (dataChannel && dataChannel.readyState === 'open') {
        dataChannel.send(JSON.stringify(message));
      }
    } catch (error) {
      console.error(`Failed to send data channel message to ${peerId}:`, error);
    }
  }
  
  /**
   * Close peer connection
   * @param {string} peerId - ID of peer
   */
  closePeerConnection(peerId) {
    // Close data channel
    if (this.dataChannels[peerId]) {
      this.dataChannels[peerId].close();
      delete this.dataChannels[peerId];
    }
    
    // Close peer connection
    if (this.peerConnections[peerId]) {
      this.peerConnections[peerId].close();
      delete this.peerConnections[peerId];
    }
    
    // Remove encryption key
    if (this.encryptionKeys[peerId]) {
      delete this.encryptionKeys[peerId];
    }
    
    // Remove latency data
    if (this.latencyCompensation[peerId]) {
      delete this.latencyCompensation[peerId];
    }
    
    console.log(`Peer connection with ${peerId} closed`);
  }
  
  /**
   * Get latency compensation data
   * @returns {Object} Latency compensation data
   */
  getLatencyCompensation() {
    return this.latencyCompensation;
  }
  
  /**
   * Get latency to specific peer
   * @param {string} peerId - ID of peer
   * @returns {number|null} Latency in milliseconds
   */
  getLatencyToPeer(peerId) {
    if (this.latencyCompensation[peerId]) {
      return this.latencyCompensation[peerId].latency;
    }
    
    return null;
  }
  
  /**
   * Register connection state callback
   * @param {Function} callback - Callback function
   */
  onConnectionState(callback) {
    if (typeof callback === 'function') {
      this.connectionStateCallbacks.push(callback);
    }
  }
  
  /**
   * Register error callback
   * @param {Function} callback - Callback function
   */
  onError(callback) {
    if (typeof callback === 'function') {
      this.errorCallbacks.push(callback);
    }
  }
  
  /**
   * Notify connection state change
   * @param {string} peerId - ID of peer
   * @param {string} state - Connection state
   */
  notifyConnectionState(peerId, state) {
    this.connectionStateCallbacks.forEach(callback => {
      try {
        callback(peerId, state);
      } catch (error) {
        console.error('Error in connection state callback:', error);
      }
    });
  }
  
  /**
   * Notify error
   * @param {string} type - Error type
   * @param {string} message - Error message
   */
  notifyError(type, message) {
    this.errorCallbacks.forEach(callback => {
      try {
        callback(type, message);
      } catch (error) {
        console.error('Error in error callback:', error);
      }
    });
  }
  
  /**
   * Disconnect from all peers and close channel
   */
  disconnect() {
    // Clear key rotation timer
    if (this.keyRotationTimer) {
      clearInterval(this.keyRotationTimer);
      this.keyRotationTimer = null;
    }
    
    // Close all peer connections
    this.peers.forEach(peerId => {
      this.closePeerConnection(peerId);
    });
    
    // Close signaling connection
    if (this.signaling) {
      this.signaling.close();
      this.signaling = null;
    }
    
    // Stop audio processor
    if (this.audioProcessingNode) {
      this.audioProcessingNode.disconnect();
      this.audioProcessingNode = null;
    }
    
    // Stop local stream
    if (this.localStream) {
      this.localStream.getTracks().forEach(track => track.stop());
      this.localStream = null;
    }
    
    this.initialized = false;
    console.log('Secure Audio Channel disconnected');
  }
}

export default SecureAudioChannel;