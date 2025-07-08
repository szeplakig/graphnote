import { useEffect, useState } from 'react'

function Note({ note, onSelect }) {
  return (
    <div className="border p-2 mb-2" onClick={() => onSelect(note)}>
      <h3 className="font-bold">{note.title}</h3>
    </div>
  )
}

function App() {
  const [notes, setNotes] = useState([])
  const [selected, setSelected] = useState(null)
  const [content, setContent] = useState('')
  const [title, setTitle] = useState('')

  const loadNotes = async () => {
    const res = await fetch('http://localhost:8000/notes')
    setNotes(await res.json())
  }

  const loadNote = async (note) => {
    const res = await fetch(`http://localhost:8000/notes/${note.id}`)
    const data = await res.json()
    setSelected(data)
    setTitle(data.title)
    setContent(data.content)
  }

  const saveNote = async () => {
    if (!selected) return
    await fetch(`http://localhost:8000/notes/${selected.id}?title=${encodeURIComponent(title)}&content=${encodeURIComponent(content)}`, { method: 'PUT' })
    loadNotes()
  }

  useEffect(() => { loadNotes() }, [])

  return (
    <div className="flex">
      <div className="w-1/3 pr-4">
        <h2 className="text-xl mb-2">Notes</h2>
        {notes.map(n => <Note key={n.id} note={n} onSelect={loadNote} />)}
      </div>
      {selected && (
        <div className="flex-1">
          <input className="border p-1 mb-2 w-full" value={title} onChange={e => setTitle(e.target.value)} />
          <textarea className="border p-1 w-full" rows="10" value={content} onChange={e => setContent(e.target.value)} />
          <button className="mt-2 bg-blue-500 text-white px-2 py-1" onClick={saveNote}>Save</button>
        </div>
      )}
    </div>
  )
}

export default App
