import { useState } from "react";
import { addGlucose } from "../services/api";

function AddRecord({ token, refresh }) {

  const [newGlucose, setNewGlucose] = useState("");
  const [note, setNote] = useState("");

  const addRecord = async (e) => {

    e.preventDefault();

    await addGlucose(token, newGlucose, note);

    setNewGlucose("");
    setNote("");

    refresh();
  };

  return (
    <div>

      <h3>Add Glucose Record</h3>

      <form onSubmit={addRecord}>

        <input
          type="number"
          placeholder="Glucose value"
          value={newGlucose}
          onChange={(e) => setNewGlucose(e.target.value)}
          required
        />

        <input
          type="text"
          placeholder="Note"
          value={note}
          onChange={(e) => setNote(e.target.value)}
        />

        <button type="submit">Add</button>

      </form>

    </div>
  );
}

export default AddRecord;