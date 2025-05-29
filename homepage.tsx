"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import {
  Brain,
  Users,
  TrendingUp,
  Globe,
  Star,
  ArrowRight,
  Shield,
  Heart,
  MessageCircle,
  CheckCircle,
  Play,
  Menu,
  X,
  Moon,
  Sun,
  Sparkles,
  Zap,
  Target,
} from "lucide-react"
import Link from "next/link"
import { useState, useEffect } from "react"

export default function Component() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [isDarkMode, setIsDarkMode] = useState(false)

  useEffect(() => {
    // Check for saved theme preference or default to light mode
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

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId)
    if (element) {
      element.scrollIntoView({ behavior: "smooth" })
    }
  }

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 transition-colors duration-300">
      {/* Header */}
      <header className="fixed top-0 w-full bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl shadow-sm border-b border-gray-200/20 dark:border-gray-700/20 z-50 transition-all duration-300">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/25 dark:shadow-blue-500/40">
              <Heart className="w-6 h-6 text-white" />
            </div>
            <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
              AuraRecovery
            </span>
          </div>

          <nav className="hidden lg:flex items-center space-x-8">
            <button
              onClick={() => scrollToSection("home")}
              className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors font-medium"
            >
              Home
            </button>
            <button
              onClick={() => scrollToSection("features")}
              className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors font-medium"
            >
              Features
            </button>
            <button
              onClick={() => scrollToSection("how-it-works")}
              className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors font-medium"
            >
              How It Works
            </button>
            <button
              onClick={() => scrollToSection("testimonials")}
              className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors font-medium"
            >
              Stories
            </button>
            <Link
              href="#contact"
              className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors font-medium"
            >
              Contact
            </Link>
          </nav>

          <div className="flex items-center space-x-4">
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleDarkMode}
              className="w-10 h-10 rounded-full bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 transition-all duration-300"
            >
              {isDarkMode ? <Sun className="w-5 h-5 text-yellow-500" /> : <Moon className="w-5 h-5 text-gray-600" />}
            </Button>
            <Link href="/login">
              <Button
                variant="ghost"
                className="hidden sm:inline-flex text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400"
              >
                Sign In
              </Button>
            </Link>
            <Link href="/get-started">
              <Button className="bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 hover:from-blue-600 hover:via-purple-600 hover:to-pink-600 text-white shadow-lg shadow-blue-500/25 dark:shadow-blue-500/40 transition-all duration-300 hover:shadow-xl hover:shadow-blue-500/30">
                Get Started Free
              </Button>
            </Link>
            <Button variant="ghost" size="sm" className="lg:hidden" onClick={() => setIsMenuOpen(!isMenuOpen)}>
              {isMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </Button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="lg:hidden bg-white/95 dark:bg-gray-900/95 backdrop-blur-xl border-t border-gray-200/20 dark:border-gray-700/20">
            <nav className="container mx-auto px-4 py-4 space-y-4">
              <button
                onClick={() => scrollToSection("home")}
                className="block text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors font-medium"
              >
                Home
              </button>
              <button
                onClick={() => scrollToSection("features")}
                className="block text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors font-medium"
              >
                Features
              </button>
              <button
                onClick={() => scrollToSection("how-it-works")}
                className="block text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors font-medium"
              >
                How It Works
              </button>
              <button
                onClick={() => scrollToSection("testimonials")}
                className="block text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors font-medium"
              >
                Stories
              </button>
              <Link
                href="#contact"
                className="block text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors font-medium"
              >
                Contact
              </Link>
            </nav>
          </div>
        )}
      </header>

      {/* Hero Section */}
      <section
        id="home"
        className="pt-24 pb-20 px-4 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-blue-900/20 dark:to-purple-900/20 relative overflow-hidden transition-all duration-500"
      >
        {/* Animated Background Elements */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-blue-400/20 via-purple-400/20 to-pink-400/20 dark:from-blue-500/10 dark:via-purple-500/10 dark:to-pink-500/10 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-br from-green-400/20 via-blue-400/20 to-purple-400/20 dark:from-green-500/10 dark:via-blue-500/10 dark:to-purple-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-br from-purple-400/10 via-pink-400/10 to-blue-400/10 dark:from-purple-500/5 dark:via-pink-500/5 dark:to-blue-500/5 rounded-full blur-3xl animate-pulse delay-500"></div>
        </div>

        <div className="container mx-auto text-center max-w-6xl relative z-10">
          <Badge className="mb-8 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm text-blue-800 dark:text-blue-300 border border-blue-200/50 dark:border-blue-700/50 px-6 py-2 text-sm font-medium shadow-lg shadow-blue-500/10 dark:shadow-blue-500/20 hover:shadow-xl hover:shadow-blue-500/20 transition-all duration-300">
            <Sparkles className="w-4 h-4 mr-2" />
            Trusted by 25,000+ individuals across 40+ countries
          </Badge>

          <h1 className="text-5xl md:text-7xl font-bold text-gray-900 dark:text-white mb-8 leading-tight">
            Your Journey to{" "}
            <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent animate-pulse">
              Recovery
            </span>{" "}
            Starts Here
          </h1>

          <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-12 max-w-3xl mx-auto leading-relaxed">
            AI-powered addiction recovery support designed for emerging economies. Get personalized care, connect with
            peers, and access professional guidance—all in your language.
          </p>

          <div className="flex flex-col sm:flex-row gap-6 justify-center mb-16">
            <Link href="/get-started">
              <Button
                size="lg"
                className="bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 hover:from-blue-600 hover:via-purple-600 hover:to-pink-600 text-white px-10 py-6 text-lg font-semibold shadow-xl shadow-blue-500/25 dark:shadow-blue-500/40 hover:shadow-2xl hover:shadow-blue-500/30 transition-all duration-300 transform hover:-translate-y-1 hover:scale-105"
              >
                <Zap className="mr-3 w-6 h-6" />
                Start Your Recovery Journey
                <ArrowRight className="ml-3 w-6 h-6" />
              </Button>
            </Link>
            <Link href="/progress">
              <Button
                size="lg"
                className="bg-[#4A90E2] hover:bg-[#3A7BC8] text-white px-10 py-6 text-lg font-semibold shadow-xl shadow-blue-500/25 dark:shadow-blue-500/40 hover:shadow-2xl hover:shadow-blue-500/30 transition-all duration-300 transform hover:-translate-y-1 hover:scale-105"
              >
                <TrendingUp className="mr-3 w-6 h-6" />
                Track My Progress
                <ArrowRight className="ml-3 w-6 h-6" />
              </Button>
            </Link>
            <Link href="#features">
              <Button
                size="lg"
                variant="outline"
                className="px-10 py-6 text-lg font-semibold border-2 border-blue-200 dark:border-blue-700 text-blue-700 dark:text-blue-300 hover:bg-blue-50 dark:hover:bg-blue-900/20 hover:border-blue-300 dark:hover:border-blue-600 transition-all duration-300 backdrop-blur-sm bg-white/50 dark:bg-gray-800/50"
              >
                <Play className="mr-3 w-6 h-6" />
                Watch Demo (2 min)
              </Button>
            </Link>
          </div>

          {/* Enhanced Hero Visual */}
          <div className="relative max-w-4xl mx-auto">
            <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-xl rounded-3xl shadow-2xl shadow-blue-500/10 dark:shadow-blue-500/20 p-8 border border-gray-200/20 dark:border-gray-700/20 hover:shadow-3xl hover:shadow-blue-500/15 transition-all duration-500">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-center">
                <div className="space-y-4">
                  <div className="flex items-center space-x-3 group">
                    <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/25 group-hover:shadow-xl group-hover:shadow-blue-500/30 transition-all duration-300 group-hover:scale-110">
                      <Brain className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-800 dark:text-gray-200">AI-Powered Plans</h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Personalized for you</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3 group">
                    <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-green-600 rounded-xl flex items-center justify-center shadow-lg shadow-green-500/25 group-hover:shadow-xl group-hover:shadow-green-500/30 transition-all duration-300 group-hover:scale-110">
                      <Users className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-800 dark:text-gray-200">Peer Support</h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">24/7 community</p>
                    </div>
                  </div>
                </div>

                <div className="relative">
                  <div className="w-32 h-32 mx-auto bg-gradient-to-br from-purple-400 via-blue-500 to-green-400 rounded-full flex items-center justify-center shadow-2xl shadow-purple-500/30 dark:shadow-purple-500/40 animate-pulse">
                    <Heart className="w-16 h-16 text-white" />
                  </div>
                  <div className="absolute -top-2 -right-2 w-8 h-8 bg-green-500 rounded-full flex items-center justify-center shadow-lg shadow-green-500/30 animate-bounce">
                    <CheckCircle className="w-5 h-5 text-white" />
                  </div>
                  <div className="absolute -bottom-2 -left-2 w-6 h-6 bg-blue-500 rounded-full animate-ping"></div>
                </div>

                <div className="space-y-4">
                  <div className="flex items-center space-x-3 group">
                    <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg shadow-purple-500/25 group-hover:shadow-xl group-hover:shadow-purple-500/30 transition-all duration-300 group-hover:scale-110">
                      <Shield className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-800 dark:text-gray-200">Secure & Private</h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">End-to-end encrypted</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3 group">
                    <div className="w-12 h-12 bg-gradient-to-br from-orange-500 to-red-500 rounded-xl flex items-center justify-center shadow-lg shadow-orange-500/25 group-hover:shadow-xl group-hover:shadow-orange-500/30 transition-all duration-300 group-hover:scale-110">
                      <Globe className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-800 dark:text-gray-200">15+ Languages</h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Your native language</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Enhanced Stats Section */}
      <section className="py-16 px-4 bg-white dark:bg-gray-900 transition-colors duration-300">
        <div className="container mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            {[
              { number: "25K+", label: "Lives Transformed", icon: Heart, color: "from-red-500 to-pink-500" },
              { number: "40+", label: "Countries Served", icon: Globe, color: "from-blue-500 to-cyan-500" },
              {
                number: "15+",
                label: "Languages Supported",
                icon: MessageCircle,
                color: "from-green-500 to-emerald-500",
              },
              { number: "98%", label: "User Satisfaction", icon: Star, color: "from-yellow-500 to-orange-500" },
            ].map((stat, index) => (
              <div key={index} className="space-y-4 group">
                <div
                  className={`w-16 h-16 mx-auto bg-gradient-to-br ${stat.color} rounded-2xl flex items-center justify-center shadow-lg group-hover:shadow-xl transition-all duration-300 group-hover:scale-110`}
                >
                  <stat.icon className="w-8 h-8 text-white" />
                </div>
                <div className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                  {stat.number}
                </div>
                <div className="text-gray-600 dark:text-gray-400 font-medium">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Enhanced Features Section */}
      <section
        id="features"
        className="py-24 px-4 bg-gradient-to-br from-gray-50 via-blue-50 to-purple-50 dark:from-gray-900 dark:via-blue-900/10 dark:to-purple-900/10 transition-all duration-500"
      >
        <div className="container mx-auto">
          <div className="text-center mb-20">
            <Badge className="mb-6 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm text-blue-800 dark:text-blue-300 border border-blue-200/50 dark:border-blue-700/50 shadow-lg">
              <Target className="w-4 h-4 mr-2" />
              Comprehensive Recovery Platform
            </Badge>
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-6">
              Everything You Need for{" "}
              <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                Lasting Recovery
              </span>
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Our platform combines cutting-edge AI technology with human compassion to provide comprehensive support
              tailored to your unique journey.
            </p>
          </div>

          <div className="grid lg:grid-cols-2 gap-12 items-center mb-20">
            <div className="space-y-8">
              <div className="flex items-start space-x-4 group">
                <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center shadow-lg shadow-blue-500/25 dark:shadow-blue-500/40 flex-shrink-0 group-hover:shadow-xl group-hover:shadow-blue-500/30 transition-all duration-300 group-hover:scale-110">
                  <Brain className="w-8 h-8 text-white" />
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">AI-Powered Recovery Plans</h3>
                  <p className="text-gray-600 dark:text-gray-300 text-lg leading-relaxed">
                    Our advanced AI analyzes your unique situation, cultural background, and personal preferences to
                    create a customized recovery roadmap that evolves with your progress.
                  </p>
                </div>
              </div>

              <div className="flex items-start space-x-4 group">
                <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-green-600 rounded-2xl flex items-center justify-center shadow-lg shadow-green-500/25 dark:shadow-green-500/40 flex-shrink-0 group-hover:shadow-xl group-hover:shadow-green-500/30 transition-all duration-300 group-hover:scale-110">
                  <TrendingUp className="w-8 h-8 text-white" />
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">Smart Progress Tracking</h3>
                  <p className="text-gray-600 dark:text-gray-300 text-lg leading-relaxed">
                    Visualize your journey with intelligent analytics, mood tracking, and milestone celebrations that
                    keep you motivated and on track.
                  </p>
                </div>
              </div>
            </div>

            <div className="relative">
              <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-xl rounded-3xl shadow-2xl shadow-blue-500/10 dark:shadow-blue-500/20 p-8 border border-gray-200/20 dark:border-gray-700/20 hover:shadow-3xl hover:shadow-blue-500/15 transition-all duration-500">
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <h4 className="font-semibold text-gray-800 dark:text-gray-200">Today's Progress</h4>
                    <Badge className="bg-gradient-to-r from-green-500 to-green-600 text-white shadow-lg">Day 47</Badge>
                  </div>
                  <div className="space-y-4">
                    <div className="flex items-center space-x-3 group">
                      <CheckCircle className="w-5 h-5 text-green-500 group-hover:scale-110 transition-transform duration-200" />
                      <span className="text-gray-700 dark:text-gray-300">Morning meditation completed</span>
                    </div>
                    <div className="flex items-center space-x-3 group">
                      <CheckCircle className="w-5 h-5 text-green-500 group-hover:scale-110 transition-transform duration-200" />
                      <span className="text-gray-700 dark:text-gray-300">Peer support session attended</span>
                    </div>
                    <div className="flex items-center space-x-3 group">
                      <div className="w-5 h-5 border-2 border-gray-300 dark:border-gray-600 rounded-full group-hover:border-blue-500 transition-colors duration-200"></div>
                      <span className="text-gray-500 dark:text-gray-400">Evening reflection journal</span>
                    </div>
                  </div>
                  <div className="bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 h-3 rounded-full shadow-lg">
                    <div className="bg-gradient-to-r from-green-400 to-green-500 h-3 rounded-full w-2/3 shadow-lg animate-pulse"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="order-2 lg:order-1 relative">
              <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-xl rounded-3xl shadow-2xl shadow-purple-500/10 dark:shadow-purple-500/20 p-8 border border-gray-200/20 dark:border-gray-700/20 hover:shadow-3xl hover:shadow-purple-500/15 transition-all duration-500">
                <div className="space-y-6">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center shadow-lg">
                      <Users className="w-5 h-5 text-white" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-800 dark:text-gray-200">Recovery Support Group</h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400 flex items-center">
                        <div className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></div>
                        12 members online
                      </p>
                    </div>
                  </div>
                  <div className="space-y-3">
                    <div className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-3 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-200">
                      <p className="text-sm text-gray-700 dark:text-gray-300">
                        "Just completed my 30-day milestone! 🎉"
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Maria - São Paulo</p>
                    </div>
                    <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-3 hover:bg-blue-100 dark:hover:bg-blue-900/30 transition-colors duration-200">
                      <p className="text-sm text-gray-700 dark:text-gray-300">
                        "The meditation exercises really help with cravings"
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">James - Lagos</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="order-1 lg:order-2 space-y-8">
              <div className="flex items-start space-x-4 group">
                <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg shadow-purple-500/25 dark:shadow-purple-500/40 flex-shrink-0 group-hover:shadow-xl group-hover:shadow-purple-500/30 transition-all duration-300 group-hover:scale-110">
                  <Users className="w-8 h-8 text-white" />
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">Global Peer Community</h3>
                  <p className="text-gray-600 dark:text-gray-300 text-lg leading-relaxed">
                    Connect with others who understand your journey. Join support groups, share experiences, and build
                    lasting friendships in a safe, moderated environment.
                  </p>
                </div>
              </div>

              <div className="flex items-start space-x-4 group">
                <div className="w-16 h-16 bg-gradient-to-br from-orange-500 to-red-500 rounded-2xl flex items-center justify-center shadow-lg shadow-orange-500/25 dark:shadow-orange-500/40 flex-shrink-0 group-hover:shadow-xl group-hover:shadow-orange-500/30 transition-all duration-300 group-hover:scale-110">
                  <Globe className="w-8 h-8 text-white" />
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">Culturally Sensitive Care</h3>
                  <p className="text-gray-600 dark:text-gray-300 text-lg leading-relaxed">
                    Access resources and support that respect your cultural values and traditions, available in 15+
                    languages with local context and understanding.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Enhanced How It Works */}
      <section id="how-it-works" className="py-24 px-4 bg-white dark:bg-gray-900 transition-colors duration-300">
        <div className="container mx-auto">
          <div className="text-center mb-20">
            <Badge className="mb-6 bg-gradient-to-r from-purple-100 to-blue-100 dark:from-purple-900/50 dark:to-blue-900/50 text-purple-800 dark:text-purple-300 border border-purple-200/50 dark:border-purple-700/50 shadow-lg">
              <Sparkles className="w-4 h-4 mr-2" />
              Simple & Effective Process
            </Badge>
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-6">
              Your Recovery Journey in{" "}
              <span className="bg-gradient-to-r from-purple-600 via-blue-600 to-green-600 bg-clip-text text-transparent">
                4 Simple Steps
              </span>
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              We've designed our platform to be intuitive and supportive, guiding you through each step of your recovery
              journey.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                step: "1",
                title: "Secure Registration",
                desc: "Create your private account with military-grade encryption. Your privacy and safety are our top priorities.",
                icon: Shield,
                color: "from-blue-500 to-blue-600",
                shadowColor: "shadow-blue-500/25",
              },
              {
                step: "2",
                title: "Personal Assessment",
                desc: "Complete a comprehensive, culturally-sensitive assessment that helps us understand your unique situation.",
                icon: Brain,
                color: "from-purple-500 to-purple-600",
                shadowColor: "shadow-purple-500/25",
              },
              {
                step: "3",
                title: "Custom Recovery Plan",
                desc: "Receive your AI-generated, personalized recovery roadmap with daily goals and adaptive strategies.",
                icon: TrendingUp,
                color: "from-green-500 to-green-600",
                shadowColor: "shadow-green-500/25",
              },
              {
                step: "4",
                title: "Connect & Thrive",
                desc: "Join support groups, access professional guidance, and celebrate milestones with your community.",
                icon: Users,
                color: "from-orange-500 to-red-500",
                shadowColor: "shadow-orange-500/25",
              },
            ].map((item, index) => (
              <div key={index} className="text-center group">
                <div className="relative mb-8">
                  <div
                    className={`w-20 h-20 bg-gradient-to-br ${item.color} rounded-3xl flex items-center justify-center mx-auto shadow-xl ${item.shadowColor} dark:${item.shadowColor.replace("/25", "/40")} group-hover:shadow-2xl group-hover:${item.shadowColor.replace("/25", "/30")} transition-all duration-300 transform group-hover:-translate-y-2 group-hover:scale-110`}
                  >
                    <item.icon className="w-10 h-10 text-white" />
                  </div>
                  <div className="absolute -top-2 -right-2 w-8 h-8 bg-white dark:bg-gray-800 border-4 border-gray-100 dark:border-gray-700 rounded-full flex items-center justify-center shadow-lg">
                    <span className="text-sm font-bold text-gray-700 dark:text-gray-300">{item.step}</span>
                  </div>
                </div>
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">{item.title}</h3>
                <p className="text-gray-600 dark:text-gray-300 leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Enhanced Testimonials */}
      <section
        id="testimonials"
        className="py-24 px-4 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-blue-900/10 dark:to-purple-900/10 transition-all duration-500"
      >
        <div className="container mx-auto">
          <div className="text-center mb-20">
            <Badge className="mb-6 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm text-green-800 dark:text-green-300 border border-green-200/50 dark:border-green-700/50 shadow-lg">
              <Heart className="w-4 h-4 mr-2" />
              Real Stories, Real Impact
            </Badge>
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-6">
              Stories of{" "}
              <span className="bg-gradient-to-r from-green-600 via-blue-600 to-purple-600 bg-clip-text text-transparent">
                Hope & Healing
              </span>
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Hear from real people whose lives have been transformed through our platform. Their journeys inspire us
              every day.
            </p>
          </div>

          <div className="grid lg:grid-cols-3 gap-8">
            {[
              {
                name: "Maria Santos",
                location: "São Paulo, Brazil",
                role: "8 months in recovery",
                quote:
                  "AuraRecovery understood my cultural background in ways traditional resources couldn't. The AI coach felt like it truly knew me, and the Portuguese support group became my second family.",
                flag: "🇧🇷",
                rating: 5,
                gradient: "from-green-500 to-blue-500",
              },
              {
                name: "James Okafor",
                location: "Lagos, Nigeria",
                role: "Father & Caregiver",
                quote:
                  "When my son struggled with addiction, AuraRecovery helped our entire family understand and heal together. The family support resources were life-changing.",
                flag: "🇳🇬",
                rating: 5,
                gradient: "from-blue-500 to-purple-500",
              },
              {
                name: "Dr. Priya Sharma",
                location: "Mumbai, India",
                role: "Licensed Therapist",
                quote:
                  "I use AuraRecovery to extend my practice to underserved communities. The cultural sensitivity and multilingual support are unmatched in the industry.",
                flag: "🇮🇳",
                rating: 5,
                gradient: "from-purple-500 to-pink-500",
              },
            ].map((testimonial, index) => (
              <Card
                key={index}
                className="border-0 shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 bg-white/80 dark:bg-gray-800/80 backdrop-blur-xl border border-gray-200/20 dark:border-gray-700/20 group"
              >
                <CardContent className="p-8">
                  <div className="flex items-center mb-6">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star
                        key={i}
                        className="w-5 h-5 fill-yellow-400 text-yellow-400 group-hover:scale-110 transition-transform duration-200"
                        style={{ transitionDelay: `${i * 100}ms` }}
                      />
                    ))}
                  </div>
                  <blockquote className="text-gray-700 dark:text-gray-300 mb-8 text-lg leading-relaxed italic">
                    "{testimonial.quote}"
                  </blockquote>
                  <div className="flex items-center">
                    <div
                      className={`w-16 h-16 bg-gradient-to-br ${testimonial.gradient} rounded-full flex items-center justify-center mr-4 text-2xl shadow-lg group-hover:shadow-xl group-hover:scale-110 transition-all duration-300`}
                    >
                      {testimonial.flag}
                    </div>
                    <div>
                      <p className="font-bold text-gray-900 dark:text-white text-lg">{testimonial.name}</p>
                      <p className="text-gray-600 dark:text-gray-400">{testimonial.location}</p>
                      <p className="text-blue-600 dark:text-blue-400 font-medium">{testimonial.role}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Enhanced CTA Section */}
      <section className="py-24 px-4 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 relative overflow-hidden">
        <div className="absolute inset-0 bg-black/10"></div>
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-white/10 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-white/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
        </div>
        <div className="container mx-auto text-center relative z-10">
          <h2 className="text-4xl md:text-6xl font-bold text-white mb-8 leading-tight">
            Ready to Transform Your Life?
          </h2>
          <p className="text-xl md:text-2xl text-blue-100 mb-12 max-w-3xl mx-auto leading-relaxed">
            Join thousands of individuals who have found hope, healing, and lasting recovery through AuraRecovery. Your
            journey to a better life starts with a single step.
          </p>
          <div className="flex flex-col sm:flex-row gap-6 justify-center">
            <Link href="/get-started">
              <Button
                size="lg"
                className="bg-white text-blue-600 hover:bg-gray-100 px-10 py-6 text-lg font-bold shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1 hover:scale-105"
              >
                <Zap className="mr-3 w-6 h-6" />
                Start Your Recovery Journey
                <ArrowRight className="ml-3 w-6 h-6" />
              </Button>
            </Link>
            <Link href="/progress">
              <Button
                size="lg"
                variant="outline"
                className="border-2 border-white text-white hover:bg-white hover:text-blue-600 px-10 py-6 text-lg font-bold transition-all duration-300 backdrop-blur-sm bg-white/10"
              >
                <TrendingUp className="mr-3 w-6 h-6" />
                Track My Progress
              </Button>
            </Link>
          </div>
          <p className="text-blue-200 mt-8 text-lg flex items-center justify-center flex-wrap gap-4">
            <span className="flex items-center">
              <CheckCircle className="w-5 h-5 mr-2" />
              Free to start
            </span>
            <span className="flex items-center">
              <CheckCircle className="w-5 h-5 mr-2" />
              No credit card required
            </span>
            <span className="flex items-center">
              <CheckCircle className="w-5 h-5 mr-2" />
              Complete privacy guaranteed
            </span>
          </p>
        </div>
      </section>

      {/* Enhanced Footer */}
      <footer className="bg-gray-900 dark:bg-black text-white py-16 px-4 transition-colors duration-300">
        <div className="container mx-auto">
          <div className="grid md:grid-cols-2 lg:grid-cols-5 gap-8">
            <div className="lg:col-span-2">
              <div className="flex items-center space-x-3 mb-6">
                <div className="w-12 h-12 bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/25">
                  <Heart className="w-7 h-7 text-white" />
                </div>
                <span className="text-2xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                  AuraRecovery
                </span>
              </div>
              <p className="text-gray-400 mb-6 text-lg leading-relaxed max-w-md">
                Empowering recovery through technology, compassion, and community. Together, we're building a world
                where everyone has access to quality addiction recovery support.
              </p>
              <div className="flex space-x-4">
                <div className="w-10 h-10 bg-gray-800 dark:bg-gray-700 rounded-lg flex items-center justify-center hover:bg-gray-700 dark:hover:bg-gray-600 cursor-pointer transition-all duration-300 hover:scale-110">
                  <MessageCircle className="w-5 h-5 text-gray-400 hover:text-white" />
                </div>
                <div className="w-10 h-10 bg-gray-800 dark:bg-gray-700 rounded-lg flex items-center justify-center hover:bg-gray-700 dark:hover:bg-gray-600 cursor-pointer transition-all duration-300 hover:scale-110">
                  <Globe className="w-5 h-5 text-gray-400 hover:text-white" />
                </div>
                <div className="w-10 h-10 bg-gray-800 dark:bg-gray-700 rounded-lg flex items-center justify-center hover:bg-gray-700 dark:hover:bg-gray-600 cursor-pointer transition-all duration-300 hover:scale-110">
                  <Users className="w-5 h-5 text-gray-400 hover:text-white" />
                </div>
              </div>
            </div>

            <div>
              <h4 className="font-bold mb-6 text-lg">Platform</h4>
              <ul className="space-y-3 text-gray-400">
                <li>
                  <Link href="#" className="hover:text-white transition-colors hover:translate-x-1 inline-block">
                    Features
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors hover:translate-x-1 inline-block">
                    How It Works
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors hover:translate-x-1 inline-block">
                    Pricing
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors hover:translate-x-1 inline-block">
                    Mobile App
                  </Link>
                </li>
              </ul>
            </div>

            <div>
              <h4 className="font-bold mb-6 text-lg">Support</h4>
              <ul className="space-y-3 text-gray-400">
                <li>
                  <Link href="#" className="hover:text-white transition-colors hover:translate-x-1 inline-block">
                    Help Center
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors hover:translate-x-1 inline-block">
                    Crisis Resources
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors hover:translate-x-1 inline-block">
                    Community Guidelines
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors hover:translate-x-1 inline-block">
                    Contact Support
                  </Link>
                </li>
              </ul>
            </div>

            <div>
              <h4 className="font-bold mb-6 text-lg">Legal</h4>
              <ul className="space-y-3 text-gray-400">
                <li>
                  <Link href="#" className="hover:text-white transition-colors hover:translate-x-1 inline-block">
                    Privacy Policy
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors hover:translate-x-1 inline-block">
                    Terms of Service
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors hover:translate-x-1 inline-block">
                    Cookie Policy
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors hover:translate-x-1 inline-block">
                    Accessibility
                  </Link>
                </li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 dark:border-gray-700 mt-12 pt-8">
            <div className="flex flex-col md:flex-row justify-between items-center">
              <p className="text-gray-400 mb-4 md:mb-0">
                © 2024 AuraRecovery. All rights reserved. Made with ❤️ for global communities.
              </p>
              <div className="flex items-center space-x-4">
                <span className="text-gray-400">Available in:</span>
                <select className="bg-gray-800 dark:bg-gray-700 text-white rounded-lg px-3 py-2 border border-gray-700 dark:border-gray-600 focus:border-blue-500 focus:outline-none transition-colors duration-200">
                  <option>🇺🇸 English</option>
                  <option>🇪🇸 Español</option>
                  <option>🇧🇷 Português</option>
                  <option>🇮🇳 हिंदी</option>
                  <option>🇸🇦 العربية</option>
                  <option>🇫🇷 Français</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
