import { useEffect, useState } from 'react'

export default function Rooms() {
  const [rooms, setRooms] = useState([])
  const load = () => fetch('/api/rooms').then(r=>r.json()).then(setRooms).catch(()=>setRooms([]))
  useEffect(()=>{load()},[])

  return (
    <div className="card">
      <h2>Rooms — Room(R-ID, Type, Capacity, Availability)</h2>
      <table>
        <thead><tr><th>R_ID</th><th>Type</th><th>Capacity</th><th>Availability</th><th>Price/Night</th></tr></thead>
        <tbody>
          {rooms.map(r=>(
            <tr key={r.rId}>
              <td>{r.rId}</td><td>{r.type}</td><td>{r.capacity}</td>
              <td><span className={`badge badge-${r.availability.toLowerCase()}`}>{r.availability}</span></td>
              <td>₹{r.pricePerNight}</td>
            </tr>
          ))}
          {rooms.length===0 && <tr><td colSpan={5} style={{textAlign:'center', color:'#94a3b8'}}>No rooms — is backend running?</td></tr>}
        </tbody>
      </table>
    </div>
  )
}
