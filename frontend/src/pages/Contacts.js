"use client"

import { useState, useEffect } from "react"
import { Plus, Edit, Trash2, Search, User } from "lucide-react"
import { format } from "date-fns"
import axios from "axios"

const Contacts = () => {
  const [contacts, setContacts] = useState([])
  const [filteredContacts, setFilteredContacts] = useState([])
  const [todaysBirthdays, setTodaysBirthdays] = useState([])
  const [searchTerm, setSearchTerm] = useState("")
  const [showAddForm, setShowAddForm] = useState(false)
  const [editingContact, setEditingContact] = useState(null)
  const [formData, setFormData] = useState({
    name: "",
    birthdate: "",
    whatsapp_number: "",
  })

  useEffect(() => {
    fetchContacts()
    fetchTodaysBirthdays()
  }, [])

  useEffect(() => {
    const filtered = contacts.filter(
      (contact) =>
        contact.name.toLowerCase().includes(searchTerm.toLowerCase()) || contact.whatsapp_number.includes(searchTerm),
    )
    setFilteredContacts(filtered)
  }, [contacts, searchTerm])

  const fetchContacts = async () => {
    try {
      const response = await axios.get("/api/contacts")
      setContacts(response.data)
    } catch (error) {
      console.error("Error fetching contacts:", error)
    }
  }

  const fetchTodaysBirthdays = async () => {
    try {
      const response = await axios.get("/api/birthdays/today")
      setTodaysBirthdays(response.data)
    } catch (error) {
      console.error("Error fetching today's birthdays:", error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      if (editingContact) {
        await axios.put(`/api/contacts/${editingContact.id}`, formData)
      } else {
        await axios.post("/api/contacts", formData)
      }

      setFormData({ name: "", birthdate: "", whatsapp_number: "" })
      setShowAddForm(false)
      setEditingContact(null)
      fetchContacts()
    } catch (error) {
      console.error("Error saving contact:", error)
      alert("Error saving contact. Please try again.")
    }
  }

  const handleEdit = (contact) => {
    setEditingContact(contact)
    setFormData({
      name: contact.name,
      birthdate: contact.birthdate,
      whatsapp_number: contact.whatsapp_number,
    })
    setShowAddForm(true)
  }

  const handleDelete = async (contactId) => {
    if (window.confirm("Are you sure you want to delete this contact?")) {
      try {
        await axios.delete(`/api/contacts/${contactId}`)
        fetchContacts()
      } catch (error) {
        console.error("Error deleting contact:", error)
        alert("Error deleting contact. Please try again.")
      }
    }
  }

  const buildWhatsAppUrl = (contact) => {
    // wa.me expects an international number with country code and no '+' or spaces
    const digitsOnly = (contact.whatsapp_number || "").replace(/[^0-9]/g, "")
    // Use plain ASCII punctuation to avoid platform encoding quirks
    const message =
      "Hi there! This is Ribbon & Balloons with Asha Traders, and today's a super special day - it's your Birthday! Wishing you loads of happiness, laughter, and sweet surprises. Happiest Birthday from all of us to you!"
    const encoded = encodeURIComponent(message)
    const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent)
    if (isMobile) {
      // Open native app on mobile
      return `whatsapp://send?phone=${digitsOnly}&text=${encoded}`
    }
    // Desktop Web
    return `https://web.whatsapp.com/send?phone=${digitsOnly}&text=${encoded}`
  }

  const sendViaWhatsApp = (contact) => {
    const url = buildWhatsAppUrl(contact)
    // Open in a single, guaranteed new tab using an anchor element to avoid double-navigation
    const anchor = document.createElement("a")
    anchor.href = url
    anchor.target = "_blank"
    anchor.rel = "noopener noreferrer"
    document.body.appendChild(anchor)
    anchor.click()
    document.body.removeChild(anchor)
  }

  const resetForm = () => {
    setFormData({ name: "", birthdate: "", whatsapp_number: "" })
    setShowAddForm(false)
    setEditingContact(null)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-foreground">Contacts</h1>
        <button onClick={() => setShowAddForm(true)} className="btn-primary flex items-center gap-2">
          <Plus className="h-4 w-4" />
          Add Contact
        </button>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <input
          type="text"
          placeholder="Search contacts..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="input-field pl-10"
        />
      </div>

      {/* Add/Edit Form */}
      {showAddForm && (
        <div className="card">
          <h2 className="text-xl font-semibold text-foreground mb-4">
            {editingContact ? "Edit Contact" : "Add New Contact"}
          </h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">Name</label>
              <input
                type="text"
                required
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="input-field"
                placeholder="Enter full name"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-foreground mb-1">Birthdate</label>
              <input
                type="date"
                required
                value={formData.birthdate}
                onChange={(e) => setFormData({ ...formData, birthdate: e.target.value })}
                className="input-field"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-foreground mb-1">WhatsApp Number</label>
              <input
                type="tel"
                required
                value={formData.whatsapp_number}
                onChange={(e) => setFormData({ ...formData, whatsapp_number: e.target.value })}
                className="input-field"
                placeholder="+1234567890"
              />
            </div>

            <div className="flex gap-3">
              <button type="submit" className="btn-primary">
                {editingContact ? "Update Contact" : "Add Contact"}
              </button>
              <button type="button" onClick={resetForm} className="btn-secondary">
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Today's Birthdays */}
      <div className="card">
        <h2 className="text-xl font-semibold text-foreground mb-4">Today's Birthdays ({todaysBirthdays.length})</h2>
        {todaysBirthdays.length > 0 ? (
          <div className="grid grid-cols-1 gap-3">
            {todaysBirthdays.map((contact) => (
              <div key={contact.id} className="p-4 bg-muted rounded-lg hover:shadow-sm transition-shadow">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                      <User className="h-5 w-5 text-primary" />
                    </div>
                    <div>
                      <p className="font-medium text-foreground">{contact.name}</p>
                      <p className="text-sm text-muted-foreground">{format(new Date(contact.birthdate), "MMMM d, yyyy")} • {contact.whatsapp_number}</p>
                    </div>
                  </div>
                  <button onClick={() => sendViaWhatsApp(contact)} className="btn-primary px-3 py-2" title="Send via your WhatsApp">
                    Send via WhatsApp
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-muted-foreground">No birthdays today.</p>
        )}
      </div>

      {/* All Contacts List */}
      <div className="card">
        <h2 className="text-xl font-semibold text-foreground mb-4">All Contacts ({filteredContacts.length})</h2>

        {filteredContacts.length > 0 ? (
          <div className="grid grid-cols-1 gap-3">
            {filteredContacts.map((contact) => (
              <div key={contact.id} className="p-4 bg-muted rounded-lg hover:shadow-sm transition-shadow">
                <div className="flex items-center gap-3 mb-3">
                  <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                    <User className="h-5 w-5 text-primary" />
                  </div>
                  <div>
                    <p className="font-medium text-foreground">{contact.name}</p>
                    <p className="text-sm text-muted-foreground">
                      {format(new Date(contact.birthdate), "MMMM d, yyyy")} • {contact.whatsapp_number}
                    </p>
                  </div>
                </div>

                <div className="flex gap-2 justify-end">
                  <button
                    onClick={() => handleEdit(contact)}
                    className="p-2 text-muted-foreground hover:text-primary transition-colors"
                  >
                    <Edit className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => handleDelete(contact.id)}
                    className="p-2 text-muted-foreground hover:text-destructive transition-colors"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <User className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <p className="text-muted-foreground">
              {searchTerm ? "No contacts found matching your search." : "No contacts yet. Add your first contact!"}
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Contacts
