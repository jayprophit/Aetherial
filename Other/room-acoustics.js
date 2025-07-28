// src/services/RoomAcousticsAnalyzer.js

/**
 * Room Acoustics Analyzer
 * 
 * Uses microphone input to analyze room acoustics and generate 
 * optimal speaker placement and EQ settings.
 */
class RoomAcousticsAnalyzer {
  constructor() {
    this.initialized = false;
    this.audioContext = null;
    this.analyzer = null;
    this.microphone = null;
    this.isAnalyzing = false;
    this.frequencyData = null;
    this.impulseResponseData = null;
    this.roomDimensions = null;
    this.speakerPositions = [];
    this.listeningPositions = [];
    this.roomMaterials = {};
    this.rtCalculator = null;
    this.modesCalculator = null;
    this.eqSuggestion = null;
    this.reverbTime = null;
    this.bassRatio = null;
    this.clarityIndex = null;
    this.roomModes = [];
    this.suggestionEngine = null;
    this.testToneGenerator = null;
    this.recordedResponses = [];
    this.calculationInProgress = false;
    this.analysisResults = null;
    this.sweepDuration = 5000; // ms
    this.analysisCallbacks = {
      onProgress: null,
      onComplete: null,
      onError: null
    };
  }
  
  /**
   * Initialize the acoustics analyzer
   * @param {Object} options - Initialization options
   * @returns {Promise<boolean>} - Success status
   */
  async initialize(options = {}) {
    try {
      const {
        roomDimensions = null,
        speakerPositions = [],
        listeningPositions = [],
        roomMaterials = {},
        onProgress = null,
        onComplete = null,
        onError = null
      } = options;
      
      // Set up callbacks
      this.analysisCallbacks.onProgress = onProgress;
      this.analysisCallbacks.onComplete = onComplete;
      this.analysisCallbacks.onError = onError;
      
      // Initialize audio context
      window.AudioContext = window.AudioContext || window.webkitAudioContext;
      this.audioContext = new AudioContext();
      
      // Initialize analyzers
      this.analyzer = this.audioContext.createAnalyser();
      this.analyzer.fftSize = 16384; // For high resolution analysis
      this.analyzer.smoothingTimeConstant = 0.2;
      
      // Set room properties
      this.roomDimensions = roomDimensions;
      this.speakerPositions = speakerPositions;
      this.listeningPositions = listeningPositions;
      this.roomMaterials = roomMaterials;
      
      // Initialize calculation modules
      this.rtCalculator = new ReverbTimeCalculator();
      this.modesCalculator = new RoomModesCalculator();
      this.suggestionEngine = new AcousticSuggestionEngine();
      this.testToneGenerator = new TestToneGenerator(this.audioContext);
      
      // Initialize data arrays
      this.frequencyData = new Float32Array(this.analyzer.frequencyBinCount);
      this.impulseResponseData = new Float32Array(this.analyzer.fftSize);
      
      this.initialized = true;
      return true;
    } catch (error) {
      console.error('Failed to initialize Room Acoustics Analyzer:', error);
      this.notifyError('Initialization error: ' + error.message);
      return false;
    }
  }
  
  /**
   * Start room acoustics analysis
   * @returns {Promise<boolean>} - Success status
   */
  async startAnalysis() {
    if (!this.initialized) {
      this.notifyError('Analyzer not initialized');
      return false;
    }
    
    if (this.isAnalyzing) {
      this.notifyError('Analysis already in progress');
      return false;
    }
    
    try {
      this.isAnalyzing = true;
      this.analysisResults = null;
      this.calculationInProgress = false;
      this.recordedResponses = [];
      
      // Request microphone access
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.microphone = this.audioContext.createMediaStreamSource(stream);
      
      // Connect microphone to analyzer
      this.microphone.connect(this.analyzer);
      
      // Progress update
      this.notifyProgress(0, 'Microphone connected');
      
      // Run the analysis process
      const success = await this.runAnalysisProcess();
      
      // Disconnect microphone when done
      this.microphone.disconnect();
      this.microphone = null;
      
      // Stop all tracks
      stream.getTracks().forEach(track => track.stop());
      
      this.isAnalyzing = false;
      return success;
    } catch (error) {
      this.isAnalyzing = false;
      this.notifyError('Analysis error: ' + error.message);
      return false;
    }
  }
  
