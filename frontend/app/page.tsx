'use client';

import { useState } from 'react';

interface AllocationData {
  stockPercent: number;
  bondPercent: number;
  successRate: number;
  successes: number;
  failures: number;
  avgFinalPortfolio: number;
  medianYearsToFailure: number | null;
}

interface AllocationSweepResult {
  type: 'allocationSweep';
  allocations: AllocationData[];
  bestAllocation: {
    stockPercent: number;
    bondPercent: number;
    successRate: number;
  };
  totalCombinations: number;
  simulationsPerCombination: number;
  totalSimulations: number;
}

export default function Home() {
  const [formData, setFormData] = useState({
    yearsInRetirement: '',
    withdrawalRate: '',
    inflationRate: '',
  });

  const [errors, setErrors] = useState({
    yearsInRetirement: '',
    withdrawalRate: '',
    inflationRate: '',
  });

  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isListening, setIsListening] = useState<string | null>(null);
  const [isSimulating, setIsSimulating] = useState(false);
  const [sweepResults, setSweepResults] = useState<AllocationSweepResult | null>(null);

  // Text-to-speech function with female voice
  const speak = (text: string) => {
    if ('speechSynthesis' in window) {
      // Cancel any ongoing speech
      window.speechSynthesis.cancel();

      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.9; // Slightly slower for clarity
      utterance.pitch = 1;
      utterance.volume = 1;

      // Try to use a female voice
      const voices = window.speechSynthesis.getVoices();
      const femaleVoice = voices.find(voice =>
        voice.name.toLowerCase().includes('female') ||
        voice.name.toLowerCase().includes('woman') ||
        voice.name.includes('Samantha') || // macOS
        voice.name.includes('Victoria') || // macOS
        voice.name.includes('Zira') || // Windows
        voice.name.includes('Google US English Female') || // Chrome
        voice.name.includes('Microsoft Zira') // Edge
      );
      if (femaleVoice) {
        utterance.voice = femaleVoice;
      }

      utterance.onstart = () => setIsSpeaking(true);
      utterance.onend = () => setIsSpeaking(false);

      window.speechSynthesis.speak(utterance);
    } else {
      alert('Sorry, your browser does not support text-to-speech.');
    }
  };

  // Speech-to-text function (voice input)
  const startListening = (field: string) => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      alert('Sorry, your browser does not support voice input. Please use Chrome, Edge, or Safari.');
      return;
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const SpeechRecognitionAPI = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (!SpeechRecognitionAPI) return;

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const recognition = new SpeechRecognitionAPI() as any;

    recognition.lang = 'en-US';
    recognition.continuous = false;
    recognition.interimResults = false;

    setIsListening(field);

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      // Extract numbers from speech
      const numberMatch = transcript.match(/\d+(\.\d+)?/);
      if (numberMatch) {
        handleInputChange(field, numberMatch[0]);
      } else {
        alert(`I heard: "${transcript}". Please say a number.`);
      }
      setIsListening(null);
    };

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    recognition.onerror = (event: any) => {
      console.error('Speech recognition error:', event.error);
      alert('Could not understand. Please try again.');
      setIsListening(null);
    };

    recognition.onend = () => {
      setIsListening(null);
    };

    recognition.start();
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error when user starts typing
    if (errors[field as keyof typeof errors]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  const validateForm = (): boolean => {
    const newErrors = {
      yearsInRetirement: '',
      withdrawalRate: '',
      inflationRate: '',
    };

    let isValid = true;

    // Validate years in retirement
    const years = parseFloat(formData.yearsInRetirement);
    if (!formData.yearsInRetirement) {
      newErrors.yearsInRetirement = 'Please enter the number of years';
      isValid = false;
    } else if (isNaN(years) || years < 1 || years > 60) {
      newErrors.yearsInRetirement = 'Please enter a value between 1 and 60 years';
      isValid = false;
    } else if (!Number.isInteger(years)) {
      newErrors.yearsInRetirement = 'Please enter a whole number';
      isValid = false;
    }

    // Validate withdrawal rate
    const withdrawal = parseFloat(formData.withdrawalRate);
    if (!formData.withdrawalRate) {
      newErrors.withdrawalRate = 'Please enter your withdrawal rate';
      isValid = false;
    } else if (isNaN(withdrawal) || withdrawal < 0.1 || withdrawal > 20) {
      newErrors.withdrawalRate = 'Please enter a value between 0.1% and 20%';
      isValid = false;
    }

    // Validate inflation rate (optional)
    if (formData.inflationRate) {
      const inflation = parseFloat(formData.inflationRate);
      if (isNaN(inflation) || inflation < 0 || inflation > 10) {
        newErrors.inflationRate = 'Please enter a value between 0% and 10%';
        isValid = false;
      }
    }

    setErrors(newErrors);
    return isValid;
  };

  const handleAllocationSweep = async () => {
    if (!validateForm()) {
      const errorMessages = Object.values(errors).filter(e => e).join('. ');
      if (errorMessages) {
        const errorAnnouncement = `Please fix the following errors: ${errorMessages}`;
        speak(errorAnnouncement);
      }
      return;
    }

    // Clear previous results
    setSweepResults(null);
    setIsSimulating(true);

    try {
      // Call Monte Carlo API with allocation sweep
      const response = await fetch('/api/monte-carlo', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          years: parseInt(formData.yearsInRetirement),
          withdrawalRate: parseFloat(formData.withdrawalRate),
          inflation: formData.inflationRate ? parseFloat(formData.inflationRate) : null,
          allocationSweep: true,
        }),
      });

      if (!response.ok) {
        throw new Error('Allocation sweep failed');
      }

      const data: AllocationSweepResult = await response.json();
      setSweepResults(data);

      // Announce results for screen readers
      speak(`Allocation sweep complete. Tested ${data.totalCombinations} different allocations. Best allocation is ${data.bestAllocation.stockPercent} percent stocks with a ${data.bestAllocation.successRate.toFixed(1)} percent success rate.`);
    } catch (error) {
      console.error('Allocation sweep error:', error);
      alert('Sorry, the allocation sweep failed. Please try again.');
    } finally {
      setIsSimulating(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className={`mx-auto transition-all ${sweepResults ? 'max-w-7xl' : 'max-w-2xl'}`}>
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-4">
            Longevity Planning
          </h1>
          <p className="text-xl text-gray-700">
            Let&apos;s plan your retirement together
          </p>
        </header>

        {/* Main Form Card */}
        <div className="bg-white rounded-2xl shadow-lg p-8 sm:p-12">
          <form onSubmit={(e) => { e.preventDefault(); handleAllocationSweep(); }} noValidate>
            <div className="space-y-8">

              {/* Question 1: Years in Retirement */}
              <div>
                <label
                  htmlFor="yearsInRetirement"
                  className="block text-2xl font-semibold text-gray-900 mb-3"
                >
                  1. How many years do you plan on spending in retirement?
                  <button
                    type="button"
                    onClick={() => speak('How many years do you plan on spending in retirement? Enter a number between 1 and 60 years. This helps us calculate how long your savings need to last.')}
                    className="ml-3 inline-flex items-center justify-center w-10 h-10 rounded-full bg-blue-100 text-blue-600 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                    aria-label="Read question aloud"
                    title="Listen to this question"
                  >
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                      <path d="M10 3.5a6.5 6.5 0 100 13 6.5 6.5 0 000-13zM2 10a8 8 0 1116 0 8 8 0 01-16 0zm8-5a1 1 0 011 1v3.5a1 1 0 11-2 0V6a1 1 0 011-1zm0 7a1 1 0 100 2 1 1 0 000-2z" />
                    </svg>
                  </button>
                </label>
                <div className="flex gap-3 items-start">
                  <input
                    type="number"
                    id="yearsInRetirement"
                    name="yearsInRetirement"
                    value={formData.yearsInRetirement}
                    onChange={(e) => handleInputChange('yearsInRetirement', e.target.value)}
                    className={`flex-1 px-6 py-4 text-2xl border-2 rounded-lg focus:ring-4 focus:ring-blue-500 focus:border-blue-500 ${
                      errors.yearsInRetirement ? 'border-red-500 bg-red-50' : 'border-gray-300 bg-gray-50'
                    }`}
                    placeholder="25"
                    min="1"
                    max="60"
                    step="1"
                    aria-describedby={errors.yearsInRetirement ? 'yearsInRetirement-error' : 'yearsInRetirement-help'}
                    aria-invalid={errors.yearsInRetirement ? 'true' : 'false'}
                  />
                  <button
                    type="button"
                    onClick={() => startListening('yearsInRetirement')}
                    disabled={isListening !== null}
                    className={`flex-shrink-0 w-14 h-14 rounded-lg flex items-center justify-center transition-colors ${
                      isListening === 'yearsInRetirement'
                        ? 'bg-red-500 text-white animate-pulse'
                        : 'bg-green-100 text-green-700 hover:bg-green-200'
                    } focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50`}
                    aria-label="Speak your answer"
                    title="Click and speak your answer"
                  >
                    <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                      <path d="M7 4a3 3 0 016 0v6a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" />
                    </svg>
                  </button>
                </div>
                {errors.yearsInRetirement && (
                  <p id="yearsInRetirement-error" className="mt-2 text-lg text-red-600 font-medium" role="alert">
                    ⚠️ {errors.yearsInRetirement}
                  </p>
                )}
              </div>

              {/* Question 2: Withdrawal Rate */}
              <div>
                <label
                  htmlFor="withdrawalRate"
                  className="block text-2xl font-semibold text-gray-900 mb-3"
                >
                  2. How much would you like to withdraw in year 1 as a percentage of your total portfolio?
                  <button
                    type="button"
                    onClick={() => speak('How much would you like to withdraw in year 1 as a percentage of your total portfolio? Enter a percentage between 0.1 and 20. This is the amount you will withdraw in the first year, and it will adjust with inflation each year after.')}
                    className="ml-3 inline-flex items-center justify-center w-10 h-10 rounded-full bg-blue-100 text-blue-600 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                    aria-label="Read question aloud"
                    title="Listen to this question"
                  >
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                      <path d="M10 3.5a6.5 6.5 0 100 13 6.5 6.5 0 000-13zM2 10a8 8 0 1116 0 8 8 0 01-16 0zm8-5a1 1 0 011 1v3.5a1 1 0 11-2 0V6a1 1 0 011-1zm0 7a1 1 0 100 2 1 1 0 000-2z" />
                    </svg>
                  </button>
                </label>
                <div className="flex gap-3 items-start">
                  <div className="relative flex-1">
                    <input
                      type="number"
                      id="withdrawalRate"
                      name="withdrawalRate"
                      value={formData.withdrawalRate}
                      onChange={(e) => handleInputChange('withdrawalRate', e.target.value)}
                      className={`w-full px-6 py-4 pr-16 text-2xl border-2 rounded-lg focus:ring-4 focus:ring-blue-500 focus:border-blue-500 ${
                        errors.withdrawalRate ? 'border-red-500 bg-red-50' : 'border-gray-300 bg-gray-50'
                      }`}
                      placeholder="4"
                      min="0.1"
                      max="20"
                      step="0.1"
                      aria-describedby={errors.withdrawalRate ? 'withdrawalRate-error' : 'withdrawalRate-help'}
                      aria-invalid={errors.withdrawalRate ? 'true' : 'false'}
                    />
                    <span className="absolute right-6 top-1/2 -translate-y-1/2 text-2xl text-gray-500 pointer-events-none">
                      %
                    </span>
                  </div>
                  <button
                    type="button"
                    onClick={() => startListening('withdrawalRate')}
                    disabled={isListening !== null}
                    className={`flex-shrink-0 w-14 h-14 rounded-lg flex items-center justify-center transition-colors ${
                      isListening === 'withdrawalRate'
                        ? 'bg-red-500 text-white animate-pulse'
                        : 'bg-green-100 text-green-700 hover:bg-green-200'
                    } focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50`}
                    aria-label="Speak your answer"
                    title="Click and speak your answer"
                  >
                    <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                      <path d="M7 4a3 3 0 016 0v6a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" />
                    </svg>
                  </button>
                </div>
                {errors.withdrawalRate && (
                  <p id="withdrawalRate-error" className="mt-2 text-lg text-red-600 font-medium" role="alert">
                    ⚠️ {errors.withdrawalRate}
                  </p>
                )}
              </div>

              {/* Question 3: Inflation Rate */}
              <div>
                <label
                  htmlFor="inflationRate"
                  className="block text-2xl font-semibold text-gray-900 mb-3"
                >
                  3. What inflation rate would you like to use?
                  <button
                    type="button"
                    onClick={() => speak('What inflation rate would you like to use? Enter a percentage between 0 and 10. If you leave this blank, we will use historical numbers. This determines how much your withdrawals will increase each year to maintain your purchasing power.')}
                    className="ml-3 inline-flex items-center justify-center w-10 h-10 rounded-full bg-blue-100 text-blue-600 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                    aria-label="Read question aloud"
                    title="Listen to this question"
                  >
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                      <path d="M10 3.5a6.5 6.5 0 100 13 6.5 6.5 0 000-13zM2 10a8 8 0 1116 0 8 8 0 01-16 0zm8-5a1 1 0 011 1v3.5a1 1 0 11-2 0V6a1 1 0 011-1zm0 7a1 1 0 100 2 1 1 0 000-2z" />
                    </svg>
                  </button>
                </label>
                <p className="text-lg text-gray-600 mb-4">
                  If you leave this blank, we will use historical numbers
                </p>
                <div className="flex gap-3 items-start">
                  <div className="relative flex-1">
                    <input
                      type="number"
                      id="inflationRate"
                      name="inflationRate"
                      value={formData.inflationRate}
                      onChange={(e) => handleInputChange('inflationRate', e.target.value)}
                      className={`w-full px-6 py-4 pr-16 text-2xl border-2 rounded-lg focus:ring-4 focus:ring-blue-500 focus:border-blue-500 ${
                        errors.inflationRate ? 'border-red-500 bg-red-50' : 'border-gray-300 bg-gray-50'
                      }`}
                      placeholder="3"
                      min="0"
                      max="10"
                      step="0.1"
                      aria-describedby={errors.inflationRate ? 'inflationRate-error' : 'inflationRate-help'}
                      aria-invalid={errors.inflationRate ? 'true' : 'false'}
                    />
                    <span className="absolute right-6 top-1/2 -translate-y-1/2 text-2xl text-gray-500 pointer-events-none">
                      %
                    </span>
                  </div>
                  <button
                    type="button"
                    onClick={() => startListening('inflationRate')}
                    disabled={isListening !== null}
                    className={`flex-shrink-0 w-14 h-14 rounded-lg flex items-center justify-center transition-colors ${
                      isListening === 'inflationRate'
                        ? 'bg-red-500 text-white animate-pulse'
                        : 'bg-green-100 text-green-700 hover:bg-green-200'
                    } focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50`}
                    aria-label="Speak your answer"
                    title="Click and speak your answer"
                  >
                    <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                      <path d="M7 4a3 3 0 016 0v6a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" />
                    </svg>
                  </button>
                </div>
                {errors.inflationRate && (
                  <p id="inflationRate-error" className="mt-2 text-lg text-red-600 font-medium" role="alert">
                    ⚠️ {errors.inflationRate}
                  </p>
                )}
              </div>

              {/* Submit Button */}
              <div className="pt-6">
                <button
                  type="button"
                  onClick={handleAllocationSweep}
                  disabled={isSimulating}
                  className="w-full py-5 px-8 text-2xl font-semibold text-white bg-purple-600 rounded-lg hover:bg-purple-700 focus:outline-none focus:ring-4 focus:ring-purple-500 focus:ring-offset-2 transition-colors shadow-lg hover:shadow-xl disabled:bg-gray-400 disabled:cursor-not-allowed"
                >
                  {isSimulating ? 'Running Analysis...' : 'Find Best Stock/Bond Allocation'}
                </button>
              </div>
            </div>
          </form>

          {/* Loading Indicator */}
          {isSimulating && (
            <div className="mt-8 p-6 bg-purple-50 border-2 border-purple-200 rounded-lg text-center" role="status" aria-live="polite">
              <div className="animate-spin mx-auto w-12 h-12 border-4 border-purple-600 border-t-transparent rounded-full mb-4"></div>
              <p className="text-xl text-purple-800 font-medium">
                Running Monte Carlo simulations...
              </p>
              <p className="text-lg text-purple-700 mt-2">
                This may take a few seconds
              </p>
            </div>
          )}

          {/* Allocation Sweep Results Table */}
          {sweepResults && !isSimulating && (
            <div className="mt-8 bg-white border-4 rounded-2xl shadow-xl overflow-hidden" role="region" aria-label="Allocation Sweep Results">
              {/* Header */}
              <div className="bg-gradient-to-r from-purple-600 to-purple-700 p-8 text-white">
                <h2 className="text-3xl font-bold mb-3">
                  🎯 Portfolio Allocation Analysis
                </h2>
                <p className="text-xl opacity-90">
                  Tested {sweepResults.totalCombinations} different stock/bond allocations ({sweepResults.totalSimulations.toLocaleString()} total simulations)
                </p>
              </div>

              {/* Best Allocation Highlight */}
              <div className="p-8 bg-gradient-to-r from-green-50 to-emerald-50 border-b-4 border-green-500">
                <div className="flex items-center justify-center mb-4">
                  <span className="text-5xl mr-4">🏆</span>
                  <h3 className="text-3xl font-bold text-green-800">Best Allocation</h3>
                </div>
                <div className="text-center">
                  <p className="text-5xl font-bold text-green-700 mb-2">
                    {sweepResults.bestAllocation.stockPercent}% Stocks / {sweepResults.bestAllocation.bondPercent}% Bonds
                  </p>
                  <p className="text-3xl font-semibold text-green-600">
                    {sweepResults.bestAllocation.successRate.toFixed(1)}% Success Rate
                  </p>
                </div>
              </div>

              {/* Results Table */}
              <div className="p-8">
                <div className="overflow-x-auto">
                  <table className="w-full text-left border-collapse">
                    <thead>
                      <tr className="bg-gray-100 border-b-2 border-gray-300">
                        <th className="p-4 text-lg font-bold text-gray-700">Stocks</th>
                        <th className="p-4 text-lg font-bold text-gray-700">Bonds</th>
                        <th className="p-4 text-lg font-bold text-gray-700 text-right">Success Rate</th>
                        <th className="p-4 text-lg font-bold text-gray-700 text-right">Successes</th>
                        <th className="p-4 text-lg font-bold text-gray-700 text-right">Failures</th>
                        <th className="p-4 text-lg font-bold text-gray-700 text-right">Median Years to Failure</th>
                        <th className="p-4 text-lg font-bold text-gray-700 text-right">Avg Final Portfolio</th>
                      </tr>
                    </thead>
                    <tbody>
                      {sweepResults.allocations.map((alloc, idx) => {
                        const isBest = alloc.stockPercent === sweepResults.bestAllocation.stockPercent;
                        const successRateColor =
                          alloc.successRate >= 90 ? 'text-green-700 font-bold' :
                          alloc.successRate >= 75 ? 'text-yellow-700 font-semibold' :
                          'text-red-700';

                        return (
                          <tr
                            key={idx}
                            className={`border-b border-gray-200 hover:bg-gray-50 transition-colors ${
                              isBest ? 'bg-green-100 border-l-4 border-green-500' : ''
                            }`}
                          >
                            <td className="p-4 text-lg font-semibold">
                              {isBest && <span className="mr-2">🏆</span>}
                              {alloc.stockPercent}%
                            </td>
                            <td className="p-4 text-lg">{alloc.bondPercent}%</td>
                            <td className={`p-4 text-xl text-right ${successRateColor}`}>
                              {alloc.successRate.toFixed(1)}%
                            </td>
                            <td className="p-4 text-lg text-right text-green-600">{alloc.successes}</td>
                            <td className="p-4 text-lg text-right text-red-600">{alloc.failures}</td>
                            <td className="p-4 text-lg text-right text-orange-700 font-semibold">
                              {alloc.medianYearsToFailure !== null ? `${alloc.medianYearsToFailure.toFixed(1)} yrs` : 'N/A'}
                            </td>
                            <td className="p-4 text-lg text-right font-mono">
                              ${alloc.avgFinalPortfolio.toLocaleString('en-US', { maximumFractionDigits: 0 })}
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>

                {/* Methodology */}
                <div className="mt-8 p-6 bg-gray-100 rounded-lg text-sm text-gray-700">
                  <p className="font-semibold mb-2">📊 Methodology:</p>
                  <ul className="list-disc list-inside space-y-1">
                    <li>{sweepResults.simulationsPerCombination} Monte Carlo simulations per allocation using historical bootstrap (1988-2024)</li>
                    <li>Total of {sweepResults.totalSimulations.toLocaleString()} simulations across {sweepResults.totalCombinations} different allocations</li>
                    <li>S&P 500 for stocks, 5-Year Treasury for bonds</li>
                    <li>Inflation: {formData.inflationRate ? `Fixed at ${formData.inflationRate}%` : 'Historical bootstrap'}</li>
                    <li>Withdrawals adjusted annually for inflation</li>
                    <li>No portfolio rebalancing</li>
                  </ul>
                </div>

                {/* Run Again Button */}
                <div className="mt-8 text-center">
                  <button
                    onClick={() => {
                      setSweepResults(null);
                      window.scrollTo({ top: 0, behavior: 'smooth' });
                    }}
                    className="px-8 py-4 text-xl font-semibold text-purple-600 bg-white border-2 border-purple-600 rounded-lg hover:bg-purple-50 focus:outline-none focus:ring-4 focus:ring-purple-500 focus:ring-offset-2 transition-colors"
                  >
                    Adjust Parameters & Run Again
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Text-to-speech indicator */}
          {isSpeaking && (
            <div className="mt-6 p-4 bg-blue-50 border-2 border-blue-200 rounded-lg text-center" role="status" aria-live="polite">
              <p className="text-lg text-blue-800 font-medium">
                🔊 Reading aloud...
              </p>
            </div>
          )}

          {/* Voice input indicator */}
          {isListening && (
            <div className="mt-6 p-4 bg-red-50 border-2 border-red-200 rounded-lg text-center" role="status" aria-live="polite">
              <p className="text-lg text-red-800 font-medium">
                🎤 Listening... Speak your answer now
              </p>
            </div>
          )}
        </div>

        {/* Help Text Footer */}
        <div className="mt-8 text-center text-gray-600">
          <p className="text-lg">
            💡 <strong>Hear questions:</strong> Click the 🔊 icon to listen
          </p>
          <p className="text-lg mt-2">
            🎤 <strong>Speak answers:</strong> Click the green microphone button and say a number
          </p>
          <p className="text-lg mt-2">
            ⌨️ <strong>Keyboard:</strong> Use Tab to navigate and Enter to submit
          </p>
        </div>
      </div>
    </div>
  );
}
