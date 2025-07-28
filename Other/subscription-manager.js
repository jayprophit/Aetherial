// src/services/SubscriptionManager.js

/**
 * Subscription Manager Service
 * 
 * Handles subscription plans, billing, and entitlements
 */
class SubscriptionManager {
  constructor(apiClient, auth) {
    this.apiClient = apiClient;
    this.auth = auth;
    this.currentPlan = null;
    this.entitlements = null;
    this.paymentMethods = [];
    this.subscriptionStatus = null;
    this.billingHistory = [];
    this.trialStatus = null;
    
    // Subscription plan definitions
    this.plans = {
      free: {
        id: 'free',
        name: 'Free',
        price: 0,
        maxSpeakers: 2,
        audioQuality: 'standard', // 128kbps
        features: [
          'Basic speaker synchronization',
          'Standard audio quality',
          'Basic EQ controls',
          'Local file playback',
          'Ad-supported'
        ],
        restrictions: [
          'Limited to 2 speakers',
          'No advanced audio processing',
          'No speaker profiles',
          'No API access',
          'No social features'
        ]
      },
      premium: {
        id: 'premium',
        name: 'Premium',
        price: 4.99,
        interval: 'month',
        maxSpeakers: 8,
        audioQuality: 'high', // 256kbps
        features: [
          'Up to 8 speakers',
          'High-quality audio',
          'Advanced synchronization',
          'No advertisements',
          'Speaker profiles library',
          'Custom EQ settings',
          'Basic social features',
          'Music service integration',
          'Group presets (up to 5)'
        ],
        restrictions: [
          'Limited to 8 speakers',
          'No API access',
          'No multi-zone audio'
        ]
      },
      pro: {
        id: 'pro',
        name: 'Pro',
        price: 9.99,
        interval: 'month',
        maxSpeakers: 0, // Unlimited
        audioQuality: 'ultra', // 320kbps or lossless
        features: [
          'Unlimited speakers',
          'Ultra-high quality audio',
          'Professional synchronization',
          'Professional audio effects',
          'Neural audio processing',
          'Priority support',
          'Advanced analytics',
          'API access',
          'Room acoustic analysis',
          'Unlimited group presets',
          'All social features',
          'Custom speaker profiles'
        ],
        restrictions: [
          'Single zone only',
          'No commercial use'
        ]
      },
      business: {
        id: 'business',
        name: 'Business',
        price: 49.99,
        interval: 'month',
        maxSpeakers: 0, // Unlimited
        audioQuality: 'ultra', // 320kbps or lossless
        features: [
          'Unlimited speakers',
          'Multi-zone audio management',
          'Commercial use license',
          'User access controls',
          'Scheduled playback',
          'Multiple audio sources',
          'Business analytics',
          'Custom branding options',
          'Enterprise API access',
          'SLA & dedicated support',
          'All Pro features'
        ],
        restrictions: []
      }
    };
    
    // Initialize subscription data
    this.initialize();
  }
  
  /**
   * Initialize subscription data
   */
  async initialize() {
    try {
      // Skip if not logged in
      if (!this.auth.isAuthenticated()) {
        this.currentPlan = this.plans.free;
        return;
      }
      
      // Fetch current subscription data from API
      const subscriptionData = await this.apiClient.get('/subscriptions');
      
      if (subscriptionData && subscriptionData.plan) {
        this.currentPlan = this.plans[subscriptionData.plan] || this.plans.free;
        this.subscriptionStatus = subscriptionData.status;
        this.entitlements = subscriptionData.entitlements;
        this.trialStatus = subscriptionData.trialStatus;
        this.billingHistory = subscriptionData.billingHistory || [];
        this.renewalDate = subscriptionData.renewalDate
          ? new Date(subscriptionData.renewalDate)
          : null;
      } else {
        // Default to free plan if no subscription found
        this.currentPlan = this.plans.free;
        this.subscriptionStatus = 'active';
        this.entitlements = this.getEntitlementsForPlan('free');
      }
      
      // Fetch payment methods
      if (subscriptionData && subscriptionData.paymentMethods) {
        this.paymentMethods = subscriptionData.paymentMethods;
      }
      
      console.log('Subscription initialized:', this.currentPlan.name);
    } catch (error) {
      console.error('Failed to initialize subscription:', error);
      // Default to free plan on error
      this.currentPlan = this.plans.free;
      this.subscriptionStatus = 'active';
      this.entitlements = this.getEntitlementsForPlan('free');
    }
  }
  
  /**
   * Get all available subscription plans
   * @returns {Object} All subscription plans
   */
  getPlans() {
    return this.plans;
  }
  
  /**
   * Get current subscription plan
   * @returns {Object} Current plan
   */
  getCurrentPlan() {
    return this.currentPlan;
  }
  
  /**
   * Get subscription status
   * @returns {string} Subscription status
   */
  getStatus() {
    return this.subscriptionStatus;
  }
  
  /**
   * Check if user has access to a specific feature
   * @param {string} feature - Feature name to check
   * @returns {boolean} Whether user has access
   */
  hasFeature(feature) {
    if (!this.entitlements) {
      return false;
    }
    
    return this.entitlements[feature] === true;
  }
  