  /**
   * Run the analysis process
   * @returns {Promise<boolean>} - Success status
   */
  async runAnalysisProcess() {
    try {
      // 1. Run room sweep test with sine wave sweep
      this.notifyProgress(10, 'Beginning frequency sweep test');
      await this.runFrequencySweepTest();
      
      // 2. Record impulse response
      this.notifyProgress(30, 'Recording impulse response');
      await this.recordImpulseResponse();
      
      // 3. Calculate reverb time (RT60)
      this.notifyProgress(50, 'Calculating reverberation time');
      this.reverbTime = await this.rtCalculator.calculateRT60(this.impulseResponseData, this.audioContext.sampleRate);
      
      // 4. Calculate room modes
      this.notifyProgress(60, 'Calculating room modes');
      if (this.roomDimensions) {
        this.roomModes = this.modesCalculator.calculateRoomModes(this.roomDimensions);
      }
      
      // 5. Analyze frequency response
      this.notifyProgress(70, 'Analyzing frequency response');
      const frequencyAnalysis = this.analyzeFrequencyResponse();
      
      // 6. Calculate acoustic metrics
      this.notifyProgress(80, 'Calculating acoustic metrics');
      this.clarityIndex = this.calculateClarityIndex();
      this.bassRatio = this.calculateBassRatio();
      
      // 7. Generate recommendations
      this.notifyProgress(90, 'Generating recommendations');
      const recommendations = this.generateRecommendations();
      
      // 8. Compile results
      this.analysisResults = {
        timestamp: new Date(),
        reverbTime: this.reverbTime,
        roomModes: this.roomModes,
        clarityIndex: this.clarityIndex,
        bassRatio: this.bassRatio,
        frequencyResponse: frequencyAnalysis.frequencyResponse,
        problemFrequencies: frequencyAnalysis.problemFrequencies,
        recommendations: recommendations,
        eqSuggestions: this.generateEQSuggestions(frequencyAnalysis),
        speakerPlacement: this.generateSpeakerPlacement(),
        roomQualityScore: this.calculateRoomQualityScore()
      };
      
      // 9. Complete analysis
      this.notifyProgress(100, 'Analysis complete');
      this.notifyComplete(this.analysisResults);
      
      return true;
    } catch (error) {
      console.error('Error in analysis process:', error);
      this.notifyError('Analysis process error: ' + error.message);
      return false;
    }
  }
  
  /**
   * Run frequency sweep test
   * @returns {Promise<void>}
   */
  async runFrequencySweepTest() {
    return new Promise(async (resolve, reject) => {
      try {
        // Create a pink noise test for better room excitation
        const noiseNode = await this.testToneGenerator.createPinkNoise(2); // 2 seconds of pink noise
        
        // Record the response
        const startTime = this.audioContext.currentTime;
        const responseBuffer = await this.recordAudioForDuration(2.5); // Record for 2.5 seconds (noise + decay)
        
        // Store the recorded response
        this.recordedResponses.push({
          type: 'noise',
          buffer: responseBuffer,
          startTime,
          endTime: startTime + 2.5
        });
        
        // Now run a sine sweep for frequency response
        this.notifyProgress(15, 'Running sine sweep');
        
        // Create swept sine wave (20Hz to 20kHz logarithmic sweep)
        const sweepNode = await this.testToneGenerator.createLogSweep(20, 20000, this.sweepDuration / 1000);
        
        // Record the sweep response
        const sweepStartTime = this.audioContext.currentTime;
        const sweepResponseBuffer = await this.recordAudioForDuration(this.sweepDuration / 1000 + 2); // Sweep + 2s decay
        
        // Store the recorded sweep response
        this.recordedResponses.push({
          type: 'sweep',
          buffer: sweepResponseBuffer,
          startTime: sweepStartTime,
          endTime: sweepStartTime + (this.sweepDuration / 1000) + 2
        });
        
        resolve();
      } catch (error) {
        reject(error);
      }
    });
  }
  
  /**
   * Record audio for a specific duration
   * @param {number} durationSeconds - Recording duration in seconds
   * @returns {Promise<Float32Array>} - Recorded audio buffer
   */
  async recordAudioForDuration(durationSeconds) {
    return new Promise((resolve, reject) => {
      try {
        const sampleRate = this.audioContext.sampleRate;
        const bufferSize = durationSeconds * sampleRate;
        const recordingBuffer = new Float32Array(bufferSize);
        let recordedSamples = 0;
        
        // Create a script processor for recording
        const recorderNode = this.audioContext.createScriptProcessor(4096, 1, 1);
        
        // Connect analyzer to recorder
        this.analyzer.connect(recorderNode);
        recorderNode.connect(this.audioContext.destination);
        
        // Process audio data
        recorderNode.onaudioprocess = (e) => {
          const input = e.inputBuffer.getChannelData(0);
          const remaining = bufferSize - recordedSamples;
          
          if (remaining > 0) {
            // Calculate how many samples to copy
            const toCopy = Math.min(input.length, remaining);
            
            // Copy samples to recording buffer
            for (let i = 0; i < toCopy; i++) {
              recordingBuffer[recordedSamples + i] = input[i];
            }
            
            recordedSamples += toCopy;
            
            // Update progress for sweep
            const progress = (recordedSamples / bufferSize) * 100;
            if (progress % 10 < 1) { // Update roughly every 10%
              this.notifyProgress(15 + (progress * 0.15), `Recording audio: ${Math.round(progress)}%`);
            }
          }
          
          // If we've recorded enough samples, resolve the promise
          if (recordedSamples >= bufferSize) {
            // Disconnect nodes
            recorderNode.disconnect();
            this.analyzer.disconnect(recorderNode);
            
            // Resolve with the recording buffer
            resolve(recordingBuffer);
          }
        };
      } catch (error) {
        reject(error);
      }
    });
  }
  
