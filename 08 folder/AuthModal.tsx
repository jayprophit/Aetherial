import React, { useState } from 'react';

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialMode?: 'login' | 'register';
}

const AuthModal: React.FC<AuthModalProps> = ({ isOpen, onClose, initialMode = 'login' }) => {
  const [mode, setMode] = useState<'login' | 'register' | 'profile-type'>(initialMode);
  const [profileType, setProfileType] = useState<'personal' | 'business'>('personal');
  const [kycLevel, setKycLevel] = useState<'no_kyc' | 'basic_kyc' | 'full_kyc'>('no_kyc');
  const [businessTier, setBusinessTier] = useState<'starter' | 'professional' | 'enterprise'>('starter');
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    firstName: '',
    lastName: '',
    businessName: '',
    businessType: '',
    agreeToTerms: false
  });

  if (!isOpen) return null;

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value
    }));
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    // Login logic here
    console.log('Login attempt:', { email: formData.email, password: formData.password });
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      alert('Passwords do not match');
      return;
    }
    
    const registrationData = {
      email: formData.email,
      password: formData.password,
      firstName: formData.firstName,
      lastName: formData.lastName,
      profileType,
      kycLevel,
      businessTier: profileType === 'business' ? businessTier : undefined,
      businessName: profileType === 'business' ? formData.businessName : undefined,
      businessType: profileType === 'business' ? formData.businessType : undefined
    };
    
    console.log('Registration attempt:', registrationData);
    // Registration logic here
  };

  const renderLoginForm = () => (
    <form onSubmit={handleLogin} className="space-y-6">
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
          Email Address
        </label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleInputChange}
          required
          className="w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-white"
          placeholder="Enter your email"
        />
      </div>
      
      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
          Password
        </label>
        <input
          type="password"
          id="password"
          name="password"
          value={formData.password}
          onChange={handleInputChange}
          required
          className="w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-white"
          placeholder="Enter your password"
        />
      </div>
      
      <button
        type="submit"
        className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all duration-300"
      >
        Sign In
      </button>
      
      <div className="text-center">
        <button
          type="button"
          onClick={() => setMode('register')}
          className="text-blue-400 hover:text-blue-300 text-sm"
        >
          Don't have an account? Sign up
        </button>
      </div>
    </form>
  );

  const renderProfileTypeSelection = () => (
    <div className="space-y-6">
      <h3 className="text-xl font-semibold text-white mb-4">Choose Your Profile Type</h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div
          onClick={() => setProfileType('personal')}
          className={`p-6 border-2 rounded-lg cursor-pointer transition-all duration-300 ${
            profileType === 'personal'
              ? 'border-blue-500 bg-blue-500/10'
              : 'border-gray-600 hover:border-gray-500'
          }`}
        >
          <div className="text-center">
            <div className="text-3xl mb-3">👤</div>
            <h4 className="text-lg font-semibold text-white mb-2">Personal</h4>
            <p className="text-gray-400 text-sm">
              For individual users who want to explore, learn, and connect
            </p>
            <div className="mt-3 text-green-400 font-semibold">FREE</div>
          </div>
        </div>
        
        <div
          onClick={() => setProfileType('business')}
          className={`p-6 border-2 rounded-lg cursor-pointer transition-all duration-300 ${
            profileType === 'business'
              ? 'border-blue-500 bg-blue-500/10'
              : 'border-gray-600 hover:border-gray-500'
          }`}
        >
          <div className="text-center">
            <div className="text-3xl mb-3">🏢</div>
            <h4 className="text-lg font-semibold text-white mb-2">Business</h4>
            <p className="text-gray-400 text-sm">
              For businesses, entrepreneurs, and organizations
            </p>
            <div className="mt-3 text-blue-400 font-semibold">Starting at $29/month</div>
          </div>
        </div>
      </div>
      
      {profileType === 'business' && (
        <div className="space-y-4">
          <h4 className="text-lg font-semibold text-white">Business Tier</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {[
              { id: 'starter', name: 'Starter', price: '$29', features: ['Basic tools', 'Limited analytics'] },
              { id: 'professional', name: 'Professional', price: '$99', features: ['Advanced tools', 'Full analytics'] },
              { id: 'enterprise', name: 'Enterprise', price: '$299', features: ['Custom solutions', 'Dedicated support'] }
            ].map((tier) => (
              <div
                key={tier.id}
                onClick={() => setBusinessTier(tier.id as any)}
                className={`p-4 border rounded-lg cursor-pointer transition-all duration-300 ${
                  businessTier === tier.id
                    ? 'border-blue-500 bg-blue-500/10'
                    : 'border-gray-600 hover:border-gray-500'
                }`}
              >
                <h5 className="font-semibold text-white">{tier.name}</h5>
                <div className="text-blue-400 font-bold">{tier.price}/month</div>
                <ul className="text-sm text-gray-400 mt-2">
                  {tier.features.map((feature, idx) => (
                    <li key={idx}>• {feature}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      )}
      
      <div className="space-y-4">
        <h4 className="text-lg font-semibold text-white">Verification Level</h4>
        <div className="space-y-3">
          {[
            { id: 'no_kyc', name: 'No Verification', desc: 'Basic features, limited access to financial services' },
            { id: 'basic_kyc', name: 'Basic Verification', desc: 'Email + Phone verification, access to most features' },
            { id: 'full_kyc', name: 'Full Verification', desc: 'Complete identity verification, access to all features including blockchain and DeFi' }
          ].map((level) => (
            <label key={level.id} className="flex items-start space-x-3 cursor-pointer">
              <input
                type="radio"
                name="kycLevel"
                value={level.id}
                checked={kycLevel === level.id}
                onChange={(e) => setKycLevel(e.target.value as any)}
                className="mt-1"
              />
              <div>
                <div className="text-white font-medium">{level.name}</div>
                <div className="text-gray-400 text-sm">{level.desc}</div>
              </div>
            </label>
          ))}
        </div>
      </div>
      
      <button
        onClick={() => setMode('register')}
        className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all duration-300"
      >
        Continue to Registration
      </button>
    </div>
  );

  const renderRegistrationForm = () => (
    <form onSubmit={handleRegister} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label htmlFor="firstName" className="block text-sm font-medium text-gray-300 mb-2">
            First Name
          </label>
          <input
            type="text"
            id="firstName"
            name="firstName"
            value={formData.firstName}
            onChange={handleInputChange}
            required
            className="w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-white"
            placeholder="First name"
          />
        </div>
        
        <div>
          <label htmlFor="lastName" className="block text-sm font-medium text-gray-300 mb-2">
            Last Name
          </label>
          <input
            type="text"
            id="lastName"
            name="lastName"
            value={formData.lastName}
            onChange={handleInputChange}
            required
            className="w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-white"
            placeholder="Last name"
          />
        </div>
      </div>
      
      {profileType === 'business' && (
        <>
          <div>
            <label htmlFor="businessName" className="block text-sm font-medium text-gray-300 mb-2">
              Business Name
            </label>
            <input
              type="text"
              id="businessName"
              name="businessName"
              value={formData.businessName}
              onChange={handleInputChange}
              required
              className="w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-white"
              placeholder="Your business name"
            />
          </div>
          
          <div>
            <label htmlFor="businessType" className="block text-sm font-medium text-gray-300 mb-2">
              Business Type
            </label>
            <select
              id="businessType"
              name="businessType"
              value={formData.businessType}
              onChange={handleInputChange}
              required
              className="w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-white"
            >
              <option value="">Select business type</option>
              <option value="sole_proprietorship">Sole Proprietorship</option>
              <option value="partnership">Partnership</option>
              <option value="corporation">Corporation</option>
              <option value="llc">LLC</option>
              <option value="nonprofit">Nonprofit</option>
              <option value="other">Other</option>
            </select>
          </div>
        </>
      )}
      
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
          Email Address
        </label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleInputChange}
          required
          className="w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-white"
          placeholder="Enter your email"
        />
      </div>
      
      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
          Password
        </label>
        <input
          type="password"
          id="password"
          name="password"
          value={formData.password}
          onChange={handleInputChange}
          required
          className="w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-white"
          placeholder="Create a password"
        />
      </div>
      
      <div>
        <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-300 mb-2">
          Confirm Password
        </label>
        <input
          type="password"
          id="confirmPassword"
          name="confirmPassword"
          value={formData.confirmPassword}
          onChange={handleInputChange}
          required
          className="w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-white"
          placeholder="Confirm your password"
        />
      </div>
      
      <div className="flex items-start space-x-3">
        <input
          type="checkbox"
          id="agreeToTerms"
          name="agreeToTerms"
          checked={formData.agreeToTerms}
          onChange={handleInputChange}
          required
          className="mt-1"
        />
        <label htmlFor="agreeToTerms" className="text-sm text-gray-300">
          I agree to the <a href="#" className="text-blue-400 hover:text-blue-300">Terms of Service</a> and{' '}
          <a href="#" className="text-blue-400 hover:text-blue-300">Privacy Policy</a>
        </label>
      </div>
      
      <div className="bg-gray-800 p-4 rounded-lg">
        <h4 className="text-white font-semibold mb-2">Selected Configuration:</h4>
        <div className="text-sm text-gray-300 space-y-1">
          <div>Profile Type: <span className="text-blue-400 capitalize">{profileType}</span></div>
          {profileType === 'business' && (
            <div>Business Tier: <span className="text-blue-400 capitalize">{businessTier}</span></div>
          )}
          <div>Verification Level: <span className="text-blue-400">{kycLevel.replace('_', ' ').toUpperCase()}</span></div>
        </div>
      </div>
      
      <button
        type="submit"
        disabled={!formData.agreeToTerms}
        className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Create Account
      </button>
      
      <div className="text-center">
        <button
          type="button"
          onClick={() => setMode('profile-type')}
          className="text-blue-400 hover:text-blue-300 text-sm mr-4"
        >
          ← Back to Profile Type
        </button>
        <button
          type="button"
          onClick={() => setMode('login')}
          className="text-blue-400 hover:text-blue-300 text-sm"
        >
          Already have an account? Sign in
        </button>
      </div>
    </form>
  );

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 rounded-xl p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-white">
            {mode === 'login' ? 'Sign In' : mode === 'profile-type' ? 'Choose Profile Type' : 'Create Account'}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white text-2xl"
          >
            ×
   
(Content truncated due to size limit. Use line ranges to read in chunks)