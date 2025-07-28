import React, { useState, useEffect } from 'react';

/**
 * ContentModerationSystem - AI-powered content moderation system for the unified platform
 * 
 * Features:
 * - Real-time content monitoring across all platform modules
 * - Age-appropriate content filtering (13+ for chat/messaging)
 * - Inappropriate behavior detection and flagging
 * - Temporary and permanent ban management
 * - Multi-language support
 * - Integration with platform notification system
 */
class ContentModerationSystem {
  constructor() {
    this.moderationRules = {
      ageRestrictions: {
        chat: 13,
        messaging: 13,
        adultContent: 18,
        financialTransactions: 18
      },
      contentCategories: {
        hate: { severity: 'high', action: 'ban_temporary' },
        violence: { severity: 'high', action: 'ban_temporary' },
        sexual: { severity: 'high', action: 'ban_temporary' },
        harassment: { severity: 'medium', action: 'warning' },
        spam: { severity: 'low', action: 'warning' },
        misinformation: { severity: 'medium', action: 'warning' }
      },
      banDurations: {
        warning: 0,
        ban_temporary: 7, // days
        ban_permanent: -1 // permanent
      }
    };
    
    this.flaggedUsers = new Map();
    this.bannedUsers = new Map();
    this.warningThreshold = 3; // Number of warnings before temporary ban
    this.tempBanThreshold = 3; // Number of temporary bans before permanent ban
  }

  /**
   * Analyze content using AI models to detect inappropriate material
   * @param {string} content - The content to analyze
   * @param {string} contentType - Type of content (text, image, video, etc.)
   * @param {object} context - Additional context about the content
   * @returns {object} Analysis results with detected categories and confidence scores
   */
  async analyzeContent(content, contentType, context = {}) {
    try {
      // In production, this would call the AI content analysis service
      // For demo purposes, we're simulating the AI response
      
      // Simulate AI processing delay
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Check for keywords that might indicate problematic content
      const lowerContent = content.toLowerCase();
      const results = {
        isAppropriate: true,
        categories: {},
        confidence: 0.95,
        recommendedAction: 'allow'
      };
      
      // Simple keyword detection for demo purposes
      const keywords = {
        hate: ['hate', 'racist', 'discrimination'],
        violence: ['kill', 'attack', 'fight', 'hurt'],
        sexual: ['sex', 'explicit', 'nude'],
        harassment: ['stupid', 'idiot', 'loser'],
        spam: ['buy now', 'click here', 'free money'],
        misinformation: ['fake news', 'conspiracy']
      };
      
      // Check each category
      for (const [category, words] of Object.entries(keywords)) {
        for (const word of words) {
          if (lowerContent.includes(word)) {
            results.categories[category] = {
              detected: true,
              confidence: 0.85 + Math.random() * 0.1,
              severity: this.moderationRules.contentCategories[category].severity
            };
            results.isAppropriate = false;
            results.recommendedAction = this.moderationRules.contentCategories[category].action;
            break;
          }
        }
      }
      
      return results;
    } catch (error) {
      console.error('Content analysis error:', error);
      // Default to conservative approach on error
      return {
        isAppropriate: false,
        error: 'Analysis failed',
        recommendedAction: 'review'
      };
    }
  }

  /**
   * Check if user meets age requirements for specific feature
   * @param {number} userAge - User's age
   * @param {string} feature - Platform feature to check
   * @returns {boolean} Whether user meets age requirements
   */
  checkAgeRequirement(userAge, feature) {
    const requiredAge = this.moderationRules.ageRestrictions[feature] || 0;
    return userAge >= requiredAge;
  }

  /**
   * Process content before it's published on the platform
   * @param {string} content - Content to be published
   * @param {string} contentType - Type of content
   * @param {object} user - User publishing the content
   * @param {object} context - Additional context
   * @returns {object} Processing result with approval status
   */
  async processContent(content, contentType, user, context = {}) {
    // Check if user is banned
    if (this.isUserBanned(user.id)) {
      return {
        approved: false,
        reason: 'User is banned from posting content',
        banInfo: this.getBanInfo(user.id)
      };
    }
    
    // Check age restrictions
    if (context.feature && !this.checkAgeRequirement(user.age, context.feature)) {
      return {
        approved: false,
        reason: `Age restriction: must be ${this.moderationRules.ageRestrictions[context.feature]}+ to use this feature`
      };
    }
    
    // Analyze content
    const analysisResult = await this.analyzeContent(content, contentType, context);
    
    if (!analysisResult.isAppropriate) {
      // Handle inappropriate content
      this.flagContent(content, analysisResult, user.id);
      
      // Take action based on severity
      if (analysisResult.recommendedAction !== 'allow') {
        this.takeAction(user.id, analysisResult.recommendedAction, analysisResult.categories);
      }
      
      return {
        approved: false,
        reason: 'Content violates community guidelines',
        categories: analysisResult.categories
      };
    }
    
    return {
      approved: true
    };
  }