  /**
   * Record impulse response
   * @returns {Promise<void>}
   */
  async recordImpulseResponse() {
    // In a real implementation, we would use the recorded sweep response
    // and deconvolve it with the original sweep to get the impulse response
    
    // For this demonstration, we'll create a synthetic impulse response
    return new Promise((resolve) => {
      const sampleRate = this.audioContext.sampleRate;
      const numSamples = sampleRate * 2; // 2 seconds
      
      // Create a synthetic impulse response
      // In reality, this would be calculated from the sweep response
      for (let i = 0; i < numSamples; i++) {
        // Direct sound impulse
        if (i === 0) {
          this.impulseResponseData[i] = 1.0;
        } 
        // Early reflections (within ~50ms)
        else if (i < sampleRate * 0.05) {
          this.impulseResponseData[i] = Math.random() * 0.2 * Math.exp(-i / (sampleRate * 0.02));
        } 
        // Reverb tail
        else {
          this.impulseResponseData[i] = Math.random() * 0.05 * Math.exp(-i / (sampleRate * 0.5));
        }
      }
      
      // Simulate some calculation time
      setTimeout(() => {
        resolve();
      }, 500);
    });
  }
  
  /**
   * Analyze frequency response
   * @returns {Object} - Frequency analysis results
   */
  analyzeFrequencyResponse() {
    // In a real implementation, this would analyze the recorded frequency response
    // from the sweep test to identify peaks, dips, and overall response curve
    
    // Create frequency analysis data
    const frequencyResponse = [];
    const problemFrequencies = [];
    
    // Frequency bands for analysis
    const frequencyBands = [
      20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 
      630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 
      8000, 10000, 12500, 16000, 20000
    ];
    
    // Create a synthetic frequency response with some realistic room characteristics
    for (let i = 0; i < frequencyBands.length; i++) {
      const frequency = frequencyBands[i];
      
      // Base response (slight roll-off at higher frequencies)
      let response = 0;
      
      if (frequency < 100) {
        // Typical room boost at low frequencies (standing waves)
        response = 3 + (Math.sin(frequency / 20) * 4);
      } else if (frequency < 300) {
        // Often a muddy region
        response = 2 + (Math.sin(frequency / 50) * 3);
      } else if (frequency < 1000) {
        // Midrange
        response = Math.sin(frequency / 200) * 2;
      } else if (frequency < 5000) {
        // Upper midrange to presence
        response = (Math.sin(frequency / 500) * 1.5) - 1;
      } else {
        // High frequencies (usually absorption causes roll-off)
        response = -2 - (frequency / 10000) * 3;
      }
      
      // Add some random variation
      response += (Math.random() * 2 - 1);
      
      // Add room modes effects if we have room dimensions
      if (this.roomModes && this.roomModes.length > 0) {
        for (const mode of this.roomModes) {
          // Add resonance at room modes
          if (Math.abs(frequency - mode.frequency) < mode.frequency * 0.05) {
            const proximity = 1 - (Math.abs(frequency - mode.frequency) / (mode.frequency * 0.05));
            response += proximity * 5; // Boost at room mode frequencies
          }
        }
      }
      
      // Round to 1 decimal place
      response = Math.round(response * 10) / 10;
      
      // Add to frequency response
      frequencyResponse.push({
        frequency,
        response
      });
      
      // Check for potential problem areas
      if (response > 3.5 || response < -3.5) {
        problemFrequencies.push({
          frequency,
          response,
          issue: response > 3.5 ? 'peak' : 'dip',
          severity: Math.abs(response) > 5 ? 'high' : 'medium'
        });
      }
    }
    
    return {
      frequencyResponse,
      problemFrequencies
    };
  }
  
