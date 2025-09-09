"use client"

import { useEffect, useState } from "react"

type SchedulerStatus = {
  running: boolean
  next_run: string | null
  job_count: number
  daily?: { running: boolean; next_run: string | null }
  interval?: { running: boolean; next_run: string | null; interval_minutes?: number | null; end_time?: string | null }
}

type PreviewContact = {
  id: number
  name: string
  whatsapp_number: string
  message_text: string
}

type PreviewResponse = {
  date: string
  contacts: PreviewContact[]
  count: number
  scheduler_status: SchedulerStatus
}

export default function DashboardPage() {
  const [data, setData] = useState<PreviewResponse | null>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchPreview = async () => {
      try {
        setLoading(true)
        setError(null)
        const res = await fetch("http://127.0.0.1:5000/api/scheduler/preview")
        if (!res.ok) throw new Error(`Failed to load preview (${res.status})`)
        const json = (await res.json()) as PreviewResponse
        setData(json)
      } catch (e: any) {
        setError(e?.message ?? "Failed to load")
      } finally {
        setLoading(false)
      }
    }

    fetchPreview()
    const id = setInterval(fetchPreview, 15_000)
    return () => clearInterval(id)
  }, [])

  if (loading) return <div style={{ padding: 16 }}>Loading…</div>
  if (error) return <div style={{ padding: 16, color: "red" }}>Error: {error}</div>
  if (!data) return <div style={{ padding: 16 }}>No data</div>

  const s = data.scheduler_status
  const intervalInfo = s.interval

  return (
    <div style={{ padding: 16, display: "grid", gap: 16 }}>
      <h1>Scheduled Messages</h1>
      <div style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: 12 }}>
        <div><strong>Date</strong>: {data.date}</div>
        <div><strong>Scheduler running</strong>: {String(s.running)}</div>
        <div><strong>Next run</strong>: {s.next_run ?? "—"}</div>
        {intervalInfo && (
          <div style={{ display: "grid", gap: 4, marginTop: 8 }}>
            <div><strong>Interval</strong>: {intervalInfo.interval_minutes ?? "—"} min</div>
            <div><strong>Interval next run</strong>: {intervalInfo.next_run ?? "—"}</div>
            <div><strong>End time</strong>: {intervalInfo.end_time ?? "—"}</div>
          </div>
        )}
      </div>

      <div style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: 12 }}>
        <div style={{ marginBottom: 8 }}><strong>Contacts today</strong>: {data.count}</div>
        {data.contacts.length === 0 ? (
          <div>No birthdays today.</div>
        ) : (
          <div style={{ display: "grid", gap: 12 }}>
            {data.contacts.map((c) => (
              <div key={c.id} style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: 12 }}>
                <div><strong>{c.name}</strong> — {c.whatsapp_number}</div>
                <div style={{ marginTop: 6 }}>
                  <div style={{ fontSize: 12, color: "#6b7280" }}>Scheduled message</div>
                  <div style={{ whiteSpace: "pre-wrap" }}>{c.message_text}</div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}