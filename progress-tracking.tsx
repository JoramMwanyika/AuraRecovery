"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Calendar } from "@/components/ui/calendar"
import { Textarea } from "@/components/ui/textarea"
import {
  Heart,
  TrendingUp,
  CalendarIcon,
  Target,
  Award,
  Smile,
  Frown,
  Meh,
  Sun,
  Moon,
  ArrowLeft,
  Plus,
  CheckCircle,
  Clock,
  BarChart3,
  PieChart,
  Activity,
  Zap,
  Users,
  BookOpen,
  Star,
  Trophy,
  Flame,
  Brain,
  Shield,
} from "lucide-react"
import Link from "next/link"
import { useState, useEffect } from "react"

export default function ProgressTrackingPage() {
  const [isDarkMode, setIsDarkMode] = useState(false)
  const [selectedDate, setSelectedDate] = useState<Date | undefined>(new Date())
  const [currentMood, setCurrentMood] = useState("")
  const [journalEntry, setJournalEntry] = useState("")
  const [activeTab, setActiveTab] = useState("overview")

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

  const moodOptions = [
    {
      value: "excellent",
      label: "Excellent",
      icon: Smile,
      color: "text-green-500",
      bg: "bg-green-100 dark:bg-green-900/20",
    },
    { value: "good", label: "Good", icon: Smile, color: "text-[#A8E6CF]", bg: "bg-[#A8E6CF]/20" },
    {
      value: "neutral",
      label: "Neutral",
      icon: Meh,
      color: "text-yellow-500",
      bg: "bg-yellow-100 dark:bg-yellow-900/20",
    },
    { value: "low", label: "Low", icon: Frown, color: "text-orange-500", bg: "bg-orange-100 dark:bg-orange-900/20" },
    {
      value: "struggling",
      label: "Struggling",
      icon: Frown,
      color: "text-red-500",
      bg: "bg-red-100 dark:bg-red-900/20",
    },
  ]

  const dailyGoals = [
    { id: 1, title: "Morning meditation", completed: true, time: "8:00 AM" },
    { id: 2, title: "Peer support check-in", completed: true, time: "2:00 PM" },
    { id: 3, title: "Evening reflection journal", completed: false, time: "8:00 PM" },
    { id: 4, title: "Gratitude practice", completed: false, time: "9:00 PM" },
  ]

  const weeklyStats = [
    { label: "Days Sober", value: 47, target: 50, color: "[#4A90E2]" },
    { label: "Goals Completed", value: 85, target: 100, color: "[#A8E6CF]" },
    { label: "Support Sessions", value: 12, target: 15, color: "purple-500" },
    { label: "Journal Entries", value: 28, target: 30, color: "orange-500" },
  ]

  const milestones = [
    { title: "7 Days Sober", date: "2 weeks ago", achieved: true, icon: Trophy },
    { title: "30 Days Sober", date: "3 days ago", achieved: true, icon: Award },
    { title: "First Support Group", date: "1 week ago", achieved: true, icon: Users },
    { title: "60 Days Sober", date: "In 13 days", achieved: false, icon: Target },
  ]

  const moodHistory = [
    { date: "Mon", mood: "good" },
    { date: "Tue", mood: "excellent" },
    { date: "Wed", mood: "neutral" },
    { date: "Thu", mood: "good" },
    { date: "Fri", mood: "excellent" },
    { date: "Sat", mood: "good" },
    { date: "Sun", mood: "excellent" },
  ]

  return (
    <div className="min-h-screen bg-[#F5F5F5] dark:bg-gray-900 transition-colors duration-300">
      {/* Header */}
      <header className="bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl shadow-sm border-b border-gray-200/20 dark:border-gray-700/20">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Link
              href="/"
              className="flex items-center space-x-2 text-gray-600 dark:text-gray-300 hover:text-[#4A90E2] transition-colors"
            >
              <ArrowLeft className="w-5 h-5" />
              <span>Back to Dashboard</span>
            </Link>
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-[#4A90E2] rounded-lg flex items-center justify-center shadow-lg">
                <Heart className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-[#333333] dark:text-white">AuraRecovery</span>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleDarkMode}
              className="w-10 h-10 rounded-full bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700"
            >
              {isDarkMode ? <Sun className="w-5 h-5 text-yellow-500" /> : <Moon className="w-5 h-5 text-gray-600" />}
            </Button>
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-[#A8E6CF] rounded-full flex items-center justify-center">
                <span className="text-sm font-bold text-[#333333]">MS</span>
              </div>
              <span className="text-sm font-medium text-[#333333] dark:text-white">Maria Santos</span>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold text-[#333333] dark:text-white mb-2">Progress Tracking</h1>
              <p className="text-gray-600 dark:text-gray-300">
                Monitor your recovery journey and celebrate your achievements
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <Badge className="bg-[#A8E6CF] text-[#333333] px-4 py-2 text-lg font-semibold">
                <Flame className="w-5 h-5 mr-2" />
                Day 47 Streak
              </Badge>
            </div>
          </div>
        </div>

        {/* Quick Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {weeklyStats.map((stat, index) => (
            <Card
              key={index}
              className="border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:shadow-lg transition-all duration-300"
            >
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">{stat.label}</h3>
                  <div className={`w-8 h-8 bg-${stat.color}/10 rounded-lg flex items-center justify-center`}>
                    <TrendingUp className={`w-4 h-4 text-${stat.color}`} />
                  </div>
                </div>
                <div className="space-y-2">
                  <div className="flex items-baseline space-x-2">
                    <span className="text-2xl font-bold text-[#333333] dark:text-white">{stat.value}</span>
                    <span className="text-sm text-gray-500 dark:text-gray-400">/ {stat.target}</span>
                  </div>
                  <Progress value={(stat.value / stat.target) * 100} className="h-2" />
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Main Content Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
            <TabsTrigger value="overview" className="data-[state=active]:bg-[#4A90E2] data-[state=active]:text-white">
              <BarChart3 className="w-4 h-4 mr-2" />
              Overview
            </TabsTrigger>
            <TabsTrigger value="mood" className="data-[state=active]:bg-[#4A90E2] data-[state=active]:text-white">
              <Activity className="w-4 h-4 mr-2" />
              Mood Tracking
            </TabsTrigger>
            <TabsTrigger value="goals" className="data-[state=active]:bg-[#4A90E2] data-[state=active]:text-white">
              <Target className="w-4 h-4 mr-2" />
              Daily Goals
            </TabsTrigger>
            <TabsTrigger value="milestones" className="data-[state=active]:bg-[#4A90E2] data-[state=active]:text-white">
              <Award className="w-4 h-4 mr-2" />
              Milestones
            </TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6">
            <div className="grid lg:grid-cols-3 gap-6">
              {/* Progress Chart */}
              <Card className="lg:col-span-2 border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
                <CardHeader>
                  <CardTitle className="text-[#333333] dark:text-white flex items-center">
                    <PieChart className="w-5 h-5 mr-2 text-[#4A90E2]" />
                    Weekly Progress Overview
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    {/* Mood Trend */}
                    <div>
                      <h4 className="font-medium text-[#333333] dark:text-white mb-3">Mood Trend (Last 7 Days)</h4>
                      <div className="flex items-center justify-between">
                        {moodHistory.map((day, index) => {
                          const moodData = moodOptions.find((m) => m.value === day.mood)
                          return (
                            <div key={index} className="text-center">
                              <div
                                className={`w-10 h-10 rounded-full ${moodData?.bg} flex items-center justify-center mb-2`}
                              >
                                {moodData && <moodData.icon className={`w-5 h-5 ${moodData.color}`} />}
                              </div>
                              <span className="text-xs text-gray-600 dark:text-gray-400">{day.date}</span>
                            </div>
                          )
                        })}
                      </div>
                    </div>

                    {/* Activity Summary */}
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-[#4A90E2]/10 dark:bg-[#4A90E2]/5 rounded-lg p-4">
                        <div className="flex items-center space-x-3">
                          <Brain className="w-8 h-8 text-[#4A90E2]" />
                          <div>
                            <p className="text-sm text-gray-600 dark:text-gray-400">AI Insights</p>
                            <p className="font-semibold text-[#333333] dark:text-white">Positive Trend</p>
                          </div>
                        </div>
                      </div>
                      <div className="bg-[#A8E6CF]/20 dark:bg-[#A8E6CF]/10 rounded-lg p-4">
                        <div className="flex items-center space-x-3">
                          <Shield className="w-8 h-8 text-[#A8E6CF]" />
                          <div>
                            <p className="text-sm text-gray-600 dark:text-gray-400">Risk Level</p>
                            <p className="font-semibold text-[#333333] dark:text-white">Low</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Today's Summary */}
              <Card className="border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
                <CardHeader>
                  <CardTitle className="text-[#333333] dark:text-white flex items-center">
                    <CalendarIcon className="w-5 h-5 mr-2 text-[#4A90E2]" />
                    Today's Summary
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-[#4A90E2] mb-2">Day 47</div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Consecutive days sober</p>
                  </div>

                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600 dark:text-gray-400">Goals Completed</span>
                      <span className="font-semibold text-[#333333] dark:text-white">2/4</span>
                    </div>
                    <Progress value={50} className="h-2" />
                  </div>

                  <div className="space-y-2">
                    <h4 className="font-medium text-[#333333] dark:text-white">Quick Actions</h4>
                    <div className="space-y-2">
                      <Button size="sm" className="w-full bg-[#4A90E2] hover:bg-[#3A7BC8] text-white">
                        <Plus className="w-4 h-4 mr-2" />
                        Log Mood
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        className="w-full border-[#A8E6CF] text-[#333333] dark:text-white hover:bg-[#A8E6CF]/10"
                      >
                        <BookOpen className="w-4 h-4 mr-2" />
                        Add Journal Entry
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Mood Tracking Tab */}
          <TabsContent value="mood" className="space-y-6">
            <div className="grid lg:grid-cols-2 gap-6">
              {/* Mood Logger */}
              <Card className="border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
                <CardHeader>
                  <CardTitle className="text-[#333333] dark:text-white">How are you feeling today?</CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="grid grid-cols-1 gap-3">
                    {moodOptions.map((mood) => (
                      <button
                        key={mood.value}
                        onClick={() => setCurrentMood(mood.value)}
                        className={`flex items-center space-x-3 p-4 rounded-lg border-2 transition-all duration-200 ${
                          currentMood === mood.value
                            ? `border-[#4A90E2] ${mood.bg}`
                            : "border-gray-200 dark:border-gray-600 hover:border-[#4A90E2]/50"
                        }`}
                      >
                        <mood.icon className={`w-6 h-6 ${mood.color}`} />
                        <span className="font-medium text-[#333333] dark:text-white">{mood.label}</span>
                      </button>
                    ))}
                  </div>

                  <div className="space-y-3">
                    <label className="text-sm font-medium text-[#333333] dark:text-white">
                      What's on your mind? (Optional)
                    </label>
                    <Textarea
                      placeholder="Share your thoughts, feelings, or what triggered this mood..."
                      value={journalEntry}
                      onChange={(e) => setJournalEntry(e.target.value)}
                      className="border-gray-300 dark:border-gray-600 focus:border-[#4A90E2] focus:ring-[#4A90E2] bg-white dark:bg-gray-700"
                      rows={4}
                    />
                  </div>

                  <Button className="w-full bg-[#4A90E2] hover:bg-[#3A7BC8] text-white" disabled={!currentMood}>
                    <Heart className="w-4 h-4 mr-2" />
                    Save Mood Entry
                  </Button>
                </CardContent>
              </Card>

              {/* Mood Calendar */}
              <Card className="border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
                <CardHeader>
                  <CardTitle className="text-[#333333] dark:text-white">Mood Calendar</CardTitle>
                </CardHeader>
                <CardContent>
                  <Calendar
                    mode="single"
                    selected={selectedDate}
                    onSelect={setSelectedDate}
                    className="rounded-md border border-gray-200 dark:border-gray-600"
                  />
                  <div className="mt-4 space-y-2">
                    <h4 className="font-medium text-[#333333] dark:text-white">Mood Legend</h4>
                    <div className="grid grid-cols-2 gap-2 text-xs">
                      {moodOptions.map((mood) => (
                        <div key={mood.value} className="flex items-center space-x-2">
                          <mood.icon className={`w-4 h-4 ${mood.color}`} />
                          <span className="text-gray-600 dark:text-gray-400">{mood.label}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Daily Goals Tab */}
          <TabsContent value="goals" className="space-y-6">
            <div className="grid lg:grid-cols-3 gap-6">
              {/* Today's Goals */}
              <Card className="lg:col-span-2 border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
                <CardHeader>
                  <CardTitle className="text-[#333333] dark:text-white flex items-center justify-between">
                    <span className="flex items-center">
                      <Target className="w-5 h-5 mr-2 text-[#4A90E2]" />
                      Today's Goals
                    </span>
                    <Button size="sm" className="bg-[#A8E6CF] hover:bg-[#98D6BF] text-[#333333]">
                      <Plus className="w-4 h-4 mr-2" />
                      Add Goal
                    </Button>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {dailyGoals.map((goal) => (
                      <div
                        key={goal.id}
                        className={`flex items-center space-x-4 p-4 rounded-lg border-2 transition-all duration-200 ${
                          goal.completed ? "border-[#A8E6CF] bg-[#A8E6CF]/10" : "border-gray-200 dark:border-gray-600"
                        }`}
                      >
                        <button
                          className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all duration-200 ${
                            goal.completed
                              ? "border-[#A8E6CF] bg-[#A8E6CF]"
                              : "border-gray-300 dark:border-gray-600 hover:border-[#4A90E2]"
                          }`}
                        >
                          {goal.completed && <CheckCircle className="w-4 h-4 text-white" />}
                        </button>
                        <div className="flex-1">
                          <h4
                            className={`font-medium ${goal.completed ? "text-[#333333] dark:text-white line-through" : "text-[#333333] dark:text-white"}`}
                          >
                            {goal.title}
                          </h4>
                          <div className="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
                            <Clock className="w-4 h-4" />
                            <span>{goal.time}</span>
                          </div>
                        </div>
                        {goal.completed && (
                          <Badge className="bg-[#A8E6CF] text-[#333333]">
                            <CheckCircle className="w-3 h-3 mr-1" />
                            Completed
                          </Badge>
                        )}
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Goal Categories */}
              <Card className="border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
                <CardHeader>
                  <CardTitle className="text-[#333333] dark:text-white">Goal Categories</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {[
                    { name: "Mindfulness", count: 5, color: "bg-blue-500", completed: 3 },
                    { name: "Social Support", count: 3, color: "bg-purple-500", completed: 2 },
                    { name: "Self-Care", count: 4, color: "bg-green-500", completed: 4 },
                    { name: "Learning", count: 2, color: "bg-orange-500", completed: 1 },
                  ].map((category, index) => (
                    <div key={index} className="space-y-2">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <div className={`w-3 h-3 rounded-full ${category.color}`}></div>
                          <span className="text-sm font-medium text-[#333333] dark:text-white">{category.name}</span>
                        </div>
                        <span className="text-xs text-gray-600 dark:text-gray-400">
                          {category.completed}/{category.count}
                        </span>
                      </div>
                      <Progress value={(category.completed / category.count) * 100} className="h-2" />
                    </div>
                  ))}
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Milestones Tab */}
          <TabsContent value="milestones" className="space-y-6">
            <div className="grid lg:grid-cols-2 gap-6">
              {/* Achievement Timeline */}
              <Card className="border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
                <CardHeader>
                  <CardTitle className="text-[#333333] dark:text-white flex items-center">
                    <Trophy className="w-5 h-5 mr-2 text-[#4A90E2]" />
                    Achievement Timeline
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    {milestones.map((milestone, index) => (
                      <div key={index} className="flex items-start space-x-4">
                        <div
                          className={`w-12 h-12 rounded-full flex items-center justify-center ${
                            milestone.achieved
                              ? "bg-[#A8E6CF] text-[#333333]"
                              : "bg-gray-200 dark:bg-gray-700 text-gray-400"
                          }`}
                        >
                          <milestone.icon className="w-6 h-6" />
                        </div>
                        <div className="flex-1">
                          <h4
                            className={`font-medium ${milestone.achieved ? "text-[#333333] dark:text-white" : "text-gray-500 dark:text-gray-400"}`}
                          >
                            {milestone.title}
                          </h4>
                          <p className="text-sm text-gray-600 dark:text-gray-400">{milestone.date}</p>
                          {milestone.achieved && (
                            <Badge className="mt-2 bg-[#A8E6CF] text-[#333333]">
                              <Star className="w-3 h-3 mr-1" />
                              Achieved
                            </Badge>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Next Milestone */}
              <Card className="border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
                <CardHeader>
                  <CardTitle className="text-[#333333] dark:text-white flex items-center">
                    <Target className="w-5 h-5 mr-2 text-[#4A90E2]" />
                    Next Milestone
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="text-center">
                    <div className="w-20 h-20 bg-[#4A90E2]/10 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Target className="w-10 h-10 text-[#4A90E2]" />
                    </div>
                    <h3 className="text-xl font-bold text-[#333333] dark:text-white mb-2">60 Days Sober</h3>
                    <p className="text-gray-600 dark:text-gray-400">13 days to go</p>
                  </div>

                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600 dark:text-gray-400">Progress</span>
                      <span className="font-medium text-[#333333] dark:text-white">78%</span>
                    </div>
                    <Progress value={78} className="h-3" />
                  </div>

                  <div className="bg-[#4A90E2]/10 dark:bg-[#4A90E2]/5 rounded-lg p-4">
                    <h4 className="font-medium text-[#333333] dark:text-white mb-2">Milestone Reward</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Unlock advanced AI insights and join the 60-day champions group!
                    </p>
                  </div>

                  <Button className="w-full bg-[#4A90E2] hover:bg-[#3A7BC8] text-white">
                    <Zap className="w-4 h-4 mr-2" />
                    Share Progress
                  </Button>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