  /**
   * Calculate clarity index (C50)
   * @returns {number} - Clarity index in dB
   */
  calculateClarityIndex() {
    // In a real implementation, this would be calculated from the impulse response
    // C50 is the ratio of energy in first 50ms to energy after 50ms (speech clarity)
    
    // Simplified calculation
    const sampleRate = this.audioContext.sampleRate;
    const boundary = Math.floor(sampleRate * 0.05); // 50ms
    
    let earlyEnergy = 0;
    let lateEnergy = 0;
    
    // Calculate energy in early and late parts of impulse response
    for (let i = 0; i < this.impulseResponseData.length; i++) {
      const sample = this.impulseResponseData[i];
      const energy = sample * sample;
      
      if (i < boundary) {
        earlyEnergy += energy;
      } else {
        lateEnergy += energy;
      }
    }
    
    // Avoid division by zero
    if (lateEnergy === 0) lateEnergy = 1e-10;
    
    // Calculate C50 in dB
    const c50 = 10 * Math.log10(earlyEnergy / lateEnergy);
    
    // Round to 1 decimal place
    return Math.round(c50 * 10) / 10;
  }
  
  /**
   * Calculate bass ratio
   * @returns {number} - Bass ratio
   */
  calculateBassRatio() {
    // Bass Ratio = RT60 average at 125Hz and 250Hz divided by RT60 average at 500Hz and 1000Hz
    
    // In a real implementation, this would be calculated from band-specific RT60 values
    // For this example, we'll just return a typical value for untreated rooms
    
    // Typical values:
    // < 0.9: Lack of bass response
    // 0.9-1.1: Neutral bass response (ideal for most music)
    // > 1.1: Elevated bass response (warm, but can be boomy)
    
    return 1.3; // Slightly elevated bass, typical for untreated rooms
  }
  
  /**
   * Generate recommendations for room treatment
   * @returns {Array} - Room treatment recommendations
   */
  generateRecommendations() {
    const recommendations = [];
    
    // Check reverberation time
    if (this.reverbTime > 0.8) {
      recommendations.push({
        type: 'acoustic',
        issue: 'High reverberation time',
        solution: 'Add acoustic absorption panels to walls and ceiling',
        priority: this.reverbTime > 1.2 ? 'high' : 'medium',
        details: `Your room's reverberation time (RT60) of ${this.reverbTime.toFixed(2)}s is ${
          this.reverbTime > 1.2 ? 'significantly' : 'slightly'
        } higher than ideal for critical listening. Consider adding acoustic treatment to reduce reflections.`
      });
    }
    
    // Check bass ratio
    if (this.bassRatio > 1.1) {
      recommendations.push({
        type: 'acoustic',
        issue: 'Elevated bass response',
        solution: 'Add bass traps in room corners',
        priority: this.bassRatio > 1.3 ? 'high' : 'medium',
        details: `Your room has an elevated bass response (Bass Ratio: ${this.bassRatio.toFixed(2)}), which can cause muddy sound and decreased clarity. Bass traps in room corners will help control low frequency resonances.`
      });
    } else if (this.bassRatio < 0.9) {
      recommendations.push({
        type: 'acoustic',
        issue: 'Lacking bass response',
        solution: 'Consider adding a subwoofer or adjusting speaker placement',
        priority: 'medium',
        details: `Your room has a weak bass response (Bass Ratio: ${this.bassRatio.toFixed(2)}). This could be due to excessive bass absorption or speaker placement issues.`
      });
    }
    
    // Check clarity index
    if (this.clarityIndex < 0) {
      recommendations.push({
        type: 'acoustic',
        issue: 'Poor speech clarity',
        solution: 'Add diffusion panels to side walls',
        priority: this.clarityIndex < -5 ? 'high' : 'medium',
        details: `Your room's clarity index (C50) of ${this.clarityIndex.toFixed(1)}dB indicates poor speech intelligibility. Adding diffusion panels can help create a more balanced sound field.`
      });
    }
    
    // Add speaker placement recommendations
    if (this.speakerPositions.length > 0) {
      const optimalPositions = this.generateSpeakerPlacement();
      
      recommendations.push({
        type: 'placement',
        issue: 'Sub-optimal speaker placement',
        solution: 'Adjust speaker positions as recommended',
        priority: 'medium',
        details: 'Optimizing speaker placement can significantly improve sound quality without requiring additional treatments.',
        positions: optimalPositions
      });
    }
    
    // If we have problem frequencies, add specific EQ recommendations
    if (this.analyzeFrequencyResponse().problemFrequencies.length > 0) {
      recommendations.push({
        type: 'equalization',
        issue: 'Frequency response issues',
        solution: 'Apply recommended EQ settings',
        priority: 'medium',
        details: 'There are several peaks and dips in your room\'s frequency response that can be improved with equalization.',
        eqSettings: this.generateEQSuggestions(this.analyzeFrequencyResponse())
      });
    }
    
    // Sort recommendations by priority
    recommendations.sort((a, b) => {
      const priorityOrder = { high: 0, medium: 1, low: 2 };
      return priorityOrder[a.priority] - priorityOrder[b.priority];
    });
    
    return recommendations;
  }
  
