import { useEffect, useState } from 'react'

export default function App() {
  const [tab, setTab] = useState('enter')
  const [guests, setGuests] = useState([])
  const [rooms, setRooms] = useState([])
  const [bookings, setBookings] = useState([])
  const [bills, setBills] = useState([])
  const [health, setHealth] = useState('checking...')
  const [msg, setMsg] = useState('')

  // --- Tab 1 forms ---
  const [guestForm, setGuestForm] = useState({ firstName: '', lastName: '', dob: '', gender: 'Male', mobNo: '' })
  const [roomForm, setRoomForm] = useState({ type: 'Single', capacity: 1, availability: 'Available', pricePerNight: 1500 })
  const [bookingForm, setBookingForm] = useState({ gId: '', rId: '', bookingType: 'Walk-in', status: 'Confirmed', checkIn: '', checkOut: '' })
  const [billForm, setBillForm] = useState({ gId: '', amount: '', bookingId: '', paymentStatus: 'Unpaid' })

  // --- Tab 2 filters ---
  const [f, setF] = useState({ arrivalDate: '', roomType: '', bookingType: '', status: '', guestSearch: '' })

  const load = async () => {
    try {
      const [g, r, b, billsData, h] = await Promise.all([
        fetch('/api/guests').then(x => x.json()).catch(() => []),
        fetch('/api/rooms').then(x => x.json()).catch(() => []),
        fetch('/api/bookings?detailed').then(x => x.json()).catch(() => []),
        fetch('/api/bills').then(x => x.json()).catch(() => []),
        fetch('/api/health').then(x => x.json()).catch(() => ({ status: 'offline' })),
      ])
      setGuests(Array.isArray(g) ? g : [])
      setRooms(Array.isArray(r) ? r : [])
      setBookings(Array.isArray(b) ? b : [])
      setBills(Array.isArray(billsData) ? billsData : [])
      setHealth(h.status || 'UP')
    } catch { setHealth('offline') }
  }
  useEffect(() => { load() }, [])

  const flash = (m) => { setMsg(m); setTimeout(() => setMsg(''), 3000) }

  // ---------- TAB 1 : INSERTS (JDBC) ----------
  const addGuest = async (e) => {
    e.preventDefault()
    const payload = { ...guestForm, dob: guestForm.dob || null }
    const res = await fetch('/api/guests', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
    if (res.ok) { flash('Guest saved to DB'); setGuestForm({ firstName: '', lastName: '', dob: '', gender: 'Male', mobNo: '' }); load() }
    else flash('Failed to save guest')
  }
  const addRoom = async (e) => {
    e.preventDefault()
    const res = await fetch('/api/rooms', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ...roomForm, capacity: parseInt(roomForm.capacity), pricePerNight: parseFloat(roomForm.pricePerNight) }) })
    if (res.ok) { flash('Room saved to DB'); load() }
    else flash('Failed to save room')
  }
  const addBooking = async (e) => {
    e.preventDefault()
    const body = { gId: parseInt(bookingForm.gId), rId: parseInt(bookingForm.rId), bookingType: bookingForm.bookingType, status: bookingForm.status, checkIn: bookingForm.checkIn, checkOut: bookingForm.checkOut }
    const res = await fetch('/api/bookings', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
    if (res.ok) { flash('Booking saved to DB'); setBookingForm({ gId: '', rId: '', bookingType: 'Walk-in', status: 'Confirmed', checkIn: '', checkOut: '' }); load() }
    else flash('Failed — check Guest/Room IDs and dates')
  }
  const addBill = async (e) => {
    e.preventDefault()
    const body = { gId: parseInt(billForm.gId), amount: parseFloat(billForm.amount), bookingId: billForm.bookingId ? parseInt(billForm.bookingId) : null, billingDate: new Date().toISOString().slice(0, 10), paymentStatus: billForm.paymentStatus }
    const res = await fetch('/api/bills', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
    if (res.ok) { flash('Bill saved to DB'); setBillForm({ gId: '', amount: '', bookingId: '', paymentStatus: 'Unpaid' }); load() }
    else flash('Failed to save bill')
  }

  // ---------- TAB 2 : FILTERED RETRIEVAL ----------
  // bookings[] comes from vw_booking_details: Booking_ID, Guest_Name, Guest_Phone, R_ID, Room_Type, Booking_Type, Status, Check_In, Check_Out
  const get = (b, ...keys) => { for (const k of keys) { if (b[k] !== undefined && b[k] !== null) return b[k] } return '' }
  // Backend sends dates as "Sep 1, 2026" (Gson) or "2026-09-01" — normalise both to yyyy-mm-dd
  const toISO = (v) => {
    if (!v) return ''
    const s = String(v)
    if (/^\d{4}-\d{2}-\d{2}/.test(s)) return s.slice(0, 10)
    const d = new Date(s)
    if (!isNaN(d)) return d.toISOString().slice(0, 10)
    return s
  }
  const results = bookings.filter(b => {
    const checkIn = toISO(get(b, 'Check_In', 'checkIn'))
    const roomType = get(b, 'Room_Type', 'roomType')
    const bookingType = get(b, 'Booking_Type', 'bookingType')
    const status = get(b, 'Status', 'status')
    const guestName = String(get(b, 'Guest_Name', 'guestName') + ' ' + get(b, 'Guest_Phone', 'guestPhone')).toLowerCase()
    if (f.arrivalDate && checkIn !== f.arrivalDate) return false
    if (f.roomType && roomType !== f.roomType) return false
    if (f.bookingType && bookingType !== f.bookingType) return false
    if (f.status && status !== f.status) return false
    if (f.guestSearch && !guestName.includes(f.guestSearch.toLowerCase())) return false
    return true
  })
  const clearFilters = () => setF({ arrivalDate: '', roomType: '', bookingType: '', status: '', guestSearch: '' })

  // Show equivalent SQL for viva/demo
  const whereParts = []
  if (f.arrivalDate) whereParts.push(`Check_In = '${f.arrivalDate}'`)
  if (f.roomType) whereParts.push(`Room_Type = '${f.roomType}'`)
  if (f.bookingType) whereParts.push(`Booking_Type = '${f.bookingType}'`)
  if (f.status) whereParts.push(`Status = '${f.status}'`)
  if (f.guestSearch) whereParts.push(`Guest_Name LIKE '%${f.guestSearch}%'`)
  const sqlPreview = `SELECT * FROM vw_booking_details${whereParts.length ? ' WHERE ' + whereParts.join(' AND ') : ''};`

  return (
    <>
      <header className="top">
        <div>
          <h1>Hotel Management System</h1>
          <p>Pranav Jahagirdar • Reception • DB: {health}</p>
        </div>
        <nav>
          <button className={tab === 'enter' ? 'active' : ''} onClick={() => setTab('enter')}>1. Enter Details</button>
          <button className={tab === 'retrieve' ? 'active' : ''} onClick={() => setTab('retrieve')}>2. Retrieve / Search</button>
          <button className="ghost" onClick={load}>Refresh</button>
        </nav>
      </header>

      {msg && <div className="toast">{msg}</div>}

      <main className="wrap">
        {/* ================= TAB 1 ================= */}
        {tab === 'enter' && (
          <>
            <p className="hint">Fill any form and Save — it does a JDBC INSERT into MySQL. Use IDs from the lists below.</p>

            <div className="card">
              <h2>Add Guest → Guest(G-ID, First_Name, Last_Name, DOB, Gender, Mob-No)</h2>
              <form onSubmit={addGuest} className="grid">
                <input placeholder="First Name *" value={guestForm.firstName} onChange={e => setGuestForm({ ...guestForm, firstName: e.target.value })} required />
                <input placeholder="Last Name *" value={guestForm.lastName} onChange={e => setGuestForm({ ...guestForm, lastName: e.target.value })} required />
                <input type="date" value={guestForm.dob} onChange={e => setGuestForm({ ...guestForm, dob: e.target.value })} />
                <select value={guestForm.gender} onChange={e => setGuestForm({ ...guestForm, gender: e.target.value })}>
                  <option>Male</option><option>Female</option><option>Other</option>
                </select>
                <input placeholder="Mobile (10-15 digits) *" value={guestForm.mobNo} onChange={e => setGuestForm({ ...guestForm, mobNo: e.target.value })} required />
                <button type="submit">Save Guest</button>
              </form>
            </div>

            <div className="card">
              <h2>Add Room → Room(R-ID, Type, Capacity, Availability)</h2>
              <form onSubmit={addRoom} className="grid">
                <select value={roomForm.type} onChange={e => setRoomForm({ ...roomForm, type: e.target.value })}>
                  <option>Single</option><option>Double</option><option>Deluxe</option><option>Suite</option>
                </select>
                <input type="number" min="1" max="6" placeholder="Capacity" value={roomForm.capacity} onChange={e => setRoomForm({ ...roomForm, capacity: e.target.value })} required />
                <select value={roomForm.availability} onChange={e => setRoomForm({ ...roomForm, availability: e.target.value })}>
                  <option>Available</option><option>Occupied</option><option>Maintenance</option>
                </select>
                <input type="number" placeholder="Price/Night" value={roomForm.pricePerNight} onChange={e => setRoomForm({ ...roomForm, pricePerNight: e.target.value })} required />
                <button type="submit">Save Room</button>
              </form>
            </div>

            <div className="card">
              <h2>Add Booking → Booking_Record(Booking-ID, G-ID, R-ID, Booking_Type, Status)</h2>
              <form onSubmit={addBooking} className="grid">
                <select value={bookingForm.gId} onChange={e => setBookingForm({ ...bookingForm, gId: e.target.value })} required>
                  <option value="">Guest *</option>
                  {guests.map(g => <option key={g.gId} value={g.gId}>#{g.gId} {g.firstName} {g.lastName}</option>)}
                </select>
                <select value={bookingForm.rId} onChange={e => setBookingForm({ ...bookingForm, rId: e.target.value })} required>
                  <option value="">Room *</option>
                  {rooms.map(r => <option key={r.rId} value={r.rId}>#{r.rId} {r.type} ({r.availability})</option>)}
                </select>
                <select value={bookingForm.bookingType} onChange={e => setBookingForm({ ...bookingForm, bookingType: e.target.value })}>
                  <option>Walk-in</option><option>Online</option><option>Phone</option><option>Agent</option>
                </select>
                <select value={bookingForm.status} onChange={e => setBookingForm({ ...bookingForm, status: e.target.value })}>
                  <option>Confirmed</option><option>Checked-in</option><option>Checked-out</option><option>Pending</option><option>Cancelled</option>
                </select>
                <input type="date" value={bookingForm.checkIn} onChange={e => setBookingForm({ ...bookingForm, checkIn: e.target.value })} required />
                <input type="date" value={bookingForm.checkOut} onChange={e => setBookingForm({ ...bookingForm, checkOut: e.target.value })} required />
                <button type="submit">Save Booking</button>
              </form>
            </div>

            <div className="card">
              <h2>Add Bill → Bill(B-ID, G-ID, Amount)</h2>
              <form onSubmit={addBill} className="grid">
                <select value={billForm.gId} onChange={e => setBillForm({ ...billForm, gId: e.target.value })} required>
                  <option value="">Guest *</option>
                  {guests.map(g => <option key={g.gId} value={g.gId}>#{g.gId} {g.firstName} {g.lastName}</option>)}
                </select>
                <input type="number" placeholder="Amount ₹ *" value={billForm.amount} onChange={e => setBillForm({ ...billForm, amount: e.target.value })} required />
                <select value={billForm.bookingId} onChange={e => setBillForm({ ...billForm, bookingId: e.target.value })}>
                  <option value="">Booking (optional)</option>
                  {bookings.map(b => <option key={get(b, 'Booking_ID', 'bookingId')} value={get(b, 'Booking_ID', 'bookingId')}>#{get(b, 'Booking_ID', 'bookingId')}</option>)}
                </select>
                <select value={billForm.paymentStatus} onChange={e => setBillForm({ ...billForm, paymentStatus: e.target.value })}>
                  <option>Unpaid</option><option>Paid</option><option>Partial</option>
                </select>
                <button type="submit">Save Bill</button>
              </form>
            </div>
          </>
        )}

        {/* ================= TAB 2 ================= */}
        {tab === 'retrieve' && (
          <>
            <p className="hint">Filter bookings with WHERE-style criteria. Examples: arriving on a date, booked Deluxe room, Walk-in only.</p>

            <div className="card">
              <h2>Filter Criteria</h2>
              <div className="grid">
                <label>Arriving on (Check-In)
                  <input type="date" value={f.arrivalDate} onChange={e => setF({ ...f, arrivalDate: e.target.value })} />
                </label>
                <label>Room Type
                  <select value={f.roomType} onChange={e => setF({ ...f, roomType: e.target.value })}>
                    <option value="">All</option>
                    <option>Single</option><option>Double</option><option>Deluxe</option><option>Suite</option>
                  </select>
                </label>
                <label>Booking Type
                  <select value={f.bookingType} onChange={e => setF({ ...f, bookingType: e.target.value })}>
                    <option value="">All</option>
                    <option>Walk-in</option><option>Online</option><option>Phone</option><option>Agent</option>
                  </select>
                </label>
                <label>Status
                  <select value={f.status} onChange={e => setF({ ...f, status: e.target.value })}>
                    <option value="">All</option>
                    <option>Confirmed</option><option>Checked-in</option><option>Checked-out</option><option>Pending</option><option>Cancelled</option>
                  </select>
                </label>
                <label>Guest name / phone
                  <input placeholder="e.g. Aarav or 98765" value={f.guestSearch} onChange={e => setF({ ...f, guestSearch: e.target.value })} />
                </label>
                <div style={{ display: 'flex', alignItems: 'end', gap: '0.5rem' }}>
                  <button className="ghost" onClick={clearFilters} type="button">Clear</button>
                </div>
              </div>
              <code className="sql">{sqlPreview}</code>
              <p className="count">{results.length} of {bookings.length} bookings match</p>
            </div>

            <div className="card">
              <h2>Results (Guest + Room + Booking join)</h2>
              <table>
                <thead><tr><th>#</th><th>Guest</th><th>Room</th><th>Type</th><th>Check-In → Out</th><th>Status</th></tr></thead>
                <tbody>
                  {results.map(b => (
                    <tr key={get(b, 'Booking_ID', 'bookingId')}>
                      <td>#{get(b, 'Booking_ID', 'bookingId')}</td>
                      <td>{get(b, 'Guest_Name', 'guestName')} <span className="muted">{get(b, 'Guest_Phone', 'guestPhone')}</span></td>
                      <td>#{get(b, 'R_ID', 'rId')} {get(b, 'Room_Type', 'roomType')}</td>
                      <td>{get(b, 'Booking_Type', 'bookingType')}</td>
                      <td>{toISO(get(b, 'Check_In', 'checkIn'))} → {toISO(get(b, 'Check_Out', 'checkOut'))}</td>
                      <td>{get(b, 'Status', 'status')}</td>
                    </tr>
                  ))}
                  {results.length === 0 && <tr><td colSpan={6} className="empty">No matches — change filters or check backend :8080 is running.</td></tr>}
                </tbody>
              </table>
            </div>
          </>
        )}
      </main>
    </>
  )
}
