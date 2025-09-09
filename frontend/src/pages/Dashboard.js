"use client"

import { useState, useEffect } from "react"
import { Calendar, Gift, Users } from "lucide-react"
import { format } from "date-fns"
import axios from "axios"

const Dashboard = () => {
  const [contacts, setContacts] = useState([])
  const [todaysBirthdays, setTodaysBirthdays] = useState([])
  const [upcomingBirthdays, setUpcomingBirthdays] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchContacts()
    fetchTodaysBirthdays()
  }, [])

  const fetchContacts = async () => {
    try {
      const response = await axios.get("/api/contacts")
      setContacts(response.data)
      calculateUpcomingBirthdays(response.data)
    } catch (error) {
      console.error("Error fetching contacts:", error)
    }
  }

  const fetchTodaysBirthdays = async () => {
    try {
      const response = await axios.get("/api/birthdays/today")
      setTodaysBirthdays(response.data)
      setLoading(false)
    } catch (error) {
      console.error("Error fetching today's birthdays:", error)
      setLoading(false)
    }
  }

  const calculateUpcomingBirthdays = (contactList) => {
    const today = new Date()
    const upcoming = contactList
      .map((contact) => {
        const birthDate = new Date(contact.birthdate)
        const thisYear = new Date(today.getFullYear(), birthDate.getMonth(), birthDate.getDate())
        const nextYear = new Date(today.getFullYear() + 1, birthDate.getMonth(), birthDate.getDate())

        const nextBirthday = thisYear >= today ? thisYear : nextYear
        const daysUntil = Math.ceil((nextBirthday - today) / (1000 * 60 * 60 * 24))

        return {
          ...contact,
          nextBirthday,
          daysUntil,
        }
      })
      .filter((contact) => contact.daysUntil > 0 && contact.daysUntil <= 30)
      .sort((a, b) => a.daysUntil - b.daysUntil)
      .slice(0, 8)

    setUpcomingBirthdays(upcoming)
  }

  const getDaysUntilText = (days) => {
    if (days === 1) return "Tomorrow"
    if (days <= 7) return `In ${days} days`
    return `In ${days} days`
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-muted-foreground animate-pulse">Loading dashboard…</div>
      </div>
    )
  }

  return (
    <div className="space-y-6 container">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
        <h1 className="text-2xl md:text-3xl font-bold text-foreground">Dashboard</h1>
        <div className="text-muted-foreground">{format(new Date(), "EEEE, MMMM d, yyyy")}</div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
        <div className="card hover:shadow-md transition-shadow">
          <div className="flex items-center gap-3">
            <Users className="h-8 w-8 text-primary" />
            <div>
              <p className="text-2xl font-bold text-foreground">{contacts.length}</p>
              <p className="text-sm text-muted-foreground">Total Contacts</p>
            </div>
          </div>
        </div>

        <div className="card hover:shadow-md transition-shadow">
          <div className="flex items-center gap-3">
            <Gift className="h-8 w-8 text-accent" />
            <div>
              <p className="text-2xl font-bold text-foreground">{todaysBirthdays.length}</p>
              <p className="text-sm text-muted-foreground">Today's Birthdays</p>
            </div>
          </div>
        </div>

        <div className="card hover:shadow-md transition-shadow">
          <div className="flex items-center gap-3">
            <Calendar className="h-8 w-8 text-chart-1" />
            <div>
              <p className="text-2xl font-bold text-foreground">{upcomingBirthdays.length}</p>
              <p className="text-sm text-muted-foreground">Upcoming (30 days)</p>
            </div>
          </div>
        </div>
      </div>

      {/* Today's Birthdays */}
      {todaysBirthdays.length > 0 && (
        <div className="card">
          <h2 className="text-lg md:text-xl font-semibold text-foreground mb-4 flex items-center gap-2">
            <Gift className="h-5 w-5 text-accent" />
            Today's Birthdays
          </h2>
          <div className="space-y-3">
            {todaysBirthdays.map((contact) => (
              <div key={contact.id} className="flex items-center justify-between p-3 bg-accent/10 rounded-lg">
                <div>
                  <p className="font-medium text-foreground">{contact.name}</p>
                  <p className="text-sm text-muted-foreground">{contact.whatsapp_number}</p>
                </div>
                <div className="text-accent font-medium">Happy Birthday!</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Upcoming Birthdays */}
      <div className="card">
        <h2 className="text-lg md:text-xl font-semibold text-foreground mb-4 flex items-center gap-2">
          <Calendar className="h-5 w-5 text-primary" />
          Upcoming Birthdays
        </h2>
        {upcomingBirthdays.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {upcomingBirthdays.map((contact) => (
              <div key={contact.id} className="flex items-center justify-between p-3 bg-muted rounded-lg hover:bg-muted/80 transition-colors">
                <div>
                  <p className="font-medium text-foreground">{contact.name}</p>
                  <p className="text-sm text-muted-foreground">
                    {format(new Date(contact.birthdate), "MMMM d")} • {contact.whatsapp_number}
                  </p>
                </div>
                <div className="text-primary font-medium">{getDaysUntilText(contact.daysUntil)}</div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-muted-foreground text-center py-8">No upcoming birthdays in the next 30 days</p>
        )}
      </div>
    </div>
  )
}

export default Dashboard