  /**
   * Generate EQ suggestions based on frequency analysis
   * @param {Object} frequencyAnalysis - Frequency analysis results
   * @returns {Object} - EQ suggestions
   */
  generateEQSuggestions(frequencyAnalysis) {
    const eqBands = [];
    
    // Standard EQ centers for parametric EQ
    const standardBands = [
      32, 64, 125, 250, 500, 1000, 2000, 4000, 8000, 16000
    ];
    
    // Process each standard band
    standardBands.forEach(centerFreq => {
      // Find closest frequency in the analysis
      const closestFreqs = frequencyAnalysis.frequencyResponse.filter(f => 
        f.frequency >= centerFreq * 0.8 && f.frequency <= centerFreq * 1.25
      );
      
      if (closestFreqs.length === 0) return;
      
      // Find average response in this band
      const avgResponse = closestFreqs.reduce((sum, f) => sum + f.response, 0) / closestFreqs.length;
      
      // Find peaks or dips that need correction
      const needsCorrection = Math.abs(avgResponse) > 2;
      
      if (needsCorrection) {
        // Calculate correction (invert the response, but attenuate the correction)
        const correction = -avgResponse * 0.7;
        
        // Calculate appropriate Q based on frequency
        let q = 1.4; // Default Q
        
        // Use narrower Q for higher frequencies, wider for lower
        if (centerFreq < 100) {
          q = 1.0; // Wider for bass
        } else if (centerFreq > 4000) {
          q = 1.8; // Narrower for treble
        }
        
        // Add EQ band
        eqBands.push({
          frequency: centerFreq,
          gain: Math.round(correction * 10) / 10, // Round to 1 decimal place
          q: q,
          type: 'peaking'
        });
      }
    });
    
    // Add a high-pass filter if needed
    if (this.bassRatio > 1.3) {
      eqBands.push({
        frequency: 30,
        gain: 0,
        q: 0.7,
        type: 'highpass'
      });
    }
    
    return {
      bands: eqBands,
      notes: `These EQ settings are designed to compensate for your room's frequency response. They should be applied to the master output or to each speaker individually.`
    };
  }
  
  /**
   * Generate optimal speaker placement
   * @returns {Object} - Optimal speaker placement
   */
  generateSpeakerPlacement() {
    // If we already have speaker positions and room dimensions, calculate improvements
    if (this.roomDimensions && this.speakerPositions.length > 0) {
      // Clone speaker positions for modification
      const optimizedPositions = JSON.parse(JSON.stringify(this.speakerPositions));
      
      // Apply the Rule of Thirds for better placement
      optimizedPositions.forEach(speaker => {
        // Calculate room modes and avoid placing speakers at mode resonance points
        const roomModes = this.roomModes || [];
        
        // Avoid placing speakers at modal resonance points
        const badXPositions = roomModes
          .filter(mode => mode.axis === 'x')
          .map(mode => mode.antinode_positions)
          .flat();
        
        const badYPositions = roomModes
          .filter(mode => mode.axis === 'y')
          .map(mode => mode.antinode_positions)
          .flat();
          
        // Adjust position if too close to a modal resonance
        if (badXPositions.some(pos => Math.abs(speaker.x - pos) < 0.3)) {
          // Move towards the next best position (often 1/3 room width)
          speaker.x = this.roomDimensions.width / 3;
        }
        
        if (badYPositions.some(pos => Math.abs(speaker.y - pos) < 0.3)) {
          // Move towards the next best position (often 1/5 room depth)
          speaker.y = this.roomDimensions.depth / 5;
        }
        
        // Ensure speakers are not too close to walls
        if (speaker.x < 0.5) speaker.x = 0.5;
        if (speaker.y < 0.5) speaker.y = 0.5;
        if (speaker.x > this.roomDimensions.width - 0.5) speaker.x = this.roomDimensions.width - 0.5;
        if (speaker.y > this.roomDimensions.depth - 0.5) speaker.y = this.roomDimensions.depth - 0.5;
      });
      
      // For stereo setups, ensure symmetrical placement
      if (optimizedPositions.length === 2) {
        // Create equilateral triangle with listening position
        if (this.listeningPositions.length > 0) {
          const listener = this.listeningPositions[0];
          
          // Calculate distance between speakers
          const speakerDistance = Math.sqrt(
            Math.pow(optimizedPositions[0].x - optimizedPositions[1].x, 2) + 
            Math.pow(optimizedPositions[0].y - optimizedPositions[1].y, 2)
          );
          
          // Adjust listener position to form equilateral triangle
          listener.x = (optimizedPositions[0].x + optimizedPositions[1].x) / 2;
          listener.y = optimizedPositions[0].y + Math.sqrt(
            Math.pow(speakerDistance, 2) - Math.pow(speakerDistance / 2, 2)
          );
        }
      }
      
      return {
        speakers: optimizedPositions,
        listeners: this.listeningPositions,
        notes: `The optimized speaker positions avoid room mode resonances and create a better stereo image. Move your speakers to these positions for improved sound quality.`
      };
    }
    
    // If we don't have dimensions, return general guidelines
    return {
      notes: `Without room dimensions, specific placement cannot be calculated. Generally, follow these guidelines:
        1. Place speakers at least 0.5m from walls
        2. Form an equilateral triangle between the speakers and listening position
        3. Avoid placing speakers in corners
        4. Try to keep speakers at ear height when seated
        5. For stereo, keep speakers symmetrical in the room`
    };
  }
  
