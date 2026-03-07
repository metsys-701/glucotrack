import { useState } from "react"

function AddGlucoseForm({ token, onAdded }) {

  const [glucose, setGlucose] = useState("")
  const [type, setType] = useState("FASTING")
  const [insulinType, setInsulinType] = useState("")
  const [insulinUnits, setInsulinUnits] = useState("")
  const [note, setNote] = useState("")

  const submit = async (e) => {

    e.preventDefault()

    const response = await fetch("http://127.0.0.1:8000/glucose/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        glucose_value: Number(glucose),
        measurement_type: type,
        insulin_type: insulinType || null,
        insulin_units: insulinUnits ? Number(insulinUnits) : 0,
        note: note
      })
    })

    if (response.ok) {
      setGlucose("")
      setInsulinType("")
      setInsulinUnits("")
      setNote("")
      onAdded()
    }

  }

  return (

    <form onSubmit={submit} className="bg-white p-6 rounded-xl shadow mb-8">

      <h2 className="text-xl font-semibold mb-4">
        Add Glucose Record
      </h2>

      <div className="grid grid-cols-2 gap-4">

        <input
          type="number"
          placeholder="Glucose mg/dL"
          value={glucose}
          onChange={(e) => setGlucose(e.target.value)}
          className="border rounded p-2"
          required
        />

        <select
          value={type}
          onChange={(e) => setType(e.target.value)}
          className="border rounded p-2"
        >
          <option value="FASTING">Fasting</option>
          <option value="BEFORE_MEAL">Before Meal</option>
          <option value="AFTER_MEAL">After Meal</option>
          <option value="BEDTIME">Bedtime</option>
        </select>

        <input
          type="text"
          placeholder="Insulin Type (Humalog etc)"
          value={insulinType}
          onChange={(e) => setInsulinType(e.target.value)}
          className="border rounded p-2"
        />

        <input
          type="number"
          placeholder="Units"
          value={insulinUnits}
          onChange={(e) => setInsulinUnits(e.target.value)}
          className="border rounded p-2"
        />

      </div>

      <textarea
        placeholder="Note"
        value={note}
        onChange={(e) => setNote(e.target.value)}
        className="border rounded p-2 w-full mt-4"
      />

      <button
        type="submit"
        className="bg-blue-600 text-white px-4 py-2 rounded mt-4 hover:bg-blue-700"
      >
        Save Record
      </button>

    </form>

  )

}

export default AddGlucoseForm