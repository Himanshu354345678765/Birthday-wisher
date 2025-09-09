import React, { useState } from "react"
import { Link, useLocation } from "react-router-dom"
import { Home, Users, Settings, Calendar, Menu, X } from "lucide-react"

const Layout = ({ children }) => {
  const location = useLocation()
  const navigation = [
    { name: "Dashboard", href: "/", icon: Home },
    { name: "Contacts", href: "/contacts", icon: Users },
    { name: "Settings", href: "/settings", icon: Settings },
  ]

  const [mobileOpen, setMobileOpen] = useState(false)

  function NavList({ onNavigate }) {
    return (
      <ul className="space-y-2">
        {navigation.map((item) => {
          const Icon = item.icon
          const isActive = location.pathname === item.href
          return (
            <li key={item.name}>
              <Link
                to={item.href}
                onClick={() => onNavigate && onNavigate()}
                className={`flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-sidebar-primary text-sidebar-primary-foreground"
                    : "text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
                }`}
              >
                <Icon className="h-5 w-5" />
                {item.name}
              </Link>
            </li>
          )
        })}
      </ul>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="bg-card border-b border-border px-4 md:px-6 py-3 md:py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              className="md:hidden p-2 rounded-md border border-border"
              aria-label="Toggle navigation"
              onClick={() => setMobileOpen((v) => !v)}
            >
              {mobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </button>
            <Calendar className="h-7 w-7 md:h-8 md:w-8 text-primary" />
            <h1 className="text-lg md:text-xl font-bold text-foreground">Birthday Reminder</h1>
          </div>
          <div className="hidden sm:block text-sm text-muted-foreground">Never miss a birthday again</div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar - desktop */}
        <nav className="hidden md:block w-64 bg-sidebar border-r border-sidebar-border min-h-screen">
          <div className="p-4">
            <NavList />
          </div>
        </nav>

        {/* Sidebar - mobile drawer */}
        {mobileOpen && (
          <div className="md:hidden fixed inset-0 z-40">
            <div className="absolute inset-0 bg-black/40" onClick={() => setMobileOpen(false)} />
            <nav className="absolute left-0 top-0 h-full w-72 bg-sidebar border-r border-sidebar-border p-4">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <Calendar className="h-6 w-6 text-primary" />
                  <span className="font-semibold text-foreground">Menu</span>
                </div>
                <button className="p-2" onClick={() => setMobileOpen(false)} aria-label="Close menu">
                  <X className="h-5 w-5" />
                </button>
              </div>
              <NavList onNavigate={() => setMobileOpen(false)} />
            </nav>
          </div>
        )}

        {/* Main Content */}
        <main className="flex-1 p-4 md:p-6 w-full">{children}</main>
      </div>
    </div>
  )
}

export default Layout