  /**
   * Calculate overall room quality score
   * @returns {number} - Room quality score (0-100)
   */
  calculateRoomQualityScore() {
    let score = 50; // Start with neutral score
    
    // Adjust based on reverberation time
    // Ideal is around 0.3-0.5s for critical listening
    if (this.reverbTime) {
      if (this.reverbTime < 0.3) {
        score -= 10; // Too dead
      } else if (this.reverbTime > 0.8) {
        score -= 15; // Too reverberant
      } else if (this.reverbTime > 0.5 && this.reverbTime <= 0.8) {
        score -= 5; // Slightly reverberant
      } else {
        score += 15; // Ideal
      }
    }
    
    // Adjust based on bass ratio
    if (this.bassRatio) {
      if (this.bassRatio < 0.9) {
        score -= 10; // Lacking bass
      } else if (this.bassRatio > 1.3) {
        score -= 15; // Too boomy
      } else if (this.bassRatio > 1.1 && this.bassRatio <= 1.3) {
        score -= 5; // Slightly warm
      } else {
        score += 15; // Balanced
      }
    }
    
    // Adjust based on clarity index
    if (this.clarityIndex) {
      if (this.clarityIndex < -5) {
        score -= 15; // Very muddy
      } else if (this.clarityIndex < 0) {
        score -= 10; // Slightly muddy
      } else if (this.clarityIndex > 10) {
        score -= 5; // Too dry/clinical
      } else {
        score += 15; // Good clarity
      }
    }
    
    // Adjust based on problem frequencies
    const problemFrequencies = this.analyzeFrequencyResponse().problemFrequencies;
    if (problemFrequencies.length > 0) {
      const severeProblemCount = problemFrequencies.filter(p => p.severity === 'high').length;
      const moderateProblemCount = problemFrequencies.filter(p => p.severity === 'medium').length;
      
      score -= severeProblemCount * 5;
      score -= moderateProblemCount * 2;
    }
    
    // Ensure score is in 0-100 range
    return Math.max(0, Math.min(100, score));
  }
  
  /**
   * Get analysis results
   * @returns {Object|null} - Analysis results or null if not available
   */
  getAnalysisResults() {
    return this.analysisResults;
  }
  
  /**
   * Generate 3D visualization data
   * @returns {Object} - 3D visualization data
   */
  generate3DVisualizationData() {
    if (!this.roomDimensions) {
      return null;
    }
    
    // Create visualization data
    const visualizationData = {
      room: this.roomDimensions,
      speakers: this.speakerPositions,
      listeners: this.listeningPositions,
      roomModes: this.roomModes,
      reflectionPaths: this.generateReflectionPaths(),
      standingWaves: this.generateStandingWavesVisualization(),
      frequencyResponse: this.analyzeFrequencyResponse().frequencyResponse
    };
    
    return visualizationData;
  }
  
  /**
   * Generate reflection paths for visualization
   * @returns {Array} - Reflection paths
   */
  generateReflectionPaths() {
    // In a real implementation, this would calculate actual reflection paths
    // based on speaker and listener positions
    
    // For demonstration, return empty array
    return [];
  }
  
  /**
   * Generate standing waves visualization
   * @returns {Array} - Standing waves data
   */
  generateStandingWavesVisualization() {
    // In a real implementation, this would generate visualization data
    // for room modes and standing waves
    
    // For demonstration, return empty array
    return [];
  }
  
  /**
   * Notify progress update
   * @param {number} percent - Progress percentage
   * @param {string} message - Progress message
   */
  notifyProgress(percent, message) {
    if (typeof this.analysisCallbacks.onProgress === 'function') {
      this.analysisCallbacks.onProgress({
        percent,
        message
      });
    }
  }
  
  /**
   * Notify analysis complete
   * @param {Object} results - Analysis results
   */
  notifyComplete(results) {
    if (typeof this.analysisCallbacks.onComplete === 'function') {
      this.analysisCallbacks.onComplete(results);
    }
  }
  
  /**
   * Notify analysis error
   * @param {string} message - Error message
   */
  notifyError(message) {
    if (typeof this.analysisCallbacks.onError === 'function') {
      this.analysisCallbacks.onError(message);
    }
  }
  
