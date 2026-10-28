import { useEffect, useState } from 'react'

export default function Guests() {
  const [guests, setGuests] = useState([])
  const [form, setForm] = useState({ firstName:'', lastName:'', dob:'', gender:'Male', mobNo:'' })

  const load = () => fetch('/api/guests').then(r=>r.json()).then(setGuests).catch(()=>setGuests([]))
  useEffect(()=>{load()},[])

  const submit = async (e) => {
    e.preventDefault()
    await fetch('/api/guests', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(form) })
    setForm({ firstName:'', lastName:'', dob:'', gender:'Male', mobNo:'' })
    load()
  }
  const del = async (id) => { await fetch(`/api/guests/${id}`, {method:'DELETE'}); load() }

  return (
    <>
      <div className="card">
        <h2>Add Guest</h2>
        <form onSubmit={submit} className="form-grid">
          <input placeholder="First Name" value={form.firstName} onChange={e=>setForm({...form, firstName:e.target.value})} required />
          <input placeholder="Last Name" value={form.lastName} onChange={e=>setForm({...form, lastName:e.target.value})} required />
          <input type="date" value={form.dob} onChange={e=>setForm({...form, dob:e.target.value})} />
          <select value={form.gender} onChange={e=>setForm({...form, gender:e.target.value})}>
            <option>Male</option><option>Female</option><option>Other</option>
          </select>
          <input placeholder="Mobile (10-15 digits)" value={form.mobNo} onChange={e=>setForm({...form, mobNo:e.target.value})} required />
          <button className="btn" type="submit">Add Guest (JDBC INSERT)</button>
        </form>
      </div>
      <div className="card">
        <h2>Guests — Guest(G-ID, First_Name, Last_Name, DOB, Gender, Mob-No)</h2>
        <table>
          <thead><tr><th>G_ID</th><th>Name</th><th>DOB</th><th>Gender</th><th>Mobile</th><th>Action</th></tr></thead>
          <tbody>
            {guests.map(g=>(
              <tr key={g.gId}>
                <td>{g.gId}</td><td>{g.firstName} {g.lastName}</td><td>{g.dob||'-'}</td><td>{g.gender}</td><td>{g.mobNo}</td>
                <td><button className="btn" style={{background:'#ef4444'}} onClick={()=>del(g.gId)}>Delete</button></td>
              </tr>
            ))}
            {guests.length===0 && <tr><td colSpan={6} style={{textAlign:'center', color:'#94a3b8'}}>No guests — is backend running?</td></tr>}
          </tbody>
        </table>
      </div>
    </>
  )
}