  /**
   * Flag content for review
   * @param {string} content - The flagged content
   * @param {object} analysisResult - Analysis results
   * @param {string} userId - User ID who posted the content
   */
  flagContent(content, analysisResult, userId) {
    // In production, this would store the flagged content in a database for review
    console.log(`Content flagged for user ${userId}:`, {
      timestamp: new Date(),
      content: content.substring(0, 100) + (content.length > 100 ? '...' : ''),
      categories: analysisResult.categories,
      action: analysisResult.recommendedAction
    });
  }

  /**
   * Take action against a user based on violation
   * @param {string} userId - User ID
   * @param {string} action - Action to take (warning, ban_temporary, ban_permanent)
   * @param {object} categories - Violation categories
   */
  takeAction(userId, action, categories) {
    const now = new Date();
    
    if (action === 'warning') {
      // Add warning
      if (!this.flaggedUsers.has(userId)) {
        this.flaggedUsers.set(userId, {
          warnings: 1,
          lastWarning: now,
          categories: categories
        });
      } else {
        const userData = this.flaggedUsers.get(userId);
        userData.warnings += 1;
        userData.lastWarning = now;
        
        // Check if warning threshold reached
        if (userData.warnings >= this.warningThreshold) {
          this.banUser(userId, 'ban_temporary', categories);
          userData.warnings = 0; // Reset warnings after ban
        }
        
        this.flaggedUsers.set(userId, userData);
      }
    } else {
      // Ban user
      this.banUser(userId, action, categories);
    }
  }

  /**
   * Ban a user from the platform
   * @param {string} userId - User ID
   * @param {string} banType - Type of ban (ban_temporary, ban_permanent)
   * @param {object} categories - Violation categories
   */
  banUser(userId, banType, categories) {
    const now = new Date();
    const banDuration = this.moderationRules.banDurations[banType];
    
    let endDate = null;
    if (banDuration > 0) {
      endDate = new Date();
      endDate.setDate(now.getDate() + banDuration);
    }
    
    // Check if user has previous bans
    if (this.bannedUsers.has(userId)) {
      const banData = this.bannedUsers.get(userId);
      banData.banCount += 1;
      
      // Check if temporary ban threshold reached
      if (banType === 'ban_temporary' && banData.banCount >= this.tempBanThreshold) {
        banType = 'ban_permanent';
        endDate = null;
      }
      
      banData.currentBan = {
        type: banType,
        startDate: now,
        endDate: endDate,
        categories: categories
      };
      
      this.bannedUsers.set(userId, banData);
    } else {
      this.bannedUsers.set(userId, {
        banCount: 1,
        currentBan: {
          type: banType,
          startDate: now,
          endDate: endDate,
          categories: categories
        }
      });
    }
    
    // In production, this would trigger notifications to the user and admin
    console.log(`User ${userId} banned:`, {
      type: banType,
      duration: banDuration === -1 ? 'Permanent' : `${banDuration} days`,
      endDate: endDate
    });
  }

  /**
   * Check if a user is currently banned
   * @param {string} userId - User ID
   * @returns {boolean} Whether user is banned
   */
  isUserBanned(userId) {
    if (!this.bannedUsers.has(userId)) {
      return false;
    }
    
    const banData = this.bannedUsers.get(userId);
    const currentBan = banData.currentBan;
    
    // Permanent ban
    if (currentBan.type === 'ban_permanent') {
      return true;
    }
    
    // Check if temporary ban has expired
    const now = new Date();
    return now < currentBan.endDate;
  }

  /**
   * Get ban information for a user
   * @param {string} userId - User ID
   * @returns {object|null} Ban information or null if not banned
   */
  getBanInfo(userId) {
    if (!this.isUserBanned(userId)) {
      return null;
    }
    
    const banData = this.bannedUsers.get(userId);
    return banData.currentBan;
  }

  /**
   * Filter content based on user age
   * @param {array} contentItems - Array of content items
   * @param {number} userAge - User's age
   * @param {string} contentType - Type of content
   * @returns {array} Filtered content items
   */
  filterContentByAge(contentItems, userAge, contentType) {
    return contentItems.filter(item => {
      // Check if content has age restriction
      if (!item.ageRestriction) {
        return true;
      }
      
      // Different content types might have different age thresholds
      let requiredAge = 0;
      
      if (contentType === 'chat' || contentType === 'messaging') {
        requiredAge = this.moderationRules.ageRestrictions[contentType];
      } else if (item.adultContent) {
        requiredAge = this.moderationRules.ageRestrictions.adultContent;
      }
      
      return userAge >= requiredAge;
    });
  }
}

export default ContentModerationSystem;