  /**
   * Clean up resources
   */
  cleanup() {
    if (this.microphone) {
      this.microphone.disconnect();
      this.microphone = null;
    }
    
    if (this.analyzer) {
      this.analyzer.disconnect();
    }
    
    if (this.audioContext && this.audioContext.state !== 'closed') {
      this.audioContext.close();
    }
    
    this.initialized = false;
    this.isAnalyzing = false;
    
    console.log('Room Acoustics Analyzer resources cleaned up');
  }
}

/**
 * Reverb Time Calculator
 * Calculates RT60 (reverb time) from impulse response
 */
class ReverbTimeCalculator {
  /**
   * Calculate RT60 (time for reverb to decay by 60dB)
   * @param {Float32Array} impulseResponse - Impulse response data
   * @param {number} sampleRate - Audio sample rate
   * @returns {number} - RT60 in seconds
   */
  calculateRT60(impulseResponse, sampleRate) {
    // Convert impulse response to energy decay curve
    const edc = this.calculateEDC(impulseResponse);
    
    // Find -5dB and -35dB points (avoid early reflections and noise floor)
    const startIndex = this.findLevelIndex(edc, -5);
    const endIndex = this.findLevelIndex(edc, -35);
    
    if (!startIndex || !endIndex) {
      return 0.5; // Default value if calculation fails
    }
    
    // Calculate time between these points
    const timeDelta = (endIndex - startIndex) / sampleRate;
    
    // Scale to get RT60 (60dB decay)
    const rt60 = timeDelta * (60 / 30); // Scale from 30dB to 60dB
    
    return rt60;
  }
  
  /**
   * Calculate Energy Decay Curve
   * @param {Float32Array} impulseResponse - Impulse response data
   * @returns {Float32Array} - Energy decay curve in dB
   */
  calculateEDC(impulseResponse) {
    const length = impulseResponse.length;
    const edc = new Float32Array(length);
    
    // Calculate total energy
    let totalEnergy = 0;
    for (let i = 0; i < length; i++) {
      totalEnergy += impulseResponse[i] * impulseResponse[i];
    }
    
    // Calculate backwards integration
    let remainingEnergy = totalEnergy;
    for (let i = 0; i < length; i++) {
      remainingEnergy -= impulseResponse[i] * impulseResponse[i];
      
      // Convert to dB
      if (remainingEnergy <= 0) {
        edc[i] = -100; // Effectively negative infinity
      } else {
        edc[i] = 10 * Math.log10(remainingEnergy / totalEnergy);
      }
    }
    
    return edc;
  }
  
  /**
   * Find index where the EDC reaches a specific level
   * @param {Float32Array} edc - Energy decay curve
   * @param {number} levelDb - Level in dB to find
   * @returns {number|null} - Index or null if not found
   */
  findLevelIndex(edc, levelDb) {
    for (let i = 0; i < edc.length; i++) {
      if (edc[i] <= levelDb) {
        return i;
      }
    }
    
    return null;
  }
}

/**
 * Room Modes Calculator
 * Calculates room modes based on dimensions
 */
class RoomModesCalculator {
  /**
   * Calculate room modes
   * @param {Object} dimensions - Room dimensions in meters
   * @returns {Array} - Room modes
   */
  calculateRoomModes(dimensions) {
    const width = dimensions.width;
    const height = dimensions.height;
    const depth = dimensions.depth;
    
    const c = 343; // Speed of sound in m/s
    const modes = [];
    
    // Calculate modes up to 300Hz (most relevant for room acoustics)
    // Formula: f = (c/2) * sqrt((nx/Lx)^2 + (ny/Ly)^2 + (nz/Lz)^2)
    
    // Calculate axial modes (one-dimensional)
    for (let nx = 1; nx <= 4; nx++) {
      const freq = (nx * c) / (2 * width);
      if (freq <= 300) {
        const antinodes = [];
        for (let i = 0; i <= nx; i++) {
          antinodes.push((i * width) / nx);
        }
        
        modes.push({
          type: 'axial',
          axis: 'x',
          indices: [nx, 0, 0],
          frequency: Math.round(freq),
          antinode_positions: antinodes,
          wavelength: 2 * width / nx
        });
      }
    }
    
    for (let ny = 1; ny <= 4; ny++) {
      const freq = (ny * c) / (2 * depth);
      if (freq <= 300) {
        const antinodes = [];
        for (let i = 0; i <= ny; i++) {
          antinodes.push((i * depth) / ny);
        }
        
        modes.push({
          type: 'axial',
          axis: 'y',
          indices: [0, ny, 0],
          frequency: Math.round(freq),
          antinode_positions: antinodes,
          wavelength: 2 * depth / ny
        });
      }
    }
    
    for (let nz = 1; nz <= 4; nz++) {
      const freq = (nz * c) / (2 * height);
      if (freq <= 300) {
        const antinodes = [];
        for (let i = 0; i <= nz; i++) {
          antinodes.push((i * height) / nz);
        }
        
        modes.push({
          type: 'axial',
          axis: 'z',
          indices: [0, 0, nz],
          frequency: Math.round(freq),
          antinode_positions: antinodes,
          wavelength: 2 * height / nz
        });
      }
    }
    
    // Calculate tangential modes (selective ones)
    for (let nx = 1; nx <= 2; nx++) {
      for (let ny = 1; ny <= 2; ny++) {
        const freq = (c / 2) * Math.sqrt(Math.pow(nx / width, 2) + Math.pow(ny / depth, 2));
        if (freq <= 300) {
          modes.push({
            type: 'tangential',
            axis: 'xy',
            indices: [nx, ny, 0],
            frequency: Math.round(freq)
          });
        }
      }
    }
    
    // Sort by frequency
    modes.sort((a, b) => a.frequency - b.frequency);
    
    return modes;
  }
}