  /**
   * Get maximum number of speakers allowed
   * @returns {number} Max speakers (0 = unlimited)
   */
  getMaxSpeakers() {
    if (!this.currentPlan) {
      return 2; // Default to free tier limit
    }
    
    return this.currentPlan.maxSpeakers;
  }
  
  /**
   * Get audio quality level
   * @returns {string} Audio quality level
   */
  getAudioQuality() {
    if (!this.currentPlan) {
      return 'standard';
    }
    
    return this.currentPlan.audioQuality;
  }
  
  /**
   * Get billing history
   * @returns {Array} Billing history
   */
  getBillingHistory() {
    return this.billingHistory;
  }
  
  /**
   * Get payment methods
   * @returns {Array} Payment methods
   */
  getPaymentMethods() {
    return this.paymentMethods;
  }
  
  /**
   * Check if free trial is available
   * @returns {boolean} Whether trial is available
   */
  isTrialAvailable() {
    return this.trialStatus === 'available';
  }
  
  /**
   * Check if in trial period
   * @returns {boolean} Whether in trial
   */
  isInTrial() {
    return this.trialStatus === 'active';
  }
  
  /**
   * Get trial days remaining
   * @returns {number} Days remaining in trial
   */
  getTrialDaysRemaining() {
    if (!this.isInTrial() || !this.trialStatus.expiresAt) {
      return 0;
    }
    
    const now = new Date();
    const expiresAt = new Date(this.trialStatus.expiresAt);
    const diffTime = Math.abs(expiresAt - now);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    return diffDays;
  }
  
  /**
   * Get renewal date
   * @returns {Date|null} Next renewal date
   */
  getRenewalDate() {
    return this.renewalDate;
  }
  
