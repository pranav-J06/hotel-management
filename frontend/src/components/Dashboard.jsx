import { useEffect, useState } from 'react'

export default function Dashboard() {
  const [stats, setStats] = useState({ guests: 0, rooms: 0, bookings: 0, available: 0 })
  const [health, setHealth] = useState('checking...')

  useEffect(() => {
    Promise.all([
      fetch('/api/guests').then(r=>r.json()).catch(()=>[]),
      fetch('/api/rooms').then(r=>r.json()).catch(()=>[]),
      fetch('/api/bookings').then(r=>r.json()).catch(()=>[]),
      fetch('/api/health').then(r=>r.json()).then(d=> setHealth(d.status)).catch(()=> setHealth('offline'))
    ]).then(([guests, rooms, bookings]) => {
      setStats({
        guests: Array.isArray(guests)? guests.length : 0,
        rooms: Array.isArray(rooms)? rooms.length : 0,
        bookings: Array.isArray(bookings)? bookings.length : 0,
        available: Array.isArray(rooms)? rooms.filter(r=>r.availability==='Available').length : 0
      })
    })
  }, [])

  return (
    <>
      <div className="stats">
        <div className="stat"><h3>{stats.guests}</h3><p>Total Guests</p></div>
        <div className="stat"><h3>{stats.rooms}</h3><p>Total Rooms</p></div>
        <div className="stat"><h3>{stats.available}</h3><p>Available Rooms</p></div>
        <div className="stat"><h3>{stats.bookings}</h3><p>Bookings</p></div>
      </div>
      <div className="card">
        <h2>System Status</h2>
        <p>Backend: <strong>{health}</strong> — Make sure MySQL + JDBC backend is running on :8080</p>
        <p style={{marginTop:'0.8rem', color:'#64748b'}}>Schema: 13 tables (Guest, ZipCode, Employee, Room, Manager, Housekeeper, Receptionist, Booking_Record, Bill, Records, Housekeeper_Room, Guest_Manager, Receptionist_Records)</p>
      </div>
      <div className="card">
        <h2>Quick Setup</h2>
        <ol style={{marginLeft:'1.2rem', lineHeight:'1.8'}}>
          <li>Run <code>database/schema.sql</code> in MySQL</li>
          <li>Run <code>database/seed.sql</code> for sample data</li>
          <li>Update <code>backend/src/main/resources/db.properties</code> with your MySQL password</li>
          <li>Start backend: <code>mvn package; java -jar target/hotel-management-backend-1.0.0-jar-with-dependencies.jar</code></li>
          <li>Start frontend: <code>cd frontend; npm install; npm run dev</code></li>
        </ol>
      </div>
    </>
  )
}
