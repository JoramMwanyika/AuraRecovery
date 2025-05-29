"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import {
  Heart,
  Eye,
  EyeOff,
  ArrowLeft,
  ArrowRight,
  Shield,
  Globe,
  Users,
  Mail,
  Lock,
  Moon,
  Sun,
  User,
  Calendar,
  MapPin,
  Languages,
  Brain,
  Target,
} from "lucide-react"
import Link from "next/link"
import { useState, useEffect } from "react"

export default function GetStartedPage() {
  const [currentStep, setCurrentStep] = useState(1)
  const [showPassword, setShowPassword] = useState(false)
  const [isDarkMode, setIsDarkMode] = useState(false)
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    password: "",
    confirmPassword: "",
    dateOfBirth: "",
    country: "",
    language: "",
    userType: "",
    recoveryGoals: [],
    agreeToTerms: false,
    agreeToPrivacy: false,
  })

  useEffect(() => {
    const savedTheme = localStorage.getItem("theme")
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches

    if (savedTheme === "dark" || (!savedTheme && prefersDark)) {
      setIsDarkMode(true)
      document.documentElement.classList.add("dark")
    }
  }, [])

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode)
    if (!isDarkMode) {
      document.documentElement.classList.add("dark")
      localStorage.setItem("theme", "dark")
    } else {
      document.documentElement.classList.remove("dark")
      localStorage.setItem("theme", "light")
    }
  }

  const handleInputChange = (field: string, value: any) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  const nextStep = () => {
    if (currentStep < 4) setCurrentStep(currentStep + 1)
  }

  const prevStep = () => {
    if (currentStep > 1) setCurrentStep(currentStep - 1)
  }

  const steps = [
    { number: 1, title: "Personal Info", icon: User },
    { number: 2, title: "Account Setup", icon: Shield },
    { number: 3, title: "Preferences", icon: Globe },
    { number: 4, title: "Recovery Goals", icon: Target },
  ]

  return (
    <div className="min-h-screen bg-[#F5F5F5] dark:bg-gray-900 transition-colors duration-300">
      {/* Header */}
      <header className="bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl shadow-sm border-b border-gray-200/20 dark:border-gray-700/20">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center space-x-3">
            <ArrowLeft className="w-5 h-5 text-gray-600 dark:text-gray-300" />
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-[#4A90E2] rounded-lg flex items-center justify-center shadow-lg">
                <Heart className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-[#333333] dark:text-white">AuraRecovery</span>
            </div>
          </Link>

          <div className="flex items-center space-x-4">
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleDarkMode}
              className="w-10 h-10 rounded-full bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700"
            >
              {isDarkMode ? <Sun className="w-5 h-5 text-yellow-500" /> : <Moon className="w-5 h-5 text-gray-600" />}
            </Button>
            <Link href="/login">
              <Button variant="outline" className="border-[#4A90E2] text-[#4A90E2] hover:bg-[#4A90E2]/10">
                Sign In
              </Button>
            </Link>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Progress Header */}
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-[#333333] dark:text-white mb-2">Start Your Recovery Journey</h1>
            <p className="text-gray-600 dark:text-gray-300">
              Join thousands who have found hope and healing with AuraRecovery
            </p>
          </div>

          {/* Progress Steps */}
          <div className="mb-8">
            <div className="flex items-center justify-between max-w-2xl mx-auto">
              {steps.map((step, index) => (
                <div key={step.number} className="flex items-center">
                  <div className="flex flex-col items-center">
                    <div
                      className={`w-12 h-12 rounded-full flex items-center justify-center border-2 transition-all duration-300 ${
                        currentStep >= step.number
                          ? "bg-[#4A90E2] border-[#4A90E2] text-white"
                          : "bg-white dark:bg-gray-800 border-gray-300 dark:border-gray-600 text-gray-400"
                      }`}
                    >
                      <step.icon className="w-5 h-5" />
                    </div>
                    <span
                      className={`text-xs mt-2 font-medium ${
                        currentStep >= step.number
                          ? "text-[#4A90E2] dark:text-[#4A90E2]"
                          : "text-gray-400 dark:text-gray-500"
                      }`}
                    >
                      {step.title}
                    </span>
                  </div>
                  {index < steps.length - 1 && (
                    <div
                      className={`w-16 h-0.5 mx-4 transition-all duration-300 ${
                        currentStep > step.number ? "bg-[#4A90E2]" : "bg-gray-300 dark:bg-gray-600"
                      }`}
                    />
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Form Card */}
          <Card className="border border-gray-200 dark:border-gray-700 shadow-xl bg-white dark:bg-gray-800 max-w-2xl mx-auto">
            <CardHeader>
              <CardTitle className="text-2xl text-center text-[#333333] dark:text-white">
                {steps[currentStep - 1].title}
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Step 1: Personal Information */}
              {currentStep === 1 && (
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="firstName" className="text-[#333333] dark:text-gray-200">
                        First Name
                      </Label>
                      <Input
                        id="firstName"
                        placeholder="Enter your first name"
                        value={formData.firstName}
                        onChange={(e) => handleInputChange("firstName", e.target.value)}
                        className="border-gray-300 dark:border-gray-600 focus:border-[#4A90E2] focus:ring-[#4A90E2] bg-white dark:bg-gray-700"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="lastName" className="text-[#333333] dark:text-gray-200">
                        Last Name
                      </Label>
                      <Input
                        id="lastName"
                        placeholder="Enter your last name"
                        value={formData.lastName}
                        onChange={(e) => handleInputChange("lastName", e.target.value)}
                        className="border-gray-300 dark:border-gray-600 focus:border-[#4A90E2] focus:ring-[#4A90E2] bg-white dark:bg-gray-700"
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="dateOfBirth" className="text-[#333333] dark:text-gray-200">
                      Date of Birth
                    </Label>
                    <div className="relative">
                      <Calendar className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                      <Input
                        id="dateOfBirth"
                        type="date"
                        value={formData.dateOfBirth}
                        onChange={(e) => handleInputChange("dateOfBirth", e.target.value)}
                        className="pl-10 border-gray-300 dark:border-gray-600 focus:border-[#4A90E2] focus:ring-[#4A90E2] bg-white dark:bg-gray-700"
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label className="text-[#333333] dark:text-gray-200">I am a:</Label>
                    <RadioGroup
                      value={formData.userType}
                      onValueChange={(value) => handleInputChange("userType", value)}
                      className="grid grid-cols-3 gap-4"
                    >
                      <div className="flex items-center space-x-2">
                        <RadioGroupItem
                          value="individual"
                          id="individual"
                          className="border-gray-300 dark:border-gray-600 text-[#4A90E2]"
                        />
                        <Label htmlFor="individual" className="text-sm text-[#333333] dark:text-gray-200">
                          Individual
                        </Label>
                      </div>
                      <div className="flex items-center space-x-2">
                        <RadioGroupItem
                          value="caregiver"
                          id="caregiver"
                          className="border-gray-300 dark:border-gray-600 text-[#4A90E2]"
                        />
                        <Label htmlFor="caregiver" className="text-sm text-[#333333] dark:text-gray-200">
                          Caregiver
                        </Label>
                      </div>
                      <div className="flex items-center space-x-2">
                        <RadioGroupItem
                          value="therapist"
                          id="therapist"
                          className="border-gray-300 dark:border-gray-600 text-[#4A90E2]"
                        />
                        <Label htmlFor="therapist" className="text-sm text-[#333333] dark:text-gray-200">
                          Therapist
                        </Label>
                      </div>
                    </RadioGroup>
                  </div>
                </div>
              )}

              {/* Step 2: Account Setup */}
              {currentStep === 2 && (
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="email" className="text-[#333333] dark:text-gray-200">
                      Email Address
                    </Label>
                    <div className="relative">
                      <Mail className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                      <Input
                        id="email"
                        type="email"
                        placeholder="Enter your email"
                        value={formData.email}
                        onChange={(e) => handleInputChange("email", e.target.value)}
                        className="pl-10 border-gray-300 dark:border-gray-600 focus:border-[#4A90E2] focus:ring-[#4A90E2] bg-white dark:bg-gray-700"
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="password" className="text-[#333333] dark:text-gray-200">
                      Password
                    </Label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                      <Input
                        id="password"
                        type={showPassword ? "text" : "password"}
                        placeholder="Create a strong password"
                        value={formData.password}
                        onChange={(e) => handleInputChange("password", e.target.value)}
                        className="pl-10 pr-10 border-gray-300 dark:border-gray-600 focus:border-[#4A90E2] focus:ring-[#4A90E2] bg-white dark:bg-gray-700"
                      />
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                        onClick={() => setShowPassword(!showPassword)}
                      >
                        {showPassword ? (
                          <EyeOff className="h-4 w-4 text-gray-400" />
                        ) : (
                          <Eye className="h-4 w-4 text-gray-400" />
                        )}
                      </Button>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="confirmPassword" className="text-[#333333] dark:text-gray-200">
                      Confirm Password
                    </Label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                      <Input
                        id="confirmPassword"
                        type="password"
                        placeholder="Confirm your password"
                        value={formData.confirmPassword}
                        onChange={(e) => handleInputChange("confirmPassword", e.target.value)}
                        className="pl-10 border-gray-300 dark:border-gray-600 focus:border-[#4A90E2] focus:ring-[#4A90E2] bg-white dark:bg-gray-700"
                      />
                    </div>
                  </div>

                  <div className="bg-[#A8E6CF]/10 dark:bg-[#A8E6CF]/5 border border-[#A8E6CF]/30 rounded-lg p-4">
                    <div className="flex items-start space-x-3">
                      <Shield className="w-5 h-5 text-[#A8E6CF] mt-0.5" />
                      <div>
                        <h4 className="font-medium text-[#333333] dark:text-white">Your Privacy is Protected</h4>
                        <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                          We use military-grade encryption to protect your data. Your information is never shared
                          without your consent.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Step 3: Preferences */}
              {currentStep === 3 && (
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label className="text-[#333333] dark:text-gray-200">Country/Region</Label>
                    <div className="relative">
                      <MapPin className="absolute left-3 top-3 h-4 w-4 text-gray-400 z-10" />
                      <Select value={formData.country} onValueChange={(value) => handleInputChange("country", value)}>
                        <SelectTrigger className="pl-10 border-gray-300 dark:border-gray-600 focus:border-[#4A90E2] bg-white dark:bg-gray-700">
                          <SelectValue placeholder="Select your country" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="brazil">🇧🇷 Brazil</SelectItem>
                          <SelectItem value="nigeria">🇳🇬 Nigeria</SelectItem>
                          <SelectItem value="india">🇮🇳 India</SelectItem>
                          <SelectItem value="mexico">🇲🇽 Mexico</SelectItem>
                          <SelectItem value="philippines">🇵🇭 Philippines</SelectItem>
                          <SelectItem value="other">🌍 Other</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label className="text-[#333333] dark:text-gray-200">Preferred Language</Label>
                    <div className="relative">
                      <Languages className="absolute left-3 top-3 h-4 w-4 text-gray-400 z-10" />
                      <Select value={formData.language} onValueChange={(value) => handleInputChange("language", value)}>
                        <SelectTrigger className="pl-10 border-gray-300 dark:border-gray-600 focus:border-[#4A90E2] bg-white dark:bg-gray-700">
                          <SelectValue placeholder="Select your language" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="english">English</SelectItem>
                          <SelectItem value="spanish">Español</SelectItem>
                          <SelectItem value="portuguese">Português</SelectItem>
                          <SelectItem value="hindi">हिंदी</SelectItem>
                          <SelectItem value="arabic">العربية</SelectItem>
                          <SelectItem value="french">Français</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div className="bg-[#4A90E2]/10 dark:bg-[#4A90E2]/5 border border-[#4A90E2]/30 rounded-lg p-4">
                    <div className="flex items-start space-x-3">
                      <Globe className="w-5 h-5 text-[#4A90E2] mt-0.5" />
                      <div>
                        <h4 className="font-medium text-[#333333] dark:text-white">Culturally Sensitive Support</h4>
                        <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                          Our AI understands cultural contexts and provides support that respects your background and
                          values.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Step 4: Recovery Goals */}
              {currentStep === 4 && (
                <div className="space-y-6">
                  <div className="space-y-4">
                    <Label className="text-[#333333] dark:text-gray-200 text-lg font-medium">
                      What are your recovery goals? (Select all that apply)
                    </Label>
                    <div className="grid grid-cols-1 gap-3">
                      {[
                        "Maintain sobriety",
                        "Build healthy habits",
                        "Improve mental health",
                        "Strengthen relationships",
                        "Find peer support",
                        "Access professional help",
                        "Learn coping strategies",
                        "Track progress",
                      ].map((goal) => (
                        <div key={goal} className="flex items-center space-x-3">
                          <Checkbox
                            id={goal}
                            checked={formData.recoveryGoals.includes(goal)}
                            onCheckedChange={(checked) => {
                              if (checked) {
                                handleInputChange("recoveryGoals", [...formData.recoveryGoals, goal])
                              } else {
                                handleInputChange(
                                  "recoveryGoals",
                                  formData.recoveryGoals.filter((g) => g !== goal),
                                )
                              }
                            }}
                            className="border-gray-300 dark:border-gray-600 data-[state=checked]:bg-[#4A90E2] data-[state=checked]:border-[#4A90E2]"
                          />
                          <Label htmlFor={goal} className="text-[#333333] dark:text-gray-200">
                            {goal}
                          </Label>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="space-y-4">
                    <div className="flex items-center space-x-3">
                      <Checkbox
                        id="terms"
                        checked={formData.agreeToTerms}
                        onCheckedChange={(checked) => handleInputChange("agreeToTerms", checked)}
                        className="border-gray-300 dark:border-gray-600 data-[state=checked]:bg-[#4A90E2] data-[state=checked]:border-[#4A90E2]"
                      />
                      <Label htmlFor="terms" className="text-sm text-[#333333] dark:text-gray-200">
                        I agree to the{" "}
                        <Link href="/terms" className="text-[#4A90E2] hover:underline">
                          Terms of Service
                        </Link>
                      </Label>
                    </div>
                    <div className="flex items-center space-x-3">
                      <Checkbox
                        id="privacy"
                        checked={formData.agreeToPrivacy}
                        onCheckedChange={(checked) => handleInputChange("agreeToPrivacy", checked)}
                        className="border-gray-300 dark:border-gray-600 data-[state=checked]:bg-[#4A90E2] data-[state=checked]:border-[#4A90E2]"
                      />
                      <Label htmlFor="privacy" className="text-sm text-[#333333] dark:text-gray-200">
                        I agree to the{" "}
                        <Link href="/privacy" className="text-[#4A90E2] hover:underline">
                          Privacy Policy
                        </Link>
                      </Label>
                    </div>
                  </div>

                  <div className="bg-[#A8E6CF]/10 dark:bg-[#A8E6CF]/5 border border-[#A8E6CF]/30 rounded-lg p-4">
                    <div className="flex items-start space-x-3">
                      <Brain className="w-5 h-5 text-[#A8E6CF] mt-0.5" />
                      <div>
                        <h4 className="font-medium text-[#333333] dark:text-white">Personalized AI Support</h4>
                        <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                          Based on your goals, our AI will create a personalized recovery plan that adapts to your
                          progress.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Navigation Buttons */}
              <div className="flex justify-between pt-6">
                <Button
                  variant="outline"
                  onClick={prevStep}
                  disabled={currentStep === 1}
                  className="border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-300"
                >
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  Previous
                </Button>

                {currentStep < 4 ? (
                  <Button onClick={nextStep} className="bg-[#4A90E2] hover:bg-[#3A7BC8] text-white">
                    Next
                    <ArrowRight className="w-4 h-4 ml-2" />
                  </Button>
                ) : (
                  <Button
                    className="bg-[#A8E6CF] hover:bg-[#98D6BF] text-[#333333] font-semibold"
                    disabled={!formData.agreeToTerms || !formData.agreeToPrivacy}
                  >
                    Start My Journey
                    <Heart className="w-4 h-4 ml-2" />
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Trust Indicators */}
          <div className="mt-8 text-center">
            <div className="flex items-center justify-center space-x-8 text-sm text-gray-500 dark:text-gray-400">
              <div className="flex items-center space-x-2">
                <Shield className="w-5 h-5 text-[#A8E6CF]" />
                <span>End-to-End Encrypted</span>
              </div>
              <div className="flex items-center space-x-2">
                <Users className="w-5 h-5 text-[#A8E6CF]" />
                <span>25,000+ Users Trust Us</span>
              </div>
              <div className="flex items-center space-x-2">
                <Globe className="w-5 h-5 text-[#A8E6CF]" />
                <span>40+ Countries Served</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
