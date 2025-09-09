"use client"

import { useState, useEffect } from "react"
import { Save, MessageSquare, User, Key } from "lucide-react"
import axios from "axios"

const Settings = () => {
  const [settings, setSettings] = useState({
    wisher_name: "",
    twilio_account_sid: "",
    twilio_auth_token: "",
    twilio_whatsapp_number: "",
  })
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    fetchSettings()
  }, [])

  const fetchSettings = async () => {
    try {
      const response = await axios.get("/api/settings")
      setSettings(response.data)
      setLoading(false)
    } catch (error) {
      console.error("Error fetching settings:", error)
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)

    try {
      await axios.post("/api/settings", settings)
      alert("Settings saved successfully!")
    } catch (error) {
      console.error("Error saving settings:", error)
      alert("Error saving settings. Please try again.")
    } finally {
      setSaving(false)
    }
  }

  const handleChange = (field, value) => {
    setSettings((prev) => ({
      ...prev,
      [field]: value,
    }))
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-muted-foreground">Loading settings...</div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-foreground">Settings</h1>
        <p className="text-muted-foreground mt-2">
          Configure your birthday reminder preferences and WhatsApp integration
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Personal Settings */}
        <div className="card">
          <h2 className="text-xl font-semibold text-foreground mb-4 flex items-center gap-2">
            <User className="h-5 w-5 text-primary" />
            Personal Information
          </h2>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">Your Name (Wisher Name)</label>
              <input
                type="text"
                required
                value={settings.wisher_name}
                onChange={(e) => handleChange("wisher_name", e.target.value)}
                className="input-field"
                placeholder="Enter your name"
              />
              <p className="text-xs text-muted-foreground mt-1">
                This name will appear in birthday messages (e.g., "Happy Birthday! - from John")
              </p>
            </div>
          </div>
        </div>

        {/* Twilio WhatsApp Settings */}
        <div className="card">
          <h2 className="text-xl font-semibold text-foreground mb-4 flex items-center gap-2">
            <MessageSquare className="h-5 w-5 text-accent" />
            WhatsApp Integration (Twilio)
          </h2>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">Twilio Account SID</label>
              <input
                type="text"
                value={settings.twilio_account_sid}
                onChange={(e) => handleChange("twilio_account_sid", e.target.value)}
                className="input-field"
                placeholder="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-foreground mb-1">Twilio Auth Token</label>
              <input
                type="password"
                value={settings.twilio_auth_token}
                onChange={(e) => handleChange("twilio_auth_token", e.target.value)}
                className="input-field"
                placeholder="Your Twilio Auth Token"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-foreground mb-1">Twilio WhatsApp Number</label>
              <input
                type="text"
                value={settings.twilio_whatsapp_number}
                onChange={(e) => handleChange("twilio_whatsapp_number", e.target.value)}
                className="input-field"
                placeholder="whatsapp:+14155238886"
              />
              <p className="text-xs text-muted-foreground mt-1">
                Format: whatsapp:+14155238886 (include "whatsapp:" prefix)
              </p>
            </div>
          </div>
        </div>

        {/* Setup Instructions */}
        <div className="card">
          <h2 className="text-xl font-semibold text-foreground mb-4 flex items-center gap-2">
            <Key className="h-5 w-5 text-chart-1" />
            Setup Instructions
          </h2>

          <div className="space-y-3 text-sm text-muted-foreground">
            <div>
              <h3 className="font-medium text-foreground">1. Create a Twilio Account</h3>
              <p>
                Sign up at{" "}
                <a
                  href="https://www.twilio.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-primary hover:underline"
                >
                  twilio.com
                </a>{" "}
                and verify your account
              </p>
            </div>

            <div>
              <h3 className="font-medium text-foreground">2. Get Your Credentials</h3>
              <p>Find your Account SID and Auth Token in the Twilio Console dashboard</p>
            </div>

            <div>
              <h3 className="font-medium text-foreground">3. Enable WhatsApp Sandbox</h3>
              <p>Go to Messaging → Try it out → Send a WhatsApp message to enable the sandbox</p>
            </div>

            <div>
              <h3 className="font-medium text-foreground">4. Get WhatsApp Number</h3>
              <p>Use the sandbox number (usually +1 415 523 8886) with "whatsapp:" prefix</p>
            </div>
          </div>
        </div>

        {/* Save Button */}
        <div className="flex justify-end">
          <button type="submit" disabled={saving} className="btn-primary flex items-center gap-2">
            <Save className="h-4 w-4" />
            {saving ? "Saving..." : "Save Settings"}
          </button>
        </div>
      </form>
    </div>
  )
}

export default Settings