/**
 * Acoustic Suggestion Engine
 * Provides recommendations for room acoustic treatment
 */
class AcousticSuggestionEngine {
  constructor() {
    // This would contain a database of acoustic treatments, 
    // effectiveness, and decision logic in a real implementation
  }
}

/**
 * Test Tone Generator
 * Generates test tones for acoustic measurements
 */
class TestToneGenerator {
  /**
   * @param {AudioContext} audioContext - Web Audio API context
   */
  constructor(audioContext) {
    this.audioContext = audioContext;
  }
  
  /**
   * Create pink noise
   * @param {number} duration - Duration in seconds
   * @returns {Promise<AudioBufferSourceNode>} - Audio source node
   */
  async createPinkNoise(duration) {
    return new Promise((resolve) => {
      // Create buffer
      const bufferSize = this.audioContext.sampleRate * duration;
      const buffer = this.audioContext.createBuffer(1, bufferSize, this.audioContext.sampleRate);
      const data = buffer.getChannelData(0);
      
      // Generate pink noise using Voss algorithm
      let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0;
      
      for (let i = 0; i < bufferSize; i++) {
        // White noise
        const white = Math.random() * 2 - 1;
        
        // Pink noise components
        b0 = 0.99886 * b0 + white * 0.0555179;
        b1 = 0.99332 * b1 + white * 0.0750759;
        b2 = 0.96900 * b2 + white * 0.1538520;
        b3 = 0.86650 * b3 + white * 0.3104856;
        b4 = 0.55000 * b4 + white * 0.5329522;
        b5 = -0.7616 * b5 - white * 0.0168980;
        
        // Mix components
        data[i] = (b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362) * 0.11;
        
        // Clip to avoid distortion
        if (data[i] > 0.95) data[i] = 0.95;
        if (data[i] < -0.95) data[i] = -0.95;
      }
      
      // Create source node
      const source = this.audioContext.createBufferSource();
      source.buffer = buffer;
      
      // Connect to destination
      source.connect(this.audioContext.destination);
      
      // Start playback
      source.start();
      
      // Resolve promise
      resolve(source);
    });
  }
  
  /**
   * Create logarithmic sine sweep
   * @param {number} startFreq - Start frequency in Hz
   * @param {number} endFreq - End frequency in Hz
   * @param {number} duration - Duration in seconds
   * @returns {Promise<AudioBufferSourceNode>} - Audio source node
   */
  async createLogSweep(startFreq, endFreq, duration) {
    return new Promise((resolve) => {
      // Create buffer
      const bufferSize = this.audioContext.sampleRate * duration;
      const buffer = this.audioContext.createBuffer(1, bufferSize, this.audioContext.sampleRate);
      const data = buffer.getChannelData(0);
      
      // Create logarithmic sweep
      const w1 = 2 * Math.PI * startFreq;
      const w2 = 2 * Math.PI * endFreq;
      const k = (w1 / Math.log(w2 / w1)) / this.audioContext.sampleRate;
      
      for (let i = 0; i < bufferSize; i++) {
        // Exponential sine sweep formula
        const phase = k * ((w2 / w1) ** (i / bufferSize) - 1);
        
        // Apply fade-in and fade-out to avoid clicks
        let gain = 1.0;
        
        // Fade in (first 0.1%)
        if (i < bufferSize * 0.001) {
          gain = i / (bufferSize * 0.001);
        } 
        // Fade out (last 1%)
        else if (i > bufferSize * 0.99) {
          gain = (bufferSize - i) / (bufferSize * 0.01);
        }
        
        data[i] = Math.sin(phase) * gain * 0.9; // Avoid clipping
      }
      
      // Create source node
      const source = this.audioContext.createBufferSource();
      source.buffer = buffer;
      
      // Connect to destination
      source.connect(this.audioContext.destination);
      
      // Start playback
      source.start();
      
      // Resolve promise
      resolve(source);
    });
  }
}

export default RoomAcousticsAnalyzer;