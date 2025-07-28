/**
 * AI Model Registry
 * 
 * This module serves as a central registry for all AI models in the platform.
 * It provides a unified interface for accessing different types of models
 * and handles model loading, caching, and versioning.
 */

export type ModelType = 
  | 'text-generation'
  | 'text-embedding'
  | 'image-generation'
  | 'image-recognition'
  | 'recommendation'
  | 'conversation'
  | 'sentiment-analysis'
  | 'translation'
  | 'summarization'
  | 'question-answering';

export interface ModelConfig {
  id: string;
  type: ModelType;
  version: string;
  description: string;
  parameters?: Record<string, any>;
  capabilities: string[];
  requiresGPU?: boolean;
  memoryRequirements?: {
    min: number; // in MB
    recommended: number; // in MB
  };
  modelSize?: number; // in MB
  isRemote?: boolean;
  endpoint?: string;
}

export interface ModelInstance {
  config: ModelConfig;
  model: any; // The actual model instance
  isLoaded: boolean;
  lastUsed: Date;
}

class AIModelRegistry {
  private models: Map<string, ModelConfig> = new Map();
  private loadedModels: Map<string, ModelInstance> = new Map();
  private defaultModels: Map<ModelType, string> = new Map();

  /**
   * Register a new model in the registry
   */
  registerModel(config: ModelConfig): void {
    if (this.models.has(config.id)) {
      console.warn(`Model with ID ${config.id} is already registered. Overwriting.`);
    }
    
    this.models.set(config.id, config);
    
    // If this is the first model of its type, set it as default
    if (!this.defaultModels.has(config.type)) {
      this.setDefaultModel(config.type, config.id);
    }
  }

  /**
   * Set a model as the default for its type
   */
  setDefaultModel(type: ModelType, modelId: string): void {
    if (!this.models.has(modelId)) {
      throw new Error(`Cannot set default model: Model with ID ${modelId} is not registered.`);
    }
    
    const model = this.models.get(modelId)!;
    if (model.type !== type) {
      throw new Error(`Cannot set default model: Model ${modelId} is not of type ${type}.`);
    }
    
    this.defaultModels.set(type, modelId);
  }

  /**
   * Get a model configuration by ID
   */
  getModelConfig(modelId: string): ModelConfig {
    const config = this.models.get(modelId);
    if (!config) {
      throw new Error(`Model with ID ${modelId} is not registered.`);
    }
    return config;
  }

  /**
   * Get the default model for a specific type
   */
  getDefaultModel(type: ModelType): ModelConfig {
    const defaultModelId = this.defaultModels.get(type);
    if (!defaultModelId) {
      throw new Error(`No default model set for type ${type}.`);
    }
    
    return this.getModelConfig(defaultModelId);
  }

  /**
   * Get all registered models
   */
  getAllModels(): ModelConfig[] {
    return Array.from(this.models.values());
  }

  /**
   * Get all models of a specific type
   */
  getModelsByType(type: ModelType): ModelConfig[] {
    return this.getAllModels().filter(model => model.type === type);
  }

  /**
   * Load a model by ID
   * This is a placeholder for the actual model loading logic
   */
  async loadModel(modelId: string): Promise<ModelInstance> {
    if (this.loadedModels.has(modelId)) {
      const instance = this.loadedModels.get(modelId)!;
      instance.lastUsed = new Date();
      return instance;
    }
    
    const config = this.getModelConfig(modelId);
    
    // Placeholder for actual model loading logic
    // In a real implementation, this would load the model from disk or a remote endpoint
    console.log(`Loading model ${modelId}...`);
    
    // Simulate model loading
    const modelInstance: ModelInstance = {
      config,
      model: { /* This would be the actual model */ },
      isLoaded: true,
      lastUsed: new Date()
    };
    
    this.loadedModels.set(modelId, modelInstance);
    return modelInstance;
  }

  /**
   * Unload a model to free up resources
   */
  unloadModel(modelId: string): void {
    if (!this.loadedModels.has(modelId)) {
      return; // Model is not loaded, nothing to do
    }
    
    // Placeholder for actual model unloading logic
    console.log(`Unloading model ${modelId}...`);
    
    this.loadedModels.delete(modelId);
  }

  /**
   * Unload models that haven't been used recently to free up resources
   */
  unloadStaleModels(maxAgeMinutes: number = 30): void {
    const now = new Date();
    const staleThreshold = now.getTime() - (maxAgeMinutes * 60 * 1000);
    
    for (const [modelId, instance] of this.loadedModels.entries()) {
      if (instance.lastUsed.getTime() < staleThreshold) {
        this.unloadModel(modelId);
      }
    }
  }
}

// Create and export a singleton instance
const modelRegistry = new AIModelRegistry();
export default modelRegistry;
