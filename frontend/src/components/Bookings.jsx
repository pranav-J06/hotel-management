import { useEffect, useState } from 'react'

export default function Bookings() {
  const [bookings, setBookings] = useState([])
  const [guests, setGuests] = useState([])
  const [rooms, setRooms] = useState([])
  const [form, setForm] = useState({ gId:'', rId:'', bookingType:'Walk-in', status:'Confirmed', checkIn:'', checkOut:'' })

  const load = () => {
    fetch('/api/bookings?detailed').then(r=>r.json()).then(d=> setBookings(Array.isArray(d)?d:[])).catch(()=>{})
    fetch('/api/guests').then(r=>r.json()).then(setGuests).catch(()=>{})
    fetch('/api/rooms?available=true').then(r=>r.json()).then(setRooms).catch(()=>{})
  }
  useEffect(()=>{load()},[])

  const submit = async (e) => {
    e.preventDefault()
    await fetch('/api/bookings', { method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ gId: parseInt(form.gId), rId: parseInt(form.rId), bookingType: form.bookingType, status: form.status, checkIn: form.checkIn, checkOut: form.checkOut })
    })
    load()
  }

  return (
    <>
      <div className="card">
        <h2>New Booking — Booking_Record(Booking-ID, G-ID, R-ID, Booking_Type, Status)</h2>
        <form onSubmit={submit} className="form-grid">
          <select value={form.gId} onChange={e=>setForm({...form, gId:e.target.value})} required>
            <option value="">Select Guest</option>
            {guests.map(g=> <option key={g.gId} value={g.gId}>{g.gId} - {g.firstName} {g.lastName}</option>)}
          </select>
          <select value={form.rId} onChange={e=>setForm({...form, rId:e.target.value})} required>
            <option value="">Select Room (Available)</option>
            {rooms.map(r=> <option key={r.rId} value={r.rId}>{r.rId} - {r.type} (₹{r.pricePerNight})</option>)}
          </select>
          <select value={form.bookingType} onChange={e=>setForm({...form, bookingType:e.target.value})}>
            <option>Walk-in</option><option>Online</option><option>Phone</option><option>Agent</option>
          </select>
          <select value={form.status} onChange={e=>setForm({...form, status:e.target.value})}>
            <option>Confirmed</option><option>Checked-in</option><option>Pending</option><option>Cancelled</option>
          </select>
          <input type="date" value={form.checkIn} onChange={e=>setForm({...form, checkIn:e.target.value})} required />
          <input type="date" value={form.checkOut} onChange={e=>setForm({...form, checkOut:e.target.value})} required />
          <button className="btn" type="submit">Create Booking (JDBC)</button>
        </form>
      </div>
      <div className="card">
        <h2>Bookings (vw_booking_details)</h2>
        <table>
          <thead><tr><th>Booking_ID</th><th>Guest</th><th>Room</th><th>Type</th><th>Status</th><th>Check In/Out</th></tr></thead>
          <tbody>
            {bookings.map(b=>(
              <tr key={b.Booking_ID || b.bookingId}>
                <td>{b.Booking_ID || b.bookingId}</td>
                <td>{b.Guest_Name || b.gId} ({b.Guest_Phone || ''})</td>
                <td>{b.R_ID || b.rId} - {b.Room_Type || ''}</td>
                <td>{b.Booking_Type || b.bookingType}</td>
                <td>{b.Status || b.status}</td>
                <td>{b.Check_In || b.checkIn} → {b.Check_Out || b.checkOut}</td>
              </tr>
            ))}
            {bookings.length===0 && <tr><td colSpan={6} style={{textAlign:'center', color:'#94a3b8'}}>No bookings</td></tr>}
          </tbody>
        </table>
      </div>
    </>
  )
}