  /**
   * Upgrade to a new plan
   * @param {string} planId - ID of the plan to upgrade to
   * @param {Object} paymentMethod - Payment method to use
   * @returns {Promise<Object>} Result of the upgrade
   */
  async upgradePlan(planId, paymentMethod = null) {
    try {
      if (!this.auth.isAuthenticated()) {
        throw new Error('User must be logged in to upgrade');
      }
      
      if (!this.plans[planId]) {
        throw new Error(`Invalid plan ID: ${planId}`);
      }
      
      // If current plan is free, we need a payment method
      if (this.currentPlan.id === 'free' && this.plans[planId].price > 0) {
        if (!paymentMethod && this.paymentMethods.length === 0) {
          throw new Error('Payment method required for paid plan');
        }
      }
      
      // Call API to upgrade plan
      const paymentMethodId = paymentMethod ? paymentMethod.id : null;
      const result = await this.apiClient.post('/subscriptions', {
        planId,
        paymentMethodId
      });
      
      if (result.success) {
        // Update local state
        this.currentPlan = this.plans[planId];
        this.subscriptionStatus = result.status;
        this.entitlements = result.entitlements;
        this.renewalDate = result.renewalDate ? new Date(result.renewalDate) : null;
        
        console.log(`Successfully upgraded to ${this.currentPlan.name} plan`);
        return {
          success: true,
          plan: this.currentPlan
        };
      } else {
        throw new Error(result.message || 'Failed to upgrade plan');
      }
    } catch (error) {
      console.error('Failed to upgrade plan:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }
  
  /**
   * Downgrade to a lower plan
   * @param {string} planId - ID of the plan to downgrade to
   * @returns {Promise<Object>} Result of the downgrade
   */
  async downgradePlan(planId) {
    try {
      if (!this.auth.isAuthenticated()) {
        throw new Error('User must be logged in to downgrade');
      }
      
      if (!this.plans[planId]) {
        throw new Error(`Invalid plan ID: ${planId}`);
      }
      
      // Call API to downgrade plan
      const result = await this.apiClient.post('/subscriptions/downgrade', {
        planId
      });
      
      if (result.success) {
        // Downgrade is typically scheduled for end of billing period
        this.pendingPlanChange = {
          plan: this.plans[planId],
          effectiveDate: result.effectiveDate ? new Date(result.effectiveDate) : null
        };
        
        console.log(`Plan downgrade scheduled for ${this.pendingPlanChange.effectiveDate}`);
        return {
          success: true,
          pendingChange: this.pendingPlanChange
        };
      } else {
        throw new Error(result.message || 'Failed to downgrade plan');
      }
    } catch (error) {
      console.error('Failed to downgrade plan:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }
  
  /**
   * Cancel subscription
   * @returns {Promise<Object>} Result of the cancellation
   */
  async cancelSubscription() {
    try {
      if (!this.auth.isAuthenticated()) {
        throw new Error('User must be logged in to cancel');
      }
      
      // Call API to cancel subscription
      const result = await this.apiClient.post('/subscriptions/cancel');
      
      if (result.success) {
        // Cancellation is typically scheduled for end of billing period
        this.subscriptionStatus = 'canceled';
        this.cancellationDate = result.effectiveDate 
          ? new Date(result.effectiveDate) 
          : null;
        
        console.log(`Subscription canceled, effective ${this.cancellationDate}`);
        return {
          success: true,
          effectiveDate: this.cancellationDate
        };
      } else {
        throw new Error(result.message || 'Failed to cancel subscription');
      }
    } catch (error) {
      console.error('Failed to cancel subscription:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }
  
  /**
   * Add a new payment method
   * @param {Object} paymentDetails - Payment method details
   * @returns {Promise<Object>} Result of adding payment method
   */
  async addPaymentMethod(paymentDetails) {
    try {
      if (!this.auth.isAuthenticated()) {
        throw new Error('User must be logged in to add payment method');
      }
      
      // Call API to add payment method
      const result = await this.apiClient.post('/payment-methods', paymentDetails);
      
      if (result.success) {
        // Add to local state
        this.paymentMethods.push(result.paymentMethod);
        
        console.log('Payment method added successfully');
        return {
          success: true,
          paymentMethod: result.paymentMethod
        };
      } else {
        throw new Error(result.message || 'Failed to add payment method');
      }
    } catch (error) {
      console.error('Failed to add payment method:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }
  
  /**
   * Remove a payment method
   * @param {string} paymentMethodId - ID of payment method to remove
   * @returns {Promise<Object>} Result of removing payment method
   */
  async removePaymentMethod(paymentMethodId) {
    try {
      if (!this.auth.isAuthenticated()) {
        throw new Error('User must be logged in to remove payment method');
      }
      
      // Call API to remove payment method
      const result = await this.apiClient.delete(`/payment-methods/${paymentMethodId}`);
      
      if (result.success) {
        // Remove from local state
        this.paymentMethods = this.paymentMethods.filter(
          method => method.id !== paymentMethodId
        );
        
        console.log('Payment method removed successfully');
        return {
          success: true
        };
      } else {
        throw new Error(result.message || 'Failed to remove payment method');
      }
    } catch (error) {
      console.error('Failed to remove payment method:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }
  
  /**
   * Start a free trial
   * @param {string} planId - ID of the plan to trial
   * @param {Object} paymentMethod - Payment method for after trial
   * @returns {Promise<Object>} Result of starting the trial
   */
  async startTrial(planId, paymentMethod) {
    try {
      if (!this.auth.isAuthenticated()) {
        throw new Error('User must be logged in to start a trial');
      }
      
      if (!this.isTrialAvailable()) {
        throw new Error('No trial available for this account');
      }
      
      if (!this.plans[planId]) {
        throw new Error(`Invalid plan ID: ${planId}`);
      }
      
      if (!paymentMethod) {
        throw new Error('Payment method required for trial');
      }
      
      // Call API to start trial
      const result = await this.apiClient.post('/subscriptions/trial', {
        planId,
        paymentMethodId: paymentMethod.id
      });
      
      if (result.success) {
        // Update local state
        this.currentPlan = this.plans[planId];
        this.subscriptionStatus = 'active';
        this.trialStatus = 'active';
        this.trialStatus.expiresAt = result.trialExpiresAt;
        this.entitlements = result.entitlements;
        
        console.log(`Successfully started ${this.currentPlan.name} trial`);
        return {
          success: true,
          plan: this.currentPlan,
          expiresAt: result.trialExpiresAt
        };
      } else {
        throw new Error(result.message || 'Failed to start trial');
      }
    } catch (error) {
      console.error('Failed to start trial:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }
  
  /**
   * Get entitlements for a specific plan
   * @param {string} planId - ID of the plan
   * @returns {Object} Entitlements for the plan
   */
  getEntitlementsForPlan(planId) {
    switch (planId) {
      case 'free':
        return {
          maxSpeakers: 2,
          audioQuality: 'standard',
          advancedAudio: false,
          speakerProfiles: false,
          noAds: false,
          socialFeatures: false,
          apiAccess: false,
          multiZone: false,
          analyticsAccess: false,
          neuralProcessing: false,
          roomAnalysis: false
        };
      case 'premium':
        return {
          maxSpeakers: 8,
          audioQuality: 'high',
          advancedAudio: true,
          speakerProfiles: true,
          noAds: true,
          socialFeatures: true,
          apiAccess: false,
          multiZone: false,
          analyticsAccess: false,
          neuralProcessing: false,
          roomAnalysis: false
        };
      case 'pro':
        return {
          maxSpeakers: 0, // Unlimited
          audioQuality: 'ultra',
          advancedAudio: true,
          speakerProfiles: true,
          noAds: true,
          socialFeatures: true,
          apiAccess: true,
          multiZone: false,
          analyticsAccess: true,
          neuralProcessing: true,
          roomAnalysis: true
        };
      case 'business':
        return {
          maxSpeakers: 0, // Unlimited
          audioQuality: 'ultra',
          advancedAudio: true,
          speakerProfiles: true,
          noAds: true,
          socialFeatures: true,
          apiAccess: true,
          multiZone: true,
          analyticsAccess: true,
          neuralProcessing: true,
          roomAnalysis: true,
          commercialUse: true,
          userAccess: true,
          scheduledPlayback: true,
          customBranding: true
        };
      default:
        return this.getEntitlementsForPlan('free');
    }
  }
}

export default SubscriptionManager;